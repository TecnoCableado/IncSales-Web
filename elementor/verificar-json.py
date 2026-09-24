#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Compara el texto visible del HTML contra el texto que quedó en los JSON.
Lo que aparezca aquí es contenido que el generador tiró en silencio."""
import json, re, sys, glob, os, unicodedata, html as _html

def normalizar(t):
    t = _html.unescape(_html.unescape(t))
    t = unicodedata.normalize("NFKD", t)
    t = "".join(c for c in t if not unicodedata.combining(c))
    t = re.sub(r"[^a-z0-9 ]", " ", t.lower())
    return re.sub(r"\s+", " ", t).strip()

def palabras(t):
    return [p for p in normalizar(t).split() if len(p) > 3]

def texto_json(d):
    out = []
    def rec(e):
        s = e.get("settings", {})
        for k in ("title", "editor", "text"):
            if isinstance(s.get(k), str): out.append(s[k])
        for it in s.get("icon_list", []) or []:
            if isinstance(it, dict) and it.get("text"): out.append(it["text"])
        for it in s.get("items", []) or []:
            if isinstance(it, dict) and it.get("item_title"): out.append(it["item_title"])
        for h in e.get("elements", []): rec(h)
    for e in d["content"]: rec(e)
    return re.sub(r"<[^>]+>", " ", " ".join(out))

def secciones_html(ruta):
    html = open(ruta, encoding="utf-8").read()
    html = re.sub(r"<svg.*?</svg>", " ", html, flags=re.S)
    bloques = re.findall(r"<!--\s*(S\d+)\s*·[^>]*-->\s*(<(?:section|header|footer)[\s\S]*?</(?:section|header|footer)>)", html)
    return {cod: re.sub(r"<[^>]+>", " ", cuerpo) for cod, cuerpo in bloques}

def main(pagina, carpeta, prefijo):
    sec = secciones_html(pagina)
    problemas = 0
    for cod in sorted(sec):
        arch = glob.glob(os.path.join(carpeta, f"{prefijo}-{cod}-*.json"))
        if not arch:
            print(f"  {cod}: SIN ARCHIVO JSON"); problemas += 1; continue
        d = json.load(open(arch[0], encoding="utf-8"))
        src, dst = set(palabras(sec[cod])), set(palabras(texto_json(d)))
        faltan = src - dst
        pct = 100 * len(src & dst) // max(1, len(src))
        estado = "OK  " if not faltan else "FUGA"
        print(f"  {estado} {cod}  {pct:3d}% conservado  ({len(src)} palabras únicas)")
        if faltan:
            problemas += 1
            print(f"        perdidas: {' '.join(sorted(faltan)[:18])}")
    return problemas

if __name__ == "__main__":
    n = main(sys.argv[1], sys.argv[2], sys.argv[3])
    print(f"\n{'TODO CONSERVADO' if n == 0 else str(n) + ' SECCIONES CON FUGA DE CONTENIDO'}")
    sys.exit(1 if n else 0)
