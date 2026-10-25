// Template base para recetas deportivas en Typst

#let receta(
  titulo: "",
  categoria: "",
  momento: "",
  tiempo_prep: "",
  porciones: "",
  calorias_porcion: "",
  macros: (prot: "", carbs: "", grasas: ""),
  ingredientes: (),
  pasos: (),
  tips: ()
) = [
  #block(
    width: 100%,
    stroke: 1pt + rgb("#e2e8f0"),
    radius: 8pt,
    inset: 12pt,
    fill: white
  )[
    // Header de la receta
    #grid(
      columns: (1fr, auto),
      gutter: 10pt,
      [
        #text(size: 8.5pt, weight: "bold", fill: rgb("#3182ce"))[#upper(categoria)]
        #v(1pt)
        #text(size: 14pt, weight: "bold", fill: rgb("#1a365d"))[#titulo]
        #v(1pt)
        #text(size: 8.5pt, fill: rgb("#718096"), style: "italic")[Momento ideal: #momento]
      ],
      [
        #rect(
          fill: rgb("#ebf8ff"),
          radius: 5pt,
          inset: (x: 8pt, y: 6pt),
          stroke: 0.5pt + rgb("#bee3f8")
        )[
          #align(center)[
            #text(size: 11pt, weight: "bold", fill: rgb("#2b6cb0"))[#calorias_porcion] \
            #text(size: 7.5pt, fill: rgb("#4a5568"))[por porción]
          ]
        ]
      ]
    )

    #v(4pt)
    #line(length: 100%, stroke: 0.5pt + rgb("#cbd5e0"))
    #v(4pt)

    // Cuadro de Macros y Tiempos
    #grid(
      columns: (1fr, 1fr, 1fr, 1fr),
      gutter: 6pt,
      [
        #rect(width: 100%, fill: rgb("#f7fafc"), inset: 5pt, radius: 4pt)[
          #align(center)[
            #text(size: 8pt, fill: rgb("#718096"))[Proteínas] \
            #text(size: 10pt, weight: "bold", fill: rgb("#2d3748"))[#macros.prot]
          ]
        ]
      ],
      [
        #rect(width: 100%, fill: rgb("#f7fafc"), inset: 5pt, radius: 4pt)[
          #align(center)[
            #text(size: 8pt, fill: rgb("#718096"))[Carbohidratos] \
            #text(size: 10pt, weight: "bold", fill: rgb("#2d3748"))[#macros.carbs]
          ]
        ]
      ],
      [
        #rect(width: 100%, fill: rgb("#f7fafc"), inset: 5pt, radius: 4pt)[
          #align(center)[
            #text(size: 8pt, fill: rgb("#718096"))[Grasas] \
            #text(size: 10pt, weight: "bold", fill: rgb("#2d3748"))[#macros.grasas]
          ]
        ]
      ],
      [
        #rect(width: 100%, fill: rgb("#f7fafc"), inset: 5pt, radius: 4pt)[
          #align(center)[
            #text(size: 8pt, fill: rgb("#718096"))[Rinde / Tiempo] \
            #text(size: 9pt, weight: "bold", fill: rgb("#2d3748"))[#porciones · #tiempo_prep]
          ]
        ]
      ]
    )

    #v(8pt)

    // Ingredientes y Preparación
    #grid(
      columns: (1fr, 1.4fr),
      gutter: 14pt,
      [
        #text(size: 10pt, weight: "bold", fill: rgb("#2d3748"))[🛒 Ingredientes:]
        #v(3pt)
        #list(..ingredientes)
      ],
      [
        #text(size: 10pt, weight: "bold", fill: rgb("#2d3748"))[👨‍🍳 Preparación:]
        #v(3pt)
        #enum(..pasos)
      ]
    )

    #if tips.len() > 0 [
      #v(6pt)
      #rect(
        width: 100%,
        fill: rgb("#fffaf0"),
        radius: 4pt,
        inset: (x: 8pt, y: 6pt),
        stroke: 0.5pt + rgb("#fbd38d")
      )[
        #text(size: 8.5pt, weight: "bold", fill: rgb("#c05621"))[💡 Tips Nutricionales & Rendimiento:] \
        #text(size: 8.5pt, fill: rgb("#744210"))[
          #for tip in tips [ · #tip \ ]
        ]
      ]
    ]
  ]
]
