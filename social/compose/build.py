#!/usr/bin/env python3
"""Social composer do Virtus (port do BudgetPilot social/compose/build.py, SOCIAL-AUTOPILOT.md seção 5).
posts.json → out/<slug>.html (1080×1350). Depois render.py transforma HTML em PNG.
`--queue` copia out/<slug>.png + escreve queue.json em $SOCIAL_WEB_DIR (C:\\dev\\Virtus\\docs\\social).

Mudanças Virtus: tema escuro verde/preto/dourado vindo do brand.json; lockup com o ícone PNG;
image no queue.json é relativa ao manifesto (GitHub Pages em subpasta); filtro de IA por palavra inteira
(o original barrava "dia ", "estratégia " etc.).

Famílias:  app  = cartão + screenshots reais em moldura. variant: phone | phones2 | phone-web | tablet | web
           life = foto de pessoa real + aparelho sobreposto. device: phone | browser | tablet
Chaves do post: slug, family, variant/device, platform (iphone|android|web), shots[], photo, focal, kicker,
                headline (<em> permitido, ≤ 2 linhas), sub, caption, date | evergreen:true,
                fade, crop, shot_h, offset, url, text_top (life)
Rodar:  py -3.12 build.py            py -3.12 build.py --queue
"""
import json, os, re, sys, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
SCR  = os.path.join(HERE, 'screens')
PHO  = os.path.join(HERE, 'photos')
OUT  = os.path.join(HERE, 'out')
B    = json.load(open(os.path.join(HERE, 'brand.json'), encoding='utf-8'))
WEB  = os.environ.get(B.get('web_dir_env', 'SOCIAL_WEB_DIR'), '')

APPLE = '<svg width="17" height="20" viewBox="0 0 384 512"><path fill="currentColor" d="M318.7 268.7c-.2-36.7 16.4-64.4 50-84.8-18.8-26.9-47.2-41.7-84.7-44.6-35.5-2.7-74.3 20.7-88.5 20.7-15 0-49.4-19.7-76.4-19.7C63.3 141.2 4 184.8 4 273.5q0 39.3 14.4 81.2c12.8 36.7 59 126.7 107.2 125.2 25.2-.6 43-17.9 75.8-17.9 31.8 0 48.3 17.9 76.4 17.9 48.6-.7 90.4-82.5 102.6-119.3-65.2-30.7-61.7-90-61.7-91.9zm-56.6-164.2c27.3-32.4 24.8-61.9 24-72.5-24.1 1.4-52 16.4-67.9 34.9-17.5 19.8-27.8 44.3-25.6 71.9 26.1 2 49.9-11.4 69.5-34.3z"/></svg>'
PLAY  = '<svg width="16" height="18" viewBox="0 0 16 16"><path fill="currentColor" d="M2 1.5 L13.5 8 L2 14.5 Z"/></svg>'
GLOBE = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M3 12 h18 M12 3 a14 14 0 0 1 0 18 M12 3 a14 14 0 0 0 0 18"/></svg>'
PILL_DEFS = {'iphone': (APPLE, 'iPhone'), 'android': (PLAY, 'Android'), 'web': (GLOBE, 'Web')}

FONTS = '<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600&family=Lora:ital,wght@0,700;1,600&family=Inter:wght@400;500;600;700;800&display=block" rel="stylesheet">'

def themed(css):
    for k in ('accent', 'accent_light', 'bg_top', 'bg_bottom', 'text', 'muted', 'pill_bg'):
        css = css.replace(f'__{k.upper()}__', B[k])
    return css

