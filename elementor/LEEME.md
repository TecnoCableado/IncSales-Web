# IncSales para Elementor gratuito

Las plantillas JSON del sitio, para importarlas a mano en WordPress con **Elementor GRATIS**.

```
elementor/
  json/               206 plantillas, una por sección, numeradas por página
  generar-json.py     convierte cualquier página de la raíz en sus .json
  verificar-json.py   compara el HTML contra los .json y avisa si se perdió texto
```

**El origen es la raíz del proyecto**, no esta carpeta. Las 23 páginas `.html` de la raíz son la
fuente; estos JSON salen de ellas. Si cambias una página, regenera:

```bash
cd elementor
python3 generar-json.py ../crm.html json crm
python3 verificar-json.py ../crm.html json crm
```

El segundo comando es el que importa: compara palabra por palabra el HTML contra el JSON y falla si
el traductor tiró algo. Así se encontraron y arreglaron catorce fugas de contenido.
**No subas un JSON sin correrlo.**

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


## El sitio

23 páginas, 18,400 palabras. El sitio anterior tenía 112,244: se recortó el 84%.

Trece son landings de producto, cada una con el color de su familia —magenta para la demanda,
cian para el documento, violeta para el material, verde para la conversación, azul noche para lo
que hacemos nosotros—. Las otras diez son de apoyo: precios, pantallas, clientes, comparativa,
giros, preguntas, contacto, quiénes somos y las dos legales.

## Lo que hay que hacer a mano en WordPress

1. **Las capturas del producto.** Las maquetas de pantalla están dibujadas con HTML y no se
   traducen: el JSON deja un marco con un hueco de imagen y una nota. Son 52 huecos. Hay que
   exportar los PNG y subirlos a la biblioteca de medios.
2. **Los enlaces.** Apuntan a `archivo.html`. Cámbialos por las rutas reales de WordPress.
3. **Los logos.** Viajan con la ruta de la maqueta y con `id` vacío: vuelve a seleccionarlos desde
   la biblioteca de medios.
4. **Los formularios.** Elementor gratuito no trae widget de formulario. Donde había uno, el JSON
   deja un aviso con los campos en orden y sus textos de ayuda, para armarlo con Fluent Forms o
   WPForms Lite e insertarlo por código corto.
