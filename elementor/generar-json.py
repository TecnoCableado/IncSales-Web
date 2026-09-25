#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Convierte las secciones de una página HTML de este proyecto en plantillas
JSON importables en Elementor GRATUITO (una por sección).

Solo emite widgets y contenedores de la versión gratuita. Nada de CSS por
widget, animaciones ni widgets Pro.
"""
import json, re, sys, os, hashlib
from html.parser import HTMLParser

# ---- Paleta. Se teclea una vez en Ajustes del sitio → Colores globales ----
COL = {
    "primario": "#1e5bd4", "secundario": "#0b3587", "titulo": "#21252d",
    "exito": "#00874a", "cuerpo": "#4d535d", "tenue": "#6a6f78",
    "linea": "#dbdee3", "lienzo": "#f4f6f9", "azul": "#f2f7ff",
    "ambar": "#8a5a00", "ambarTenue": "#fff7e9", "blanco": "#ffffff",
    "claro": "#b9cbe8", "noche": "#021035",
}

# Fondos noche por familia de producto. Se generaron en OKLab con la misma
# claridad que --noche: solo cambia el matiz, por eso se sienten igual de
# profundos y ninguno compite con los otros. Ver productos.css.
NOCHE_FAM = {
    "p-crm": "#27031b", "p-forms": "#27031b", "p-correo": "#27031b",
    "p-cotiza": "#001c1a", "p-facturacion": "#001c1a", "p-woosync": "#001c1a",
    "p-proveedores": "#001c1a", "p-orquestador": "#001c1a", "p-portal": "#001c1a",
    "p-inventarios": "#19092e", "p-compras": "#19092e",
    "p-whatsapp": "#001c04",
    "p-erp": "#021035", "p-migracion": "#021035", "p-metodo": "#021035",
}
CLARO_FAM = {
    "p-crm": "#e6bdd4", "p-forms": "#e6bdd4", "p-correo": "#e6bdd4",
    "p-cotiza": "#a2d7d2", "p-facturacion": "#a2d7d2", "p-woosync": "#a2d7d2",
    "p-proveedores": "#a2d7d2", "p-orquestador": "#a2d7d2", "p-portal": "#a2d7d2",
    "p-inventarios": "#d0c3ea", "p-compras": "#d0c3ea",
    "p-whatsapp": "#b0d6ba",
    "p-erp": "#b9cbe8", "p-migracion": "#b9cbe8", "p-metodo": "#b9cbe8",
}
def familia(clases):
    """Devuelve la clase p-* de la seccion, si la trae."""
    for c in clases.split():
        if c in NOCHE_FAM: return c
    return None
FONDO = {"seccion--gris": COL["lienzo"], "seccion--azul": COL["azul"],
         "seccion--oscura": COL["secundario"]}

_n = [0]
_sal = [""]          # el prefijo del archivo, para que dos páginas no repitan ids
def ident(semilla=""):
    """Elementor exige id único por elemento. Determinista para que
    regenerar no produzca diferencias falsas en git."""
    _n[0] += 1
    return hashlib.md5(f"{_sal[0]}-{semilla}-{_n[0]}".encode()).hexdigest()[:7]

def px(v):        return {"unit": "px", "size": v, "sizes": []}
def caja(t, r, b, l, link=False):
    return {"unit": "px", "top": str(t), "right": str(r), "bottom": str(b),
            "left": str(l), "isLinked": link}

def marcar_centro(elementos):
    """En Elementor la alineación no vive en el contenedor sino en cada widget."""
    for e in elementos:
        if e.get("elType") == "widget":
            e["settings"]["align"] = "center"
        elif e.get("elements"):
            marcar_centro(e["elements"])

def contenedor(hijos, **s):
    return {"id": ident("c"), "elType": "container", "settings": s,
            "elements": hijos, "isInner": False}

def widget(tipo, s):
    return {"id": ident(tipo), "elType": "widget", "widgetType": tipo,
            "settings": s, "elements": [], "isInner": False}

# ---------------------------------------------------------------- widgets
def w_titulo(texto, nivel="h2", color=None, centro=False, tam=None):
    s = {"title": texto, "header_size": nivel}
    if centro: s["align"] = "center"
    if color:  s["title_color"] = color
    if tam:
        s["typography_typography"] = "custom"
        s["typography_font_size"] = px(tam)
        s["typography_font_weight"] = "600"
    return widget("heading", s)

def w_texto(html, color=None, centro=False, tam=None):
    s = {"editor": html}
    if centro: s["align"] = "center"
    if color:  s["text_color"] = color
    if tam:
        s["typography_typography"] = "custom"
        s["typography_font_size"] = px(tam)
    return widget("text-editor", s)

def w_boton(texto, url, variante="", centro=False):
    s = {"text": texto, "link": {"url": url, "is_external": "", "nofollow": ""},
         "size": "md", "border_radius": caja(6, 6, 6, 6, True),
         "text_padding": caja(15, 26, 15, 26)}
    s["align"] = "center" if centro else "left"
    if "btn--linea" in variante:
        s.update({"background_color": "#00000000", "button_text_color": COL["primario"],
                  "border_border": "solid", "border_width": caja(1, 1, 1, 1, True),
                  "border_color": COL["linea"]})
    elif "btn--blanco" in variante:
        s.update({"background_color": COL["blanco"], "button_text_color": COL["secundario"]})
    elif "btn--lineaclara" in variante:
        s.update({"background_color": "#00000000", "button_text_color": COL["blanco"],
                  "border_border": "solid", "border_width": caja(1, 1, 1, 1, True),
                  "border_color": "rgba(255,255,255,0.4)"})
    else:
        s.update({"background_color": COL["primario"], "button_text_color": COL["blanco"]})
    if "btn--bloque" in variante:
        s["align"] = "justify"
    return widget("button", s)

ICONO = {"ok": {"value": "fas fa-check", "library": "fa-solid"},
         "no": {"value": "fas fa-times", "library": "fa-solid"},
         "ar": {"value": "fas fa-arrow-right", "library": "fa-solid"}}

def w_lista(items, clase=""):
    tipo = "no" if "lista--no" in clase else ("ok" if "lista--ok" in clase else "ar")
    color = {"ok": COL["exito"], "no": "#a7abb3", "ar": COL["cuerpo"]}[tipo]
    return widget("icon-list", {
        "icon_list": [{"_id": ident("li"), "text": t,
                       "selected_icon": dict(ICONO[tipo])} for t in items],
        "space_between": px(14), "icon_size": px(17), "icon_color": color,
        "icon_self_align": "left",
        "text_color": COL["tenue"] if tipo == "no" else COL["cuerpo"],
        "icon_typography_typography": "custom",
        "icon_typography_font_size": px(16),
    })

def w_acordeon(pares):
    """Acordeon anidado: es widget de la version GRATUITA desde 3.15.
    Los titulos van en settings.items y cada respuesta es un contenedor hijo."""
    items, hijos = [], []
    for titulo, cuerpo in pares:
        iid = ident("acc")
        items.append({"_id": iid, "item_title": titulo})
        hijos.append(contenedor([w_texto(cuerpo)],
                                flex_direction="column",
                                padding=caja(0, 0, 22, 0)))
    return {"id": ident("faq"), "elType": "widget", "widgetType": "nested-accordion",
            "settings": {"items": items, "default_state": "all_collapsed",
                         "title_typography_typography": "custom",
                         "title_typography_font_size": px(17),
                         "title_typography_font_weight": "600",
                         "accordion_item_title_space_between": px(0),
                         "accordion_padding": caja(20, 40, 20, 0)},
            "elements": hijos, "isInner": False}

def recolectar(n, tag):
    """Todos los descendientes con esa etiqueta, en orden."""
    out = []
    for h in n["hijos"]:
        if h["tag"] == tag: out.append(h)
        out += recolectar(h, tag)
    return out

def w_nota_formulario(campos=None, ayudas=None, legal=None):
    """Elementor gratuito NO trae widget de formulario. Se deja el aviso
    para que quien arme sepa que ahi va el codigo corto del plugin."""
    return contenedor([
        widget("heading", {"title": "Aqui va el formulario", "header_size": "div",
                           "title_color": COL["secundario"],
                           "typography_typography": "custom",
                           "typography_font_size": px(16),
                           "typography_font_weight": "600"}),
        w_texto("Elementor gratuito no trae widget de formulario. Inserta aqui el codigo corto de "
                "Fluent Forms o WPForms Lite, y dale estilo en Estilo del tema, Campos de formulario."
                + (" Campos, en este orden: " + "; ".join(campos) + "."
                   if campos else "")
                + (" Textos de ayuda: " + " ".join(ayudas) if ayudas else "")
                + (" Aviso legal bajo el boton: " + " ".join(legal) if legal else ""))],
        background_background="classic", background_color=COL["azul"],
        border_radius=caja(8, 8, 8, 8, True), padding=caja(18, 20, 18, 20),
        flex_direction="column", flex_gap={"unit":"px","size":4,"column":"4","row":"4"})

def w_imagen(src, alto=None):
    s = {"image": {"url": src, "id": ""}}
    if alto:
        s["width"] = px(alto)
    return widget("image", s)

def w_etiqueta(texto, tono=""):
    fondo, tinta = COL["azul"], COL["primario"]
    if "verde" in tono: fondo, tinta = "#e8f5ee", COL["exito"]
    elif "ambar" in tono: fondo, tinta = COL["ambarTenue"], COL["ambar"]
    elif "gris"  in tono: fondo, tinta = COL["lienzo"], COL["tenue"]
    return contenedor([widget("heading", {
        "title": texto, "header_size": "div", "title_color": tinta,
        "typography_typography": "custom", "typography_font_size": px(12),
        "typography_font_weight": "600", "typography_text_transform": "uppercase",
        "typography_letter_spacing": px(0.6)})],
        content_width="full",
        background_background="classic", background_color=fondo,
        border_radius=caja(999, 999, 999, 999, True),
        padding=caja(5, 11, 5, 11), flex_direction="row",
        margin=caja(0, 0, 14, 0))

# ------------------------------------------------------- lector del HTML
class Lector(HTMLParser):
    """Arma un árbol simple de los nodos que nos importan."""
    INTERES = {"section", "div", "header", "footer", "h1", "h2", "h3", "h4", "h5", "h6",
               "p", "ul", "ol", "li", "a", "img", "span", "strong", "em", "b", "small",
               "svg", "nav", "details", "summary", "blockquote",
               "form", "label", "select", "option", "textarea", "input", "button",
               "article", "aside", "figure", "figcaption",
               "table", "thead", "tbody", "tfoot", "tr", "td", "th", "caption"}
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.pila = [{"tag": "raiz", "clase": "", "hijos": [], "texto": ""}]
        self.svg = 0
    VACIAS = {"img", "br", "hr", "input", "meta", "link"}
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "svg": self.svg += 1; return
        if self.svg: return
        if tag == "br":
            self.pila[-1]["hijos"].append({"tag": "#texto", "clase": "", "texto": " ", "hijos": []})
            return
        if tag not in self.INTERES: return
        nodo = {"tag": tag, "clase": a.get("class", ""), "href": a.get("href", ""),
                "src": a.get("src", ""), "alt": a.get("alt", ""),
                "id": a.get("id", ""), "hijos": [], "texto": ""}
        self.pila[-1]["hijos"].append(nodo)
        # Las etiquetas vacías NO abren contexto: si se empujan, todo lo que
        # viene después queda colgando dentro de ellas y se pierde.
        if tag not in self.VACIAS:
            self.pila.append(nodo)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
    def handle_endtag(self, tag):
        if tag == "svg": self.svg = max(0, self.svg - 1); return
        if self.svg or tag not in self.INTERES or tag == "br": return
        for i in range(len(self.pila) - 1, 0, -1):
            if self.pila[i]["tag"] == tag:
                del self.pila[i:]; break
    def handle_data(self, d):
        if self.svg: return
        if d.strip():
            # Se guarda como nodo, no como atributo, para no perder el orden
            # respecto de las etiquetas hermanas.
            self.pila[-1]["hijos"].append({"tag": "#texto", "clase": "", "texto": d, "hijos": []})

def escapar(t):
    """El contenido de texto se escapa. Si no, un ejemplo de código
    como <script src="..."> entra al editor de Elementor como marcado real."""
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def texto_de(n):
    if n["tag"] == "#texto":
        return n["texto"]
    t = n.get("texto") or ""
    for h in n["hijos"]:
        t += " " + texto_de(h)
    return re.sub(r"\s+", " ", t).strip()

def html_de(n):
    """Reconstruye el texto conservando solo <strong>, que Elementor sí respeta."""
    partes = [escapar(n.get("texto") or "")]
    for h in n["hijos"]:
        if h["tag"] == "#texto":
            partes.append(escapar(h["texto"]))
        elif h["tag"] in ("strong", "b"):
            partes.append(f"<strong>{html_de(h)}</strong>")
        elif h["tag"] in ("em", "small"):
            partes.append(f"<em>{html_de(h)}</em>")
        elif h["tag"] == "a":
            partes.append(f'<a href="{h["href"]}">{html_de(h)}</a>')
        else:
            partes.append(html_de(h))
    return re.sub(r"\s+", " ", " ".join(p for p in partes if p)).strip()

# ------------------------------------------------------------- traducción
def traducir(n, oscura=False, fam_claro=None):
    """Un nodo del HTML → cero o más elementos de Elementor."""
    c = n["clase"]; t = n["tag"]
    tinta = COL["blanco"] if oscura else None
    cuerpo = (fam_claro or COL["claro"]) if oscura else None

    if t == "img":
        return [w_imagen(n["src"])]

    if t in ("h1", "h2", "h3", "h4", "h5", "h6"):
        tam = {"h1": 52, "h2": 36, "h3": 22, "h4": 18, "h5": 17, "h6": 16}[t]
        if "t-tarjeta" in c: tam = 18
        return [w_titulo(texto_de(n), t, tinta, False, tam)]

    if t == "ol":
        items = [html_de(li) for li in n["hijos"] if li["tag"] == "li"]
        if not items: return []
        return [w_texto("<ol>" + "".join(f"<li>{i}</li>" for i in items) + "</ol>",
                        cuerpo or COL["cuerpo"])]

    if t == "blockquote":
        return [w_texto(f"<blockquote>{html_de(n)}</blockquote>", tinta or COL["titulo"])]

    if t == "table":
        filas = recolectar(n, "tr")
        if not filas: return []
        pie_tabla = [w_texto(html_de(x), COL["tenue"], False, 13)
                     for x in recolectar(n, "caption") if texto_de(x)]
        ncol = max(len([x for x in f["hijos"] if x["tag"] in ("td","th")]) for f in filas)
        ncol = max(1, min(ncol, 6))
        out = []
        for i, f in enumerate(filas):
            celdas = [x for x in f["hijos"] if x["tag"] in ("td","th")]
            cab = all(x["tag"] == "th" for x in celdas) and i == 0
            ws = []
            for x in celdas:
                txt = html_de(x)
                if not txt: txt = "—"
                ws.append(w_titulo(re.sub(r"<[^>]+>", "", txt), "div",
                                   tinta or COL["titulo"], False, 13) if cab
                          else w_texto(txt, cuerpo or COL["cuerpo"], False, 15))
            out.append(contenedor(ws, container_type="grid",
                                  grid_columns_grid={"unit":"fr","size":ncol,"sizes":[]},
                                  grid_columns_grid_mobile={"unit":"fr","size":ncol,"sizes":[]},
                                  grid_gaps={"unit":"px","size":16,"column":"16","row":"8"},
                                  padding=caja(12,0,12,0),
                                  border_border="solid", border_width=caja(0,0,1,0),
                                  border_color=COL["linea"]))
        return [contenedor(out, flex_direction="column",
                           flex_gap={"unit":"px","size":0,"column":"0","row":"0"},
                           border_border="solid", border_width=caja(1,0,0,0),
                           border_color=COL["linea"])] + pie_tabla

    if t in ("caption", "figcaption"):
        return [w_texto(html_de(n), COL["tenue"], False, 13)]

    if t in ("thead","tbody","tfoot","tr","td","th"):
        return []   # los consume la rama de <table>

    if t == "form":
        campos = [texto_de(l) for l in recolectar(n, "label")]
        legal = [texto_de(p) for p in recolectar(n, "p")
                 if "aviso" in texto_de(p).lower() or "privacidad" in texto_de(p).lower()]
        ayudas = [texto_de(d) for d in recolectar(n, "div") if "campo__ayuda" in d["clase"]]
        ayudas += [texto_de(p) for p in recolectar(n, "p") if "campo__ayuda" in p["clase"]]
        botones = [b for b in recolectar(n, "button")]
        piezas = [w_nota_formulario(campos, ayudas, legal)]
        for b in botones:
            piezas.append(w_boton(texto_de(b), "#", b["clase"]))
        return piezas

    if t == "p":
        if "sobre-titulo" in c or "rotulo" in c:
            return [w_titulo(texto_de(n), "div",
                             (fam_claro or COL["primario"]) if oscura else COL["primario"],
                             False, 13)]
        if "apunte" in c:
            return [w_texto(html_de(n), COL["tenue"], "centro" in c, 13)]
        if "entradilla" in c:
            return [w_texto(html_de(n), cuerpo or COL["tenue"], "centro" in c, 19)]
        if "suave" in c or "tenue" in c:
            return [w_texto(html_de(n), cuerpo or COL["tenue"], "centro" in c, None)]
        if "cita__texto" in c:
            return [w_titulo(texto_de(n), "div", tinta, False, 19)]
        if "cita__quien" in c:
            return [w_texto(html_de(n), COL["tenue"], False, 15)]
        if "pantalla__pie" in c:
            return [w_texto(html_de(n), COL["tenue"], False, 13)]
        if "etiqueta" in c or "rotulo" in c:
            return [w_etiqueta(texto_de(n), c)]
        tam = 19 if "entradilla" in c else (13 if ("pauta" in c or "sustento" in c or "nota-pie" in c) else None)
        col = cuerpo
        if "precio" in c:
            return [w_titulo(texto_de(n), "div", tinta, False, 40)]
        if "nota-pie" in c or "sustento" in c or "pauta" in c:
            col = COL["tenue"]
        return [w_texto(f"<p>{html_de(n)}</p>", col, "nota-pie" in c, tam)]

    if t == "ul":
        items = [html_de(li) for li in n["hijos"] if li["tag"] == "li"]
        return [w_lista(items, c)] if items else []

    if t == "a":
        if "btn" in c:
            return [w_boton(texto_de(n), n["href"], c)]
        imgs = [h for h in n["hijos"] if h["tag"] == "img"]
        if imgs and not texto_de(n).strip():
            w = w_imagen(imgs[0]["src"])
            w["settings"]["link_to"] = "custom"
            w["settings"]["link"] = {"url": n["href"], "is_external": "", "nofollow": ""}
            return [w]
        return [w_texto(f'<a href="{n["href"]}">{texto_de(n)}</a>', cuerpo or COL["cuerpo"])]

    if t == "strong":
        return [w_texto(f"<strong>{html_de(n)}</strong>", tinta or COL["titulo"])]

    if t == "span":
        if "chip" in c.split() or "estado" in c.split():
            return [w_etiqueta(texto_de(n), c)]
        if "icono-caja" in c.split():
            return []   # es solo el contenedor del glifo
        if "etiqueta" in c or "rotulo" in c:
            return [w_etiqueta(texto_de(n), c)]
        # Un span suelto dentro de un contenedor es una celda de texto.
        col = cuerpo or COL["cuerpo"]
        if "tabla__si" in c: col = COL["exito"]
        elif "tabla__no" in c: col = COL["tenue"]
        return [w_texto(html_de(n), col)]

    if t == "div" and ("paquete__nombre" in c or "modulo__nombre" in c or "paso__titulo" in c):
        return [w_titulo(texto_de(n), "div", tinta, False, 20)]

    # --- contenedores ---
    if t in ("label", "select", "option", "textarea", "input", "button", "summary"):
        return []

    if t in ("div", "nav", "li", "article", "aside", "figure"):
        if "acordeon" in c.split() or "faq" in c.split():
            pares = []
            for d in recolectar(n, "details"):
                tit = next((texto_de(x) for x in d["hijos"] if x["tag"] == "summary"), "")
                cue = " ".join(html_de(x) for x in d["hijos"] if x["tag"] != "summary")
                if tit: pares.append((tit, cue))
            if pares: return [w_acordeon(pares)]
            return []

        if False:
            pares = []
            for d in n["hijos"]:
                if d["tag"] != "details": continue
                titulo = next((texto_de(x) for x in d["hijos"] if x["tag"] == "summary"), "")
                resto = " ".join(html_de(x) for x in d["hijos"] if x["tag"] != "summary")
                if titulo:
                    pares.append((titulo, resto))
            return [w_acordeon(pares)] if pares else []

        hijos = []
        # El texto que cuelga directamente del contenedor, sin <p> que lo envuelva,
        # se perdía en silencio. Va primero, en el orden en que estaba escrito.
        # El texto suelto y las etiquetas en línea se juntan en un solo párrafo,
        # pero respetando dónde estaban: se acumulan y se vuelcan cuando llega
        # un hijo de bloque o cuando se acaban los hermanos.
        buffer = []
        def volcar():
            if buffer:
                t = re.sub(r"\s+", " ", " ".join(buffer)).strip()
                if t:
                    hijos.append(w_texto(t, cuerpo or COL["cuerpo"]))
                buffer.clear()
        for h in n["hijos"]:
            if h["tag"] == "#texto":
                buffer.append(escapar(h["texto"].strip())); continue
            if h["tag"] in ("strong", "b"):
                buffer.append(f"<strong>{html_de(h)}</strong>"); continue
            if h["tag"] in ("em", "small"):
                buffer.append(f"<em>{html_de(h)}</em>"); continue
            volcar()
            hijos += traducir(h, oscura, fam_claro)
        volcar()
        if not hijos:
            return []
        # --- La maqueta de pantalla del producto NO se traduce: son cientos de
        #     divs que dibujan una interfaz falsa. En Elementor va como IMAGEN.
        # La barra falsa del navegador (puntos y URL) no aporta nada en Elementor.
        if "marco__barra" in c.split() or "marco__puntos" in c.split():
            return []

        # Un .marco solo se vuelve imagen cuando DIBUJA una interfaz, es decir
        # cuando trae un .app adentro. Si lo que enmarca son datos de verdad
        # —una tabla de cifras, por ejemplo— se traduce como cualquier caja.
        def dibuja_interfaz(nodo):
            for h in nodo["hijos"]:
                if "app" in h["clase"].split() or "lienzo-app" in h["clase"].split():
                    return True
                if dibuja_interfaz(h): return True
            return False

        if ("marco" in c.split() and dibuja_interfaz(n)) or "app" in c.split() or "lienzo-app" in c.split():
            return [contenedor([
                w_imagen("assets/pantallas/POR-SUBIR.png"),
                w_texto("Sustituye esta imagen por la captura real de la pantalla. "
                        "La maqueta dibujada con HTML no se traduce a Elementor: se exporta como PNG.",
                        COL["tenue"], False, 13)],
                background_background="classic", background_color=COL["blanco"],
                border_border="solid", border_width=caja(1,1,1,1,True), border_color=COL["linea"],
                border_radius=caja(12,12,12,12,True),
                box_shadow_box_shadow_type="yes",
                box_shadow_box_shadow={"horizontal":0,"vertical":8,"blur":24,"spread":0,
                                       "color":"rgba(15,19,25,0.08)"},
                padding=caja(0,0,0,0), flex_direction="column")]

        if "marco" in c.split():
            return [contenedor(hijos, background_background="classic",
                               background_color=COL["blanco"],
                               border_border="solid", border_width=caja(1,1,1,1,True),
                               border_color=COL["linea"], border_radius=caja(12,12,12,12,True),
                               box_shadow_box_shadow_type="yes",
                               box_shadow_box_shadow={"horizontal":0,"vertical":8,"blur":24,
                                                      "spread":0,"color":"rgba(15,19,25,0.08)"},
                               padding=caja(20,20,20,20,True), flex_direction="column")]

        if "envoltura" in c.split():
            w = 820 if "envoltura--angosta" in c else (1280 if "envoltura--ancha" in c else 1140)
            return [contenedor(hijos, content_width="boxed", boxed_width=px(w),
                               padding=caja(0,24,0,24), padding_mobile=caja(0,20,0,20),
                               flex_direction="column",
                               flex_gap={"unit":"px","size":0,"column":"0","row":"0"})]

        if "encabezado" in c.split():
            e = dict(flex_direction="column", content_width="boxed", boxed_width=px(720),
                     margin=caja(0,0,40,0),
                     flex_gap={"unit":"px","size":12,"column":"12","row":"12"})
            if "encabezado--centro" in c:
                e["flex_align_items"] = "center"
                marcar_centro(hijos)
            return [contenedor(hijos, **e)]

        if "rejilla" in c.split():
            m = re.search(r"rejilla--(\d)", c)
            n = int(m.group(1)) if m else 3
            return [contenedor(hijos, container_type="grid",
                               grid_columns_grid={"unit":"fr","size":n,"sizes":[]},
                               grid_columns_grid_tablet={"unit":"fr","size":2 if n>2 else n,"sizes":[]},
                               grid_columns_grid_mobile={"unit":"fr","size":1,"sizes":[]},
                               grid_gaps={"unit":"px","size":24,"column":"24","row":"24"})]

        if "portada__reja" in c.split() or "portada__cabeza" in c.split():
            return [contenedor(hijos, container_type="grid",
                               grid_columns_grid={"unit":"fr","size":2,"sizes":[]},
                               grid_columns_grid_tablet={"unit":"fr","size":1,"sizes":[]},
                               grid_columns_grid_mobile={"unit":"fr","size":1,"sizes":[]},
                               grid_gaps={"unit":"px","size":48,"column":"48","row":"32"})]

        if "portada__lado" in c.split() or "portada__acciones" in c.split():
            return [contenedor(hijos, flex_direction="column",
                               flex_gap={"unit":"px","size":16,"column":"16","row":"16"})]

        if "portada__firma" in c.split():
            items = [texto_de(h) for h in n["hijos"] if h["tag"] == "span"]
            return [w_lista(items, "lista--ok")] if items else [
                contenedor(hijos, flex_direction="column",
                           flex_gap={"unit":"px","size":8,"column":"8","row":"8"})]

        if "migas" in c.split():
            partes = [texto_de(h) for h in n["hijos"] if h["tag"] == "li"]
            return [w_texto(" &rsaquo; ".join(partes), cuerpo or COL["tenue"], False, 13)] if partes else []

        if "icono-caja" in c.split():
            return [contenedor(hijos, background_background="classic",
                               background_color=COL["azul"],
                               border_radius=caja(9,9,9,9,True),
                               padding=caja(9,9,9,9,True), content_width="full",
                               flex_direction="row", flex_align_items="center",
                               margin=caja(0,0,16,0))]

        if "ancho" in c.split():
            return [contenedor(hijos, content_width="boxed",
                               boxed_width=px(820 if "ancho--angosto" in c else 1140),
                               padding=caja(0, 24, 0, 24), padding_mobile=caja(0, 20, 0, 20),
                               flex_direction="column", flex_gap={"unit":"px","size":0,"column":"0","row":"0"})]
        if "cols" in c.split():
            m = re.search(r"cols-(\d)", c)
            ncol = int(m.group(1)) if m else 3
            return [contenedor(hijos, container_type="grid",
                               grid_columns_grid={"unit":"fr","size":ncol,"sizes":[]},
                               grid_columns_grid_tablet={"unit":"fr","size":2 if ncol>2 else ncol,"sizes":[]},
                               grid_columns_grid_mobile={"unit":"fr","size":1,"sizes":[]},
                               grid_gaps={"unit":"px","size":24,"column":"24","row":"24"})]
        if "par" in c.split():
            return [contenedor(hijos, container_type="grid",
                               grid_columns_grid={"unit":"fr","size":2,"sizes":[]},
                               grid_columns_grid_tablet={"unit":"fr","size":1,"sizes":[]},
                               grid_columns_grid_mobile={"unit":"fr","size":1,"sizes":[]},
                               grid_gaps={"unit":"px","size":48,"column":"48","row":"32"})]
        if "planes" in c.split():
            return [contenedor(hijos, container_type="grid",
                               grid_columns_grid={"unit":"fr","size":3,"sizes":[]},
                               grid_columns_grid_tablet={"unit":"fr","size":2,"sizes":[]},
                               grid_columns_grid_mobile={"unit":"fr","size":1,"sizes":[]},
                               grid_gaps={"unit":"px","size":24,"column":"24","row":"24"})]
        if "plan" in c.split():
            e = dict(background_background="classic", background_color=COL["blanco"],
                     border_border="solid",
                     border_width=caja(*([2]*4 if "plan--elegido" in c else [1]*4), True),
                     border_color=COL["primario"] if "plan--elegido" in c else COL["linea"],
                     border_radius=caja(12,12,12,12,True),
                     padding=caja(28,28,28,28,True), padding_mobile=caja(22,22,22,22,True),
                     flex_direction="column",
                     flex_gap={"unit":"px","size":10,"column":"10","row":"10"})
            if "plan--elegido" in c:
                e.update(box_shadow_box_shadow_type="yes",
                         box_shadow_box_shadow={"horizontal":0,"vertical":8,"blur":24,
                                                "spread":0,"color":"rgba(15,19,25,0.08)"})
            return [contenedor(hijos, **e)]
        if "tarjeta" in c.split() or "paquete" in c.split() or "cita" in c.split():
            s = dict(background_background="classic",
                     background_color=("rgba(255,255,255,0.06)" if "tarjeta--tinta" in c
                                       else COL["lienzo"] if ("tarjeta--plana" in c or "cita" in c)
                                       else COL["blanco"]),
                     border_radius=caja(10, 10, 10, 10, True),
                     padding=caja(28, 28, 28, 28, True), padding_mobile=caja(22, 22, 22, 22, True),
                     flex_direction="column",
                     flex_gap={"unit":"px","size":12,"column":"12","row":"12"})
            if "tarjeta--plana" not in c and "cita" not in c:
                s.update(border_border="solid",
                         border_width=caja(2 if "paquete--elegido" in c else 1,
                                           2 if "paquete--elegido" in c else 1,
                                           2 if "paquete--elegido" in c else 1,
                                           2 if "paquete--elegido" in c else 1, True),
                         border_color=COL["primario"] if "paquete--elegido" in c else COL["linea"])
            if "tarjeta--sombra" in c or "paquete--elegido" in c:
                s.update(box_shadow_box_shadow_type="yes",
                         box_shadow_box_shadow={"horizontal":0,"vertical":2,"blur":6,
                                                "spread":0,"color":"rgba(15,19,25,0.07)"})
            return [contenedor(hijos, **s)]
        if "aviso" in c.split():
            return [contenedor(hijos, background_background="classic",
                               background_color=COL["ambarTenue"] if "aviso--ambar" in c else COL["azul"],
                               border_radius=caja(8, 8, 8, 8, True),
                               padding=caja(18, 20, 18, 20), flex_direction="column",
                               flex_gap={"unit":"px","size":4,"column":"4","row":"4"})]
        if "cabeza" in c.split():
            s = dict(flex_direction="column", content_width="boxed", boxed_width=px(720),
                     margin=caja(0, 0, 40, 0),
                     flex_gap={"unit":"px","size":12,"column":"12","row":"12"})
            if "cabeza--centro" in c:
                s["flex_align_items"] = "center"
                marcar_centro(hijos)
            return [contenedor(hijos, **s)]
        if "centrado" in c.split():
            marcar_centro(hijos)
            return [contenedor(hijos, flex_direction="column", flex_align_items="center",
                               margin=caja(40, 0, 0, 0),
                               flex_gap={"unit":"px","size":12,"column":"12","row":"12"})]
        if "tabla__fila" in c.split():
            return [contenedor(hijos, container_type="grid",
                               grid_columns_grid={"unit":"fr","size":3,"sizes":[]},
                               grid_columns_grid_mobile={"unit":"fr","size":3,"sizes":[]},
                               grid_gaps={"unit":"px","size":16,"column":"16","row":"8"},
                               padding=caja(14, 0, 14, 0),
                               border_border="solid", border_width=caja(0, 0, 1, 0),
                               border_color=COL["linea"])]
        if "barra__fila" in c.split():
            return [contenedor(hijos, flex_direction="row", flex_align_items="center",
                               flex_gap={"unit":"px","size":24,"column":"24","row":"24"},
                               flex_gap_mobile={"unit":"px","size":12,"column":"12","row":"12"},
                               min_height=px(72))]
        if "barra__menu" in c.split():
            return [contenedor(hijos, flex_direction="row", flex_align_items="center",
                               flex_gap={"unit":"px","size":22,"column":"22","row":"22"},
                               content_width="full")]
        if "datos" in c.split() or "logos" in c.split():
            return [contenedor(hijos, container_type="grid",
                               grid_columns_grid={"unit":"fr","size":2,"sizes":[]},
                               grid_columns_grid_mobile={"unit":"fr","size":2,"sizes":[]},
                               grid_gaps={"unit":"px","size":24,"column":"24","row":"24"})]
        if "pantalla" in c.split():
            return [contenedor(hijos, background_background="classic", background_color=COL["blanco"],
                               border_border="solid", border_width=caja(1, 1, 1, 1, True),
                               border_color=COL["linea"], border_radius=caja(10, 10, 10, 10, True),
                               box_shadow_box_shadow_type="yes",
                               box_shadow_box_shadow={"horizontal":0,"vertical":8,"blur":24,
                                                      "spread":0,"color":"rgba(15,19,25,0.08)"},
                               flex_direction="column", padding=caja(0, 0, 0, 0))]
        if "modulo" in c.split():
            return [contenedor(hijos, flex_direction="column",
                               flex_gap={"unit":"px","size":8,"column":"8","row":"8"})]
        if "tabla" in c.split():
            return [contenedor(hijos, flex_direction="column",
                               border_border="solid", border_width=caja(1, 0, 0, 0),
                               border_color=COL["linea"],
                               flex_gap={"unit":"px","size":0,"column":"0","row":"0"})]
        if "interruptor" in c.split():
            return [contenedor(hijos, flex_direction="row", flex_align_items="center",
                               flex_gap={"unit":"px","size":4,"column":"4","row":"4"},
                               border_border="solid", border_width=caja(1, 1, 1, 1, True),
                               border_color=COL["linea"], border_radius=caja(999, 999, 999, 999, True),
                               padding=caja(4, 4, 4, 4, True), content_width="full")]
        if "campo" in c.split():
            return [contenedor(hijos, flex_direction="column",
                               flex_gap={"unit":"px","size":6,"column":"6","row":"6"},
                               margin=caja(0, 0, 16, 0))]
        if "paso" in c.split():
            return [contenedor(hijos, flex_direction="row", flex_gap={"unit":"px","size":16,"column":"16","row":"16"},
                               padding=caja(14, 0, 14, 0))]
        return [contenedor(hijos, flex_direction="column",
                           flex_gap={"unit":"px","size":12,"column":"12","row":"12"})]
    return []

def seccion_a_json(nodo, titulo):
    c = nodo["clase"]
    oscura = ("seccion--oscura" in c or "portada--tinta" in c or "bloque--tinta" in c
              or "pie" in c.split())
    fam = familia(c)
    fam_claro = CLARO_FAM.get(fam)
    hijos = []
    for h in nodo["hijos"]:
        hijos += traducir(h, oscura, fam_claro)
    rel = 48 if ("seccion--corta" in c or "bloque--corto" in c) else 88
    s = dict(content_width="full", flex_direction="column",
             padding=caja(rel, 0, rel, 0),
             padding_tablet=caja(min(rel, 64), 0, min(rel, 64), 0),
             padding_mobile=caja(48, 0, 48, 0))
    for clase, color in FONDO.items():
        if clase in c:
            s.update(background_background="classic", background_color=color)
    # El sistema de diseño bueno: bloque hundido, y portada o bloque en tinta,
    # que se tiñe con el noche de la familia del producto.
    if "bloque--hundido" in c:
        s.update(background_background="classic", background_color=COL["lienzo"])
    if "portada--tinta" in c or "bloque--tinta" in c:
        s.update(background_background="classic",
                 background_color=NOCHE_FAM.get(fam, COL["noche"]))
    if "portada" in c.split() and "portada--tinta" not in c:
        s.update(background_background="classic", background_color=COL["blanco"])
    if "pie" in c.split():
        s.update(background_background="classic", background_color=COL["secundario"],
                 padding=caja(56, 0, 28, 0), padding_mobile=caja(48, 0, 24, 0))
    if "barra" in c.split():
        s.update(background_background="classic", background_color=COL["blanco"],
                 padding=caja(0, 0, 0, 0),
                 padding_tablet=caja(0, 0, 0, 0), padding_mobile=caja(0, 0, 0, 0),
                 border_border="solid", border_width=caja(0, 0, 1, 0),
                 border_color=COL["linea"])
    if nodo.get("id"):
        s["_element_id"] = nodo["id"]
    return {"version": "0.4", "title": titulo, "type": "container",
            "content": [contenedor(hijos, **s)], "page_settings": []}

def procesar(ruta, destino, prefijo):
    html = open(ruta, encoding="utf-8").read()
    etiquetas = []
    for m in re.finditer(r"<!--\s*(S\d+)\s*·\s*([^\n>]*?)-->", html):
        etiquetas.append((m.group(1), m.group(2).strip()))
    p = Lector(); p.feed(html)
    raiz = p.pila[0]
    bloques = [n for n in raiz["hijos"] if n["tag"] in ("section", "header", "footer")]
    os.makedirs(destino, exist_ok=True)
    # Se borran los archivos previos de ESTA pagina antes de escribir. Si no,
    # al renombrar una seccion el archivo viejo se queda huerfano y acabaria
    # importandose a WordPress como una seccion fantasma.
    import glob as _glob
    for viejo in _glob.glob(os.path.join(destino, prefijo + "-S*.json")):
        os.remove(viejo)
    hechos = []
    for i, b in enumerate(bloques):
        cod, nombre = etiquetas[i] if i < len(etiquetas) else (f"S{i+1:02d}", b.get("id") or b["tag"])
        _n[0] = i * 1000
        _sal[0] = prefijo
        doc = seccion_a_json(b, f"{prefijo} · {cod} {nombre}")
        arch = os.path.join(destino, f"{prefijo}-{cod}-{re.sub(r'[^a-z0-9]+','-',nombre.lower()).strip('-')}.json")
        with open(arch, "w", encoding="utf-8") as f:
            json.dump(doc, f, ensure_ascii=False, indent=1)
        hechos.append((os.path.basename(arch), contar(doc)))
    return hechos

def contar(doc):
    n = 0
    def rec(e):
        nonlocal n
        n += 1
        for h in e.get("elements", []): rec(h)
    for e in doc["content"]: rec(e)
    return n

if __name__ == "__main__":
    origen, destino, prefijo = sys.argv[1], sys.argv[2], sys.argv[3]
    for arch, n in procesar(origen, destino, prefijo):
        print(f"  {n:4d} elementos  {arch}")
