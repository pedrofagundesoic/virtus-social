#!/usr/bin/env python3
"""Folha de revisão de uma foto composta (photo-screen.py): visão geral + os 4 cantos e o meio de cada lado
ampliados 1:1, com o contorno do quad em vermelho na metade esquerda de cada recorte e o resultado na direita.
   py -3.12 qa-photo.py <out-id>        → photos/qa/<out-id>.png
Ler QUALIDADE.md (regras 5, 8 e 9)."""
import json, os, sys
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
PHO = os.path.join(HERE, 'photos')


def main(out_id, box=260):
    e = json.load(open(os.path.join(PHO, 'screens.json'), encoding='utf-8'))[out_id]
    orig = Image.open(os.path.join(PHO, e['photo'] + '.jpg')).convert('RGB')
    comp = Image.open(os.path.join(PHO, out_id + '.jpg')).convert('RGB')
    ox, oy = (e.get('crop') or [0, 0])[:2]
    quad = [tuple(p) for p in e['quad']]
    lined = orig.copy(); ImageDraw.Draw(lined).polygon(quad, outline=(255, 0, 0), width=3)
    pts = quad + [((a[0] + b[0]) / 2, (a[1] + b[1]) / 2) for a, b in zip(quad, quad[1:] + quad[:1])]
    tiles = []
    for x, y in pts:
        r = (int(x - box), int(y - box), int(x + box), int(y + box))
        a = lined.crop(r); b = comp.crop((r[0] - ox, r[1] - oy, r[2] - ox, r[3] - oy))
        t = Image.new('RGB', (box * 4 + 8, box * 2), 'white'); t.paste(a, (0, 0)); t.paste(b, (box * 2 + 8, 0)); tiles.append(t)
    over = comp.copy(); over.thumbnail((900, 1125))
    W = max(over.width, (box * 4 + 8) * 2 + 10)
    H = over.height + 10 + ((len(tiles) + 1) // 2) * (box * 2 + 10)
    sheet = Image.new('RGB', (W, H), (40, 40, 40)); sheet.paste(over, (0, 0))
    for i, t in enumerate(tiles):
        sheet.paste(t, ((i % 2) * (t.width + 10), over.height + 10 + (i // 2) * (box * 2 + 10)))
    os.makedirs(os.path.join(PHO, 'qa'), exist_ok=True)
    dst = os.path.join(PHO, 'qa', out_id + '.png'); sheet.save(dst); print('saved', dst)


if __name__ == '__main__':
    for k in sys.argv[1:]: main(k)
