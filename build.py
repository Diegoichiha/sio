#!/usr/bin/env python3
"""
SIO · generador del sitio estático.

Uso:  python build.py
Lee  src/partials/*.html (sprite, topbar, header, footer) y src/pages/index.html
y genera en la raíz: index.html + las páginas internas (soluciones, casos, nosotros, contacto…).
El HTML generado se versiona para que GitHub Pages lo sirva tal cual.
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
WA = 'https://wa.me/573185067331'
SUPPORT = 'https://tbg.sio.com.co/login'


def read(*parts):
    with open(os.path.join(ROOT, *parts), encoding='utf-8') as f:
        return f.read()


def write(name, content):
    with open(os.path.join(ROOT, name), 'w', encoding='utf-8') as f:
        f.write(content)


# ------------------------------------------------------------------ iconos extra
EXTRA_ICONS = '''
    <symbol id="i-wifi" viewBox="0 0 24 24"><path d="M5 12.55a11 11 0 0 1 14.08 0"/><path d="M1.42 9a16 16 0 0 1 21.16 0"/><path d="M8.53 16.11a6 6 0 0 1 6.95 0"/><path d="M12 20h.01"/></symbol>
    <symbol id="i-wind" viewBox="0 0 24 24"><path d="M17.7 7.7a2.5 2.5 0 1 1 1.8 4.3H2"/><path d="M9.6 4.6A2 2 0 1 1 11 8H2"/><path d="M12.6 19.4A2 2 0 1 0 14 16H2"/></symbol>
    <symbol id="i-coffee" viewBox="0 0 24 24"><path d="M10 2v2M14 2v2M6 2v2"/><path d="M16 8a1 1 0 0 1 1 1v8a4 4 0 0 1-4 4H7a4 4 0 0 1-4-4V9a1 1 0 0 1 1-1z"/><path d="M17 12h2a2 2 0 0 1 0 4h-2"/></symbol>
    <symbol id="i-key" viewBox="0 0 24 24"><path d="m21 2-9.6 9.6"/><circle cx="7.5" cy="15.5" r="5.5"/><path d="m15.5 7.5 3 3L22 7l-3-3"/></symbol>
    <symbol id="i-utensils" viewBox="0 0 24 24"><path d="M3 2v7c0 1.1.9 2 2 2h4a2 2 0 0 0 2-2V2"/><path d="M7 2v20"/><path d="M21 15V2a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h3Zm0 0v7"/></symbol>
    <symbol id="i-arrow-up" viewBox="0 0 24 24"><path d="m5 12 7-7 7 7"/><path d="M12 19V5"/></symbol>
    <symbol id="i-sparkles" viewBox="0 0 24 24"><path d="M9.937 15.5A2 2 0 0 0 8.5 14.063l-6.135-1.582a.5.5 0 0 1 0-.962L8.5 9.936A2 2 0 0 0 9.937 8.5l1.582-6.135a.5.5 0 0 1 .963 0L14.063 8.5A2 2 0 0 0 15.5 9.937l6.135 1.581a.5.5 0 0 1 0 .964L15.5 14.063a2 2 0 0 0-1.437 1.437l-1.582 6.135a.5.5 0 0 1-.963 0z"/></symbol>
    <symbol id="i-headset" viewBox="0 0 24 24"><path d="M3 11h3a2 2 0 0 1 2 2v3a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-5Zm0 0a9 9 0 1 1 18 0m0 0v5a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3Z"/><path d="M21 16v2a4 4 0 0 1-4 4h-5"/></symbol>
    <symbol id="i-printer" viewBox="0 0 24 24"><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><path d="M6 9V3a1 1 0 0 1 1-1h10a1 1 0 0 1 1 1v6"/><rect x="6" y="14" width="12" height="8" rx="1"/></symbol>
    <symbol id="i-archive" viewBox="0 0 24 24"><rect width="20" height="5" x="2" y="3" rx="1"/><path d="M4 8v11a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8"/><path d="M10 12h4"/></symbol>
    <symbol id="i-inbox" viewBox="0 0 24 24"><path d="M22 12h-6l-2 3h-4l-2-3H2"/><path d="M5.45 5.11 2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z"/></symbol>
    <symbol id="i-graduation" viewBox="0 0 24 24"><path d="M21.42 10.922a1 1 0 0 0-.019-1.838L12.83 5.18a2 2 0 0 0-1.66 0L2.6 9.08a1 1 0 0 0 0 1.832l8.57 3.908a2 2 0 0 0 1.66 0z"/><path d="M22 10v6"/><path d="M6 12.5V16a6 3 0 0 0 12 0v-3.5"/></symbol>
    <symbol id="i-refresh" viewBox="0 0 24 24"><path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/><path d="M21 3v5h-5"/><path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"/><path d="M8 16H3v5"/></symbol>
    <symbol id="i-gauge" viewBox="0 0 24 24"><path d="m12 14 4-4"/><path d="M3.34 19a10 10 0 1 1 17.32 0"/></symbol>
    <symbol id="i-eye" viewBox="0 0 24 24"><path d="M2.06 12.35a1 1 0 0 1 0-.7 10.75 10.75 0 0 1 19.88 0 1 1 0 0 1 0 .7 10.75 10.75 0 0 1-19.88 0"/><circle cx="12" cy="12" r="3"/></symbol>
    <symbol id="i-cpu" viewBox="0 0 24 24"><rect width="16" height="16" x="4" y="4" rx="2"/><rect width="6" height="6" x="9" y="9" rx="1"/><path d="M15 2v2M15 20v2M2 15h2M2 9h2M20 15h2M20 9h2M9 2v2M9 20v2"/></symbol>
    <symbol id="i-expand" viewBox="0 0 24 24"><path d="m15 3 6 0 0 6"/><path d="m9 21-6 0 0-6"/><path d="M21 3l-7 7"/><path d="M3 21l7-7"/></symbol>
    <symbol id="i-download" viewBox="0 0 24 24"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="m7 10 5 5 5-5"/><path d="M12 15V3"/></symbol>
    <symbol id="i-pointer" viewBox="0 0 24 24"><path d="M14 4.1 12 6"/><path d="m5.1 8-2.9-.8"/><path d="m6 12-1.9 2"/><path d="M7.2 2.2 8 5.1"/><path d="M9.037 9.69a.498.498 0 0 1 .653-.653l11 4.5a.5.5 0 0 1-.074.949l-4.349 1.041a1 1 0 0 0-.74.739l-1.04 4.35a.5.5 0 0 1-.95.074z"/></symbol>
    <symbol id="i-ticket" viewBox="0 0 24 24"><path d="M2 9a3 3 0 0 1 0 6v2a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-2a3 3 0 0 1 0-6V7a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2Z"/><path d="M13 5v2"/><path d="M13 17v2"/><path d="M13 11v2"/></symbol>
    <symbol id="i-log-in" viewBox="0 0 24 24"><path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/><path d="m10 17 5-5-5-5"/><path d="M15 12H3"/></symbol>
    <symbol id="i-pen" viewBox="0 0 24 24"><path d="M12 20h9"/><path d="M16.376 3.622a1 1 0 0 1 3.002 3.002L7.368 18.635a2 2 0 0 1-.855.506l-2.872.838a.5.5 0 0 1-.62-.62l.838-2.872a2 2 0 0 1 .506-.854z"/></symbol>
'''

# ------------------------------------------------------------------ helpers de marcado
def ic(name):
    return f'<svg class="ic"><use href="#i-{name}"/></svg>'


def btn(label, href, kind='dark', arrow=True, ext=False, size='lg'):
    cls = {'dark': 'btn-dark', 'yellow': 'btn-yellow', 'ghost': 'btn-ghost', 'light': 'btn-outline-light'}[kind]
    tgt = ' target="_blank" rel="noopener"' if ext else ''
    icon = ic('arrow-up-right' if ext else 'arrow-right') if arrow else ''
    sz = f' btn-{size}' if size else ''
    return f'<a class="btn {cls}{sz}" href="{href}"{tgt}>{label} {icon}</a>'


def sec_head(pill, h2, p='', dark=False):
    pc = 'pill pill-dark' if dark else 'pill'
    pp = f'<p>{p}</p>' if p else ''
    return (f'<header class="sec-head center"><span class="{pc}" data-reveal>{pill}</span>'
            f'<h2 data-reveal style="--d:.06s">{h2}</h2>{pp}</header>')


def section(inner, cls=''):
    return f'<section class="section {cls}"><div class="container">{inner}</div></section>'


def feats(items, cols=3, cvar=None):
    cls = {2: ' c2', 3: '', 4: ' c4'}[cols]
    out = []
    for it in items:
        icon, title, text = it[0], it[1], it[2]
        bullets = it[3] if len(it) > 3 else None
        color = it[4] if len(it) > 4 else None
        style = f' style="--c:{color}"' if color else ''
        accent = ' accent' if color else ''
        ul = '<ul>' + ''.join(f'<li>{b}</li>' for b in bullets) + '</ul>' if bullets else ''
        p = f'<p>{text}</p>' if text else ''
        out.append(f'<div class="feat{accent}"{style}><span class="f-ico">{ic(icon)}</span><h3>{title}</h3>{p}{ul}</div>')
    return f'<div class="feat-grid{cls}" data-reveal>' + ''.join(out) + '</div>'


def checks(items):
    return '<ul class="checks">' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'


def split(pill, h2, paras, bullets=None, visual='', rev=False, cta=None):
    p = ''.join(f'<p>{x}</p>' for x in paras)
    b = checks(bullets) if bullets else ''
    c = cta or ''
    rv = ' rev' if rev else ''
    return (f'<div class="split{rv}"><div class="split-copy" data-reveal><span class="pill">{pill}</span>'
            f'<h2>{h2}</h2>{p}{b}{c}</div><div class="split-visual" data-reveal style="--d:.1s">{visual}</div></div>')


def shot(src, alt, pad=False):
    return f'<div class="shot{" pad" if pad else ""}"><img src="{src}" alt="{alt}" loading="lazy"></div>'


def cta_band(h2, p, primary=('Solicitar demo', 'contacto.html'), secondary=('Hablar con un asesor', WA)):
    sec = ''
    if secondary:
        sec = btn(secondary[0], secondary[1], 'light', ext=secondary[1].startswith('http'), size='lg')
    return ('<section class="section tight"><div class="container"><div class="cta-band" data-reveal>'
            f'<div><h2>{h2}</h2><p>{p}</p></div>'
            f'<div class="cta-actions">{btn(primary[0], primary[1], "yellow")}{sec}</div>'
            '</div></div></section>')


def timeline(head_pill, head_h2, head_p, steps, cta=None):
    items = []
    for icon, title, text in steps:
        items.append(
            f'<li class="tl-item" tabindex="0"><span class="tl-node" aria-hidden="true">{ic(icon)}</span>'
            f'<div class="tl-card"><h3>{title}</h3><p>{text}</p></div></li>')
    c = cta or ''
    return ('<section class="process"><div class="container process-grid">'
            f'<header class="process-head"><span class="pill" data-reveal>{head_pill}</span>'
            f'<h2 data-reveal style="--d:.06s">{head_h2}</h2><p data-reveal style="--d:.12s">{head_p}</p>{c}</header>'
            f'<ol class="timeline" data-timeline>{"".join(items)}</ol></div></section>')



def h_timeline(pill, h2, p, items):
    """Línea de tiempo horizontal en zigzag. items: (icono, etiqueta, título, texto)"""
    lis = []
    for icon, tag, title, text in items:
        lis.append(
            f'<li class="ht-item" tabindex="0"><span class="ht-node" aria-hidden="true">{ic(icon)}</span>'
            f'<div class="ht-card"><span class="ht-tag">{tag}</span><h3>{title}</h3><p>{text}</p></div></li>')
    return (sec_head(pill, h2, p)
            + '<div class="h-timeline" data-htimeline><div class="ht-track" aria-hidden="true"></div>'
              '<div class="ht-fill" aria-hidden="true"></div>'
              f'<ol class="ht-list">{"".join(lis)}</ol></div>')



def sub_cards(subs):
    """Cards con imagen de fondo + overlay azul SIO. Estado inactivo: ícono y título abajo.
    Hover: los bullets aparecen de abajo hacia arriba y el overlay se refuerza.
    subs: (color, icono, titulo, [bullets], imagen, posición)"""
    out = []
    for color, icon, title, items, img, pos in subs:
        lis = ''.join(f'<li style="--i:{k}">{t}</li>' for k, t in enumerate(items))
        out.append(
            f'<article class="sub-card" style="--c:{color}" tabindex="0">'
            f'<img class="sub-bg" src="assets/img/{img}" alt="" loading="lazy" style="--pos:{pos}">'
            '<span class="sub-shade" aria-hidden="true"></span>'
            f'<div class="sub-body"><div class="sub-head"><span class="f-ico">{ic(icon)}</span><h3>{title}</h3></div>'
            f'<div class="sub-list-wrap"><ul class="sub-list">{lis}</ul></div></div>'
            '</article>')
    return '<div class="sub-grid" data-reveal>' + ''.join(out) + '</div>'



def img_panel(img, pos, pill, h2, p, items, cta=None, tag=''):
    """Panel con imagen de fondo: overlay oscuro a la izquierda con el texto y tarjetas;
    hacia la derecha el overlay se desvanece y la imagen se ve completa."""
    steps = ''.join(
        f'<div class="ip-step"><span class="f-ico">{ic(icon)}</span>'
        f'<div><span class="mono">{label}</span><b>{title}</b><p>{text}</p></div></div>'
        for icon, label, title, text in items)
    c = cta or ''
    t = f'<span class="ip-tag"><i></i>{tag}</span>' if tag else ''
    return (f'<div class="img-panel" data-reveal><img class="ip-bg" src="assets/img/{img}" alt="" loading="lazy" style="--pos:{pos}">'
            f'<div class="ip-copy"><span class="pill pill-dark">{pill}</span><h2>{h2}</h2><p>{p}</p>'
            f'<div class="ip-steps">{steps}</div>{c}</div>{t}</div>')


def real_visual(img, alt, floats=''):
    """Monitor con un pantallazo real (recorte de la plataforma) y ventanas flotantes."""
    return (floats + '<div class="device flat"><div class="device-bezel"><span class="device-cam"></span>'
            f'<div class="screen real"><img src="assets/img/shots/{img}" alt="{alt}"></div></div></div>')


def tour(label, steps, caption):
    """Recorrido interactivo por pantallazos reales.
    steps: (icono, título, texto, imagen, zoom, origen_del_zoom)"""
    tabs, imgs = [], []
    for i, (icon, title, text, img, z, o) in enumerate(steps):
        first = i == 0
        on = ' is-on' if first else ''
        sel = 'true' if first else 'false'
        idx = '' if first else ' tabindex="-1"'
        tabs.append(
            f'<button type="button" class="tour-tab{on}" role="tab" aria-selected="{sel}"{idx} data-label="{label} · {title}">'
            f'<span class="f-ico">{ic(icon)}</span>'
            f'<span class="tt-main"><b>{title}</b><span class="tt-body"><span><span class="tt-text">{text}</span></span></span></span></button>')
        imgs.append(
            f'<img class="{"is-on" if first else ""}" src="assets/img/shots/{img}" alt="{label}: {title}" '
            f'style="--z:{z};--o:{o}" width="1600" height="1000" loading="lazy">')
    return ('<div class="tour" data-tour>'
            f'<div class="tour-tabs" role="tablist" aria-label="Recorrido por la plataforma" data-reveal>{"".join(tabs)}</div>'
            '<figure class="tour-stage" data-reveal style="--d:.1s"><div class="tour-frame">'
            f'<div class="tour-bar"><i></i><i></i><i></i><span class="tour-url">{label} · {steps[0][1]}</span></div>'
            f'<div class="tour-shots">{"".join(imgs)}'
            f'<button type="button" class="tour-zoom" aria-label="Ampliar el pantallazo">{ic("expand")}<span>Ampliar</span></button></div></div>'
            f'<figcaption class="tour-cap">{caption}</figcaption></figure></div>')


def support_strip(name, kind='tbg', detail=''):
    """Franja de soporte para cada software. kind: 'tbg' (ticket electrónico) o 'soon' (canal en preparación)."""
    if kind == 'tbg':
        h3 = f'Soporte para {name}'
        text = (f'{detail}Registra tus solicitudes en The Bug Genie, el ticket electrónico de SIO. '
                'Te atendemos de 8:00 a. m. a 12:00 m. y de 2:00 a 5:30 p. m.')
        actions = (btn('Ir al ticket electrónico', SUPPORT, 'dark', ext=True, size='')
                   + btn('Soporte por solución', 'soporte.html', 'ghost', arrow=False, size=''))
    else:
        h3 = f'Soporte para {name}'
        text = (f'Estamos habilitando el aplicativo de soporte para los clientes de {name}. '
                'Mientras tanto, nuestro equipo te atiende desde la página de contacto.')
        actions = (btn('Contactar a SIO', 'contacto.html', 'dark', size='')
                   + btn('Soporte por solución', 'soporte.html', 'ghost', arrow=False, size=''))
    return ('<section class="support"><div class="container"><div class="support-card" data-reveal>'
            f'<span class="support-ic">{ic("life-buoy")}</span>'
            f'<div class="support-copy"><h3>{h3}</h3><p>{text}</p></div>'
            f'<div class="support-actions">{actions}</div></div></div></section>')


# ------------------------------------------------------------------ catálogo de soluciones
SOL = {
    'saman-solution':          dict(name='SAMAN SOLUTION', tag='Gestión hospitalaria', desc='Toda la operación de tu institución en una sola solución.', img='hero/solution.jpg', icon='hospital'),
    'saman-soft':              dict(name='Saman Soft', tag='Documentos electrónicos · DIAN', desc='Facturación y nómina electrónica en la nube.', img='bg/soft.jpg', icon='receipt', logo='logo-saman-soft.png'),
    'health-sq':               dict(name='Health SQ', tag='Calidad en salud · SOGC', desc='Habilitación, acreditación, seguridad e indicadores.', img='bg/health.jpg', icon='clipboard-check', logo='logo-health-sq.png'),
    'saman-rips':              dict(name='Saman RIPS', tag='RIPS · Resolución 2275', desc='RIPS automáticos, seguros y sin errores.', img='bg/rips.jpg', icon='file-text', logo='logo-saman-rips.png'),
    'gestion-documental':      dict(name='Gestión documental', tag='Servicios BPO', desc='TRD, digitalización, custodia y ventanilla única.', img='bg/doc.jpg', icon='folder', hint='TRD, digitalización y custodia'),
    'gestion-de-informacion':  dict(name='Gestión de información', tag='Servicios BPO', desc='Captura masiva con OCR, ICR, OMR, QR y RFID.', img='bg/info.jpg', icon='scan', hint='Captura masiva con OCR e ICR'),
    'suministros-tecnologicos': dict(name='Suministros tecnológicos', tag='Servicios BPO', desc='Equipos, espacios de trabajo y mesa de ayuda.', img='bg/supply.jpg', icon='monitor', hint='Equipos y mesa de ayuda'),
    'servicios-publicos':      dict(name='Servicios públicos', tag='Energía, agua y gas', desc='Supernova S.C. e inteligencia de negocios.', img='bg/utilities.jpg', icon='zap', hint='Energía, agua y gas'),
    'gobierno-de-datos':       dict(name='Gobierno de datos', tag='Oracle', desc='Administración, tuning y alta disponibilidad.', img='bg/data.jpg', icon='database', hint='Administración Oracle'),
    'centro-de-negocios':      dict(name='Centro de negocios', tag='Cali', desc='Oficinas, oficina virtual y salas de reuniones.', img='bg/center.jpg', icon='building', hint='Oficinas y salas en Cali'),
}


def related(slugs, pill='Soluciones relacionadas', title='Descubre más soluciones'):
    cards = []
    for s in slugs:
        d = SOL[s]
        cards.append(
            f'<a class="rel-card" href="{s}.html"><img class="bg" src="assets/img/{d["img"]}" alt="" loading="lazy">'
            f'<span class="go">{ic("arrow-up-right")}</span><span class="tag">{d["tag"]}</span>'
            f'<h3>{d["name"]}</h3><p>{d["desc"]}</p></a>')
    return section(
        f'<div class="rel-head"><div><span class="pill">{pill}</span><h2 class="h2-sm" style="margin-top:14px">{title}</h2></div></div>'
        f'<div class="rel-grid" data-reveal>{"".join(cards)}</div>')


def hero(spec):
    """Cabecera de página interna. spec: crumbs, pill, h1, lead, logo(optional), ctas, visual(optional)
    Con 'visual' el hero se divide: texto a la izquierda y la pieza visual a la derecha."""
    crumbs = []
    for i, (label, href) in enumerate(spec['crumbs']):
        last = i == len(spec['crumbs']) - 1
        crumbs.append(f'<b>{label}</b>' if last else f'<a href="{href}">{label}</a><i>/</i>')
    logo = (f'<span class="hero-logo"><img src="assets/img/{spec["logo"]}" alt="{spec.get("logo_alt", "")}"></span>'
            if spec.get('logo') else '')
    ctas = ''.join(spec.get('ctas', []))
    cta_row = f'<div class="cta-row">{ctas}</div>' if ctas else ''
    copy = (f'<div class="page-hero-inner"><nav class="crumbs" aria-label="Ruta">{"".join(crumbs)}</nav>{logo}'
            f'<span class="pill">{spec["pill"]}</span><h1>{spec["h1"]}</h1><p class="lead">{spec["lead"]}</p>{cta_row}</div>')
    if spec.get('visual'):
        return (f'<section class="page-hero has-visual"><div class="container hero-split">{copy}'
                f'<div class="hero-visual">{spec["visual"]}</div></div></section>')
    return f'<section class="page-hero"><div class="container">{copy}</div></section>'


def crumbs_sol(name):
    return [('Inicio', 'index.html'), ('Soluciones', 'soluciones.html'), (name, '')]


# ------------------------------------------------------------------ piezas reutilizadas de la home
HOME = read('src', 'pages', 'index.html')


def grab(start_marker, end_marker):
    i = HOME.index(start_marker)
    j = HOME.index(end_marker, i) + len(end_marker)
    return HOME[i:j]


def hub_section():
    html = grab('<section class="solution" id="saman-solution">', '</section>')
    html = html.replace('<section class="solution" id="saman-solution">', '<section class="solution" id="subsistemas">')
    html = html.replace('href="#contacto"', 'href="contacto.html"')
    html = re.sub(r'<a class="btn btn-yellow js-more"[^>]*>.*?</a>', '', html, flags=re.S)
    return html


def pcards(slugs):
    out = []
    for i, s in enumerate(slugs):
        d = SOL[s]
        delay = f' style="--d:{i * .08:.2f}s"' if i else ''
        out.append(
            f'<div class="p-cell" data-reveal{delay}><a class="p-card" id="{s}" href="{s}.html">'
            f'<img class="p-bg" src="assets/img/{d["img"]}" alt="" loading="lazy">'
            '<span class="p-shade" aria-hidden="true"></span>'
            f'<div class="p-top"><span class="p-logo"><img src="assets/img/{d["logo"]}" alt="{d["name"]}"></span>'
            f'<span class="p-integ">{ic("link")}Integrado</span></div>'
            f'<div class="p-copy"><span class="p-tag">{d["tag"]}</span><h3>{d["name"]}</h3><p>{d["desc"]}</p></div>'
            f'<span class="p-go" aria-hidden="true">{ic("arrow-up-right")}</span></a></div>')
    return '<div class="p-grid">' + ''.join(out) + '</div>'


def otiles(slugs, first_active=True):
    out = []
    for i, s in enumerate(slugs):
        d = SOL[s]
        act = ' is-active' if (i == 0 and first_active) else ''
        out.append(
            f'<a class="o-tile{act}" href="{s}.html"><img class="o-bg" src="assets/img/{d["img"]}" alt="" loading="lazy">'
            '<span class="o-shade" aria-hidden="true"></span>'
            f'<span class="o-ic">{ic(d["icon"])}</span>'
            f'<span class="o-text"><b>{d["name"]}</b><small>{d["hint"]}</small></span></a>')
    return '<div class="o-grid" data-reveal>' + ''.join(out) + '</div>'


OTHER = ['gestion-documental', 'gestion-de-informacion', 'suministros-tecnologicos',
         'servicios-publicos', 'gobierno-de-datos', 'centro-de-negocios']

CLIENTS = [
    ('r1-01', 'Hospital San José'), ('r1-02', 'Fundación Hospital San Pedro'), ('r1-03', 'Hospital Isaías Duarte Cancino E.S.E.'),
    ('r1-04', 'HFPS'), ('r1-05', 'Cliente SIO'), ('r1-06', 'Comfenalco Valle'), ('r1-07', 'Comfandi'), ('r1-08', 'Coomeva'),
    ('r1-09', 'IPS Municipal de Ipiales E.S.E.'), ('r2-01', 'Hospital Ricaurte E.S.E.'), ('r2-02', 'IPS Genesis'),
    ('r2-03', 'Caprecom'), ('r2-04', 'Cliente SIO'), ('r2-05', 'Medinuclear'), ('r2-06', 'IPS Ahakka'),
    ('r2-07', 'IPS Unimedic'), ('r2-08', 'IPS Puente del Medio'), ('r2-09', 'Clínica Oncológica Aurora'),
    ('r3-01', 'Clinical Spa'), ('r3-02', 'Hospital Cumbal E.S.E.'), ('r3-03', 'Clínica Las Lajas'), ('r3-04', 'TrauMedical'),
    ('r3-05', 'Patólogos Asociados'), ('r3-06', 'Cedenar'), ('r3-07', 'Gobernación del Valle del Cauca'),
    ('r3-08', 'SOS'), ('r3-09', 'Registraduría Nacional del Estado Civil'),
]


def logos(keys):
    d = dict(CLIENTS)
    return ''.join(f'<span class="client"><img src="assets/img/clients/{k}.png" alt="{d[k]}" loading="lazy"></span>' for k in keys)


def _qr_svg(n=9, seed=7):
    """QR decorativo determinista (no es un código real)."""
    cells = []
    x = seed
    def finder(ox, oy):
        for dx in range(3):
            for dy in range(3):
                cells.append((ox + dx, oy + dy))
    finder(0, 0); finder(n - 3, 0); finder(0, n - 3)
    for yy in range(n):
        for xx in range(n):
            x = (x * 1103515245 + 12345) & 0x7fffffff
            in_finder = (xx < 3 and yy < 3) or (xx >= n - 3 and yy < 3) or (xx < 3 and yy >= n - 3)
            if not in_finder and (x >> 16) % 2 == 0:
                cells.append((xx, yy))
    rects = ''.join(f'<rect x="{cx}" y="{cy}" width="1" height="1"/>' for cx, cy in cells)
    return f'<svg viewBox="0 0 {n} {n}" width="100%" height="100%" fill="currentColor" shape-rendering="crispEdges" aria-hidden="true">{rects}</svg>'


def _f_item(cls, r, dur, delay, icon, title, sub, chip='', ok=False):
    c = ' ok' if ok else ''
    ch = f'<span class="f-chip">{chip}</span>' if chip else ''
    return (f'<div class="float sf {cls}" style="animation-duration:{dur}s;animation-delay:{delay}s">'
            f'<span class="f-ic{c}">{ic(icon)}</span><div><b>{title}</b><small>{sub}</small></div>{ch}</div>')


def _f_qr(cls, r, dur, delay, title, sub):
    return (f'<div class="float sf {cls}" style="animation-duration:{dur}s;animation-delay:{delay}s">'
            f'<span class="qr">{_qr_svg()}</span><div><b>{title}</b><small>{sub}</small></div>'
            f'<span class="sf-dl">{ic("arrow-up")}</span></div>')


def _f_list(cls, r, dur, delay, title, items):
    lis = ''.join(f'<li><i class="{c}"></i>{t}</li>' for c, t in items)
    return (f'<div class="float sf {cls}" style="animation-duration:{dur}s;animation-delay:{delay}s">'
            f'<b>{title}</b><ul class="sf-list">{lis}</ul></div>')


def _f_dark(cls, r, dur, delay, label, pct, title, sub):
    return (f'<div class="float sf {cls} dark" style="animation-duration:{dur}s;animation-delay:{delay}s">'
            f'<div class="f-head"><span class="mono">{label}</span><span class="f-val">{pct}</span></div>'
            f'<b>{title}</b><div class="f-bar"><i></i></div><small>{sub}</small></div>')


_R = [-4, 3, -3, 4, -2, 3]
_DUR = [7, 8, 9, 7.5, 8.5, 9.5]
_DEL = [0, -2, -4, -1, -3, -5]


def mock_visual(cfg):
    """Monitor con el panel del software y 6 ventanas flotantes (datos ilustrativos). cfg: ver CFG_*"""
    nav = ''.join(
        f'<a{" class=on" if i == 0 else ""}>{ic(icon)}{label}</a>' for i, (icon, label) in enumerate(cfg['nav']))
    kpis = ''.join(
        f'<div class="s-kpi {c}"><span class="k-ic">{ic(i)}</span><div><span>{l}</span><b>{v}</b><em class="{d}">{t}</em></div></div>'
        for c, i, l, v, d, t in cfg['kpis'])
    t = cfg['table']
    rows = ''.join(
        f'<div class="s-tr"><span>{c1}</span><b>{c2}</b><span>{c3}</span><em class="{cls}">{est}</em></div>'
        for c1, c2, c3, est, cls in t['rows'])
    th = ''.join(f'<span>{h}</span>' for h in t['head'])
    d = cfg['donut']
    legend = ''.join(f'<li><i style="--c:{c}"></i>{l}</li>' for c, l in d['legend'])
    ch = cfg['chart']
    hi = ch.get('hi', 4)
    bars = ''.join(f'<i style="--h:{h}%"{" class=hi" if k == hi else ""}></i>' for k, h in enumerate(ch['values']))
    axis = ''.join(f'<span>{a}</span>' for a in ch['axis'])
    sd = cfg['side']
    side_rows = ''.join(f'<div class="s-ib"><span>{l}</span><b class="{c}">{v}</b></div>' for l, v, c in sd['rows'])
    av, org, role = cfg['user']
    top = cfg['top']

    app = f'''<div class="app app-soft" aria-hidden="true">
      <aside class="m-side">
        <div class="m-brand"><span class="m-tree"></span><span>{cfg['brand']}</span></div>
        <nav class="m-nav">{nav}</nav>
        <div class="m-user"><span class="m-av">{av}</span><span>{org}<small>{role}</small></span></div>
      </aside>
      <div class="m-main">
        <div class="m-top">
          <div><h4>{top['title']}</h4><span>{top['sub']}</span></div>
          <div class="m-search">{ic('search')}{top['search']}</div>
          <span class="m-chip">{top['chip']}</span>
        </div>
        <div class="s-kpis">{kpis}</div>
        <div class="s-row">
          <div class="m-card s-table"><div class="m-ch-head"><b>{t['title']}</b><span>{t['link']}</span></div>
            <div class="s-th">{th}</div>{rows}</div>
          <div class="m-card s-donut"><div class="m-ch-head"><b>{d['title']}</b></div>
            <div class="m-donut s-ring" style="background:{d['gradient']}"><span>{d['center']}</span></div>
            <ul class="m-legend">{legend}</ul></div>
        </div>
        <div class="s-row r2">
          <div class="m-card m-chart"><div class="m-ch-head"><b>{ch['title']}</b><span>{ch['sub']}</span></div>
            <div class="m-bars s-bars">{bars}</div><div class="m-axis">{axis}</div></div>
          <div class="m-card s-inbox"><div class="m-ch-head"><b>{sd['title']}</b></div>{side_rows}</div>
        </div>
      </div>
    </div>'''

    fl = cfg['floats']
    # 4 ventanas discretas en los bordes (como en la home): arriba-derecha, izquierda, abajo-izquierda, abajo-derecha
    floats = ''.join([
        _f_dark('sfa', 0, _DUR[5], _DEL[5], *fl[5]),
        _f_item('sfb', 0, _DUR[0], _DEL[0], *fl[0][:3], ok=True),
        _f_item('sfc', 0, _DUR[4], _DEL[4], *fl[4]),
        _f_list('sfd', 0, _DUR[3], _DEL[3], fl[3][0], fl[3][1]),
    ])

    return (floats
            + '<div class="device flat"><div class="device-bezel"><span class="device-cam"></span>'
              '<div class="screen" data-screen>' + app + '</div></div></div>')


# ---- configuraciones del panel por producto (datos ilustrativos; luego se reemplazan por capturas reales)
CFG_SOFT = dict(
    brand='<b>Saman</b> Soft', user=('SS', 'Mi institución', 'Administrador'),
    top=dict(title='Panel de documentos', sub='Resumen de la operación de hoy', search='Buscar documento, CUFE o cliente…', chip='Octubre'),
    nav=[('bar-chart', 'Panel'), ('receipt', 'Facturas'), ('file-text', 'Notas'), ('users', 'Nómina electrónica'),
         ('layers', 'Doc. soporte'), ('inbox', 'Buzón de facturas'), ('trending-up', 'Reportes'), ('lock', 'Configuración')],
    kpis=[('k-blue', 'file-text', 'Documentos hoy', '1.284', 'up', '▲ 12%'),
          ('k-green', 'shield-check', 'Validados DIAN', '1.271', 'up', '▲ 8%'),
          ('k-orange', 'clock', 'En proceso', '9', '', 'En línea'),
          ('k-purple', 'x', 'Rechazados', '4', 'down', '▼ 3%')],
    table=dict(title='Documentos recientes', link='Ver todos', head=['Hora', 'Documento', 'Tipo', 'Estado'],
               rows=[('08:00', 'FE-1284', 'Factura electrónica', 'Validada', 's-ok'),
                     ('09:30', 'NC-0312', 'Nota crédito', 'Enviada', 's-sent'),
                     ('11:00', 'NE-0987', 'Nómina electrónica', 'En proceso', 's-wait'),
                     ('12:30', 'DS-0145', 'Documento soporte', 'Validada', 's-ok')]),
    donut=dict(title='Validación DIAN', center='99%', gradient='conic-gradient(#1FB36B 0 99%, #F59E1B 0 99.6%, #EB5757 0 100%)',
               legend=[('#1FB36B', 'Validados 1.271'), ('#F59E1B', 'En proceso 9'), ('#EB5757', 'Rechazados 4')]),
    chart=dict(title='Documentos por día', sub='Última semana', values=[46, 58, 52, 70, 88, 40, 34], axis=list('LMMJVSD'), hi=4),
    side=dict(title='Buzón de facturas', rows=[('Recibidas', '18', ''), ('Por gestionar', '6', 'w'), ('Gestionadas', '12', 'g')]),
    floats=[('check', 'Factura electrónica', 'FE-1284 · Validada ante la DIAN'),
            ('users', 'Nómina electrónica', 'Periodo de octubre generado'),
            ('qr', 'Código QR', 'CUFE verificable'),
            ('Buzón de facturas', [('g', 'Factura recibida'), ('y', 'Por gestionar'), ('g', 'Gestionada')]),
            ('layers', 'Documento soporte', 'DS-0145 · Generado', 'Listo'),
            ('Envío por correo', '100%', 'Distribución automática', '1.284 documentos entregados')],
)

CFG_SOLUTION = dict(
    brand='<b>Saman</b> Solution', user=('SS', 'Sede principal', 'Cali'),
    top=dict(title='Panel gerencial', sub='Resumen de la operación', search='Buscar paciente, factura o RIPS…', chip='Octubre'),
    nav=[('bar-chart', 'Panel gerencial'), ('heart-pulse', 'Asistencial'), ('receipt', 'Comercial'), ('wallet', 'Financiero'),
         ('users', 'Talento humano'), ('package', 'Administrativo'), ('trending-up', 'Análisis y reportes'), ('lock', 'Configuración')],
    kpis=[('k-blue', 'heart-pulse', 'Atenciones hoy', '1.284', 'up', '▲ 8%'),
          ('k-green', 'receipt', 'Facturas radicadas', '312', 'up', '▲ 5%'),
          ('k-orange', 'clipboard-check', 'RIPS validados', '100%', '', 'Res. 2275'),
          ('k-purple', 'wallet', 'Cartera recuperada', '76%', 'up', '▲ 3%')],
    table=dict(title='Cuentas por radicar', link='Ver todas', head=['Hora', 'Servicio', 'Cuentas', 'Estado'],
               rows=[('08:00', 'Consulta externa', '128 cuentas', 'Radicadas', 's-ok'),
                     ('09:30', 'Urgencias', '64 cuentas', 'En auditoría', 's-wait'),
                     ('11:00', 'Hospitalización', '41 cuentas', 'Radicadas', 's-ok'),
                     ('12:30', 'Cirugía', '19 cuentas', 'Programada', 's-sent')]),
    donut=dict(title='Cartera por edades', center='76%',
               gradient='conic-gradient(#1C4593 0 46%, #F4D53B 0 74%, #7B3A8F 0 90%, #EB5757 0 100%)',
               legend=[('#1C4593', '0-30 días'), ('#F4D53B', '31-60 días'), ('#7B3A8F', '61-90 días'), ('#EB5757', '+90 días')]),
    chart=dict(title='Atenciones por día', sub='Última semana', values=[52, 60, 56, 74, 90, 48, 38], axis=list('LMMJVSD'), hi=4),
    side=dict(title='Agenda de hoy', rows=[('Citas programadas', '36', ''), ('En sala', '9', 'w'), ('Atendidas', '27', 'g')]),
    floats=[('check', 'Factura electrónica', 'Validada ante la DIAN'),
            ('heart-pulse', 'Historia clínica', 'Evolución registrada'),
            ('item', 'calendar', 'Cita web', 'Confirmada · 09:30'),
            ('Auditoría concurrente', [('g', 'Cuenta revisada'), ('y', 'Pendiente de glosa'), ('g', 'Cerrada')]),
            ('smartphone', 'H.C.E. móvil', 'Registro de enfermería sincronizado'),
            ('Resultados', 'Listo', 'Apoyo diagnóstico', 'Disponibles en la historia clínica')],
)

CFG_HEALTH = dict(
    brand='<b>health</b>SQ', user=('HQ', 'Calidad', 'Coordinador'),
    top=dict(title='Panel de calidad', sub='Cumplimiento y seguimiento de hoy', search='Buscar estándar, plan o evento…', chip='2026'),
    nav=[('bar-chart', 'Panel'), ('clipboard-check', 'Habilitación'), ('award', 'Acreditación'), ('shield-check', 'Seguridad'),
         ('trending-up', 'Indicadores'), ('layers', 'Planes de mejora'), ('file-text', 'Reportes'), ('lock', 'Configuración')],
    kpis=[('k-blue', 'clipboard-check', 'Cumplimiento', '92%', 'up', '▲ 4%'),
          ('k-green', 'award', 'Planes de mejora', '14', '', 'Activos'),
          ('k-orange', 'clock', 'Por vencer', '5', '', 'Esta semana'),
          ('k-purple', 'shield-check', 'Eventos adversos', '3', 'down', '▼ 2%')],
    table=dict(title='Plan de auditoría', link='Ver todo', head=['Fecha', 'Estándar', 'Responsable', 'Estado'],
               rows=[('08 oct', 'Habilitación', 'Calidad', 'En tiempo', 's-ok'),
                     ('10 oct', 'Seguridad', 'Enfermería', 'Por vencer', 's-wait'),
                     ('14 oct', 'Acreditación', 'Planeación', 'En tiempo', 's-ok'),
                     ('18 oct', 'Indicadores', 'Gerencia', 'Programada', 's-sent')]),
    donut=dict(title='Cumplimiento', center='92%',
               gradient='conic-gradient(#1FB36B 0 92%, #F4D53B 0 97%, #EB5757 0 100%)',
               legend=[('#1FB36B', 'En tiempo'), ('#F4D53B', 'Por vencer'), ('#EB5757', 'Vencido')]),
    chart=dict(title='Indicadores en meta', sub='Últimos 7 meses', values=[48, 54, 60, 58, 72, 80, 90], axis=list('AMJJASO'), hi=6),
    side=dict(title='Seguridad del paciente', rows=[('Reportados', '3', ''), ('En análisis', '2', 'w'), ('Cerrados', '1', 'g')]),
    floats=[('check', 'Habilitación', 'Semaforización de tiempos'),
            ('award', 'Acreditación', 'Ciclo PAMEC en seguimiento'),
            ('item', 'shield-check', 'Evento adverso', 'Análisis con protocolo de Londres'),
            ('Plan de mejora', [('g', 'Acción asignada'), ('y', 'En ejecución'), ('g', 'Verificada')]),
            ('bar-chart', 'Ficha técnica', 'Indicador dentro de la meta', 'Meta'),
            ('Notificaciones', '100%', 'Alertas automáticas', 'Responsables avisados a tiempo')],
)

CFG_RIPS = dict(
    brand='<b>Saman</b> RIPS', user=('SR', 'Mi institución', 'Facturación'),
    top=dict(title='Panel de RIPS', sub='Generación y control del periodo', search='Buscar archivo, factura o periodo…', chip='Octubre'),
    nav=[('bar-chart', 'Panel'), ('file-text', 'Generar RIPS'), ('shield-check', 'Validaciones'), ('archive', 'Archivos'),
         ('clock', 'Historial'), ('users', 'Usuarios'), ('lock', 'Configuración')],
    kpis=[('k-blue', 'file-text', 'Archivos del periodo', '4', '', 'Generados'),
          ('k-green', 'shield-check', 'Registros validados', '12.840', 'up', '▲ 9%'),
          ('k-orange', 'clock', 'Inconsistencias', '0', '', 'Sin errores'),
          ('k-purple', 'clipboard-check', 'Cumplimiento', '100%', '', 'Res. 2275')],
    table=dict(title='Archivos del periodo', link='Ver historial', head=['Código', 'Archivo', 'Registros', 'Estado'],
               rows=[('US', 'Usuarios', '2.310', 'Validado', 's-ok'),
                     ('AC', 'Consultas', '4.120', 'Validado', 's-ok'),
                     ('AP', 'Procedimientos', '3.045', 'Validado', 's-ok'),
                     ('AM', 'Medicamentos', '3.365', 'Generado', 's-sent')]),
    donut=dict(title='Validación del periodo', center='100%',
               gradient='conic-gradient(#1FB36B 0 100%)',
               legend=[('#1FB36B', 'Válidos 12.840'), ('#F59E1B', 'Con advertencia 0'), ('#EB5757', 'Con error 0')]),
    chart=dict(title='RIPS generados', sub='Últimos 7 meses', values=[40, 52, 58, 62, 70, 84, 92], axis=list('AMJJASO'), hi=6),
    side=dict(title='Radicación', rows=[('Listos para radicar', '4', ''), ('Pendientes', '0', 'w'), ('Radicados', '18', 'g')]),
    floats=[('check', 'Resolución 2275', 'Estructura validada'),
            ('cloud', 'En la nube', 'Información segura'),
            ('item', 'search', 'Consulta', 'RIPS por periodo y entidad'),
            ('Validaciones', [('g', 'Estructura correcta'), ('g', 'Datos completos'), ('g', 'Sin inconsistencias')]),
            ('file-text', 'Archivo RIPS', 'Listo para radicar', 'Listo'),
            ('Generación automática', '100%', 'Sin errores', 'Archivos generados y validados')],
)


# ------------------------------------------------------------------ páginas
PAGES = {}   # nombre.html -> dict(title, description, nav, content)


def add(name, title, description, nav, content):
    PAGES[name] = dict(title=title, description=description, nav=nav, content=content)


# ---------- SAMAN SOLUTION
add('saman-solution.html', 'SAMAN SOLUTION | Gestión hospitalaria integrada · SIO',
    'Solución tecnológica integral para la gestión hospitalaria con la historia clínica electrónica como eje central. Toda la operación en una sola solución, con un único proveedor.',
    'soluciones',
    hero(dict(
        crumbs=crumbs_sol('SAMAN SOLUTION'), img='hero/solution.jpg', pos='50% 35%',
        logo='logo-saman-solution.svg', logo_alt='SAMAN SOLUTION Gestión hospitalaria',
        pill='Gestión hospitalaria',
        h1='Toda la operación de tu institución, <span class="hl-y">en una sola solución</span>',
        lead='Solución tecnológica integral para la gestión hospitalaria que apoya las actividades administrativas y financieras derivadas de los procesos de atención en salud, con la historia clínica electrónica del paciente como eje central.',
        ctas=[btn('Cotiza ya', 'contacto.html', 'yellow'), btn('Ver subsistemas', '#subsistemas', 'light', arrow=False)],
        visual=mock_visual(CFG_SOLUTION)))
    + section(img_panel(
        'panels/solution.jpg', '78% 35%', 'Experiencia',
        '30 años integrando la <span class="hl-y">gestión hospitalaria</span>',
        'Brindamos soluciones integrales para las IPS, en gestión asistencial, financiera y administrativa, con la historia clínica electrónica del paciente como eje central.',
        [('heart-pulse', 'Asistencial', 'Historia clínica electrónica', 'Agendas, enfermería, órdenes médicas y auditoría concurrente.'),
         ('receipt', 'Comercial y financiero', 'Facturación, cartera y contabilidad', 'Facturación y radicación electrónicas, tesorería y presupuesto.'),
         ('bar-chart', 'Análisis y reportes', 'Decisiones con datos', 'Módulo gerencial, trazabilidad e indicadores de gestión.')],
        cta=btn('Cotiza ya', 'contacto.html', 'yellow'), tag='Gestión hospitalaria integrada'), 'tight')
    + hub_section()
    + section(
        sec_head('Atributos por subsistema', 'Todo lo que cubre cada subsistema',
                 'Cada subsistema se integra con los demás y comparte la información de la historia clínica electrónica.')
        + sub_cards([
            ('#17998A', 'heart-pulse', 'Subsistema Asistencial',
             ['Historia clínica electrónica', 'Registro de enfermería', 'Interoperabilidad', 'Órdenes médicas electrónicas integradas',
              'Mecanismos de seguridad', 'Historias clínicas por especialidades', 'Citas web', 'Salud móvil', 'Auditoría interna y concurrente'],
             'stock/sub-asistencial.jpg', '50% 40%'),
            ('#7B3A8F', 'receipt', 'Subsistema Comercial',
             ['Control total de la cartera', 'Facturación electrónica', 'Radicación electrónica'],
             'stock/sub-comercial.jpg', '50% 50%'),
            ('#0F4C7A', 'wallet', 'Subsistema Financiero',
             ['Contabilidad', 'Buzón para gestión de facturas', 'Gestión y contratación con proveedores', 'Documento soporte',
              'Tesorería', 'Seguimiento y control del presupuesto'],
             'stock/sub-financiero.jpg', '50% 55%'),
            ('#EB5757', 'bar-chart', 'Subsistema de Análisis y Reportes',
             ['Trazabilidad de facturación, de inicio a fin', 'Módulo gerencial para análisis de información'],
             'stock/sub-analisis.jpg', '50% 50%'),
            ('#F59E1B', 'package', 'Subsistema Administrativo',
             ['Gestión de almacén', 'Control total de activos fijos'],
             'stock/sub-administrativo.jpg', '50% 50%'),
            ('#63C3CC', 'users', 'Subsistema del Talento Humano',
             ['Nómina electrónica', 'Gestión del talento humano', 'Liquidación de nómina, prenómina y nómina definitiva'],
             'stock/sub-talento.jpg', '50% 50%'),
        ]), 'alt')
    + section(h_timeline(
        'Por qué SAMAN SOLUTION', 'Una sola solución, un único proveedor',
        'Toda la operación de tu institución trabaja sobre la misma información, de la atención del paciente a los indicadores gerenciales.',
        [('layers', 'Operación', 'Toda la operación integrada',
          'Lo asistencial, lo comercial, lo financiero, el talento humano y lo administrativo trabajan sobre la misma información.'),
         ('heart-pulse', 'Historia clínica', 'La historia clínica como eje',
          'La atención del paciente alimenta de forma natural la facturación, la cartera y los indicadores.'),
         ('link', 'Ecosistema', 'Se conecta con tu ecosistema',
          'Se integra con Saman Soft para documentos electrónicos, Health SQ para calidad en salud y Saman RIPS.'),
         ('award', 'Respaldo', 'Respaldo certificado',
          'Procesos evaluados bajo CMMI-SVC nivel 3, seguridad de la información ISO/IEC 27001 y respaldo tecnológico de Oracle.')]))
    + support_strip('SAMAN SOLUTION', detail='Los clientes de SAMAN HC, SAMAN HCM y SAMAN FCA cuentan con soporte funcional y técnico. ')
    + related(['saman-soft', 'health-sq', 'saman-rips'], 'Se integra con', 'Soluciones que potencian SAMAN SOLUTION')
    + cta_band('Conoce SAMAN SOLUTION en acción', 'Solicita una demostración sin costo y descubre cómo unificar la operación de tu institución.'))

# ---------- SAMAN SOFT
add('saman-soft.html', 'Saman Soft | Facturación y nómina electrónica · SIO',
    'Proveedor tecnológico autorizado por la DIAN. Facturación electrónica, nómina electrónica, documento soporte y buzón de gestión de facturas en la nube.',
    'soluciones',
    hero(dict(
        crumbs=crumbs_sol('Saman Soft'),
        logo='logo-saman-soft.png', logo_alt='Saman Soft Documentación electrónica',
        pill='Documentos electrónicos · DIAN',
        h1='Facturación y nómina electrónica, <span class="hl-y">en la nube</span>',
        lead='Somos proveedores autorizados por la DIAN. Genera, valida y distribuye tus documentos electrónicos desde una plataforma integrada con SAMAN SOLUTION.',
        ctas=[btn('Solicitar información', 'contacto.html', 'yellow'), btn('Hablar por WhatsApp', WA, 'light', ext=True)],
        visual=mock_visual(CFG_SOFT)))
    + section(img_panel(
        'panels/soft.jpg', '100% 50%', 'Autorizados por la DIAN',
        'Un proveedor tecnológico <span class="hl-y">habilitado desde 2020</span>',
        'SIO SAS se habilitó como proveedor tecnológico de la DIAN en febrero de 2020. A través de Saman Soft ofrece sus servicios en una plataforma en la nube, integrada con SAMAN SOLUTION.',
        [('receipt', 'Facturación', 'Facturación electrónica', 'Facturas, notas débito y notas crédito validadas ante la DIAN.'),
         ('users', 'Nómina', 'Nómina electrónica y documento soporte', 'Genera y distribuye tus documentos electrónicos desde un solo lugar.'),
         ('inbox', 'Proveedores', 'Buzón de gestión para facturas', 'Recibe y gestiona las facturas de tus proveedores.')],
        cta=btn('Solicitar información', 'contacto.html', 'yellow'), tag='Saman Soft en la nube'), 'tight')
    + section(
        sec_head('Funcionalidades', 'Todo el ciclo del documento electrónico')
        + feats([
            ('file-text', 'Generación de documentos', 'Facturas, notas débito, notas crédito, nómina electrónica y documento soporte.'),
            ('shield-check', 'Validación ante la DIAN', 'Valida los documentos tributarios ante la DIAN antes de distribuirlos.'),
            ('mail', 'Distribución por correo', 'Envío automático de los documentos al correo electrónico del destinatario.'),
            ('link', 'Integración flexible', 'Se integra mediante servicios REST o archivos planos con tus otros sistemas.'),
            ('scan', 'Captura y generación', 'Módulo para la captura y la generación de documentos electrónicos.'),
            ('archive', 'Conservación por 10 años', 'Los documentos se conservan durante 10 años, durante la vigencia del contrato.'),
            ('layers', 'Plantillas a tu medida', 'Plantillas prediseñadas o personalizadas con la imagen de tu institución.'),
            ('life-buoy', 'Soporte funcional y técnico', 'Acompañamiento de nuestro equipo para resolver tus dudas y novedades.'),
        ], cols=4), 'alt')
    + support_strip('Saman Soft', 'soon')
    + related(['saman-solution', 'health-sq', 'saman-rips'], 'Se integra con', 'Más soluciones para tu institución')
    + cta_band('Pon al día tu facturación y nómina electrónica', 'Cuéntanos tu operación y te mostramos cómo funciona Saman Soft.'))

# ---------- HEALTH SQ
add('health-sq.html', 'Health SQ | Calidad en salud · SIO',
    'Solución tecnológica para la administración, seguimiento y control integral de los Sistemas Obligatorios de Calidad en salud: habilitación, acreditación, seguridad del paciente e indicadores.',
    'soluciones',
    hero(dict(
        crumbs=crumbs_sol('Health SQ'), img='hero/health.jpg', pos='50% 45%',
        logo='logo-health-sq.png', logo_alt='Health SQ',
        pill='Calidad en salud · SOGC',
        h1='El Sistema Obligatorio de Garantía de Calidad, <span class="hl-y">bajo control</span>',
        lead='Una solución tecnológica completa que permite la administración, el seguimiento y el control integral de los Sistemas Obligatorios de Calidad en salud.',
        ctas=[btn('Solicitar información', 'contacto.html', 'yellow'), btn('Hablar por WhatsApp', WA, 'light', ext=True)],
        visual=mock_visual(CFG_HEALTH)))
    + section(img_panel(
        'panels/health.jpg', '72% 50%', 'Beneficios',
        'Calidad asistencial con <span class="hl-y">evidencia y trazabilidad</span>',
        'Health SQ integra la información del sistema obligatorio de garantía de calidad y facilita la mejora continua con énfasis en la acreditación.',
        [('clipboard-check', 'Habilitación', 'Seguimiento a los estándares', 'Control a los estándares de habilitación con semaforización de tiempos.'),
         ('shield-check', 'Seguridad', 'Riesgos del paciente bajo monitoreo', 'Gestión de eventos adversos, barreras y fallas latentes.'),
         ('award', 'Acreditación', 'Evidencia para las auditorías', 'Recopila la evidencia y optimiza los procesos de mejoramiento.')],
        cta=btn('Solicitar información', 'contacto.html', 'yellow'), tag='Sistemas obligatorios de calidad'), 'tight')
    + section(
        sec_head('Módulos principales', 'Cuatro módulos, una sola visión de la calidad')
        + feats([
            ('clipboard-check', 'Habilitación', 'Auditorías de planes y acciones de obligatorio cumplimiento, con semaforización de tiempos y notificaciones.', None, '#1C4593'),
            ('award', 'Acreditación', 'Administración de planes de auditoría y mejoramiento asociados al PAMEC y control de los ciclos de acreditación.', None, '#2F63D1'),
            ('shield-check', 'Seguridad del paciente', 'Captura de eventos adversos con análisis mediante el protocolo de Londres y gestión de barreras y fallas latentes.', None, '#0F4C7A'),
            ('bar-chart', 'Indicadores', 'Diseño de fichas técnicas para medir la eficiencia y la calidad de los procesos organizacionales.', None, '#F59E1B'),
        ], cols=4), 'alt')
    + support_strip('Health SQ')
    + related(['saman-solution', 'saman-rips', 'saman-soft'], 'Se integra con', 'Más soluciones para tu institución')
    + cta_band('Lleva la calidad de tu institución al siguiente nivel', 'Agenda una demostración de Health SQ con un asesor de SIO.'))

# ---------- SAMAN RIPS
add('saman-rips.html', 'Saman RIPS | RIPS automáticos · Resolución 2275 · SIO',
    'Software en la nube para la consulta, gestión y control de la generación de RIPS de forma automática, segura y sin errores, conforme a la Resolución 2275.',
    'soluciones',
    hero(dict(
        crumbs=crumbs_sol('Saman RIPS'), img='hero/rips.jpg', pos='50% 50%',
        logo='logo-saman-rips.png', logo_alt='Saman RIPS',
        pill='RIPS · Resolución 2275',
        h1='RIPS automáticos, seguros y <span class="hl-y">sin errores</span>',
        lead='¿Confundido con los RIPS? Te lo ponemos fácil. Saman RIPS tiene la solución.',
        ctas=[btn('Solicita una demo gratis', 'contacto.html', 'yellow'), btn('Asesoría gratuita por WhatsApp', WA, 'light', ext=True)],
        visual=real_visual(
            'rips-hero.jpg', 'Saman RIPS: documentos y opciones de exportación en ZIP, RIPS y CUV',
            _f_dark('sfa', 0, _DUR[5], _DEL[5], 'Historial', '', 'Trazabilidad de envíos', 'Fecha, hora y resultado')
            + _f_item('sfb', 0, _DUR[0], _DEL[0], 'check', 'Resolución 2275', 'Estructura validada', ok=True)
            + _f_item('sfc', 0, _DUR[4], _DEL[4], 'download', 'ZIP · RIPS · CUV', 'Exporta con clic secundario'))))
    + section(img_panel(
        'panels/rips.jpg', '75% 50%', 'Cómo funciona',
        'Consulta, gestiona y controla tus <span class="hl-y">RIPS</span>',
        'Software en la nube que permite la consulta, gestión y control de la generación de tus RIPS de forma rápida, automática y segura, dando cumplimiento a la Resolución 2275.',
        [('file-text', 'Automático', 'Generación sin errores', 'Archivos RIPS generados y validados de forma automática.'),
         ('clipboard-check', 'Normativo', 'Resolución 2275', 'Estructura y cumplimiento conforme a la norma vigente.'),
         ('cloud', 'En la nube', 'Información segura', 'Consulta, gestión y control disponibles cuando los necesites.')],
        cta=btn('Solicita una demo gratis', 'contacto.html', 'yellow'), tag='Saman RIPS'), 'tight')
    + section(
        sec_head('Conoce la plataforma', 'Así se ve <span class="hl">Saman RIPS</span> por dentro',
                 'Recorre las pantallas reales de la plataforma: elige una opción y mira cómo funciona.')
        + tour('Saman RIPS', [
            ('file-text', 'Documentos',
             'Consulta todos tus documentos en una sola tabla: tipo, número, código único de validación (CUV), fecha y estado. Filtra por tipo, estado y fechas, o busca un documento.',
             'rips-documentos.jpg', 1.15, '100% 0%'),
            ('pointer', 'Acciones con clic secundario',
             'Haz clic derecho sobre un documento para modificar sus RIPS, enviarlo de nuevo, ver su histórico, exportarlo o eliminarlo.',
             'rips-acciones.jpg', 1.5, '100% 18%'),
            ('download', 'Exporta lo que necesitas',
             'Descarga el paquete en ZIP, el archivo RIPS o el CUV de cada documento, directamente desde la plataforma.',
             'rips-exportar.jpg', 1.5, '100% 24%'),
            ('clock', 'Historial de envíos',
             'Revisa cada envío con su fecha, hora y resultado, y consulta las reglas de validación aplicadas.',
             'rips-historial.jpg', 1.0, '50% 40%'),
            ('users', 'Usuarios y roles',
             'Administra quién accede a la plataforma: busca, agrega y elimina usuarios según su rol.',
             'rips-usuarios.jpg', 1.15, '100% 0%'),
        ], 'Pantallas reales de Saman RIPS. Haz clic en la imagen para ampliarla.'), 'alt')
    + timeline('Implementación', 'Listo para usar, paso a paso',
               'Un proceso claro para que tu institución genere sus RIPS sin complicaciones.',
               [('search', 'Diagnóstico inicial', 'Revisamos cómo gestionas hoy los RIPS en tu institución.'),
                ('layers', 'Configuración personalizada', 'Parametrizamos la plataforma según tus procesos.'),
                ('users', 'Capacitación virtual', 'Formamos a tu equipo para operar la plataforma con seguridad.'),
                ('clipboard-check', 'Pruebas con datos reales', 'Validamos la generación de RIPS con tu información.'),
                ('check', 'Sistema listo para usar', 'Tu operación queda automatizada y en marcha.')],
               cta=btn('Solicitar demo gratis', 'contacto.html', 'dark'))
    + support_strip('Saman RIPS')
    + related(['saman-solution', 'saman-soft', 'health-sq'], 'Se integra con', 'Más soluciones para tu institución')
    + cta_band('Deja de preocuparte por los RIPS', 'Escríbenos por WhatsApp para una asesoría gratuita o solicita una demostración.'))

# ---------- GESTIÓN DOCUMENTAL
add('gestion-documental.html', 'Gestión documental | Servicios BPO · SIO',
    'Análisis, desarrollo e implementación de actividades para la planificación, manejo y organización de la documentación, desde su origen hasta su disposición final.',
    'soluciones',
    hero(dict(
        crumbs=crumbs_sol('Gestión documental'), img='hero/doc.jpg', pos='50% 50%',
        pill='Servicios BPO',
        h1='Gestión documental, <span class="hl-y">de su origen a su disposición final</span>',
        lead='Servicios de análisis, desarrollo e implementación de actividades para la planificación, el manejo y la organización de la documentación de tu organización.',
        ctas=[btn('Solicitar información', 'contacto.html', 'yellow'), btn('Hablar por WhatsApp', WA, 'light', ext=True)]))
    + section(
        sec_head('Servicios', 'Todo el ciclo de vida de tus documentos')
        + feats([
            ('folder', 'Tablas de Retención Documental (TRD)', 'Recolección y análisis de series documentales y tipos de documentos; ordenación y recuperación de información semiactiva e inactiva.'),
            ('scan', 'Digitalización e indexación', 'Conversión de documentos analógicos a formatos digitales mediante infraestructura tecnológica especializada.'),
            ('layers', 'Intervención de archivo', 'Organización, depuración, foliación y disposición final de documentos.'),
            ('archive', 'Custodia de archivos', 'Depósito y administración en locaciones especializadas con tecnología avanzada.'),
            ('inbox', 'Ventanilla única de correspondencia', 'Registro centralizado de la información recibida, enviada e interna, con seguimiento y trazabilidad.'),
            ('monitor', 'Software de gestión documental', 'Solución tecnológica para la administración documental con altos niveles de oportunidad, efectividad y trazabilidad.'),
            ('graduation', 'Capacitación especializada', 'Programas de formación en los productos y servicios del sistema.'),
        ], cols=3))
    + related(['gestion-de-informacion', 'suministros-tecnologicos', 'gobierno-de-datos'])
    + cta_band('Organiza la documentación de tu organización', 'Cuéntanos tu necesidad y diseñamos el servicio a tu medida.'))

# ---------- GESTIÓN DE INFORMACIÓN
add('gestion-de-informacion.html', 'Gestión de información | Servicios BPO · SIO',
    'Procesos para controlar el ciclo de vida de la información, desde su obtención hasta su disposición final: digitalización, captura masiva y tecnologías avanzadas de captura.',
    'soluciones',
    hero(dict(
        crumbs=crumbs_sol('Gestión de información'), img='hero/info.jpg', pos='50% 50%',
        pill='Servicios BPO',
        h1='Controla el ciclo de vida de tu <span class="hl-y">información</span>',
        lead='Servicio de procesos por los cuales se controla el ciclo de vida de la información, desde su obtención hasta su disposición final.',
        ctas=[btn('Solicitar información', 'contacto.html', 'yellow'), btn('Hablar por WhatsApp', WA, 'light', ext=True)]))
    + section(
        sec_head('Servicios', 'De la captura a la disposición final')
        + feats([
            ('scan', 'Digitalización e indexación', 'Reproducción de la información almacenada en formato analógico mediante infraestructura tecnológica especializada, hardware y software.'),
            ('database', 'Captura masiva de información', 'Procesamiento extensivo de documentos mediante digitación o digitalización automatizada.'),
            ('graduation', 'Capacitación', 'Formación en todos los productos y servicios relacionados con la gestión informática.'),
        ], cols=3))
    + section(
        split('Tecnologías avanzadas de captura', 'Menos digitación manual, más calidad en el dato',
              ['Múltiples métodos orientados a disminuir la cantidad de entradas de datos manuales para la captura de la información impresa.'],
              None,
              '<div class="feat-grid c2" data-reveal>'
              + ''.join(f'<div class="feat"><span class="f-ico">{ic(i)}</span><h3>{t}</h3><p>{d}</p></div>'
                        for i, t, d in [('scan', 'OCR', 'Reconocimiento óptico de caracteres.'),
                                        ('cpu', 'ICR', 'Reconocimiento inteligente de caracteres.'),
                                        ('check', 'OMR', 'Reconocimiento de marcas ópticas.'),
                                        ('link', 'QR y RFID', 'Identificación y lectura automática de códigos y etiquetas.')])
              + '</div>'), 'alt')
    + related(['gestion-documental', 'suministros-tecnologicos', 'gobierno-de-datos'])
    + cta_band('Automatiza la captura de tu información', 'Cuéntanos el volumen y el tipo de documentos y te proponemos la solución.'))

# ---------- SUMINISTROS TECNOLÓGICOS
add('suministros-tecnologicos.html', 'Suministros tecnológicos | Servicios BPO · SIO',
    'Suministro y administración de los espacios físicos de trabajo según las especificaciones técnicas y tecnológicas: equipos, puestos de trabajo y mesa de ayuda.',
    'soluciones',
    hero(dict(
        crumbs=crumbs_sol('Suministros tecnológicos'), img='hero/supply.jpg', pos='50% 50%',
        pill='Servicios BPO',
        h1='Infraestructura y espacios de trabajo, <span class="hl-y">listos para operar</span>',
        lead='Suministro y administración de los espacios físicos de trabajo, de acuerdo con las especificaciones técnicas y tecnológicas de tu proceso.',
        ctas=[btn('Solicitar información', 'contacto.html', 'yellow'), btn('Hablar por WhatsApp', WA, 'light', ext=True)]))
    + section(
        sec_head('Servicios', 'Soluciones integrales con soporte continuo',
                 'Combinamos infraestructura física y tecnológica personalizada con acompañamiento permanente.')
        + feats([
            ('monitor', 'Equipos tecnológicos', 'Alquiler y venta de infraestructura: computadores, servidores, impresoras y escáneres, con instalación y adecuación incluidas.'),
            ('building', 'Espacios de trabajo', 'Suministro de sistemas de puestos de trabajo adaptados a procesos específicos.'),
            ('headset', 'Asistencia técnica', 'Servicio de mesa de ayuda local y remota para resolver problemas técnicos.'),
            ('graduation', 'Capacitación', 'Programas educativos en los productos y servicios suministrados.'),
        ], cols=4))
    + related(['gestion-documental', 'gestion-de-informacion', 'centro-de-negocios'])
    + cta_band('Equipa tu operación sin complicaciones', 'Cuéntanos qué necesitas y armamos la propuesta a tu medida.'))

# ---------- SERVICIOS PÚBLICOS
add('servicios-publicos.html', 'Servicios públicos | Supernova S.C. · SIO',
    'Soluciones informáticas especializadas para el sector de servicios públicos (energía, agua y gas): software comercial Supernova S.C., consultoría en inteligencia de negocios y minería de datos.',
    'soluciones',
    hero(dict(
        crumbs=crumbs_sol('Servicios públicos'), img='hero/utilities.jpg', pos='50% 60%',
        logo='logo-supernova.png', logo_alt='Supernova S.C.',
        pill='Energía, agua y gas',
        h1='Soluciones informáticas para <span class="hl-y">servicios públicos</span>',
        lead='Servicios profesionales, aplicativos y hardware para empresas de energía, agua y gas.',
        ctas=[btn('Solicitar información', 'contacto.html', 'yellow'), btn('Hablar por WhatsApp', WA, 'light', ext=True)]))
    + section(split(
        'Supernova S.C.', 'Software integral comercial para empresas de servicios públicos',
        ['Implementa modelos de negocio de manera dinámica considerando el marco regulatorio, y gestiona las pérdidas no técnicas mediante la detección de anomalías.',
         'Su integración modular y flexible es compatible con módulos financieros y soporta procesos comerciales, operativos, técnicos, financieros y contables.'],
        ['Venta de productos y servicios', 'Infraestructura eléctrica', 'Atención al cliente y contact center',
         'Facturación y recaudos', 'Financiaciones y recuperación de cartera',
         'Micromedición, macromedición y control de pérdidas', 'Estadísticas y reportes gerenciales', 'Seguridad y auditoría'],
        shot('assets/img/shots/supernova-modulos.jpg', 'Módulos de Supernova S.C.', pad=True)))
    + section(
        sec_head('Servicios profesionales', 'Del dato a la decisión')
        + feats([
            ('bar-chart', 'Inteligencia de negocios', 'Consultoría en inteligencia de negocios con CONOZE B.I.®.'),
            ('database', 'Minería de datos', 'Minería de datos especializada para descubrir patrones y oportunidades.'),
            ('gauge', 'Planeación', 'Software de restricciones para la planeación operativa.'),
        ], cols=3), 'alt')
    + related(['gobierno-de-datos', 'gestion-documental', 'saman-solution'])
    + cta_band('Moderniza la gestión de tu empresa de servicios públicos', 'Cuéntanos tu operación y conversemos sobre Supernova S.C.'))

# ---------- GOBIERNO DE DATOS
add('gobierno-de-datos.html', 'Gobierno de datos | Oracle · SIO',
    'Servicios de outsourcing especializados en captura, procesamiento y administración de información basados en las mejores prácticas: administración Oracle, tuning, migración, alta disponibilidad y nube.',
    'soluciones',
    hero(dict(
        crumbs=crumbs_sol('Gobierno de datos'), img='hero/data.jpg', pos='50% 50%',
        logo='cert/oracle-partner.png', logo_alt='Oracle Partner',
        pill='Oracle Partner Network',
        h1='Tus datos, <span class="hl-y">disponibles, seguros y optimizados</span>',
        lead='Servicios de outsourcing especializados en captura, procesamiento y administración de información, basados en las mejores prácticas.',
        ctas=[btn('Solicitar información', 'contacto.html', 'yellow'), btn('Hablar por WhatsApp', WA, 'light', ext=True)]))
    + section(
        sec_head('Servicios', 'Administración integral de bases de datos Oracle')
        + feats([
            ('server', 'Instalación y configuración', None,
             ['Motores Oracle 9i, 10g, 11g y 12c', 'Ambientes de desarrollo, testing y producción', 'Oracle ASM e implementación de auditorías', 'Clonación de bases de datos']),
            ('database', 'Administración de bases de datos', None,
             ['Implementación de seguridades personalizadas', 'Solución de errores y monitoreo preventivo', 'Mantenimiento de filesystems y esquemas', 'Aplicación de parches y monitoreo de backups']),
            ('gauge', 'Tuning y optimización', None,
             ['Análisis de parámetros y procesos críticos', 'Implementación de técnicas de optimización']),
            ('refresh', 'Migración, backup y recuperación', None,
             ['Migraciones entre versiones y storage', 'Configuración de RMAN', 'Recuperación de bases de datos, esquemas o tablas']),
            ('zap', 'Alta disponibilidad', None,
             ['Implementación de Oracle RAC', 'Base de datos Standby con Data Guard']),
            ('cloud', 'Servicios en la nube', None,
             ['Bases de datos en la nube', 'Backup de archivos']),
        ], cols=3))
    + section(split(
        'Respaldo', 'Con el respaldo tecnológico de Oracle',
        ['Nuestros productos cuentan con el respaldo tecnológico de ORACLE, líder mundial en motores de bases de datos robustas e infraestructura tecnológica en la nube. SIO cuenta con la membresía de Oracle Partner Network.'],
        ['Capacitación según las necesidades de tu equipo'],
        '<div class="shot pad" style="display:grid;place-items:center;min-height:220px"><img src="assets/img/cert/oracle-partner.png" alt="Oracle Partner Network" style="max-width:320px"></div>'), 'alt')
    + related(['servicios-publicos', 'gestion-de-informacion', 'saman-solution'])
    + cta_band('Pon tus bases de datos en manos expertas', 'Cuéntanos tu ambiente actual y te proponemos un plan de administración.'))

# ---------- CENTRO DE NEGOCIOS
add('centro-de-negocios.html', 'Centro de negocios | Oficinas en Cali · SIO',
    'Espacio ideal para profesionales y empresas de distintos sectores en una de las mejores ubicaciones comerciales de Cali: oficinas amobladas, oficina virtual y salas de reuniones por horas.',
    'soluciones',
    hero(dict(
        crumbs=crumbs_sol('Centro de negocios'), img='hero/center.jpg', pos='50% 50%',
        pill='Cali, Valle del Cauca',
        h1='Un espacio ideal para tu <span class="hl-y">empresa</span>',
        lead='Centro de negocios SIO: el espacio ideal para profesionales y empresas de distintos sectores, en una de las mejores ubicaciones comerciales de Cali.',
        ctas=[btn('Solicitar información', 'contacto.html', 'yellow'), btn('Hablar por WhatsApp', WA, 'light', ext=True)]))
    + section(
        sec_head('Servicios', 'Elige el espacio que tu empresa necesita')
        + feats([
            ('building', 'Alquiler de oficinas amobladas', 'De 1 a 20 puestos de trabajo según tus necesidades, con todos los servicios incluidos en una única tarifa.',
             ['Aire acondicionado', 'Sillas ergonómicas y escritorios', 'Internet WiFi', 'Recepción']),
            ('cloud', 'Oficina virtual', 'Recursos tecnológicos para el trabajo remoto a menor costo y posicionamiento de marca sin un espacio físico permanente.',
             ['Buzón para llamadas', 'Recepción de documentos físicos']),
            ('users', 'Salas de reuniones por horas', 'Para tus comités y reuniones de junta directiva, con capacidad para hasta 10 personas.',
             ['Ayudas audiovisuales', 'Catering opcional: desayuno, brunch o almuerzo', 'Aire acondicionado y WiFi']),
        ], cols=3))
    + section(
        sec_head('Todo incluido', 'Servicios y comodidades para tu día a día')
        + '<div class="feat-grid c4" data-reveal>'
        + ''.join(f'<div class="feat"><span class="f-ico">{ic(i)}</span><h3>{t}</h3></div>' for i, t in [
            ('wifi', 'Internet WiFi'), ('wind', 'Aire acondicionado'), ('coffee', 'Estación de bebidas'),
            ('shield-check', 'Portería con seguridad privada'), ('key', 'Recepción'), ('arrow-up', 'Elevador'),
            ('utensils', 'Comedor'), ('sparkles', 'Servicio de limpieza')])
        + '</div>', 'alt')
    + related(['suministros-tecnologicos', 'gestion-documental', 'gobierno-de-datos'])
    + cta_band('Conoce el Centro de negocios', 'Agenda una visita o solicita una cotización sin compromiso.'))

# ---------- SOLUCIONES (índice)
add('soluciones.html', 'Soluciones | SIO',
    'Soluciones para la gestión hospitalaria, documentos electrónicos, calidad en salud, BPO y servicios de datos. Un ecosistema que se integra para que la información fluya.',
    'soluciones',
    hero(dict(
        crumbs=[('Inicio', 'index.html'), ('Soluciones', '')],
        pill='Soluciones',
        h1='Soluciones para cada proceso de tu <span class="hl-y">organización</span>',
        lead='Un ecosistema de soluciones que se integran entre sí: gestión hospitalaria, documentos electrónicos, calidad en salud, servicios BPO y servicios de datos.',
        ctas=[btn('Solicitar demo', 'contacto.html', 'yellow')]))
    + section(
        f'''<a class="sol-feature" href="saman-solution.html" data-reveal>
          <img class="bg" src="assets/img/hero/solution.jpg" alt="" loading="lazy">
          <div class="sol-feature-copy">
            <span class="hero-logo"><img src="assets/img/logo-saman-solution.svg" alt="SAMAN SOLUTION"></span>
            <h2>Toda la operación de tu institución, en una sola solución</h2>
            <p>Gestión asistencial, comercial, financiera, administrativa y de talento humano con la historia clínica electrónica como eje central.</p>
            <span class="link-arrow" style="color:var(--yellow)">Conocer SAMAN SOLUTION {ic("arrow-right")}</span>
          </div><span></span></a>''')
    + section(
        sec_head('Se integran entre sí', 'Soluciones que se integran a SAMAN SOLUTION',
                 'Cada una resuelve una necesidad específica y se conecta para que la información fluya sin reprocesos.')
        + pcards(['saman-soft', 'health-sq', 'saman-rips']), 'alt')
    + f'<section class="section" id="otras-soluciones"><div class="container">'
      + '<div class="others-head"><div><span class="pill pill-sm">Otras soluciones</span><h3>Servicios que complementan tu operación</h3></div>'
      + f'<a class="link-arrow" href="contacto.html">Hablar con un asesor {ic("arrow-right")}</a></div>'
      + otiles(OTHER) + '</div></section>'
    + cta_band('¿No sabes por dónde empezar?', 'Un asesor de SIO te ayuda a identificar la solución que mejor se ajusta a tu operación.'))

# ---------- CASOS DE ÉXITO
sectors = [
    ('hospital', 'Hospitales, clínicas e IPS',
     'Gestión asistencial, financiera y administrativa integrada en una sola solución, con la calidad y los RIPS bajo control.',
     ['r1-02', 'r3-02', 'r3-03', 'r2-05', 'r2-01', 'r3-04'],
     ['saman-solution', 'health-sq', 'saman-rips', 'saman-soft']),
    ('users', 'Cajas de compensación y aseguradoras',
     'Documentos electrónicos y procesos de información a gran escala, con trazabilidad y cumplimiento.',
     ['r1-07', 'r1-06', 'r1-08', 'r3-08'],
     ['saman-soft', 'gestion-de-informacion', 'gestion-documental']),
    ('building', 'Sector público y servicios públicos',
     'Gestión documental, gobierno de datos y soluciones comerciales para energía, agua y gas.',
     ['r3-07', 'r3-09', 'r3-06'],
     ['gestion-documental', 'servicios-publicos', 'gobierno-de-datos']),
]
def case_logos(keys):
    names = dict(CLIENTS)
    return ''.join(f'<img src="assets/img/clients/{k}.png" alt="{names[k]}" loading="lazy">' for k in keys)


sector_html = ''
for icon, title, text, cl, sols in sectors:
    chips = ''.join(f'<a class="chip" href="{s}.html">{SOL[s]["name"]}</a>' for s in sols)
    sector_html += (
        f'<div class="sector"><span class="case-ic">{ic(icon)}</span><div><h3>{title}</h3><p>{text}</p>'
        f'<div class="case-logos">{case_logos(cl)}</div>'
        f'<div class="chips">{chips}</div></div></div>')

add('casos-de-exito.html', 'Casos de éxito | SIO',
    'Más de tres décadas implementando soluciones para hospitales, clínicas, cajas de compensación y entidades del sector público en Colombia.',
    'casos',
    hero(dict(
        crumbs=[('Inicio', 'index.html'), ('Casos de éxito', '')],
        pill='Casos de éxito',
        h1='Experiencia comprobada <span class="hl-y">en cada sector</span>',
        lead='Más de tres décadas implementando soluciones para instituciones de salud, cajas de compensación y entidades del sector público.',
        ctas=[btn('Hablar con un asesor', 'contacto.html', 'yellow')]))
    + section(
        sec_head('Sectores', 'Soluciones aplicadas a la realidad de cada institución')
        + f'<div class="feat-grid c2" data-reveal style="grid-template-columns:1fr">{sector_html}</div>')
    + section(
        sec_head('Clientes', 'Instituciones que confían en SIO',
                 'Hospitales, clínicas, cajas de compensación y entidades públicas que operan con nuestras soluciones.')
        + f'<div class="client-grid" data-reveal>{logos([k for k, _ in CLIENTS])}</div>', 'alt')
    + cta_band('Que tu institución sea el próximo caso de éxito', 'Cuéntanos tu reto y construimos juntos la solución.'))

# ---------- NOSOTROS
IHCE_SRC = 'assets/img/cert/ihce-reconocimiento.webp'
IHCE_CAP = 'Reconocimiento del Ministerio de Salud y Protección Social (IHCE) a Soluciones Integrales de Oficina SIO S.A.S. · 17 de abril de 2026'


def _tech_card(title, logos, text, extra=''):
    return (f'<article class="tech-card" data-reveal><h3>{title}</h3><span class="tech-rule" aria-hidden="true"></span>'
            f'<div class="tech-logos">{logos}</div><p>{text}</p>{extra}</article>')


TECH = ''.join([
    _tech_card(
        'Integración total sin terceros',
        '<img class="tl-sio" src="assets/img/logo-sio.svg" alt="SIO" loading="lazy">'
        '<img class="tl-saman" src="assets/img/logo-saman-solution.svg" alt="SAMAN SOLUTION Gestión hospitalaria" loading="lazy">',
        'SIO integra la operación asistencial, comercial, financiera, administrativa y de talento humano en SAMAN SOLUTION, con un único proveedor para toda la institución.'),
    _tech_card(
        'Respaldo y escalabilidad global',
        '<img class="tl-oci" src="assets/img/cert/oracle-cloud-infrastructure.png" alt="Oracle Cloud Infrastructure" loading="lazy">'
        '<img class="tl-partner" src="assets/img/cert/oracle-partner.png" alt="Oracle Partner" loading="lazy">',
        'Nuestros productos cuentan con el respaldo de Oracle, líder mundial en bases de datos e infraestructura en la nube, y SIO hace parte de Oracle Partner Network.'),
    _tech_card(
        'Cumplimiento normativo automatizado',
        '<img class="tl-dian" src="assets/img/cert/dian.png" alt="DIAN, Dirección de Impuestos y Aduanas Nacionales" loading="lazy">'
        f'<button type="button" class="tech-doc" data-lightbox="{IHCE_SRC}" data-caption="{IHCE_CAP}" aria-label="Ampliar el reconocimiento del Ministerio de Salud (IHCE)">'
        f'<img src="{IHCE_SRC}" alt="Reconocimiento del Ministerio de Salud y Protección Social (IHCE) a SIO" loading="lazy"></button>',
        'Proveedor tecnológico autorizado por la DIAN y reconocido por el Ministerio de Salud por su aporte a la validación técnica del Resumen Digital de Atención (RDA) en el proyecto de Interoperabilidad de la Historia Clínica Electrónica (IHCE).',
        f'<button type="button" class="link-arrow tech-link" data-lightbox="{IHCE_SRC}" data-caption="{IHCE_CAP}">Ver reconocimiento {ic("expand")}</button>'),
    _tech_card(
        'Seguridad de clase mundial',
        '<img class="tl-iso" src="assets/img/cert/iso-27001-bureau-veritas.webp" alt="ISO 27001 Bureau Veritas Certification" loading="lazy">',
        'Sistema de gestión de seguridad de la información certificado bajo la norma ISO/IEC 27001 por Bureau Veritas.'),
])

add('nosotros.html', 'Nosotros | SIO',
    'Soluciones Integrales de Oficina S.A.S: más de 30 años de experiencia en soluciones TIC, con procesos evaluados bajo CMMI nivel 3, ISO/IEC 27001 y respaldo de Oracle.',
    'nosotros',
    hero(dict(
        crumbs=[('Inicio', 'index.html'), ('Nosotros', '')],
        pill='Nosotros',
        h1='Más de 30 años construyendo <span class="hl-y">confianza</span> en TI',
        lead='Soluciones Integrales de Oficina S.A.S es una organización colombiana, fundada en 1992, que brinda soluciones de valor agregado soportadas en las tecnologías de la información y las comunicaciones.',
        ctas=[btn('Hablar con un asesor', 'contacto.html', 'yellow')]))
    + section(split(
        'Quiénes somos', 'Soluciones de valor agregado para la misión de tu organización',
        ['Cubrimos procesos de desarrollo, implementación, soporte, actualización, mantenimiento y operación de soluciones informáticas misionales dentro de las organizaciones.',
         'También ofrecemos servicios de outsourcing en captura, procesamiento y administración de la información, basados en las mejores prácticas.'],
        ['Fundada en 1992 y con sede en Cali, Colombia', 'Evaluada bajo el modelo CMMI nivel III y IT Mark',
         'Procesos caracterizados y descritos en estándares, procedimientos, herramientas y métodos'],
        '<div class="stats-card" style="grid-template-columns:1fr 1fr"><div class="stat"><div class="stat-n"><span data-count="30">0</span><i>+</i></div><b>años de experiencia</b></div>'
        '<div class="stat"><div class="stat-n"><span data-count="1992">0</span></div><b>año de fundación</b></div>'
        '<div class="stat"><div class="stat-n"><i class="pre">Nivel</i><span data-count="3">0</span></div><b>CMMI-SVC</b></div>'
        '<div class="stat"><div class="stat-n"><span data-count="10">0</span><i>años</i></div><b>de conservación documental</b></div></div>'))
    + section(
        '<div class="mv-big" data-reveal>'
        '<div class="mv-card dark"><span class="mono" style="color:var(--yellow)">Misión</span><h3>Generar valor a partir de la información</h3>'
        '<p>Gestionar o apoyar la información estratégica o los procesos de nuestros clientes, generando valor mediante el talento, la innovación, el conocimiento, la integración de tecnologías y la aplicación efectiva de las TI.</p></div>'
        '<div class="mv-card"><span class="mono" style="color:var(--blue)">Visión 2030</span><h3>La mejor opción para integrar tecnología</h3>'
        '<p>Para el año 2030, ser reconocidos en Colombia como la mejor opción para integrar, implementar y operar soluciones tecnológicas que optimicen los procesos de nuestros clientes, destacándonos por la alta experticia, el compromiso, la innovación, la mejor tecnología y equipos de alto desempeño.</p></div>'
        '</div>', 'alt tight')
    + section(
        sec_head('Calidad', 'Nuestra política y objetivos',
                 'Prestamos servicios y soluciones de calidad, basados en el mejoramiento continuo, la flexibilidad y la confiabilidad, apoyando el desarrollo de nuestros colaboradores y la rentabilidad de la organización.')
        + feats([
            ('trending-up', 'Competitividad', 'Brindar soluciones de TI que mejoren la competitividad de nuestros clientes.'),
            ('users', 'Clima organizacional', 'Construir un clima organizacional que satisfaga las necesidades de nuestros colaboradores.'),
            ('graduation', 'Formación continua', 'Mantener la organización actualizada mediante la capacitación permanente.'),
            ('wallet', 'Viabilidad financiera', 'Lograr la viabilidad financiera de la organización.'),
        ], cols=4))
    + section(
        sec_head('Respaldo', 'Tecnología que <span class="hl">respalda</span> tu operación',
                 'Integración, infraestructura, cumplimiento y seguridad al nivel que exige el sector salud.')
        + f'<div class="tech-grid">{TECH}</div>', 'alt')
    + '''<section class="about" style="margin-block:clamp(12px,2vw,28px)"><div class="panel-dark"><div class="panel-glow alt" aria-hidden="true"></div>
        <div class="container about-grid">
          <div class="about-copy">
            <span class="pill pill-dark" data-reveal>Certificaciones y respaldo</span>
            <h2 data-reveal style="--d:.06s">Procesos <span class="hl-y">certificados</span> y respaldo de clase mundial</h2>
            <p data-reveal style="--d:.12s">Evaluados bajo el modelo CMMI nivel III e IT Mark, con un sistema de gestión de seguridad de la información certificado y la membresía de Oracle Partner Network.</p>
            <div class="doc-links" data-reveal style="--d:.18s">
              <a class="doc-link" href="https://sio.com.co/wp-content/uploads/2025/10/PO-SI-01-POLITICA-Y-OBJETIVOS-DEL-SGSI-3-1-2.pdf" target="_blank" rel="noopener"><span class="f-ico">''' + ic('lock') + '''</span><span><b>Sistema de gestión de seguridad de la información</b><small>Política y objetivos del SGSI (PDF)</small></span>''' + ic('arrow-up-right') + '''</a>
              <a class="doc-link" href="https://sio.com.co/wp-content/uploads/2025/10/SOLUCIONES_INTEGRALES_DE_OFICINA_27K_V2-1.pdf" target="_blank" rel="noopener"><span class="f-ico">''' + ic('award') + '''</span><span><b>Certificado de calidad</b><small>ISO/IEC 27001 (PDF)</small></span>''' + ic('arrow-up-right') + '''</a>
            </div>
          </div>
          <div data-reveal style="--d:.1s"><div class="cert-shot"><img src="assets/img/certificaciones.svg" alt="Certificaciones de SIO: CMMI, ISO/IEC 27001 e IT Mark, Oracle Partner Network"></div></div>
        </div></div></section>'''
    + cta_band('Trabajemos juntos', 'Conversemos sobre los retos de tu organización y cómo SIO puede ayudarte.'))

# ---------- SOPORTE
HORARIO = '8:00 a. m. – 12:00 m. y 2:00 – 5:30 p. m.'

# (monograma, nombre, etiqueta, color, con ticket electrónico)
SOPORTE_SW = [
    ('RIPS', 'Saman RIPS', 'RIPS · Resolución 2275', '#17998A', True),
    ('SQ', 'Health SQ', 'Calidad en salud · SOGC', '#0F4C7A', True),
    ('HC', 'SAMAN HC', 'Familia SAMAN', '#7B3A8F', True),
    ('HCM', 'SAMAN HCM', 'Familia SAMAN', '#EB5757', True),
    ('FCA', 'SAMAN FCA', 'Familia SAMAN', '#F59E1B', True),
    ('SOFT', 'Saman Soft', 'Documentos electrónicos · DIAN', '#63C3CC', False),
]


def _sp_card(mono, name, tag, color, ready, delay):
    if ready:
        status = '<span class="sp-status"><i></i>Disponible</span>'
        text = f'Soporte funcional y técnico para los clientes de {name}. Registra tu solicitud en el ticket electrónico de SIO.'
        foot = btn('Abrir ticket', SUPPORT, 'dark', ext=True, size='')
        cls = ''
    else:
        status = '<span class="sp-status is-soon"><i></i>Próximamente</span>'
        text = f'Estamos habilitando el aplicativo de soporte para los clientes de {name}. Mientras tanto, contáctanos y te atendemos.'
        foot = btn('Contactar a SIO', 'contacto.html', 'ghost', size='')
        cls = ' is-pending'
    return (f'<article class="sp-card{cls}" style="--c:{color};--d:{delay:.2f}s" data-reveal>'
            f'<div class="sp-top"><span class="sp-mono">{mono}</span>{status}</div>'
            f'<span class="sp-tag">{tag}</span><h3>{name}</h3><p>{text}</p><div class="sp-foot">{foot}</div></article>')


PORTAL = ('<div class="sp-portal" data-reveal style="--d:.1s">'
          f'<div class="spp-head"><span class="f-ico">{ic("ticket")}</span><div><span class="mono">Ticket electrónico</span><b>The Bug Genie</b></div></div>'
          '<p>Registra tus solicitudes de soporte funcional y técnico para estas soluciones:</p>'
          '<ul class="spp-chips"><li>Saman RIPS</li><li>Health SQ</li><li>SAMAN HC</li><li>SAMAN HCM</li><li>SAMAN FCA</li></ul>'
          f'<div class="spp-hours">{ic("clock")}<span>{HORARIO}</span></div>'
          + btn('Ingresar al ticket electrónico', SUPPORT, 'yellow', ext=True) + '</div>')

add('soporte.html', 'Soporte | SIO',
    'Soporte funcional y técnico para los clientes de SIO: ticket electrónico The Bug Genie para Saman RIPS, Health SQ, SAMAN HC, SAMAN HCM y SAMAN FCA. Saman Soft, próximamente.',
    'soporte',
    hero(dict(
        crumbs=[('Inicio', 'index.html'), ('Soporte', '')],
        pill='Soporte',
        h1='Soporte cercano para <span class="hl-y">cada solución</span>',
        lead='Los clientes de SIO cuentan con un ticket electrónico para registrar sus solicitudes de soporte funcional y técnico. Encuentra aquí el canal de cada software.',
        ctas=[btn('Ir al ticket electrónico', SUPPORT, 'yellow', ext=True), btn('Ver soporte por solución', '#software', 'light', arrow=False)],
        visual=PORTAL))
    + '<section class="section" id="software"><div class="container">'
    + sec_head('Soporte por solución', 'El canal de soporte de cada software',
               'Elige tu solución y abre una solicitud. Todas las soluciones con ticket electrónico comparten el mismo portal.')
    + '<div class="sp-grid">' + ''.join(_sp_card(*sw, i * .06) for i, sw in enumerate(SOPORTE_SW)) + '</div></div></section>'
    + timeline('Cómo funciona', 'Abre tu ticket en tres pasos',
               'Un proceso sencillo para que nuestro equipo atienda tu solicitud.',
               [('log-in', 'Ingresa al ticket electrónico', 'Entra a The Bug Genie desde cualquiera de los botones de esta página.'),
                ('lock', 'Inicia sesión', 'Accede con tu usuario y contraseña.'),
                ('pen', 'Registra tu solicitud', 'Describe lo que necesitas y nuestro equipo de soporte funcional y técnico la atenderá.')],
               cta=btn('Ir al ticket electrónico', SUPPORT, 'dark', ext=True))
    + section(
        '<div class="sp-contact"><div class="split-copy" data-reveal><span class="pill">Contacto</span>'
        '<h2>Otros canales para encontrarnos</h2>'
        '<p>Si necesitas ayuda con otro tema o quieres conocer una solución de SIO, aquí nos encuentras.</p>'
        + btn('Hablar con un asesor', 'contacto.html', 'dark') + '</div>'
        '<div class="info-grid" data-reveal style="--d:.1s">'
        f'<a class="info-card" href="tel:+573006770106"><span class="f-ico">{ic("phone")}</span><div><b>Teléfono</b><span>+57 300 677 0106</span></div></a>'
        f'<a class="info-card" href="mailto:mercadeo@sio.com.co"><span class="f-ico">{ic("mail")}</span><div><b>Correo electrónico</b><span>mercadeo@sio.com.co</span></div></a>'
        f'<div class="info-card"><span class="f-ico">{ic("clock")}</span><div><b>Horario de soporte</b><span>{HORARIO}</span></div></div>'
        f'<a class="info-card" href="https://www.google.com/maps/search/?api=1&query=Centro+Empresarial+Versalles+Calle+22+Norte+%233N-15+Cali" target="_blank" rel="noopener"><span class="f-ico">{ic("map-pin")}</span>'
        '<div><b>Dirección</b><span>Calle 22 Norte # 3N&nbsp;–&nbsp;15 · Piso&nbsp;4</span><small>Edificio Centro Empresarial Versalles · San Vicente, Cali</small></div></a>'
        '</div></div>', 'alt')
    + cta_band('¿Aún no eres cliente de SIO?', 'Cuéntanos tu operación y te mostramos la solución que mejor se ajusta a tu institución.'))

# ---------- CONTACTO
FORM = '''<form class="form-card" data-form novalidate>
          <h3>Solicitar información o demo</h3>
          <div class="field-row">
            <label class="field"><span>Nombre</span><input type="text" id="f-nombre" name="nombre" autocomplete="name" placeholder="Tu nombre" required></label>
            <label class="field"><span>Institución</span><input type="text" id="f-institucion" name="institucion" autocomplete="organization" placeholder="Nombre de tu institución" required></label>
          </div>
          <div class="field-row">
            <label class="field"><span>Correo</span><input type="email" id="f-correo" name="correo" autocomplete="email" placeholder="correo@institucion.com" required></label>
            <label class="field"><span>Teléfono</span><input type="tel" id="f-telefono" name="telefono" autocomplete="tel" placeholder="+57"></label>
          </div>
          <label class="field"><span>Me interesa</span>
            <select id="f-interes" name="interes">
              <option>SAMAN SOLUTION · Gestión hospitalaria</option>
              <option>Saman Soft · Facturación y nómina electrónica</option>
              <option>Health SQ · Calidad en salud</option>
              <option>Saman RIPS</option>
              <option>Gestión documental</option>
              <option>Gestión de información</option>
              <option>Suministros tecnológicos</option>
              <option>Servicios públicos</option>
              <option>Gobierno de datos</option>
              <option>Centro de negocios</option>
            </select>
          </label>
          <label class="field"><span>Mensaje</span><textarea id="f-mensaje" name="mensaje" rows="4" placeholder="Cuéntanos brevemente qué necesitas"></textarea></label>
          <button class="btn btn-yellow btn-lg btn-block" type="submit">Solicitar demo ''' + ic('arrow-right') + '''</button>
          <p class="form-note">Al enviar aceptas ser contactado por un asesor de SIO.</p>
          <div class="form-ok" role="status" hidden><span>''' + ic('check') + '''</span><b>¡Gracias!</b><p>Recibimos tu solicitud. Un asesor te contactará pronto.</p></div>
        </form>'''

add('contacto.html', 'Contacto | SIO',
    'Solicita información o una demo. Edificio Centro Empresarial Versalles, Calle 22 Norte # 3N-15, piso 4, barrio San Vicente, Cali. Teléfono +57 300 677 0106, WhatsApp +57 318 506 7331, mercadeo@sio.com.co.',
    'contacto',
    hero(dict(
        crumbs=[('Inicio', 'index.html'), ('Contacto', '')],
        pill='Contacto',
        h1='Hablemos de la operación de tu <span class="hl-y">institución</span>',
        lead='Cuéntanos qué necesitas. Un asesor de SIO te contactará para resolver tus dudas y programar una demostración sin costo.'))
    + section(
        '<div class="contact-layout"><div data-reveal>' + FORM + '</div>'
        '<div class="info-stack" data-reveal style="--d:.1s">'
        f'<a class="info-card" href="{WA}" target="_blank" rel="noopener"><span class="f-ico">{ic("message")}</span><div><b>Asesoría gratuita por WhatsApp</b><span>+57 318 506 7331</span></div></a>'
        f'<a class="info-card" href="tel:+573006770106"><span class="f-ico">{ic("phone")}</span><div><b>Teléfono</b><span>+57 300 677 0106</span></div></a>'
        f'<a class="info-card" href="mailto:mercadeo@sio.com.co"><span class="f-ico">{ic("mail")}</span><div><b>Correo electrónico</b><span>mercadeo@sio.com.co</span></div></a>'
        f'<a class="info-card" href="https://www.google.com/maps/search/?api=1&query=Centro+Empresarial+Versalles+Calle+22+Norte+%233N-15+Cali" target="_blank" rel="noopener"><span class="f-ico">{ic("map-pin")}</span><div><b>Dirección</b><span>Edificio Centro Empresarial Versalles</span><small>Calle 22 Norte # 3N&nbsp;–&nbsp;15 · Piso&nbsp;4 · Barrio San Vicente, Cali</small></div></a>'
        f'<a class="info-card dark" href="{SUPPORT}" target="_blank" rel="noopener"><span class="f-ico">{ic("life-buoy")}</span><div><b>¿Ya eres cliente? Soporte {ic("arrow-up-right")}</b><span>Abre un ticket en el sistema electrónico de SIO.</span><small>8:00 a. m. – 12:00 m. y 2:00 – 5:30 p. m.</small></div></a>'
        '</div></div>'))

# ------------------------------------------------------------------ ensamblado
SHELL = '''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="theme-color" content="#00102E">
<link rel="icon" type="image/png" sizes="32x32" href="assets/img/favicon-32.png">
<link rel="icon" type="image/png" sizes="192x192" href="assets/img/favicon-192.png">
<link rel="shortcut icon" href="assets/img/favicon.ico">
<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@500&family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/styles.css">
<script>document.documentElement.classList.add('js')</script>
</head>
<body class="{body_class}">

{sprite}
{topbar}
{header}
<main id="main">
{content}
</main>

{footer}
<script src="assets/js/main.js" defer></script>
</body>
</html>
'''


def mark_nav(html, nav):
    html = html.replace(f'class="mega-trigger" data-nav="{nav}"', f'class="mega-trigger is-active" data-nav="{nav}"')
    html = html.replace(f'<summary data-nav="{nav}"', f'<summary class="is-active" data-nav="{nav}"')
    html = re.sub(rf'<a href="([^"]+)" data-nav="{nav}">', rf'<a href="\1" data-nav="{nav}" class="is-active" aria-current="page">', html)
    if nav == 'soporte':
        html = html.replace('class="link-support" href="soporte.html" data-nav="soporte"',
                            'class="link-support is-active" href="soporte.html" data-nav="soporte" aria-current="page"')
        html = html.replace('href="soporte.html" data-nav="soporte" class="d-support"',
                            'href="soporte.html" data-nav="soporte" class="d-support is-active" aria-current="page"')
    return html


def render(name, page, sprite, topbar, header, footer):
    html = SHELL.format(
        title=page['title'], description=page['description'], body_class='page-' + name.replace('.html', ''),
        sprite=sprite, topbar=topbar, header=mark_nav(header, page['nav']), content=page['content'], footer=footer)
    return html


def main():
    sprite = read('src', 'partials', 'sprite.html')
    sprite = sprite.replace('</defs>', EXTRA_ICONS + '  </defs>')
    topbar = read('src', 'partials', 'topbar.html')
    header = read('src', 'partials', 'header.html')
    footer = read('src', 'partials', 'footer.html')

    # Home
    m = re.match(r'<!--meta (.*?) -->\n', HOME, re.S)
    meta = json.loads(m.group(1))
    home = dict(title=meta['title'], description=meta['description'], nav=meta['nav'], content=HOME[m.end():])
    PAGES['index.html'] = home

    for name, page in PAGES.items():
        write(name, render(name, page, sprite, topbar, header, footer))
        print('ok', name)


if __name__ == '__main__':
    main()
