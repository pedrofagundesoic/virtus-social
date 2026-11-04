#!/usr/bin/env python3
"""Story avulso (1080x1920, 9:16) para divulgar em perfil pessoal. Fora da fila automática.
   py -3.12 story.py    gera social/stories/<id>.png (+ -preview.png com as áreas cobertas pelo Instagram marcadas)
Áreas: topo 250 px (barra e nome) e base 270 px (campo de mensagem) sem texto; o adesivo de link entra em y 1545–1645."""
import os, pathlib
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, '..', 'stories'); os.makedirs(OUT, exist_ok=True)
STORY = {'id': 'pedrofagundes-preco-justo', 'photo': 'life-story-precojusto', 'kicker': 'GRAHAM · BAZIN · GORDON',
         'head': 'O preço justo<br><em>das suas ações</em>',
         'cta': 'Os três métodos no Virtus, com a fórmula aberta.', 'cta2': 'Crie sua conta grátis no link',
         'fine': 'Preço justo no plano Premium. Dados de amostra. Não é recomendação de investimento.'}
HTML = '''<!DOCTYPE html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,700;1,600&family=Inter:wght@500;600;700&display=block" rel="stylesheet"><style>
*{margin:0;padding:0;box-sizing:border-box}html,body{width:1080px;height:1920px;overflow:hidden;background:#070707}
.bg{position:absolute;inset:0}.bg img{width:100%%;height:100%%;object-fit:cover;display:block}
.shade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(5,8,7,.92) 0,rgba(5,8,7,.86) 24%%,rgba(5,8,7,0) 34%%,rgba(5,8,7,0) 70%%,rgba(5,8,7,.93) 77%%,rgba(5,8,7,.98) 100%%)}
.kick{position:absolute;top:258px;left:64px;right:64px;text-align:center;font:700 25px Inter;letter-spacing:3px;color:#E3BF82}
.head{position:absolute;top:304px;left:56px;right:56px;text-align:center;font:700 76px/1.1 Lora;color:#fff}.head em{font-style:italic;font-weight:600;color:#E3BF82}
.cta{position:absolute;top:1412px;left:60px;right:60px;text-align:center;font:500 35px/1.3 Inter;color:rgba(255,255,255,.9)}.cta b{display:block;margin-top:6px;font:700 44px/1.25 Inter;color:#E3BF82}
.arrow{display:inline-block;margin-left:10px;vertical-align:-5px}
.fine{position:absolute;top:1524px;left:0;right:0;text-align:center;font:500 20px Inter;color:rgba(255,255,255,.62)}
.g{position:absolute;left:0;right:0;background:rgba(255,0,0,.28);border:2px dashed #f33;color:#fff;font:600 26px Inter;text-align:center}.s{position:absolute;left:310px;width:460px;top:1565px;height:86px;border-radius:18px;background:#fff;color:#1a6ee8;font:700 30px/86px Inter;text-align:center}
</style></head><body><div class="bg"><img src="%(photo)s"></div><div class="shade"></div>
<div class="kick">%(kicker)s</div><div class="head">%(head)s</div>
<div class="cta">%(cta)s<b>%(cta2)s<svg class="arrow" width="38" height="38" viewBox="0 0 24 24" fill="none" stroke="#E3BF82" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M12 4v15M5 12l7 7 7-7"/></svg></b></div>
<div class="fine">%(fine)s</div>%(guide)s</body></html>'''
GUIDE = '<div class="g" style="top:0;height:250px">área do Instagram</div><div class="g" style="bottom:0;height:270px;line-height:270px">área do Instagram</div><div class="s">🔗 CRIAR CONTA GRÁTIS</div>'
with sync_playwright() as pw:
    b = pw.chromium.launch(); p = b.new_page(viewport={'width': 1080, 'height': 1920})
    for suf, guide in (('', ''), ('-preview', GUIDE)):
        html = HTML % {**STORY, 'photo': pathlib.Path(HERE, 'photos', STORY['photo'] + '.jpg').as_uri(), 'guide': guide}
        f = os.path.join(OUT, f"{STORY['id']}{suf}.html"); open(f, 'w', encoding='utf-8').write(html)
        p.goto(pathlib.Path(f).resolve().as_uri()); p.wait_for_load_state('networkidle'); p.evaluate('document.fonts.ready'); p.wait_for_timeout(600)
        p.screenshot(path=f.replace('.html', '.png')); os.remove(f); print('saved', f.replace('.html', '.png'))
    b.close()
