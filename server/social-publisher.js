// social-publisher.js — daily Facebook Page + Instagram publisher (ESM).
// Ported from BudgetPilot server 1.9.3-social-evergreen (SOCIAL-AUTOPILOT.md, seção 5).
// Virtus changes: defaults America/Sao_Paulo 18h; image paths resolve against the manifest URL
// (GitHub Pages project sites live under /<repo>/, so origin + "/social/x.png" would 404).
//
// Contract of loadData/saveData: loadData(key) → object|null ; saveData(key, object) → void. Keys used:
//   'social_state'    { lastRunDate, lastSlug, attempts, attemptsDate, lastError }
//   'social_post_log' { [slug]: { date, at, image, kind, count, fb, ig, fbError?, igError? } }
//
// Env: FB_PAGE_ID FB_PAGE_TOKEN IG_USER_ID SOCIAL_MANIFEST_URL
//      optional SOCIAL_TZ (America/Sao_Paulo) SOCIAL_POST_HOUR (18) SOCIAL_REPEAT_DAYS (21)
import fs from 'node:fs';
import path from 'node:path';

const GRAPH = 'https://graph.facebook.com/v21.0';

export function createFileStore(file) {
  const read = () => { try { return JSON.parse(fs.readFileSync(file, 'utf8')); } catch { return {}; } };
  return {
    async loadData(key) { return read()[key] ?? null; },
    async saveData(key, value) {
      const all = read(); all[key] = value;
      fs.mkdirSync(path.dirname(file), { recursive: true });
      fs.writeFileSync(file, JSON.stringify(all, null, 1));
    },
  };
}

export function localNow(tz) {
  const parts = new Intl.DateTimeFormat('en-US', {
    timeZone: tz, hourCycle: 'h23',
    year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit',
  }).formatToParts(new Date()).reduce((o, p) => (o[p.type] = p.value, o), {});
  return { date: `${parts.year}-${parts.month}-${parts.day}`, hour: parseInt(parts.hour, 10), minute: parseInt(parts.minute, 10) };
}

