# IncSales para Elementor gratuito

Carpeta con el sitio pensado para armarse a mano en WordPress con **Elementor GRATIS**.

```
elementor/
  css/incsales.css      la hoja compatible: 92 componentes, cero cosas que Elementor gratis no pueda
  *.html                las 23 páginas del sitio (18,737 palabras, contra 111,406 del sitio viejo)
  json/                 235 plantillas, una por sección, numeradas en orden por página
  generar-json.py       convierte cualquier página de esta carpeta en sus .json
  verificar-json.py     compara el HTML contra los .json y avisa si se perdió texto
```

## El ciclo de trabajo

```bash
python3 generar-json.py index.html json inicio
python3 verificar-json.py index.html json inicio
```

El segundo comando es el importante: compara palabra por palabra el HTML contra el JSON generado
y falla si el traductor tiró algo. Así se encontraron y se arreglaron cinco fugas de contenido.
**Nunca subas un JSON sin correrlo.**

## Antes de importar nada

Estos valores **no viajan en el JSON**. Se teclean una sola vez en el sitio:

**Ajustes del sitio → Colores globales**

| Nombre | Hex | Para qué |
|---|---|---|
| Primario | `#1e5bd4` | botones, enlaces, acentos |
| Secundario | `#0b3587` | fondos oscuros y hover |
| Texto | `#21252d` | titulares |
| Destacado | `#00874a` | palomas y señales de bien |
| Cuerpo | `#4d535d` | texto corrido |
| Tenue | `#6a6f78` | notas y pies |
| Línea | `#dbdee3` | bordes |
| Lienzo | `#f4f6f9` | secciones grises |
| Azul tenue | `#f2f7ff` | secciones azules y avisos |
| Ámbar | `#be7d00` · `#fff7e9` | avisos de condiciones |

**Ajustes del sitio → Tipografía:** Inter. Cuerpo 17/16/16 px, interlineado 1.65.
H1 52/40/32 · H2 36/30/26 · H3 22/20/19 · H4 18. Peso 600 en títulos.

**Ajustes del sitio → Diseño:** ancho del contenido **1140 px**.
Puntos de quiebre: escritorio >1024 · tablet ≤1024 · móvil ≤767.

## Cómo se sube

Los archivos van numerados (`S01`, `S02`…) en el orden de la página. Se importan en
Plantillas → Plantillas guardadas → Importar, y después se insertan en la página en ese orden.

## Lo confirmado sobre el formato (Elementor 4.3.2, septiembre de 2026)

Se verificó contra el código fuente de Elementor, no de memoria:

- **Importar plantillas SÍ está en la versión gratuita.** Plantillas → Plantillas guardadas →
  Importar plantillas. Era el supuesto del que colgaba todo el plan, y se sostiene.
- `"type": "container"` es correcto: debe coincidir con el `elType` del elemento raíz. Así están.
- Obligatorias: `content`, `type`, `title`. `version` se ignora por completo.
- Los `id` van en hexadecimal minúscula de 7 u 8 caracteres, únicos dentro del archivo. Los 343
  nodos de esta carpeta cumplen y no se repite ninguno.
- **Sube los .json de uno en uno la primera vez.** Si metes un .zip y alguno falla, Elementor se
  lo salta **en silencio** y te quedas sin esa sección sin enterarte.

### Antes del primer intento

En WP-Admin → Elementor → Ajustes → Funciones, confirma que **Container** está **Activo**. Viene
activo por omisión desde la versión 3.16, pero si estuviera apagado la importación se rechaza con
«Invalid template type». Ese error es la señal correcta: significa que el sitio no puede dibujar
este diseño, no que el archivo esté mal.

## El riesgo que queda sin resolver

**El editor V4 «atómico».** Es el editor por omisión en instalaciones nuevas desde marzo de 2026.
Estos archivos usan la estructura clásica de contenedores, que es la que se puede editar con los
controles normales. **No está confirmado** si V4 abre esa estructura y te deja moverla con
comodidad, o si te obliga a convertirla.

Por eso el primer archivo que subas debe ser **`wordpress-S07-cierre.json`**: es el más chico,
trae fondo oscuro, título, texto y botón, y con él compruebas las dos cosas de golpe —que importa,
y que lo puedes editar—. Si ese entra y se deja tocar, entran los 18.

