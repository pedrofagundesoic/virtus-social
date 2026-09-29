#!/usr/bin/env python3
"""Encaixa um screenshot REAL do Virtus na tela do aparelho de uma foto (Unsplash) — família life, device "inphoto".
Nada é recriado: o print é só deformado em perspectiva para os 4 cantos da tela da foto.

   py -3.12 photo-screen.py              gera todas as entradas de photos/screens.json
   py -3.12 photo-screen.py <out-id>     só uma

photos/screens.json: { "<out-id>": { "photo": "<id da foto>", "shot": "<arquivo em screens/>",
    "quad": [[x,y] topo-esq, topo-dir, base-dir, base-esq] (px da foto original),
    "radius": 0.12 (canto arredondado, fração da largura do print), "status_bar": 0 (px pretos no topo do print),
    "crop": [x0,y0,x1,y1] (recorte final da foto, px originais), "shade": 0.93 (brilho do print),
    "blur": 0 (px de desfoque, para casar com a nitidez da foto),
    "occlude": false (true = devolve os pixels da foto que não parecem tela: manga, dedos na frente) } }
Saída: photos/<out-id>.jpg — referenciar no posts.json com "photo": "<out-id>".
"""
import json, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
PHO = os.path.join(HERE, 'photos')
SCR = os.path.join(HERE, 'screens')


def scr_path(name):
    for root, _, files in os.walk(SCR):
        if name in files: return os.path.join(root, name)
    raise SystemExit(f'missing screenshot {name} under {SCR}')


def coeffs(dst, src):
    """Coeficientes de Image.PERSPECTIVE: mapeiam ponto da saída (dst) → ponto do print (src)."""
    A, b = [], []
    for (x, y), (u, v) in zip(dst, src):
        A.append([x, y, 1, 0, 0, 0, -u * x, -u * y]); b.append(u)
        A.append([0, 0, 0, x, y, 1, -v * x, -v * y]); b.append(v)
    return np.linalg.solve(np.array(A, float), np.array(b, float)).tolist()


def make(out_id, e):
    photo = Image.open(os.path.join(PHO, e['photo'] + '.jpg')).convert('RGB')
    shot = Image.open(scr_path(e['shot'])).convert('RGB')
    if e.get('status_bar'):
        sb = Image.new('RGB', (shot.width, shot.height + e['status_bar']), '#000')
        sb.paste(shot, (0, e['status_bar'])); shot = sb
    shot = ImageEnhance.Brightness(shot).enhance(e.get('shade', 0.93))
    # canto arredondado do vidro
    r = int(shot.width * e.get('radius', 0.12))
    mask = Image.new('L', shot.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, shot.width - 1, shot.height - 1], radius=r, fill=255)
    shot.putalpha(mask)
    quad = [tuple(p) for p in e['quad']]
    w, h = shot.size
    warped = photo.copy().convert('RGBA')
    layer = shot.transform(photo.size, Image.PERSPECTIVE, coeffs(quad, [(0, 0), (w, 0), (w, h), (0, h)]), Image.BICUBIC)
    a = layer.getchannel('A').filter(ImageFilter.GaussianBlur(1.2))  # borda suave, sem serrilhado
    layer.putalpha(a)
    if e.get('blur'): layer = layer.filter(ImageFilter.GaussianBlur(e['blur']))
    if e.get('occlude'):
        # dentro do quad, o que é claro e pouco saturado é tela; o resto (braço, mão) fica na frente
        hsv = np.asarray(photo.convert('HSV')).astype(float) / 255
        occ = ~((hsv[..., 2] > 0.55) & (hsv[..., 1] < 0.35))
        occ = Image.fromarray((occ * 255).astype('uint8'))
        k = e.get('occlude_min', 25)  # abertura morfológica: some com ícones soltos da tela antiga, fica braço/mão
        occ = occ.filter(ImageFilter.MinFilter(k)).filter(ImageFilter.MaxFilter(k)).filter(ImageFilter.MaxFilter(5))
        keep = Image.fromarray(255 - np.asarray(occ)).filter(ImageFilter.GaussianBlur(2))
        layer.putalpha(Image.fromarray((np.asarray(layer.getchannel('A')).astype(float) * np.asarray(keep) / 255).astype('uint8')))
    warped.alpha_composite(layer)
    img = warped.convert('RGB')
    if e.get('crop'): img = img.crop(tuple(e['crop']))
    dst = os.path.join(PHO, out_id + '.jpg')
    img.save(dst, quality=92)
    print('saved', dst, img.size)


if __name__ == '__main__':
    spec = json.load(open(os.path.join(PHO, 'screens.json'), encoding='utf-8'))
    ids = sys.argv[1:] or [k for k in spec if not k.startswith('_')]
    for k in ids: make(k, spec[k])
