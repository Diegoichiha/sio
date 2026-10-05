# SIO · Rediseño Home — Propuesta v1

Maqueta estática (HTML + CSS + JS vanilla, sin build) del nuevo Home de sio.com.co.

```
index.html              ← Home completo (11 secciones)
assets/css/styles.css   ← Tokens de marca + componentes
assets/js/main.js       ← Interacciones (nav, hub, contadores, FAQ, marquee…)
assets/img/             ← Logos reales extraídos de sio.com.co (+ 27 logos de clientes recortados)
```

Servir en local: `npx http-server . -p 5180 -c-1` → http://localhost:5180

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
Inicio → Soluciones (mega-menú) → Casos de éxito → Nosotros → **Soporte ↗ (enlace externo)** → Contacto.
Peso visual: SAMAN SOLUTION (panel oscuro a pantalla completa + hub interactivo) > Saman Soft / Health SQ / Saman RIPS (bento) > Otras soluciones (lista compacta).

## Pendientes de validar con SIO
- URL de Soporte: se usa `https://tbg.sio.com.co/login` (ticket electrónico actual).
- WhatsApp: `+57 318 506 7331` (se asume que es el número de WhatsApp).
- Casos de éxito: hoy son tarjetas por sector con clientes reales. Faltan resultados, métricas y testimonios aprobados por cada cliente.
- Mockup del producto: es ilustrativo (datos de ejemplo). Reemplazar por capturas reales de SAMAN SOLUTION.
- Logos de clientes: recortados de una imagen de 1024 px; pedir originales vectoriales/alta resolución.
- Formulario: solo maqueta (sin backend).
- Algunos clientes con alt genérico ("Logo de cliente") por logos poco legibles.
