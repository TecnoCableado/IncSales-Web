# LOGOTIPOS DE INCSALES

Los originales que entregó César, renombrados con un criterio único: primero qué es
(`completo`, `texto`, `icono`), luego de qué color va (`blanco`, `negro`, `degradado`, `calado`).
Sin sufijo = la versión principal de esa pieza.

| Archivo | Qué es | Cuándo se usa | Original |
|---|---|---|---|
| **incsales-completo.svg** | Icono en degradado + texto en negro | **El principal.** Barra superior y cualquier fondo claro | Logo Principal IncSales.svg |
| **incsales-completo-blanco.svg** | Icono + texto, todo blanco | Fondos oscuros: pie de página, secciones tinta, portadas oscuras | Logo IncSales Blancos.svg |
| **incsales-completo-negro.svg** | Icono + texto, todo negro `#191919` | Impresión a una tinta, documentos, fax de la vida real | Logo Negro IncSales.svg |
| **incsales-texto.svg** | Solo la palabra «IncSales», negro | Cuando el icono ya aparece cerca y repetirlo estorba | Logo IncSales.svg |
| **incsales-texto-blanco.svg** | Solo la palabra, blanco | Lo mismo, sobre fondo oscuro | Logo Blanco IncSales.svg |
| **incsales-texto-degradado.svg** | Solo la palabra, en degradado | Usar con cuidado: solo sobre blanco y en tamaño grande | Logo Degradado IncSales.svg |
| **incsales-icono.svg** | Disco en degradado con las flechas en blanco | **El icono principal.** Favicon, avatar, app, esquinas chicas | Icono IncSales Blanco.svg |
| **incsales-icono-calado.svg** | Disco en degradado con las flechas caladas (transparentes) | Sobre fondos de color plano donde se quiere que el fondo se vea a través de las flechas | Icono IncSales.svg |
| **incsales-icono-blanco.svg** | Todo blanco, flechas caladas | Sobre foto o sobre un color fuerte, a una sola tinta | Favicon Blanco.svg |

`Logo Texto IncSales.svg` no se copió: es byte por byte idéntico a `Logo IncSales.svg`.

## Colores de la marca, sacados de los propios SVG
- Degradado del icono: `#0087ff` → `#0175f4` → `#0355e0` → `#0541d3` → `#063acf` → `#0734c9` → `#0c1eb5` → `#0f17ae`
- Degradado del texto: `#0188fd` → … → `#001faa`
- Negro del texto: `#191919`

En `base.css` están como tokens: `--marca-inicio`, `--marca-fin`, `--marca-negro` y `--degradado-marca`.

## Dónde está puesto cada uno en el sitio
- **Barra superior** de las 22 páginas → `incsales-completo.svg`, a 32 px de alto (27 px por debajo de 400 px de ancho).
- **Pie** de las 22 páginas → `incsales-completo-blanco.svg`, a 36 px de alto.
- **Favicon** de las 22 páginas → `incsales-icono.svg` (`<link rel="icon" type="image/svg+xml">`).
- **Maquetas del sistema** (`.ventana__marca`, 16 en todo el sitio) → `incsales-icono.svg` a 19 px, junto al nombre.

## Reglas
1. **Nunca se recolorea el logotipo por CSS** (ni `filter`, ni `fill`, ni `opacity` para simular otro tono). Para cada fondo hay ya una variante: se usa la que toca.
2. El logotipo va en un `<img>` con `alt=""` cuando el enlace que lo envuelve ya lleva `aria-label`, para que no se anuncie dos veces.
3. Siempre con `width` y `height` intrínsecos (`800×219` el completo, `800×800` el icono) para que no salte la maqueta mientras carga.
4. Espacio libre alrededor: como mínimo, la altura del icono. No se le pega texto ni se mete en una caja apretada.
5. No se deforma: la altura manda y el ancho va en `auto`.

## Sobre los tamaños pequeños

A 16 px —el tamaño de la pestaña del navegador— las tres flechas se cierran entre sí y
el icono tiende a leerse como un círculo azul. Es una característica del icono, no un
error del archivo, y **se usa tal cual**: la marca no se modifica para acomodar un
tamaño. De 24 px para arriba se lee perfecto.
