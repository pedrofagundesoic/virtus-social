// publish-once.js — Option B runner (GitHub Actions). One process, one tick, exit.
// State lives in social/state.json inside the repo (the workflow commits it back).
//   node server/publish-once.js          → tick (posts if inside the window and not yet today)
//   node server/publish-once.js --dry    → print what would be posted next (only needs SOCIAL_MANIFEST_URL)
//   node server/publish-once.js --force  → post now, ignoring the window (manual catch-up for ONE missed day)
import { createPublisher, createFileStore } from './social-publisher.js';

const store = createFileStore(process.env.SOCIAL_STATE_FILE || 'social/state.json');
const pub = createPublisher({ loadData: store.loadData, saveData: store.saveData });
const arg = process.argv[2];

if (arg === '--dry') {
  if (!pub.MANIFEST_URL) { console.error('missing SOCIAL_MANIFEST_URL'); process.exit(2); }
  console.log(JSON.stringify(await pub.publish({ dry: true, reason: 'dry' }), null, 1));
  process.exit(0);
}
if (!pub.configured) { console.error('missing FB_PAGE_ID / FB_PAGE_TOKEN / IG_USER_ID / SOCIAL_MANIFEST_URL'); process.exit(2); }

if (arg === '--force') {
  const r = await pub.publish({ reason: 'manual' });
  if (r.posted) await store.saveData('social_state', { ...(await store.loadData('social_state') || {}), lastRunDate: r.date, lastSlug: r.slug });
  console.log(JSON.stringify(r, null, 1));
  process.exit(r.posted ? 0 : 1);
} else {
  const posted = await pub.tick();
  console.log(posted ? 'posted' : `nothing to do at ${JSON.stringify(pub.localNow())}`);
}