## Dos cosas que hay que cambiar en el sitio real

1. **Las imágenes** viajan con la ruta de la maqueta (`../assets/logos/…`) y con `id` vacío.
   Elementor no las va a encontrar. Sube los dos logos a la biblioteca de medios y vuelve a
   seleccionarlos en los widgets de Imagen; son cuatro en total.
2. **Los enlaces** apuntan a `index.html` y `wordpress.html`. Cámbialos por las rutas reales de
   WordPress (`/` y `/wordpress/`, o las que queden).

## Lo que la auditoría encontró y ya está arreglado

Diecinueve agentes revisaron la entrega por cinco frentes y verificaron sus propios hallazgos:

- **Un testimonio fabricado**, firmado por un cliente real que nunca dijo esas palabras. Eliminado
  y sustituido por hechos verificables del expediente. Desde entonces la regla es dura: en este
  sitio no se escribe ninguna cita atribuida a una persona o empresa.
- Una afirmación sin respaldo: que el interesado llega con su campaña y su anuncio de origen.
  PRODUCTO.md no lo dice, así que se cambió por lo que sí es cierto.
- La portada vendía WooSync y la API como si vinieran incluidas. Ahora dicen que son complemento.
- `text_align` no existe como control de contenedor: se ignoraba en silencio y los bloques
  centrados llegaban a la izquierda. La alineación ahora va en cada widget, que sí la tiene.
- `width` junto a `content_width: boxed` no hace nada: la clave es `boxed_width`. Eran 26 casos.
- La barra se importaba como pila vertical y el pie perdía su fondo azul marino, dejando el logo
  blanco sobre blanco. El logo de la barra, además, llegaba como un enlace vacío.
- Contrastes ilegibles: la nota de contacto sobre fondo oscuro estaba a 2.22:1. Ahora 7.5:1.
  La píldora azul sobre sección azul era invisible. El ámbar pasó de 3.22:1 a 5.6:1.
- Doce saltos de jerarquía de encabezados (h2 → h4 sin h3).

## Lo que en Elementor cambia respecto de esta maqueta

- Las **capturas del producto** aquí están dibujadas con HTML. En WordPress son un widget **Imagen**
  dentro de un contenedor con borde, radio y sombra. Hay que exportar los PNG.
- El **formulario** no existe en Elementor gratis: va Fluent Forms o WPForms Lite por código corto.
- La **barra y el pie** se arman con el plugin gratuito Header Footer Elementor, no como sección.


## El sitio completo

Veintitrés páginas, 18,737 palabras. El sitio anterior tenía 111,406: **se recortó el 84%**.

| Página | Palabras | Secciones |
|---|---|---|
| `index.html` | 867 | 10 |
| `crm.html` · `cotizaciones.html` · `inventarios.html` · `compras.html` | 650–768 | 9–10 |
| `facturacion.html` · `whatsapp.html` · `forms.html` · `correo.html` | 529–692 | 9–11 |
| `wordpress.html` · `integraciones.html` | 605–679 | 8–10 |
| `por-dentro.html` | 860 | 12 |
| `precios.html` | 1,474 | 14 |
| `agencia.html` | 1,136 | 12 |
| `casos.html` · `migracion.html` · `comparativa.html` · `industrias.html` | 511–764 | 8–11 |
| `preguntas.html` · `nosotros.html` · `contacto.html` | 311–901 | 7–11 |
| `terminos.html` · `privacidad.html` | 1,704–1,786 | 13–16 |

Las 235 plantillas suman 4,962 nodos, todos con identificador único, sin un solo widget de Pro y
sin marcado ejecutable dentro de ningún campo de texto.

### Orden de subida sugerido

1. `wordpress-S07-cierre.json` — la prueba de un minuto.
2. La barra y el pie de cualquier página (`*-S01-barra.json` y el último de cada una), que se
   arman una vez con Header Footer Elementor y valen para todo el sitio.
3. `inicio-S*.json` en orden, que es la portada.
4. El resto de las páginas, cada una con sus secciones en orden.
