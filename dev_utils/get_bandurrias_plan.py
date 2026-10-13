#!/usr/bin/env python3
"""
Sincronizador de Planificación Semanal de Bandurrias Trail Running
Descarga los entrenamientos propuestos directamente desde Supabase.
"""

import os
import json
import requests

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(SCRIPT_DIR, "..", "bandurrias_config.json")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..")


def load_config():
    if not os.path.exists(CONFIG_PATH):
        raise FileNotFoundError(
            f"No se encontró el archivo de configuración en: {CONFIG_PATH}"
        )
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_config(config):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


import time
import base64


def is_token_expired(token: str, margin_seconds: int = 300) -> bool:
    """Verifica si el JWT ha expirado o está cerca de expirar."""
    try:
        parts = token.split(".")
        if len(parts) < 2:
            return True
        payload_b64 = parts[1]
        # Padding base64
        payload_b64 += "=" * ((4 - len(payload_b64) % 4) % 4)
        payload = json.loads(base64.urlsafe_b64decode(payload_b64).decode("utf-8"))
        exp = payload.get("exp", 0)
        return (exp - time.time()) < margin_seconds
    except Exception:
        return True


def refresh_access_token(config):
    """Refresca el access_token usando el refresh_token si ha expirado, y guarda el nuevo estado."""
    current_token = config.get("access_token", "")
    if current_token and not is_token_expired(current_token):
        return current_token

    url = f"{config['supabase_url']}/auth/v1/token?grant_type=refresh_token"
    headers = {"apikey": config["apikey"], "Content-Type": "application/json"}
    payload = {"refresh_token": config["refresh_token"]}

    resp = requests.post(url, headers=headers, json=payload)
    if resp.status_code != 200:
        print(f"⚠️ Error al refrescar token ({resp.status_code}): {resp.text}")
        return config.get("access_token")

    data = resp.json()
    config["access_token"] = data["access_token"]
    if "refresh_token" in data:
        config["refresh_token"] = data["refresh_token"]
    save_config(config)
    return config["access_token"]


def get_headers(config):
    token = refresh_access_token(config)
    return {
        "apikey": config["apikey"],
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }


def fetch_weeks(config, limit=5):
    headers = get_headers(config)
    url = f"{config['supabase_url']}/rest/v1/weeks?select=*&order=created_at.desc&limit={limit}"
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        raise RuntimeError(
            f"Error consultando semanas ({resp.status_code}): {resp.text}"
        )
    return resp.json()


def format_group_session(session):
    badge = session.get("badge", {})
    badge_label = badge.get("label", "Entrenamiento")
    badge_type = badge.get("type", "general")
    days = " · ".join([d.upper() for d in session.get("days", [])])

    html = []
    html.append('<div class="session-card">')
    html.append('  <div class="session-header">')
    html.append(f'    <span class="session-day-badge">📅 {days}</span>')
    html.append(f'    <span class="session-type-badge type-{badge_type}">{badge_label}</span>')
    html.append('  </div>')

    if session.get("rest"):
        rest_body = session.get("restBody", {})
        title = rest_body.get("title", "Descanso")
        html.append(f'  <h4 style="margin: 0.5rem 0;">🛌 {title}</h4>')
        for line in rest_body.get("lines", []):
            if line.strip():
                html.append(f'  <p style="margin: 0.25rem 0; color: var(--secondary);">{line}</p>')
        html.append('</div>\n')
        return "\n".join(html)

    # Info grid: Meetpoint & Turnos
    info_items = []
    mp = session.get("meetpoint", {})
    if mp.get("text"):
        url = mp.get("url", "")
        link = f'<a href="{url}" target="_blank" rel="noopener">📍 {mp["text"]}</a>' if url else f'📍 {mp["text"]}'
        info_items.append(f'<div class="session-info-item">{link}</div>')

    turnos = session.get("turnos", [])
    if turnos:
        turnos_str = " &nbsp;|&nbsp; ".join([f"<strong>{t.get('day', '').upper()}</strong>: {t.get('text', '')}" for t in turnos])
        info_items.append(f'<div class="session-info-item">⏰ {turnos_str}</div>')

    if info_items:
        html.append('<div class="session-info-grid">')
        html.extend([item for item in info_items])
        html.append('</div>')

    # Objective
    if session.get("objective"):
        html.append(f'<div class="session-objective"><strong>🎯 Objetivo:</strong> {session["objective"]}</div>')

    # Structure
    acts = session.get("activities", [])
    clean_acts = [a.strip() for a in acts if a.strip()]
    if clean_acts:
        html.append('<div class="session-structure">')
        html.append('<strong>Estructura de la sesión:</strong>')
        html.append('<ol>')
        for a in clean_acts:
            html.append(f'<li>{a}</li>')
        html.append('</ol>')
        html.append('</div>')

    # Levels (Highlighting AVANZADO)
    niveles = session.get("niveles", [])
    if niveles:
        html.append('<div class="levels-container">')
        for n in niveles:
            tipo = n.get("type", "").upper()
            text = n.get("text", "")
            if tipo == "AVZ":
                html.append('<div class="level-card level-avanzado">')
                html.append('<div class="level-card-header">')
                html.append('<span>🔴 Nivel Avanzado</span>')
                html.append('<span class="level-target-badge">🎯 TU TAREA</span>')
                html.append('</div>')
                html.append(f'<div style="font-weight: 500; line-height: 1.45;">{text}</div>')
                html.append('</div>')
            elif tipo == "MED":
                html.append('<div class="level-card level-other">')
                html.append('<div class="level-card-header" style="color: #d97706;">🟡 Nivel Medio</div>')
                html.append(f'<div>{text}</div>')
                html.append('</div>')
            elif tipo == "INI":
                html.append('<div class="level-card level-other">')
                html.append('<div class="level-card-header" style="color: #059669;">🟢 Nivel Inicial</div>')
                html.append(f'<div>{text}</div>')
                html.append('</div>')
            else:
                html.append(f'<div class="level-card level-other"><div class="level-card-header">{tipo}</div><div>{text}</div></div>')
        html.append('</div>')

    # Note / Material
    note = session.get("note") or {}
    if note and isinstance(note, dict) and note.get("text"):
        html.append('<div class="session-note">')
        html.append(f'<strong>⚠️ {note.get("strong", "Importante:")}</strong> {note.get("text").replace(chr(10), "<br>")}')
        html.append('</div>')

    html.append('</div>\n')
    return "\n".join(html)


