# SIO · Rediseño del sitio — v1

Sitio estático (HTML + CSS + JS vanilla) generado con un script de Python sin dependencias.

```
build.py                 ← genera todas las páginas (python build.py)
src/partials/            ← sprite de íconos, barra superior, header (menú) y footer compartidos
src/pages/index.html     ← contenido de la home
assets/css, assets/js    ← estilos y comportamiento
assets/img/              ← logos (SVG en alta), clientes, banners (hero/), fondos de cards (bg/), capturas reales (shots/) y sellos (cert/)
*.html (raíz)            ← páginas generadas; se versionan para que GitHub Pages las sirva tal cual
```

## Páginas
| Menú | Páginas |
|---|---|
| Inicio | `index.html` |
| Soluciones | `soluciones.html`, `saman-solution`, `saman-soft`, `health-sq`, `saman-rips`, `gestion-documental`, `gestion-de-informacion`, `suministros-tecnologicos`, `servicios-publicos`, `gobierno-de-datos`, `centro-de-negocios` |
| Casos de éxito | `casos-de-exito.html` |
| Nosotros | `nosotros.html` |
| Soporte | `soporte.html` (canal por software; el ticket es externo: `https://tbg.sio.com.co/login`) |
| Contacto | `contacto.html` |

## Flujo de trabajo
1. Editar el contenido en `build.py` (páginas internas) o en `src/` (home y componentes compartidos).
2. Ejecutar `python build.py` para regenerar los `.html`.
3. Probar en local: `npx http-server . -p 5180 -c-1`.

> El menú, el footer y el sprite se editan una sola vez en `src/partials/` y se propagan a todas las páginas.

## Marca (extraída del sitio actual)
| Token | Valor | Origen |
|---|---|---|
| `--yellow` | `#F4D53B` | color global del sitio (swoosh del logo) |
| `--blue` | `#1C4593` | azul del logo / titulares |
| `--navy` | `#092862` | azul oscuro del sitio |
| `--ink` | `#00102E` | fondo oscuro del tema |
| Subsistemas | `#17998A #7B3A8F #0F4C7A #63C3CC #F59E1B #EB5757` | diagrama original de SAMAN SOLUTION |

Tipografía: el sitio actual usa Montserrat. La propuesta usa **Plus Jakarta Sans** (display) + **Inter** (texto) + **JetBrains Mono** (pills) para lograr el look de la plantilla de referencia. Se cambia en una línea (`--font-display`).

## Estructura / jerarquía
Inicio → Soluciones (mega-menú) → Casos de éxito → Nosotros → **Soporte** (página interna con enlace al ticket) → Contacto.
Peso visual: SAMAN SOLUTION (panel oscuro a pantalla completa + hub interactivo) > Saman Soft / Health SQ / Saman RIPS (bento) > Otras soluciones (lista compacta).

## Material del cliente (carpeta Drive "VENTANAS")
- **Datos de la empresa** (docs INFORMACIÓN): Edificio Centro Empresarial Versalles, Calle 22 Norte # 3N–15, piso 4, barrio San Vicente (Cali) · Tel. 300 677 0106 · mercadeo@sio.com.co. Ya aplicados en footer, home y contacto.
- **Logos en alta** (RECURSOS): `.ai` convertidos a SVG (`logo-sio.svg`, `logo-sio-white.svg`, `logo-saman-solution.svg`); favicons regenerados desde el PNG @4x; `assets/img/cert/` con ISO 27001 Bureau Veritas, Oracle Partner, Oracle Cloud Infrastructure, DIAN y el reconocimiento IHCE del Ministerio de Salud.
- **Pantallazos reales** (SOLUCIONES): solo Saman RIPS por ahora → `assets/img/shots/rips-*.jpg` (hero + recorrido interactivo). Faltan Health SQ, SAMAN HC y Saman Soft (carpetas vacías).
- **Soporte** (doc INFORMACIÓN): The Bug Genie atiende a Saman RIPS, Health SQ, SAMAN HC, SAMAN HCM y SAMAN FCA. **Pendiente:** aplicativo de soporte para Saman Soft (se muestra como "Próximamente").
- **PDF "pared lateral"**: panel "Tecnología que respalda tu operación" reconstruido en `nosotros.html`.

## Pendientes de validar con SIO
- WhatsApp: `+57 318 506 7331` (dato del sitio anterior; el doc nuevo solo trae el teléfono 300 677 0106).
- SAMAN HC / HCM / FCA: confirmar nombre completo y si tendrán página propia.
- Casos de éxito: hoy son tarjetas por sector con clientes reales. Faltan resultados, métricas y testimonios aprobados por cada cliente.
- Mockup del producto: es ilustrativo (datos de ejemplo). Reemplazar por capturas reales de SAMAN SOLUTION.
- Logos de clientes: recortados de una imagen de 1024 px; pedir originales vectoriales/alta resolución.
- Formulario: solo maqueta (sin backend).
- Algunos clientes con alt genérico ("Logo de cliente") por logos poco legibles.