BASE_CSS = themed('''*{margin:0;padding:0;box-sizing:border-box}html,body{width:1080px;height:1350px;overflow:hidden}
.stage{width:1080px;height:1350px;position:relative;font-family:'Inter',sans-serif;overflow:hidden}
.lockup{display:flex;align-items:center;gap:14px}.badge{width:48px;height:48px;display:block}.badge img{width:100%;height:100%;display:block}
.bp{font-family:'Cinzel',serif;font-size:30px;font-weight:600;letter-spacing:6px;color:__TEXT__}
.phone{border-radius:44px;background:#050807;box-shadow:0 30px 80px rgba(0,0,0,.55),0 0 0 1px rgba(196,148,76,.25);padding:10px;position:absolute}
.phone .scr{border-radius:36px;overflow:hidden;position:relative;background:#050807;line-height:0}.phone .scr img{width:100%;display:block}
.island{position:absolute;top:11px;left:50%;transform:translateX(-50%);height:26px;border-radius:13px;background:#050807;z-index:3}
.browser{border-radius:18px;background:#fff;box-shadow:0 30px 80px rgba(0,0,0,.55),0 0 0 1px rgba(196,148,76,.25);overflow:hidden;position:absolute}
.chrome{height:44px;background:#F2F5F9;border-bottom:1px solid #E5EAF1;display:flex;align-items:center;padding:0 18px;gap:8px}.dot{width:12px;height:12px;border-radius:6px}
.urlbar{margin-left:14px;flex:1;height:26px;border-radius:13px;background:#fff;border:1px solid #E2E8F0;font-size:13px;color:#64748B;display:flex;align-items:center;padding:0 14px}
.shot{overflow:hidden;position:relative;line-height:0}.shot img{display:block}
.tablet{border-radius:30px;background:#050807;padding:14px;box-shadow:0 30px 80px rgba(0,0,0,.55),0 0 0 1px rgba(196,148,76,.25);position:absolute}.tablet .scr{border-radius:18px;overflow:hidden;line-height:0;background:#fff}.tablet .scr img{width:100%;display:block}
.pills{display:flex;justify-content:center;gap:16px}.pill{display:inline-flex;align-items:center;gap:9px;border-radius:999px;padding:13px 26px;font-size:19px;font-weight:600;background:__PILL_BG__;color:__TEXT__;border:1px solid rgba(243,238,228,.12)}.pill.on{background:__ACCENT__;color:#0B0F0D;border-color:__ACCENT__}
''')

def fileurl(p):  # Windows-safe file:// URL
    return 'file:///' + os.path.abspath(p).replace('\\', '/').lstrip('/')

def lockup():
    return f'<div class="lockup"><div class="badge"><img src="{fileurl(os.path.join(HERE, B["logo_png"]))}"></div><div class="bp">{B["name"]}</div></div>'

def pills(platform):
    return '<div class="pills">' + ''.join(
        f'<span class="pill{" on" if k == platform else ""}">{PILL_DEFS[k][0]}{PILL_DEFS[k][1]}</span>' for k in B['platforms']) + '</div>'

def phone(src, width, left, top, extra=''):
    inner = width - 20
    return (f'<div class="phone" style="width:{width}px;left:{left}px;top:{top}px;{extra}"><div class="scr" style="width:{inner}px">'
            f'<div class="island" style="width:{int(inner*0.30)}px"></div><img src="{src}"></div></div>')

def browser(path, width, left, top, url, shot_h, img_w=None, offset_y=0, extra=''):
    img_w = img_w or width
    try:
        from PIL import Image
        w, h = Image.open(path).size
        shot_h = min(shot_h, int(h * img_w / w) - offset_y)
    except Exception: pass
    return (f'<div class="browser" style="width:{width}px;left:{left}px;top:{top}px;{extra}">'
            f'<div class="chrome"><div class="dot" style="background:#F87171"></div><div class="dot" style="background:#FBBF24"></div><div class="dot" style="background:#34D399"></div><div class="urlbar">{url}</div></div>'
            f'<div class="shot" style="width:{width}px;height:{shot_h}px"><img src="{fileurl(path)}" style="width:{img_w}px;margin-top:-{offset_y}px"></div></div>')

def tablet(src, width, left, top, extra='', crop=None):
    h = f'height:{crop}px;' if crop else ''
    return f'<div class="tablet" style="width:{width}px;left:{left}px;top:{top}px;{extra}"><div class="scr" style="{h}"><img src="{src}"></div></div>'

def scr_path(name):
    for root, _, files in os.walk(SCR):
        if name in files: return os.path.join(root, name)
    raise SystemExit(f'missing screenshot {name} under {SCR}')
def scr(name): return fileurl(scr_path(name))

def photo(pid):
    p = os.path.join(PHO, pid + '.jpg')
    if not os.path.exists(p): raise SystemExit(f'missing photo {p}')
    return fileurl(p)

def footer():
    return (f'<div class="foot"><b>{B["footer_bold"]}</b> <span>{B["footer_rest"]}</span></div>'
            f'<div class="fine">{B["fine_print"]}</div>')

