# 🏔️ Plan de Entrenamiento Trail Running & Ultra Trail

Sistema integral de entrenamiento, seguimiento y análisis de Trail Running asistido por IA para **Gonzalo Molina** (Bandurrias Trail Running Team · Bariloche).

---

## 🎯 Objetivos de Carrera Actuales

### 1. 🧪 Test Evaluativo Back-to-Back (Bariloche) — *Evaluación de Viabilidad Ultra*
* **Fecha:** Sábado 12 y Domingo 13 de Diciembre de 2026 (Semana 30).
* **Formato:** Bloque **Back-to-Back** (~40–44 km | +2,100–2,400 m D+ en dos días: Sábado 26–28 km + Domingo 14–16 km con fatiga acumulada). *(Reemplaza la participación en Desafío Wayra 35k).*
* **Propósito:** 
  * Evaluar durabilidad muscular y estabilidad de tobillos/cuádriceps corriendo dos días seguidos con fatiga previa.
  * Validar la estabilidad cardiovascular en Z2/Z3 en subidas largas.
  * Testear el protocolo de nutrición e hidratación (50–65 g HC/h + sales) durante 4.5–5 horas continuas.

### 2. 🦅 El Paso Austral (70 km) — *Gran Meta en Evaluación*
* **Fecha:** Mediados de Febrero de 2027.
* **Distancia:** 70 km Ultra Trail.
* **Criterio de confirmación:** Se tomará la decisión de encarar este ultra trail en función de las sensaciones, respuesta física, digestiva y recuperación tras el test Back-to-Back (12–13 de diciembre) y la progresión de volumen en enero.

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
