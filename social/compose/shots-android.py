#!/usr/bin/env python3
"""Screenshots REAIS do app Android do Virtus (nunca recriacoes em HTML).

   py -3.12 shots-android.py --list
   py -3.12 shots-android.py --launch --name carteira
   py -3.12 shots-android.py --name calendario

Captura via `adb exec-out screencap -p` e grava em screens/android/<name>.png.
--limpo corta a barra de status (topo) e a de navegacao (rodape) do PNG: o print
entra na moldura de celular do build.py sem relogio, bateria nem botoes do sistema.
--demo tenta o System UI Demo Mode (relogio 18:00, bateria cheia); o One UI da Samsung
ignora esses broadcasts, entao em Galaxy use --limpo. --off desliga o demo mode.
"""
import argparse, os, pathlib, subprocess, sys, time

PKG = 'com.correiavirtus.virtus'
HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / 'screens' / 'android'


def adb(*args, binary=False, check=True):
    r = subprocess.run(['adb', *args], capture_output=True)
    if check and r.returncode != 0:
        sys.exit('adb ' + ' '.join(args) + ' falhou: ' + r.stderr.decode('utf-8', 'replace').strip())
    return r.stdout if binary else r.stdout.decode('utf-8', 'replace')


def devices():
    out = adb('devices', '-l')
    return [l for l in out.splitlines()[1:] if l.strip() and 'device ' in l or l.endswith('device')]


def require_device():
    d = devices()
    if not d:
        sys.exit('nenhum aparelho em `adb devices`.\n'
                 '  1) conecte o cabo USB\n'
                 '  2) Ajustes > Sobre o telefone > toque 7x em "Numero da versao" (ativa Opcoes do desenvolvedor)\n'
                 '  3) Opcoes do desenvolvedor > Depuracao USB: ligar\n'
                 '  4) aceite "Permitir depuracao USB?" na tela do celular')
    if len(d) > 1:
        sys.exit('mais de um aparelho conectado:\n  ' + '\n  '.join(d) + '\nuse ANDROID_SERIAL=<serial>')
    return d[0]


def demo_mode(on):
    """Barra de status limpa. So mexe no System UI, nunca no app."""
    if on:
        adb('shell', 'settings', 'put', 'global', 'sysui_demo_allowed', '1')
        cmds = [
            ('enter',),
            ('clock', '-e', 'hhmm', '1800'),
            ('battery', '-e', 'level', '100', '-e', 'plugged', 'false'),
            ('network', '-e', 'wifi', 'show', '-e', 'level', '4'),
            ('network', '-e', 'mobile', 'show', '-e', 'datatype', 'none', '-e', 'level', '4'),
            ('notifications', '-e', 'visible', 'false'),
        ]
    else:
        cmds = [('exit',)]
    for c in cmds:
        adb('shell', 'am', 'broadcast', '-a', 'com.android.systemui.demo',
            '-e', 'command', c[0], *c[1:], check=False)


def main():
    a = argparse.ArgumentParser()
    a.add_argument('--name', help='nome do arquivo, sem .png (ex: carteira)')
    a.add_argument('--out', default=str(OUT))
    a.add_argument('--launch', action='store_true', help='abrir o app Virtus antes de capturar')
    a.add_argument('--wait', type=float, default=0, help='segundos de espera antes do print')
    a.add_argument('--demo', action='store_true', help='tentar demo mode (ignorado no One UI)')
    a.add_argument('--limpo', action='store_true', help='cortar barra de status e de navegacao')
    a.add_argument('--crop-top', type=int, default=110, help='px cortados no topo com --limpo')
    a.add_argument('--crop-bottom', type=int, default=130, help='px cortados no rodape com --limpo')
    a.add_argument('--off', action='store_true', help='desligar o demo mode e sair')
    a.add_argument('--list', action='store_true', help='listar aparelhos e sair')
    o = a.parse_args()

    if o.list:
        print(adb('devices', '-l').strip())
        return

    require_device()

    if o.off:
        demo_mode(False)
        print('demo mode desligado')
        return

    if o.demo:
        demo_mode(True)
        time.sleep(1)

    if o.launch:
        adb('shell', 'monkey', '-p', PKG, '-c', 'android.intent.category.LAUNCHER', '1', check=False)
        time.sleep(3)

    if not o.name:
        sys.exit('faltou --name (ex: --name carteira)')

    if o.wait:
        time.sleep(o.wait)

    out = pathlib.Path(o.out)
    out.mkdir(parents=True, exist_ok=True)
    png = out / (o.name + '.png')
    data = adb('exec-out', 'screencap', '-p', binary=True)
    if not data.startswith(b'\x89PNG'):
        sys.exit('screencap nao devolveu PNG (aparelho bloqueado?)')
    png.write_bytes(data)

    if o.limpo:
        from PIL import Image
        im = Image.open(png)
        w, h = im.size
        im.crop((0, o.crop_top, w, h - o.crop_bottom)).save(png)

    try:
        from PIL import Image
        w, h = Image.open(png).size
        print('saved %s  %dx%d  %d KB' % (png, w, h, png.stat().st_size // 1024))
    except Exception:
        print('saved %s  %d KB' % (png, png.stat().st_size // 1024))


if __name__ == '__main__':
    main()
