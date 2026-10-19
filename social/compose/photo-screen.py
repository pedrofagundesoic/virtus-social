#!/usr/bin/env python3
"""Encaixa um screenshot REAL do Virtus na tela do aparelho de uma foto (Unsplash) — família life, device "inphoto".
Nada é recriado: o print é só deformado em perspectiva para os 4 cantos da tela da foto.

   py -3.12 photo-screen.py              gera todas as entradas de photos/screens.json
   py -3.12 photo-screen.py <out-id>     só uma
   py -3.12 photo-screen.py --detect <foto> x y [v s]     sugere o quad da tela clara que contém (x, y)
   py -3.12 photo-screen.py --detect-green <foto> x y     idem para tela verde (chroma key)

photos/screens.json: { "<out-id>": { "photo": "<id da foto>", "shot": "<arquivo em screens/>",
    "quad": [[x,y] topo-esq, topo-dir, base-dir, base-esq] (px da foto original),
    "radius": 0.12 (canto arredondado, fração da largura do print), "status_bar": 0 (px pretos no topo do print),
    "crop": [x0,y0,x1,y1] (recorte final da foto, px originais), "shade": 0.93 (brilho do print),
    "blur": 0 (px de desfoque, para casar com a nitidez da foto),
    "occlude": false (true = devolve os pixels da foto que não parecem tela: manga, dedos na frente),
    "chroma": false (foto com tela verde: print só onde a foto é verde, + despill),
    "chroma_box": [[x0,y0,x1,y1], ...] (opcional: limita o chroma a essas caixas — notch, dedos),
    "occlude_box": [x0,y0,x1,y1] (opcional: só procura oclusão dentro desta caixa — evita trazer de volta imagens escuras da tela antiga) } }
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


def leftover_check(photo, quad, alpha, near=6, far=16, limit=0.08):
    """Anel de near..far px (6..16; frestas < 6 px somem no post de 1080) fora do quad: no aparelho real ali é moldura (escura). Pixels claros e pouco
    saturados nesse anel = tela original aparecendo. Avisa por lado (QUALIDADE.md, regra 8)."""
    hsv = np.asarray(photo.convert('HSV')).astype(float) / 255
    bright = (hsv[..., 2] > 0.6) & (hsv[..., 1] < 0.12)
    bright |= (hsv[..., 0] > 0.17) & (hsv[..., 0] < 0.45) & (hsv[..., 1] > 0.35) & (hsv[..., 2] > 0.35)  # verde chroma key
    covered = np.asarray(alpha) > 128
    cx, cy = sum(p[0] for p in quad) / 4, sum(p[1] for p in quad) / 4
    ok = True
    for name, (a, b) in zip(('topo', 'direita', 'base', 'esquerda'), zip(quad, quad[1:] + quad[:1])):
        hits = n = 0
        nx, ny = b[1] - a[1], a[0] - b[0]                       # normal da aresta
        ln = (nx * nx + ny * ny) ** .5; nx, ny = nx / ln, ny / ln
        if (cx - a[0]) * nx + (cy - a[1]) * ny > 0: nx, ny = -nx, -ny   # aponta para fora
        for t in np.linspace(0.12, 0.88, 60):                   # evita os cantos arredondados
            px, py = a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t
            for d in range(near, far + 1, 2):
                x, y = int(px + nx * d), int(py + ny * d)
                if 0 <= x < photo.width and 0 <= y < photo.height and not covered[y, x]:
                    n += 1; hits += bright[y, x]
        frac = hits / n if n else 0
        if frac > limit:
            ok = False; print(f'  SOBRA DE TELA ({name}): {frac:.0%} do anel externo é claro — aumentar o quad desse lado')
    if ok: print('  sem sobra de tela nas bordas')


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
        occ = ~((hsv[..., 2] > e.get('screen_v', 0.55)) & (hsv[..., 1] < e.get('screen_sat', 0.35)))  # pele clara pede screen_sat menor
        occ = Image.fromarray((occ * 255).astype('uint8'))
        k = e.get('occlude_min', 25)  # abertura morfológica: some com ícones soltos da tela antiga, fica braço/mão
        occ = occ.filter(ImageFilter.MinFilter(k)).filter(ImageFilter.MaxFilter(k)).filter(ImageFilter.MaxFilter(5))
        if e.get('occlude_box'):
            box = Image.new('L', photo.size, 0); ImageDraw.Draw(box).rectangle(e['occlude_box'], fill=255)
            occ = Image.fromarray(np.minimum(np.asarray(occ), np.asarray(box)))
        keep = Image.fromarray(255 - np.asarray(occ)).filter(ImageFilter.GaussianBlur(2))
        layer.putalpha(Image.fromarray((np.asarray(layer.getchannel('A')).astype(float) * np.asarray(keep) / 255).astype('uint8')))
    if e.get('chroma'):
        # tela verde: dentro das caixas chroma_box (notch, dedos) o print só entra onde a foto é verde;
        # fora delas vale a geometria do quad (cantos limpos). Contorno alisado: blur → limiar → blur.
        hsv = np.asarray(photo.convert('HSV')).astype(float) / 255
        g = (hsv[..., 0] > 0.17) & (hsv[..., 0] < 0.45) & (hsv[..., 1] > 0.30) & (hsv[..., 2] > 0.28)
        gm = Image.fromarray((g * 255).astype('uint8')).filter(ImageFilter.GaussianBlur(5)).point(lambda v: 255 if v > 127 else 0).filter(ImageFilter.GaussianBlur(1.5))
        boxes = e.get('chroma_box') or [[0, 0, photo.width, photo.height]]
        sel = Image.new('L', photo.size, 0)
        for bx in boxes: ImageDraw.Draw(sel).rectangle(bx, fill=255)
        sel = np.asarray(sel.filter(ImageFilter.GaussianBlur(6))).astype(float) / 255
        keep = sel * np.asarray(gm) / 255 + (1 - sel)
        layer.putalpha(Image.fromarray((np.asarray(layer.getchannel('A')).astype(float) * keep).astype('uint8')))
        # despill: tira o reflexo verde da tela na pele/moldura em volta
        arr = np.asarray(warped).astype(float); r, gg, b = arr[..., 0], arr[..., 1], arr[..., 2]
        lim = np.maximum(r, b) * 1.04; spill = gg > lim
        arr[..., 1] = np.where(spill, lim, gg); warped = Image.fromarray(arr.clip(0, 255).astype('uint8'), 'RGBA')
    warped.alpha_composite(layer)
    leftover_check(photo, quad, layer.getchannel('A'))
    img = warped.convert('RGB')
    if e.get('crop'): img = img.crop(tuple(e['crop']))
    dst = os.path.join(PHO, out_id + '.jpg')
    img.save(dst, quality=92)
    print('saved', dst, img.size)


def detect(photo_id, sx, sy, v=0.6, s=0.18, green=False):
    """Acha a tela clara da foto a partir de um ponto (sx, sy) dentro dela e imprime o quad sugerido.
    Tela = região conexa clara e pouco saturada; cantos = extremos de x+y e x−y (QUALIDADE.md, regra 5)."""
    from collections import deque
    im = Image.open(os.path.join(PHO, photo_id + '.jpg')).convert('RGB')
    k = 4  # trabalha em 1/4 para ser rápido
    sm = im.resize((im.width // k, im.height // k))
    hsv = np.asarray(sm.convert('HSV')).astype(float) / 255
    ok = (hsv[..., 2] > v) & (hsv[..., 1] < s)
    if green: ok = (hsv[..., 0] > 0.17) & (hsv[..., 0] < 0.45) & (hsv[..., 1] > 0.35) & (hsv[..., 2] > 0.35)  # tela chroma key
    h, w = ok.shape; seen = np.zeros_like(ok); q = deque([(sy // k, sx // k)])
    if not ok[q[0]]: raise SystemExit('o ponto não está numa área clara')
    while q:
        y, x = q.popleft()
        if 0 <= y < h and 0 <= x < w and ok[y, x] and not seen[y, x]:
            seen[y, x] = 1; q.extend(((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)))
    ys, xs = np.nonzero(seen)
    pick = lambda f: np.array((xs[f.argmax()], ys[f.argmax()]), float)
    rough = [pick(-xs - ys), pick(xs - ys), pick(xs + ys), pick(-xs + ys)]   # cantos aproximados (arredondados)
    # reta de cada lado: pontos da borda da região no trecho central (20–80%) do lado, ajuste por mínimos quadrados
    edge = seen & ~(np.roll(seen, 1, 0) & np.roll(seen, -1, 0) & np.roll(seen, 1, 1) & np.roll(seen, -1, 1))
    ey, ex = np.nonzero(edge); E = np.stack([ex, ey], 1).astype(float)
    lines = []
    for a, b in zip(rough, rough[1:] + rough[:1]):
        d = b - a; L = np.linalg.norm(d); u = d / L; n = np.array([-u[1], u[0]])
        if (np.array(rough).mean(0) - a) @ n > 0: n = -n            # normal apontando para fora
        t = (E - a) @ u; off = (E - a) @ n
        band = (t > .2 * L) & (t < .8 * L) & (np.abs(off) < .15 * L)
        tb, ob, Pb = t[band], off[band], E[band]
        bins = np.floor((tb - .2 * L) / max(1, .6 * L / 40)).astype(int)   # 40 fatias ao longo do lado
        P = np.array([Pb[bins == i][ob[bins == i].argmax()] for i in np.unique(bins)])  # ponto mais externo de cada fatia
        oo = np.array([ob[bins == i].max() for i in np.unique(bins)]); P = P[oo >= oo.max() - max(2, .02 * L)]  # descarta fatias recuadas (notch, câmera)
        c = P.mean(0); _, _, vt = np.linalg.svd(P - c); lines.append((c, vt[0]))
    def cross(l1, l2):
        (p, r), (q, s) = l1, l2; A = np.array([r, -s]).T; t = np.linalg.solve(A, q - p); return p + t[0] * r
    quad = [cross(lines[3], lines[0]), cross(lines[0], lines[1]), cross(lines[1], lines[2]), cross(lines[2], lines[3])]
    quad = [[int(round(x * k + k / 2)), int(round(y * k + k / 2))] for x, y in quad]
    print('área', int(seen.sum()) * k * k, 'px²  quad sugerido:', json.dumps(quad))
    print('(retas ajustadas nos lados; conferir com qa-photo.py e o aviso de SOBRA DE TELA)')


if __name__ == '__main__':
    if sys.argv[1:2] == ['--detect-green']:
        detect(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), green=True); sys.exit()
    if sys.argv[1:2] == ['--detect']:
        detect(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), *map(float, sys.argv[5:7])); sys.exit()  # [v] [s] opcionais
    spec = json.load(open(os.path.join(PHO, 'screens.json'), encoding='utf-8'))
    ids = sys.argv[1:] or [k for k in spec if not k.startswith('_')]
    for k in ids: make(k, spec[k])
