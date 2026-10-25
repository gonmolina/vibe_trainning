#set page(
  paper: "a4",
  margin: (top: 2cm, bottom: 2cm, left: 2.2cm, right: 2.2cm),
  header: context {
    if here().page() > 1 [
      #text(size: 8pt, fill: rgb("#718096"))[
        *Plan Nutricional de Periodización* · Gonzalo Molina · Objetivo: 81 kg #sym.arrow 75 kg
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

// ==================== TÍTULO Y ENCABEZADO ====================
#align(center)[
  #text(size: 20pt, weight: "bold", fill: rgb("#1a365d"))[
    🏔️ Plan Nutricional de Periodización
  ]
  #v(2pt)
  #text(size: 13pt, weight: "medium", fill: rgb("#2b6cb0"))[
    Desafío Wayra (35k / +2200m D+) · Camino a El Paso Austral (70k)
  ]
  #v(4pt)
  #text(size: 9.5pt, fill: rgb("#4a5568"))[
    *Atleta:* Gonzalo Molina · *Peso Inicial:* 81.0 kg · *Meta Wayra:* 75.0–76.0 kg · *Ventana:* 7 Semanas
  ]
]

#v(8pt)
#line(length: 100%, stroke: 1.5pt + rgb("#3182ce"))
#v(6pt)

// ==================== RESUMEN EJECUTIVO ====================
#rect(
  width: 100%,
  fill: rgb("#ebf8ff"),
  radius: 6pt,
  inset: (x: 12pt, y: 10pt),
  stroke: 1pt + rgb("#bee3f8")
)[
  #text(weight: "bold", fill: rgb("#2c5282"), size: 10.5pt)[🎯 Pilares Fundamentales del Plan:]
  #v(2pt)
  - *Déficit Calórico Estructurado:* ~500–600 kcal/día de promedio para bajar ~700–800 g/semana de grasa pura sin perder masa muscular ni fuerza en las piernas.
  - *Proteína Blindada:* *~160 g diarios (~2.0 g/kg)* repartidos en 4 tomas para evitar catabolismo y mantener la saciedad.
  - *Suplementación:* *5 g de creatina diarios* innegociables (fuerza en cuestas y protección muscular).
  - *Regla del Aceite:* 1 cucharada sopera rasa por ensalada (~12–14 ml), preparada con *vinagreta emulsionada* (limón abundante + especias + agua/tomate) para mojar toda la fuente sin sumar calorías ocultas.
  - *Atún al Natural:* 1 lata entera escurrida (~120 g netos) por porción. Se complementa con 1 huevo duro si se busca mayor saciedad.
]

#v(10pt)

// ==================== DÍA TIPO A ====================
#text(size: 13pt, weight: "bold", fill: rgb("#c53030"))[
  🔴 DÍA TIPO A: Running de Tarde (Lunes, Miércoles y Sábados)
]
#text(size: 9pt, style: "italic", fill: rgb("#742a2a"))[
  *Foco:* Combustible selectivo pre-running (merienda con carbohidratos), rendimiento óptimo en montaña y recuperación nocturna.
]

#v(4pt)

