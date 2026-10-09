# 🏔️ Plan de Entrenamiento Trail Running & Ultra Trail

Sistema integral de entrenamiento, seguimiento y análisis de Trail Running asistido por IA para **Gonzalo Molina** (Bandurrias Trail Running Team · Bariloche).

---

## 🎯 Objetivos de Carrera Actuales

### 1. 🏁 Desafío Wayra (El Bolsón) — *Test de Estado de Forma*
* **Fecha:** Domingo 13 de Diciembre de 2026 (~9 semanas).
* **Distancia:** 35 km | **Desnivel Positivo:** +2200 m D+ (Ratio vertical: ~63 m D+/km).
* **Propósito:** 
  * Test evaluativo del estado aeróbico y respiratorio post-gripe.
  * Poner a prueba la estabilidad de tobillos y resistencia de cuádriceps en descensos técnicos.
  * Practicar de forma estricta el protocolo de nutrición e hidratación en subidas largas.

### 2. 🦅 El Paso Austral (70 km) — *Gran Meta en Evaluación*
* **Fecha:** Mediados de Febrero de 2027 (~18 semanas).
* **Distancia:** 70 km.
* **Criterio de confirmación:** Se tomará la decisión de encarar este ultra trail en función de las sensaciones, respuesta física y desempeño en Desafío Wayra (13 de diciembre) y la progresión de volumen en enero.

---

## 🏃 Metodología de Entrenamiento

* **Grupo:** Bandurrias Trail Running (Bariloche).
* **Nivel asignado:** **Avanzado**.
* **Esquema semanal:**
  * **Lunes / Martes:** Calidad (técnica, cambios de ritmo, series).
  * **Miércoles / Jueves:** Cuestas / Fuerza específica en montaña.
  * **Viernes:** Recuperación activa o descanso.
  * **Sábado:** Fondo de montaña en terreno variado / técnico.
  * **Domingo:** Descanso o movilidad.
* **Complementos individuales:** Rutinas de fuerza funcional, prevención para tobillos y pauta de nutrición/sales adaptada a alta sudoración salina.

---

## 🛠️ Herramientas y Scripts

### Sincronización con Strava
Descarga las actividades reales, tracks GPX, laps y fotos al blog:
```bash
python dev_utils/get_trainnings.py
```

### Sincronización con Bandurrias Trail Running
Descarga la planificación semanal oficial del equipo desde Supabase:
```bash
python dev_utils/get_bandurrias_plan.py
```

### Blog de Seguimiento (Hugo)
Compila y visualiza los entrenamientos y crónicas:
```bash
cd blog && hugo server
```
