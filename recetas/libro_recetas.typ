#set page(
  paper: "a4",
  margin: (top: 2cm, bottom: 2cm, left: 2.2cm, right: 2.2cm),
  header: context {
    if here().page() > 1 [
      #text(size: 8pt, fill: rgb("#718096"))[
        *Recetario Deportivo Periodizado* · Gonzalo Molina · Trail Running & Descenso de Peso (81 kg #sym.arrow 75 kg)
        #h(1fr) Desafío Wayra 35k
      ]
      #line(length: 100%, stroke: 0.5pt + rgb("#e2e8f0"))
    ]
  },
  footer: context {
    text(size: 8pt, fill: rgb("#718096"))[
      #h(1fr) Página #here().page() de #counter(page).final().at(0)
    ]
  }
)

#set text(
  font: "Liberation Sans",
  size: 10pt,
  fill: rgb("#2d3748"),
  lang: "es"
)

#set par(justify: true, leading: 0.65em)

// ==================== TÍTULO PRINCIPAL ====================
#align(center)[
  #text(size: 22pt, weight: "bold", fill: rgb("#1a365d"))[
    🥗 Recetario Deportivo Periodizado
  ]
  #v(2pt)
  #text(size: 13pt, weight: "medium", fill: rgb("#2b6cb0"))[
    Cocina Funcional para Trail Running & Pérdida de Grasa (81 kg #sym.arrow 75 kg)
  ]
  #v(4pt)
  #text(size: 9.5pt, fill: rgb("#4a5568"))[
    *Atleta:* Gonzalo Molina · *Objetivo:* Desafío Wayra 35k (+2200m D+) & El Paso Austral 70k
  ]
]

#v(8pt)
#line(length: 100%, stroke: 1.5pt + rgb("#3182ce"))
#v(10pt)

// ==================== CRITERIO DE PERIODIZACIÓN ====================
#rect(
  width: 100%,
  fill: rgb("#ebf8ff"),
  radius: 6pt,
  inset: (x: 12pt, y: 10pt),
  stroke: 1pt + rgb("#bee3f8")
)[
  #text(weight: "bold", fill: rgb("#2c5282"), size: 10.5pt)[📖 Criterio Nutricional y Categorías del Recetario:]
  #v(2pt)
  Este recetario organiza las preparaciones según las *demandas metabólicas del día*:
  - *1. Post-Entrenamiento & Cargas:* Ricas en proteínas de alta absorción y carbohidratos complejos para reponer glucógeno post-series o cenar la noche previa a un fondo.
  - *2. Pre-Entrenamiento:* Digestión ultrarrápida, ricas en carbohidratos simples y muy bajas en grasa/fibra para rendir sin pesadez estomacal en las cuestas de la tarde.
  - *3. Déficit & Días Light (Low Carb / High Protein):* Para días de descanso o fuerza de tren superior. Máximo volumen de vegetales y proteínas magras para quemar grasa con saciedad.
  - *4. Desayunos y Meriendas Funcionales:* Rápidos y equilibrados para la rutina de oficina, compatibles con el mate amargo matutino.
  - *5. Intra-Fondo (Combustible de Montaña):* Estrategias de 40–50g HC/h para tiradas largas de fin de semana.
]

#v(14pt)

// ==================== SECCIÓN 1: POST-ENTRENO Y CARGAS ====================
#text(size: 15pt, weight: "bold", fill: rgb("#c53030"))[
  1. Post-Entrenamiento & Cargas de Glucógeno
]
#text(size: 9pt, style: "italic", fill: rgb("#742a2a"))[
  Platos completos para reponer reservas musculares tras esfuerzos intensos o como cena previa al fondo de fin de semana.
]
#v(6pt)

#include "post_entreno/noquis_ricotta_bolonesa_light.typ"

#pagebreak()

// ==================== SECCIÓN 2: PRE-ENTRENAMIENTO ====================
#text(size: 15pt, weight: "bold", fill: rgb("#d69e2e"))[
  2. Pre-Entrenamiento (Combustible Inmediato)
]
#text(size: 9pt, style: "italic", fill: rgb("#744210"))[
  Snacks energéticos 1h30m a 2h antes del running de la tarde (Bandurrias). Carbohidrato limpio sin grasas lentas.
]
#v(6pt)

#include "pre_entreno/tostadas_batata_prerunning.typ"

#v(16pt)

// ==================== SECCIÓN 3: DÉFICIT & DÍAS LIGHT ====================
#text(size: 15pt, weight: "bold", fill: rgb("#2f855a"))[
  3. Déficit Calórico & Días Light (Low Carb / High Protein)
]
#text(size: 9pt, style: "italic", fill: rgb("#22543d"))[
  Preparaciones hiper-saciantes para los días de descanso y fuerza (Martes, Jueves, Domingos). Aquí es donde se pierden los 6 kg.
]
#v(6pt)

#include "deficit_light/ensalada_atun_huevo_emulsionada.typ"