export function createPublisher({ loadData, saveData, env = process.env, log = console }) {
  const TZ = env.SOCIAL_TZ || 'America/Sao_Paulo';
  const POST_HOUR = parseInt(env.SOCIAL_POST_HOUR || '18', 10);
  const MANIFEST_URL = env.SOCIAL_MANIFEST_URL || '';
  const FB_PAGE_ID = env.FB_PAGE_ID || '';
  const FB_TOKEN = env.FB_PAGE_TOKEN || '';
  const IG_USER_ID = env.IG_USER_ID || '';
  const REPEAT_DAYS = parseInt(env.SOCIAL_REPEAT_DAYS || '21', 10);
  const MAX_ATTEMPTS = 3;

  async function graphPost(pathname, params) {
    const body = new URLSearchParams({ ...params, access_token: FB_TOKEN });
    const res = await fetch(`${GRAPH}/${pathname}`, { method: 'POST', body });
    const json = await res.json().catch(() => ({}));
    if (!res.ok || json.error) throw new Error(`${pathname}: ${json.error?.message || res.status}`);
    return json;
  }

  async function pickNext(today) {
    const res = await fetch(MANIFEST_URL, { headers: { 'cache-control': 'no-cache' } });
    if (!res.ok) throw new Error(`manifest ${res.status}`);
    const manifest = await res.json();
    const logData = (await loadData('social_post_log')) || {};
    const abs = e => ({ ...e, image: new URL(e.image, MANIFEST_URL).href });
    const posts = (manifest.posts || []).filter(p => p.slug && p.image);
    const bank = (manifest.evergreen || []).filter(p => p.slug && p.image);
    const pending = posts.filter(p => !logData[p.slug] && (!p.date || p.date <= today)).length;
    const future = posts.filter(p => !logData[p.slug] && p.date && p.date > today).length;
    const meta = { pending, future, bank: bank.length, repeatDays: REPEAT_DAYS };
    // 1) dated/one-off queue, manifest order, first unposted that is due
    let entry = posts.find(p => !logData[p.slug] && (!p.date || p.date <= today));
    let kind = 'queue';
    // 2) evergreen bank: never-posted first, then least-recently posted older than REPEAT_DAYS
    if (!entry) {
      kind = 'evergreen';
      entry = bank.find(p => !logData[p.slug]);
      if (!entry) {
        const cutoff = Date.now() - REPEAT_DAYS * 86400000;
        entry = bank
          .filter(p => Date.parse(logData[p.slug]?.at || 0) < cutoff)
          .sort((x, y) => Date.parse(logData[x.slug].at) - Date.parse(logData[y.slug].at))[0];
      }
    }
    if (!entry) return { entry: null, log: logData, meta };
    return { entry: { ...abs(entry), kind }, log: logData, meta };
  }

  async function publish({ dry = false, reason = 'tick', quiet = false } = {}) {
    const { date: today } = localNow(TZ);
    const { entry, log: logData, meta } = await pickNext(today);
    if (!entry) {
      if (!quiet) log.log(`📣 social (${reason}): nothing queued for ${today} (bank ${meta.bank}, repeat ≥${meta.repeatDays}d)`);
      return { posted: false, today, meta };
    }
    if (dry) return { posted: false, dry: true, today, next: entry, meta };
    const prev = logData[entry.slug] || {};
    const result = { date: today, at: new Date().toISOString(), image: entry.image, kind: entry.kind, count: (prev.count || 0) + 1, fb: null, ig: null };
    try {
      const fb = await graphPost(`${FB_PAGE_ID}/photos`, { url: entry.image, message: entry.caption || '' });
      result.fb = fb.post_id || fb.id;
    } catch (err) { result.fbError = err.message; log.error('📣 social FB failed:', err.message); }
    try {
      const container = await graphPost(`${IG_USER_ID}/media`, { image_url: entry.image, caption: entry.caption || '' });
      for (let i = 0; i < 6; i++) { // Instagram needs a moment to ingest the image
        const st = await fetch(`${GRAPH}/${container.id}?fields=status_code&access_token=${FB_TOKEN}`).then(r => r.json());
        if (st.status_code === 'FINISHED') break;
        if (st.status_code === 'ERROR') throw new Error('IG container ERROR');
        await new Promise(r => setTimeout(r, 5000));
      }
      const pub = await graphPost(`${IG_USER_ID}/media_publish`, { creation_id: container.id });
      result.ig = pub.id;
    } catch (err) { result.igError = err.message; log.error('📣 social IG failed:', err.message); }
    if (!result.fb && !result.ig) {
      log.error(`📣 social (${reason}): "${entry.slug}" failed on both platforms — not consumed`);
      return { posted: false, failed: true, slug: entry.slug, ...result, meta };
    }
    logData[entry.slug] = result;
    await saveData('social_post_log', logData);
    log.log(`📣 social (${reason}): posted "${entry.slug}" [${entry.kind}#${result.count}] → FB ${result.fb || 'FAIL'} · IG ${result.ig || 'FAIL'} · queue ${Math.max(meta.pending - 1, 0)} pending, ${meta.future} scheduled, bank ${meta.bank}`);
    return { posted: true, slug: entry.slug, ...result, meta };
  }

  // One tick of the daily loop. Returns true when something was posted. Safe to call every minute.
  async function tick() {
    const { date, hour } = localNow(TZ);
    if (hour < POST_HOUR || hour >= POST_HOUR + 4) return false;              // 18:00–21:59 window
    const state = (await loadData('social_state')) || {};
    if (state.lastRunDate === date) return false;                              // already posted today
    if (state.attemptsDate === date && (state.attempts || 0) >= MAX_ATTEMPTS) return false;
    const r = await publish({ reason: `${TZ} ${date} ${String(hour).padStart(2, '0')}:00`, quiet: state.emptyNoticeDate === date });
    if (r.posted) {
      await saveData('social_state', { ...state, lastRunDate: date, lastSlug: r.slug, startedAt: new Date().toISOString(), attempts: 0, attemptsDate: date });
    } else if (r.failed) {
      const attempts = (state.attemptsDate === date ? (state.attempts || 0) : 0) + 1;
      await saveData('social_state', { ...state, attemptsDate: date, attempts, lastError: r.fbError || r.igError || 'unknown', lastErrorAt: new Date().toISOString() });
    } else if (state.emptyNoticeDate !== date) {
      await saveData('social_state', { ...state, emptyNoticeDate: date }); // log the empty notice once, keep checking
    }
    return !!r.posted;
  }

  const configured = !!(FB_PAGE_ID && FB_TOKEN && IG_USER_ID && MANIFEST_URL);
  return { publish, tick, localNow: () => localNow(TZ), configured, TZ, POST_HOUR, MANIFEST_URL };
}
