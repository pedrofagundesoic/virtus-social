#!/usr/bin/env python3
"""Render out/*.html → out/*.png at 1080×1350 with Playwright (Chromium).
   py -3.12 render.py           only HTMLs without a PNG (or older than the HTML)
   py -3.12 render.py --all     re-render everything
   py -3.12 render.py slug1 slug2
"""
import sys, pathlib
from playwright.sync_api import sync_playwright
OUT = pathlib.Path(__file__).resolve().parent / 'out'

def targets():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    htmls = sorted(OUT.glob('*.html'))
    if args: htmls = [h for h in htmls if h.stem in args]
    if '--all' in sys.argv: return htmls
    return [h for h in htmls if not h.with_suffix('.png').exists() or h.with_suffix('.png').stat().st_mtime < h.stat().st_mtime]

def main():
    todo = targets()
    if not todo: print('nothing to render'); return
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={'width': 1080, 'height': 1350}, device_scale_factor=1)
        for h in todo:
            page.goto(h.resolve().as_uri())
            page.wait_for_load_state('networkidle')
            page.evaluate('document.fonts.ready')
            page.evaluate('Promise.all([...document.images].map(i => i.complete ? 1 : new Promise(r => { i.onload = i.onerror = r; })))')
            png = h.with_suffix('.png')
            page.screenshot(path=str(png), clip={'x': 0, 'y': 0, 'width': 1080, 'height': 1350})
            print('rendered', png.name, png.stat().st_size // 1024, 'KB')
        browser.close()

if __name__ == '__main__': main()