# ───────────── família A: cartão ─────────────
APP_CSS = BASE_CSS + themed('''
.stage{background:radial-gradient(120% 70% at 50% 0%,__BG_TOP__ 0%,__BG_BOTTOM__ 78%);color:__TEXT__}
.top{position:absolute;top:44px;left:0;right:0;display:flex;justify-content:center}
.headline{position:absolute;top:122px;left:70px;right:70px;text-align:center;font-family:'Lora',serif;font-weight:700;font-size:64px;line-height:1.1;color:__TEXT__}
.headline em{font-style:italic;color:__ACCENT__;font-weight:600}
.sub{position:absolute;top:304px;left:120px;right:120px;text-align:center;font-size:25px;line-height:1.45;color:__MUTED__}
.hero{position:absolute;top:400px;left:0;right:0;height:690px;-webkit-mask-image:linear-gradient(180deg,#000 0,#000 __FADE__%,transparent 100%);mask-image:linear-gradient(180deg,#000 0,#000 __FADE__%,transparent 100%)}
.pillrow{position:absolute;top:1108px;left:0;right:0}
.foot{position:absolute;top:1194px;left:0;right:0;text-align:center;font-size:25px}.foot b{color:__ACCENT_LIGHT__;font-weight:700}.foot span{color:__MUTED__;font-weight:500}
.fine{position:absolute;top:1244px;left:0;right:0;text-align:center;font-size:15.5px;color:rgba(243,238,228,.45)}
''')

def render_app(p):
    v = p.get('variant', 'phone'); url = p.get('url', B['web_url'])
    if v == 'phone':      hero = phone(scr(p['shots'][0]), 470, 305, 30)
    elif v == 'phones2':  hero = phone(scr(p['shots'][0]), 400, 110, 60, 'transform:rotate(-4deg)') + phone(scr(p['shots'][1]), 400, 570, 20, 'transform:rotate(4deg)')
    elif v == 'phone-web':hero = browser(scr_path(p['shots'][1]), 770, 250, 30, url, p.get('shot_h', 430), img_w=770, offset_y=p.get('offset', 0)) + phone(scr(p['shots'][0]), 286, 62, 46)
    elif v == 'tablet':   hero = tablet(scr(p['shots'][0]), 900, 90, 40, crop=p.get('crop'))
    elif v == 'web':      hero = browser(scr_path(p['shots'][0]), 960, 60, 30, url, p.get('shot_h', 600), img_w=960, offset_y=p.get('offset', 0))
    else: raise SystemExit(f'unknown variant {v}')
    css = APP_CSS.replace('__FADE__', str(p.get('fade', 72)))
    return f'''<!DOCTYPE html><html><head><meta charset="utf-8">{FONTS}<style>{css}</style></head><body><div class="stage">
<div class="top">{lockup()}</div>
<div class="headline">{p['headline']}</div>
<div class="sub">{p['sub']}</div>
<div class="hero">{hero}</div>
<div class="pillrow">{pills(p.get('platform', 'iphone'))}</div>
{footer()}
</div></body></html>'''

# ───────────── família B: foto de pessoa ─────────────
LIFE_CSS = BASE_CSS + themed('''
.stage{background:__BG_BOTTOM__;color:#fff}
.bg{position:absolute;inset:0}.bg img{width:100%;height:100%;object-fit:cover;display:block}
.shade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(5,8,7,.20) 0%,rgba(5,8,7,0) 28%,rgba(7,16,12,.25) 52%,rgba(7,16,12,.88) 78%,rgba(5,8,7,.95) 100%)}
.top{position:absolute;top:44px;left:56px}.top .lockup{background:rgba(7,16,12,.45);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);border:1px solid rgba(227,191,130,.35);border-radius:999px;padding:8px 22px 8px 10px}.badge{width:40px;height:40px}.bp{font-size:24px;letter-spacing:5px}
.kicker{position:absolute;left:56px;top:__KICK__px;font-size:15px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:__ACCENT_LIGHT__}
.headline{position:absolute;left:56px;top:__HEAD__px;width:__HW__px;font-family:'Lora',serif;font-weight:700;font-size:54px;line-height:1.12;color:#fff;text-shadow:0 2px 24px rgba(0,0,0,.35)}
.headline em{font-style:italic;color:__ACCENT_LIGHT__;font-weight:600}
.sub{position:absolute;left:56px;top:__SUB__px;width:__HW__px;font-size:23px;line-height:1.45;color:rgba(255,255,255,.86)}
.foot{position:absolute;left:56px;bottom:84px;width:620px;font-size:21px;line-height:1.4;color:#fff;z-index:2}.foot b{font-weight:700;color:__ACCENT_LIGHT__}.foot span{color:rgba(255,255,255,.72);font-weight:500}
.fine{position:absolute;left:56px;bottom:40px;font-size:14px;color:rgba(255,255,255,.55)}
.pills{position:absolute;right:56px;top:52px;gap:10px}.pill{padding:10px 18px;font-size:16px;background:rgba(7,16,12,.45);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);border:1px solid rgba(255,255,255,.22);color:#fff}.pill.on{background:__ACCENT__;border-color:__ACCENT__;color:#0B0F0D}
''')

