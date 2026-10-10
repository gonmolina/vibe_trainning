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


def refresh_access_token(config):
    """Refresca el access_token usando el refresh_token y guarda el nuevo estado."""
    url = f"{config['supabase_url']}/auth/v1/token?grant_type=refresh_token"
    headers = {"apikey": config["apikey"], "Content-Type": "application/json"}
    payload = {"refresh_token": config["refresh_token"]}

    resp = requests.post(url, headers=headers, json=payload)
    if resp.status_code != 200:
        print(f"⚠️ Error al refrescar token ({resp.status_code}): {resp.text}")
        return config["access_token"]

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
    days = ", ".join([d.upper() for d in session.get("days", [])])

    md = []
    if session.get("rest"):
        rest_body = session.get("restBody", {})
        title = rest_body.get("title", "Descanso")
        md.append(f"### 🛌 {days} — {title}")
        for line in rest_body.get("lines", []):
            if line.strip():
                md.append(f"- {line}")
        md.append("")
        return "\n".join(md)

    day_label = session.get("dayLabel") or badge_label
    md.append(f"### 🏃 {days} — {day_label}")

    # Meetpoint
    mp = session.get("meetpoint", {})
    if mp.get("text"):
        url = mp.get("url", "")
        if url:
            md.append(f"- **Punto de encuentro:** [{mp['text']}]({url})")
        else:
            md.append(f"- **Punto de encuentro:** {mp['text']}")

    # Turnos
    turnos = session.get("turnos", [])
    if turnos:
        turnos_str = " | ".join(
            [f"{t.get('day', '').upper()}: {t.get('text', '')}" for t in turnos]
        )
        md.append(f"- **Horarios:** {turnos_str}")

    # Objetivo
    if session.get("objective"):
        md.append(f"- **Objetivo:** {session['objective']}")

    # Actividades
    acts = session.get("activities", [])
    clean_acts = [a.strip() for a in acts if a.strip()]
    if clean_acts:
        md.append("\n**Estructura:**")
        for a in clean_acts:
            md.append(f"1. {a}")

    # Niveles
    niveles = session.get("niveles", [])
    if niveles:
        md.append("\n**Propuesta por Niveles:**")
        for n in niveles:
            tipo = n.get("type", "").upper()
            if tipo == "INI":
                label = "🟢 Inicial"
            elif tipo == "MED":
                label = "🟡 Medio"
            elif tipo == "AVZ":
                label = "🔴 Avanzado"
            else:
                label = tipo
            md.append(f"- **{label}:** {n.get('text', '')}")

    # Notas / Material
    note = session.get("note", {})
    if note.get("text"):
        md.append(
            f"\n> [!NOTE]\n> **{note.get('strong', 'Nota:')}** {note.get('text').replace(chr(10), ' ')}"
        )

    md.append("\n---\n")
    return "\n".join(md)


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


def save_week_plan(week_data):
    plan = week_data.get("plan", {})
    week_id = week_data.get("id")
    week_num = plan.get("weekNumber", "")
    dates = plan.get("dates", week_id)
    period = plan.get("period", "")
    kind = week_data.get("kind", "grupo")

    # Archivo de salida
    clean_id = week_id.replace(":", "_")
    filename = f"plan_bandurrias_{clean_id}.md"
    filepath = os.path.join(OUTPUT_DIR, filename)

    lines = [
        f"# 🏔️ Planificación Bandurrias Trail Running — Semana {week_num}",
        f"**Fechas:** {dates}  ",
        f"**Período:** {period}  " if period else "",
        f"**Tipo:** {'Grupo Presencial' if kind != 'distance' else 'Distancia / Individual'}  ",
        f"**ID:** `{week_id}`",
        "\n---",
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

    content = "\n".join(lines)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ Plan guardado en: {filepath}")
    return filepath


def main():
    print("🦅 Conectando con Bandurrias Trail Running (Supabase)...")
    config = load_config()
    weeks = fetch_weeks(config, limit=6)

    print(f"📥 Se recuperaron {len(weeks)} semanas.")

    # Guardar la más reciente de grupo
    group_weeks = [
        w for w in weeks if w.get("kind") != "distance" or ":" not in w.get("id", "")
    ]
    if group_weeks:
        latest = group_weeks[0]
        print(f"👉 Procesando semana actual del grupo: {latest.get('id')}")
        save_week_plan(latest)
    else:
        # Guardar la más reciente disponible
        save_week_plan(weeks[0])


if __name__ == "__main__":
    main()