#table(
  columns: (1fr, 1.3fr, 1.3fr),
  stroke: 0.5pt + rgb("#cbd5e0"),
  fill: (col, row) => if row == 0 { rgb("#fed7d7") } else if calc.even(row) { rgb("#fff5f5") } else { white },
  inset: 7pt,
  align: (col, row) => if col == 0 { left } else { left },
  
  [#text(weight: "bold")[Momento]],
  [#text(weight: "bold")[Opción 1 (Predilecta / Práctica)]],
  [#text(weight: "bold")[Opción 2 (Variante)]],

  [*08:00 Desayuno*\ (Base proteica limpia)],
  [
    - 1 batido Whey Protein (1 scoop, ~25g prot) con leche descremada o agua.
    - 1 huevo duro.
    - 1 manzana o pera entera.
    - Mates amargos durante la mañana.
  ],
  [
    - Omelette de 2 huevos enteros + 1 clara con rodajas de tomate y orégano.
    - 1 infusión o mate amargo.
    - 1 vaso de agua grande con 5g de creatina.
  ],

  [*13:00 Almuerzo*\ (Magro + fibra saciante)],
  [
    - 200g de pechuga de pollo grillé.
    - Ensalada abundante: lechuga, tomate, cebolla con *vinagreta emulsionada* (1 cda. aceite oliva + limón).
    - 1 papa chica al vapor o al horno (130g).
  ],
  [
    - 1 lata entera de atún al natural + 1 huevo duro picado.
    - Ensalada completa (tomate, lechuga, cebolla morada).
    - 3 cucharadas soperas de arroz blanco o integral (~80g cocido).
  ],

  [*16:30–17:00 Merienda*\ *(2h antes de correr: CARBS)*],
  [
    - *2 tostadas de pan blanco o salvado con dulce de batata (40–50g).*
    - 1 vaso grande de agua con pizca de sales.
    - 5g de creatina (si no se tomó antes).
  ],
  [
    - 1 plátano maduro mediano.
    - 2 tostadas de arroz o pan con 1 feta de queso magro y dulce de membrillo o batata.
    - Vaso de agua o infusión ligera.
  ],

  [*19:00 Running Bandurrias*\ (Cuestas / Ritmo)],
  [
    - Hidratación: 500–750 ml de agua con electrolitos.
    - Si la sesión supera 1h15m intensa: 1 gel a los 45 min.
  ],
  [
    - Agua con sales isotónicas.
    - En tiradas largas de sábado: pastilla de cafeína + geles cada 40–45 min.
  ],

  [*21:30 Cena*\ (Reparación muscular)],
  [
    - 200g de bife de carne vacuna magra (lomo, nalga o cuadril).
    - Ensalada verde grande + zapallitos o calabaza al vapor.
    - 1 naranja o kiwi.
  ],
  [
    - 200g de pollo al horno o churrasquitos de cerdo magro.
    - Ensalada de tomate, pepino y espinacas con vinagreta.
    - 1 batata chica al horno (100g) para reponer glucógeno.
  ]
)

#v(12pt)

// ==================== DÍA TIPO B ====================
#text(size: 13pt, weight: "bold", fill: rgb("#2b6cb0"))[
  🟢 DÍA TIPO B: Fuerza por la Mañana (Martes y Jueves)
]
#text(size: 9pt, style: "italic", fill: rgb("#2c5282"))[
  *Foco:* Máxima síntesis proteica post-fuerza, carbohidratos mínimos (quema de grasa acelerada), saciedad con verduras.
]

#v(4pt)

#table(
  columns: (1fr, 1.3fr, 1.3fr),
  stroke: 0.5pt + rgb("#cbd5e0"),
  fill: (col, row) => if row == 0 { rgb("#bee3f8") } else if calc.even(row) { rgb("#ebf8ff") } else { white },
  inset: 7pt,
  
  [#text(weight: "bold")[Momento]],
  [#text(weight: "bold")[Opción 1 (Habitual de Gimnasio)]],
  [#text(weight: "bold")[Opción 2 (Comida Real)]],

  [*07:30 Pre-Fuerza*],
  [
    - Mates amargos + 1 vaso grande de agua.
    - No requiere carbohidratos previos.
  ],
  [
    - 1 café negro o infusión con agua.
    - 5g de creatina en agua.
  ],

  [*09:00 Post-Fuerza*\ (Ventana anabólica)],
  [
    - 1 batido Whey Protein (1 scoop, 25g prot) con leche descremada.
    - 1 plátano chico (acelera la asimilación).
    - Mates amargos en la oficina.
  ],
  [
    - 3 huevos revueltos con orégano y rodajas de tomate.
    - 1 batido Whey Protein en agua.
    - Mates amargos durante la mañana.
  ],

  [*13:00 Almuerzo*\ (Low-Carb estricto)],
  [
    - 220g de bife de carne vacuna magra a la plancha.
    - Ensalada enorme: lechuga, tomate, cebolla + vinagreta emulsionada (1 cda. aceite + limón).
    - *Cero arroz, papas o pastas.*
  ],
  [
    - 200g de pechuga de pollo a la plancha con limón.
    - Salteado de verduras (zapallitos, brócoli, cebolla y morrón).
    - 1 huevo duro picado encima.
  ],

  [*17:00 Merienda*\ (Proteína y saciedad)],
  [
    - 1 lata de atún al natural con rodajas de tomate y orégano.
    - Mate amargo o té verde.
  ],
  [
    - 200g de yogur natural descremado o queso cottage.
    - 5 mitades de nuez o 10 almendras (grasas saludables medidas).
  ],

  [*21:30 Cena*\ (Quema de grasa nocturna)],
  [
    - 200g de pechuga de pollo al horno con hierbas.
    - Ensalada verde grande (lechuga, rúcula, pepino) con limón.
    - Gelatina sin azúcar o infusión caliente digestiva.
  ],
  [
    - Filete de carne magra o pescado blanco (merluza al horno).
    - Coliflor o brócoli al vapor con sal, pimienta y chorrito de limón.
    - Infusión de manzanilla/menta.
  ]
)

#v(12pt)

// ==================== DÍA TIPO C ====================
#text(size: 13pt, weight: "bold", fill: rgb("#2f855a"))[
  🛌 DÍA TIPO C: Descanso Total & Recuperación (Viernes y Domingo)
]
#text(size: 9pt, style: "italic", fill: rgb("#22543d"))[
  *Foco:* Déficit calórico más profundo de la semana, reparación de articulaciones y sobrecarga limpia el viernes a la noche.
]