def format_distance_session(day_key, sessions):
    day_names = {
        "lun": "Lunes",
        "mar": "Martes",
        "mie": "Miércoles",
        "jue": "Jueves",
        "vie": "Viernes",
        "sab": "Sábado",
        "dom": "Domingo",
    }
    nombre_dia = day_names.get(day_key, day_key.upper())
    md = [f"### 📅 {nombre_dia}"]

    for s in sessions:
        tipo = s.get("type", "").upper()
        title = s.get("title") or tipo
        dist = s.get("distance", "")
        dur = s.get("duration", "")
        elev = s.get("elevation", "")
        obj = s.get("objective", "")
        rpe = s.get("rpe", "")
        hr = s.get("hr", "")

        detalles = []
        if dist:
            detalles.append(f"Distancia: {dist}")
        if dur:
            detalles.append(f"Tiempo: {dur}")
        if elev:
            detalles.append(f"Desnivel: {elev}")
        if rpe:
            detalles.append(f"RPE: {rpe}")
        if hr:
            detalles.append(f"FC: {hr}")

        md.append(f"#### {title}")
        if detalles:
            md.append(f"- **Objetivo:** {' | '.join(detalles)}")
        if obj:
            md.append(f"- **Pauta:** {obj}")

        struct = s.get("structure", [])
        clean_struct = [st.strip() for st in struct if st.strip()]
        if clean_struct:
            md.append("**Estructura:**")
            for st in clean_struct:
                md.append(f"- {st}")
        md.append("")

    return "\n".join(md)


def save_week_plan(week_data, is_latest=True):
    plan = week_data.get("plan", {})
    week_id = week_data.get("id")
    week_num = plan.get("weekNumber", "")
    dates = plan.get("dates", week_id)
    period = plan.get("period", "")
    kind = week_data.get("kind", "grupo")

    BLOG_SEMANAS_DIR = os.path.join(SCRIPT_DIR, "..", "blog", "content", "semanas")
    os.makedirs(BLOG_SEMANAS_DIR, exist_ok=True)

    clean_id = week_id.replace(":", "_")
    blog_file = os.path.join(BLOG_SEMANAS_DIR, f"{clean_id}.md")
    root_file = os.path.join(OUTPUT_DIR, f"plan_bandurrias_{clean_id}.md")

    # Fecha para frontmatter
    date_part = week_id if ":" not in week_id else week_id.split(":")[-1]

    lines = [
        "---",
        f'title: "Semana {week_num}: {dates}"',
        f'date: {date_part}',
        'categories: ["Planificación Semanal"]',
        f'tags: ["Bandurrias", "Semana {week_num}", "Avanzado"]',
        f'weight: {1 if is_latest else 10}',
        "---",
        "",
        '<div class="week-summary-banner">',
        '  <div>',
        f'    <h2 class="week-summary-title">🏔️ Semana {week_num} — {dates}</h2>',
        f'    <div style="font-size: 0.9rem; color: var(--secondary); margin-top: 0.25rem;">{period}</div>' if period else "",
        '  </div>',
        '  <div class="week-summary-meta">',
        '    <span class="week-pill highlight">🎯 Tu Tarea: Avanzado</span>',
        f'    <span class="week-pill">👥 {"Grupo Presencial" if kind != "distance" else "Distancia"}</span>',
        '  </div>',
        '</div>',
        "",
        '<div class="week-container">',
        "",
    ]

    # Si es plan de grupo (las sesiones están en 'activities') o plan individual (en 'sessions')
    raw_sessions = plan.get("activities") or plan.get("sessions")
    if isinstance(raw_sessions, list):
        for s in raw_sessions:
            lines.append(format_group_session(s))
    elif isinstance(raw_sessions, dict):
        # Es plan individual por días (lun, mar, mie...)
        for d in ["lun", "mar", "mie", "jue", "vie", "sab", "dom"]:
            if d in raw_sessions and raw_sessions[d]:
                lines.append(format_distance_session(d, raw_sessions[d]))

    lines.append('</div>')

    content = "\n".join(lines)
    with open(blog_file, "w", encoding="utf-8") as f:
        f.write(content)

    with open(root_file, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ Plan guardado en blog: {blog_file}")
    return blog_file


def main():
    print("🦅 Conectando con Bandurrias Trail Running (Supabase)...")
    config = load_config()
    weeks = fetch_weeks(config, limit=6)

    print(f"📥 Se recuperaron {len(weeks)} semanas.")

    # Guardar las semanas de grupo en el blog
    group_weeks = [
        w for w in weeks if w.get("kind") != "distance" or ":" not in w.get("id", "")
    ]
    if group_weeks:
        for idx, w in enumerate(group_weeks):
            is_latest = (idx == 0)
            print(f"👉 Procesando {'semana actual' if is_latest else 'semana anterior'}: {w.get('id')}")
            save_week_plan(w, is_latest=is_latest)
    else:
        save_week_plan(weeks[0], is_latest=True)


if __name__ == "__main__":
    main()
