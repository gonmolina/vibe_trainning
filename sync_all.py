#!/usr/bin/env python3
"""
sync_all.py - Sincronizador Maestro para Vibe Training
1. Sincroniza entrenamientos desde Strava (get_trainnings.py).
2. Sincroniza planificaciones desde Bandurrias / Supabase (get_bandurrias_plan.py).
3. Cruza los días de la semana con las actividades ejecutadas en Strava y las vincula.
4. Compila el sitio con Hugo y lo deja listo para el deploy.
"""

import os
import sys
import glob
import json
import re
import subprocess
from datetime import datetime, timedelta

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = SCRIPT_DIR
BLOG_DIR = os.path.join(BASE_DIR, "blog")
SEMANAS_DIR = os.path.join(BLOG_DIR, "content", "semanas")
ENTRENAMIENTOS_DIR = os.path.join(BLOG_DIR, "content", "entrenamientos")


def run_cmd(cmd, desc):
    print(f"\n🚀 {desc}...")
    res = subprocess.run(cmd, shell=True, cwd=BASE_DIR)
    if res.returncode != 0:
        print(f"⚠️ Aviso: '{cmd}' terminó con código {res.returncode}")
    else:
        print(f"✅ {desc} completado.")


def load_strava_activities():
    activities_by_date = {}
    for p in glob.glob(os.path.join(ENTRENAMIENTOS_DIR, "*", "activity.json")):
        try:
            with open(p, "r", encoding="utf-8") as f:
                d = json.load(f)
            dt_str = d.get("start_date_local", "")
            if not dt_str:
                continue
            date_key = dt_str[:10]  # YYYY-MM-DD
            dir_name = os.path.basename(os.path.dirname(p))

            act_summary = {
                "id": d.get("id"),
                "name": d.get("name"),
                "type": d.get("sport_type") or d.get("type"),
                "distance_km": round((d.get("distance") or 0) / 1000.0, 2),
                "elevation_m": round(d.get("total_elevation_gain") or 0, 1),
                "moving_time_min": round((d.get("moving_time") or 0) / 60.0, 1),
                "hr_avg": d.get("average_heartrate"),
                "hr_max": d.get("max_heartrate"),
                "dir_name": dir_name,
            }
            if date_key not in activities_by_date:
                activities_by_date[date_key] = []
            activities_by_date[date_key].append(act_summary)
        except Exception as e:
            print(f"Error leyendo {p}: {e}")
    return activities_by_date


def get_week_dates(start_date_str):
    """Devuelve las 7 fechas (YYYY-MM-DD) de lunes a domingo a partir del lunes de inicio."""
    start_dt = datetime.strptime(start_date_str, "%Y-%m-%d")
    dates = []
    days_map = ["lun", "mar", "mie", "jue", "vie", "sab", "dom"]
    for i in range(7):
        cur = start_dt + timedelta(days=i)
        dates.append((days_map[i], cur.strftime("%Y-%m-%d")))
    return dates


def link_activities_to_weeks():
    print("\n🔗 Cruzando planificaciones semanales con entrenamientos ejecutados...")
    acts = load_strava_activities()

    week_files = sorted(glob.glob(os.path.join(SEMANAS_DIR, "2026-*.md")))
    for w_path in week_files:
        filename = os.path.basename(w_path)
        m = re.match(r"(\d{4}-\d{2}-\d{2})\.md", filename)
        if not m:
            continue
        start_date = m.group(1)
        week_dates = get_week_dates(start_date)

        # Buscar actividades ejecutadas en esa semana
        executed_in_week = {}
        for day_code, d_str in week_dates:
            if d_str in acts:
                executed_in_week[day_code] = (d_str, acts[d_str])

        if not executed_in_week:
            continue

        with open(w_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Si ya tiene una sección de actividades ejecutadas, actualizarla; si no, agregarla al pie
        section_id = "<!-- EXECUTED_ACTIVITIES_START -->"
        if section_id in content:
            content = content.split(section_id)[0].rstrip()

        exec_md = [f"\n\n{section_id}"]
        exec_md.append("## ✅ Actividades Ejecutadas Registradas en Strava")
        exec_md.append(
            "| Fecha | Día | Actividad | Distancia | Desnivel (+D) | Tiempo | FC Media | Enlace |"
        )
        exec_md.append(
            "| :--- | :---: | :--- | :---: | :---: | :---: | :---: | :--- |"
        )

        day_names_es = {
            "lun": "Lunes",
            "mar": "Martes",
            "mie": "Miércoles",
            "jue": "Jueves",
            "vie": "Viernes",
            "sab": "Sábado",
            "dom": "Domingo",
        }

        for day_code, (d_str, day_acts) in executed_in_week.items():
            for a in day_acts:
                pace_str = ""
                if a["distance_km"] > 0:
                    dist_km = a["distance_km"]
                    t_min = a["moving_time_min"]
                    p = t_min / dist_km
                    pace_str = f" ({int(p)}:{int((p-int(p))*60):02d}/km)"
                hr_str = f"{a['hr_avg']} bpm" if a["hr_avg"] else "-"
                link_url = f"/vibe_trainning/entrenamientos/{a['dir_name']}/"
                link_md = f"[{a['name']}]({link_url})"

                elev_str = (
                    f"+{a['elevation_m']}m" if a["elevation_m"] > 0 else "-"
                )
                time_str = f"{a['moving_time_min']}m{pace_str}"

                exec_md.append(
                    f"| {d_str} | **{day_names_es.get(day_code, day_code).upper()}** | {a['name']} | {a['distance_km']} km | {elev_str} | {time_str} | {hr_str} | [Ver detalle ➔]({link_url}) |"
                )

        exec_md.append("<!-- EXECUTED_ACTIVITIES_END -->\n")
        new_content = content + "\n".join(exec_md)

        with open(w_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(
            f"   ✓ {filename}: vinculadas {sum(len(v[1]) for v in executed_in_week.values())} actividades."
        )


def main():
    print("=" * 60)
    print("🏔️  SINCRONIZADOR INTEGRAL: STRAVA + BANDURRIAS + HUGO")
    print("=" * 60)

    # 1. Strava
    run_cmd(
        "python3 dev_utils/get_trainnings.py", "Sincronizando Strava Activities"
    )

    # 2. Bandurrias
    run_cmd(
        "python3 dev_utils/get_bandurrias_plan.py",
        "Sincronizando Planes Bandurrias",
    )

    # 3. Cruzar datos
    link_activities_to_weeks()

    # 4. Compilar Hugo
    run_cmd("hugo --minify -s blog", "Compilando Blog de Hugo")

    print("\n🎉 Sincronización y cruce completados con éxito.")


if __name__ == "__main__":
    main()
