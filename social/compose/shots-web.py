#!/usr/bin/env python3
"""Screenshots REAIS do Virtus web para o compositor (nunca recriações em HTML).
   py -3.12 shots-web.py --path /carteira --name carteira --out screens\\web
Credenciais: VIRTUS_DEMO_EMAIL / VIRTUS_DEMO_PASSWORD (de %USERPROFILE%\\.social.env ou do ambiente) — nunca na linha de comando.
Opções: --url (padrão https://www.virtusapp.com.br)  --remove "css selector" (banners a remover antes do print)
        --scroll 560  --dark  --presets desktop,phone,tablet
TODO (uma vez): conferir os seletores do formulário em /entrar dentro de login().
"""
import argparse, os, pathlib
from playwright.sync_api import sync_playwright
PRESETS = {'desktop': (1440, 900), 'phone': (390, 844), 'tablet': (1180, 820)}

def load_env():
    f = pathlib.Path(os.environ['USERPROFILE']) / '.social.env'
    if f.exists():
        for line in f.read_text(encoding='utf-8-sig').splitlines():
            if '=' in line and not line.lstrip().startswith('#'):
                k, v = line.split('=', 1)
                os.environ.setdefault(k.strip(), v.split(' #')[0].strip())

def login(page, url, email, password):
    page.goto(url.rstrip('/') + '/entrar')
    # ── TODO: conferir seletores reais do /entrar ─────────────────────────
    page.fill('input[type=email]', email)
    page.fill('input[type=password]', password)
    page.click('button[type=submit]')
    page.wait_for_load_state('networkidle')
    # ──────────────────────────────────────────────────────────────────────

def main():
    load_env()
    a = argparse.ArgumentParser()
    a.add_argument('--url', default='https://www.virtusapp.com.br')
    a.add_argument('--path', default='/'); a.add_argument('--out', default='screens/web'); a.add_argument('--name', default='shot')
    a.add_argument('--remove', action='append', default=[]); a.add_argument('--scroll', type=int, default=0)
    a.add_argument('--dark', action='store_true'); a.add_argument('--presets', default='desktop,phone,tablet')
    a.add_argument('--no-login', action='store_true')
    o = a.parse_args()
    email, password = os.environ.get('VIRTUS_DEMO_EMAIL'), os.environ.get('VIRTUS_DEMO_PASSWORD')
    out = pathlib.Path(o.out); out.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for name in o.presets.split(','):
            w, h = PRESETS[name]
            ctx = browser.new_context(viewport={'width': w, 'height': h}, device_scale_factor=2, locale='pt-BR',
                                      color_scheme='dark' if o.dark else 'light', is_mobile=(name == 'phone'))
            page = ctx.new_page()
            if not o.no_login:
                if not (email and password): raise SystemExit('defina VIRTUS_DEMO_EMAIL e VIRTUS_DEMO_PASSWORD em %USERPROFILE%\\.social.env')
                login(page, o.url, email, password)
            page.goto(o.url.rstrip('/') + o.path); page.wait_for_load_state('networkidle')
            for sel in o.remove: page.evaluate(f'document.querySelectorAll({sel!r}).forEach(e => e.remove())')
            if o.scroll: page.mouse.wheel(0, o.scroll); page.wait_for_timeout(500)
            f = out / f'{"dark-" if o.dark else ""}{name}-{o.name}.png'
            page.screenshot(path=str(f)); print('saved', f); ctx.close()
        browser.close()

if __name__ == '__main__': main()