#v(4pt)

#table(
  columns: (1fr, 1.3fr, 1.3fr),
  stroke: 0.5pt + rgb("#cbd5e0"),
  fill: (col, row) => if row == 0 { rgb("#c6f6d5") } else if calc.even(row) { rgb("#f0fff4") } else { white },
  inset: 7pt,
  
  [#text(weight: "bold")[Momento]],
  [#text(weight: "bold")[Viernes (Carga pre-fondo sábado)]],
  [#text(weight: "bold")[Domingo (Déficit y Asimilación)]],

  [*Desayuno*],
  [
    - Batido Whey Protein con leche descremada.
    - 1 fruta fresca (pera o manzana).
    - Mates amargos.
  ],
  [
    - Omelette de 2 huevos enteros + 1 lata de atún al natural chica o queso magro.
    - Mates amargos en familia.
  ],

  [*Almuerzo*],
  [
    - 200g de pollo a la plancha.
    - Ensalada fresca de hojas verdes, tomate y cebolla.
    - 1 fruta cítrica.
  ],
  [
    - 220g de carne vacuna al horno o asado magro (sin grasa visible).
    - Ensalada abundante de lechuga, tomate y cebolla con limón.
  ],

  [*Merienda*],
  [
    - 2 tostadas de pan con queso untable descremado y dulce de batata (empieza la carga de glucógeno).
    - Infusión con 5g de creatina.
  ],
  [
    - Batido de proteína Whey con agua o 1 yogur descremado.
    - Mate amargo.
  ],

  [*Cena*],
  [
    - *Cena de Carga:* 180g de pollo + 1 plato mediano de fideos o arroz blanco (70g crudo) con salsa de tomate natural.
    - Buena hidratación con sales.
  ],
  [
    - 1 lata de atún al natural + 1 huevo duro + ensalada mixta grande.
    - Cero harinas. Infusión relajante antes de dormir.
  ]
)

#v(10pt)

// ==================== REGLAS DE ORO ====================
#rect(
  width: 100%,
  fill: rgb("#fffaf0"),
  radius: 6pt,
  inset: (x: 12pt, y: 10pt),
  stroke: 1pt + rgb("#fbd38d")
)[
  #text(weight: "bold", fill: rgb("#c05621"), size: 10.5pt)[⚡ Checklist Diario para Garantizar el Descenso:]
  #v(2pt)
  + *Balanza:* Pesarse 2 a 3 veces por semana (Lunes, Miércoles, Viernes) en ayunas, apenas levantado y tras orinar. Registrar la tendencia.
  + *Creatina:* 5 gramos diarios siempre. Recordar que retiene 1 kg de agua intracelular útil; el peso que baje será *grasa pura*.
  + *Fondo del Sábado:* En la montaña se comen *40–50 g HC/hora* (geles con cafeína, membrillo, sales). El déficit se hace durante la semana, nunca en la tirada larga.
  + *Hidratación Diaria:* Mínimo 2.5 a 3 litros de agua diarios para procesar el aumento de proteína y la creatina.
]