def render_life(p):
    dev = p.get('device', 'phone'); url = p.get('url', B['web_url'])
    if dev == 'phone':
        mock = phone(scr(p['shots'][0]), 330, 700, 640); hw = 610
    elif dev == 'browser':
        mock = browser(scr_path(p['shots'][0]), 460, 620, 900, url, p.get('shot_h', 420), img_w=460, offset_y=p.get('offset', 0)); hw = 545
    else:
        mock = tablet(scr(p['shots'][0]), 460, 620, 920, crop=p.get('crop')); hw = 545
    kick, head, sub = (130, 164, 400) if p.get('text_top') else (700, 734, 940)
    css = LIFE_CSS.replace('__KICK__', str(kick)).replace('__HEAD__', str(head)).replace('__SUB__', str(sub)).replace('__HW__', str(hw))
    return f'''<!DOCTYPE html><html><head><meta charset="utf-8">{FONTS}<style>{css}</style></head><body><div class="stage">
<div class="bg"><img src="{photo(p['photo'])}" style="object-position:{p.get('focal', 'center')}"></div><div class="shade"></div>
<div class="top">{lockup()}</div>
{pills(p.get('platform', 'iphone'))}
<div class="kicker">{p.get('kicker', '')}</div>
<div class="headline">{p['headline']}</div>
<div class="sub">{p['sub']}</div>
{mock}
{footer()}
</div></body></html>'''

AI_WORDS = re.compile(r'(?<![\w#])(ia|ai|i\.a\.)(?!\w)|#ia\b|#ai\b|intelig[êe]ncia artificial|artificial intelligence', re.I)
ADVICE = re.compile(r'\b(compre|venda já|garantid[oa]s?|rentabilidade garantida|lucro certo)\b', re.I)

def validate(posts):
    seen = set()
    for p in posts:
        for k in ('slug', 'family', 'headline', 'sub', 'caption'):
            if k not in p: raise SystemExit(f'{p.get("slug","?")}: missing {k}')
        if p['slug'] in seen: raise SystemExit(f'duplicate slug {p["slug"]}')
        seen.add(p['slug'])
        if not p.get('date') and not p.get('evergreen'): raise SystemExit(f'{p["slug"]}: needs date or evergreen:true')
        text = re.sub(r'<[^>]+>', ' ', p['headline'] + ' ' + p['sub'] + ' ' + p['caption'])
        m = AI_WORDS.search(text)
        if m: raise SystemExit(f'{p["slug"]}: tema IA não é permitido ("{m.group(0)}")')
        m = ADVICE.search(text)
        if m: raise SystemExit(f'{p["slug"]}: linguagem de recomendação/promessa não é permitida ("{m.group(0)}")')

def build(posts):
    os.makedirs(OUT, exist_ok=True)
    for p in posts:
        h = render_app(p) if p['family'] == 'app' else render_life(p)
        open(os.path.join(OUT, p['slug'] + '.html'), 'w', encoding='utf-8').write(h)
    print('html written:', len(posts), '→', OUT)

def queue(posts):
    if not WEB: raise SystemExit('set SOCIAL_WEB_DIR (C:\\dev\\Virtus\\docs\\social)')
    os.makedirs(WEB, exist_ok=True)
    man = {'_readme': 'Fila diária. posts = datados, em ordem (postados uma vez quando vencem). evergreen = banco: nunca postado primeiro, depois o menos recente com ≥ SOCIAL_REPEAT_DAYS (21). Gerado por build.py --queue — nunca editar à mão.',
           'posts': [], 'evergreen': []}
    for p in posts:
        png = os.path.join(OUT, p['slug'] + '.png')
        if not os.path.exists(png): raise SystemExit('missing render ' + png + ' (run render.py)')
        shutil.copy(png, os.path.join(WEB, p['slug'] + '.png'))
        e = {'slug': p['slug'], 'image': p['slug'] + '.png', 'caption': p['caption']}  # relativo ao queue.json
        if p.get('date'): e['date'] = p['date']
        (man['evergreen'] if p.get('evergreen') else man['posts']).append(e)
    json.dump(man, open(os.path.join(WEB, 'queue.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    print('queue:', len(man['posts']), 'datados +', len(man['evergreen']), 'evergreen →', WEB)
    if len(man['evergreen']) <= 21: print('ATENÇÃO: banco evergreen ≤ 21 → vai surgir dia sem post quando a fila datada acabar')

if __name__ == '__main__':
    src = os.path.join(HERE, 'posts.json')
    if not os.path.exists(src): raise SystemExit('posts.json não existe ainda')
    posts = json.load(open(src, encoding='utf-8'))
    validate(posts)
    queue(posts) if '--queue' in sys.argv else build(posts)
