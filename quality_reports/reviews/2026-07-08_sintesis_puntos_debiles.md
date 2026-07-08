# Síntesis de puntos débiles — Tesis CDD en la formación inicial
**Fecha:** 2026-07-08 · **Método:** `/review` (peer review: domain-referee + methods-referee) sobre el texto completo
**Veredicto de conjunto:** REVISIONES MAYORES — trabajo sólido, ambicioso y honesto; la mayoría de los problemas se resuelven con reanálisis o redacción, sin recoger datos nuevos.

---

## A. Prioridad máxima — señalados por LOS DOS revisores

### 1. El OE4 no se responde tal como está redactado
"**Comparar** la CD de los futuros docentes **con la de** los docentes en ejercicio", pero a los docentes en ejercicio nunca se les midió la CD (grupo de discusión, n=3, análisis temático). El Cap. XI ya lo reencuadra de facto como "utilidad profesional".
→ **Fix (redacción):** reformular el OE4 en Cap. I y Tabla 1.4 para que diga lo que se hizo ("valorar, desde la voz de docentes en ejercicio, la utilidad profesional de la formación inicial en CDD"). Sin datos nuevos.

### 2. Desalineación marco↔instrumento (constructo)
La tesis se vertebra en las 6 áreas pedagógicas del DigCompEdu/MRCDD, pero el CCDFM (5 dimensiones ISTE/DigComp) mide competencia digital **general/instrumental**, no la CDD pedagógica (áreas 3–5: enseñanza-aprendizaje, evaluación, empoderamiento). En 10.6 se triangula el CCDFM contra las 6 áreas como si las cubriera.
→ **Fix:** añadir un *crosswalk* explícito CCDFM↔áreas; marcar áreas 3–5 como "no evaluadas por el diagnóstico"; hablar de "CD autopercibida de orientación general" y reservar "CDD pedagógica" para donde la evidencia lo sostiene. Refuerza —no debilita— el argumento de la brecha.

### 3. Los perfiles GMM (Cap. VII): nivel, no forma + validación circular + solución frágil
- Los 3 perfiles son **planos** (alto/medio/bajo en todo): difieren en nivel, no en patrón → aporta poco sobre la media y debilita las "vías formativas por perfil".
- La Tabla 3 (Welch/KW sobre las mismas 5 dimensiones con que se hizo el clúster) es **circular**: la significación está garantizada por construcción.
- Solución frágil: AIC↔BIC discrepan (BIC prefiere 2), silhouette=0,197 (casi nula), solo se probó k=2 vs 3.
→ **Fix (reanálisis):** (a) validación **externa** de los perfiles contra variables no usadas para formarlos (curso, género, uso, autopercepción global); (b) reportar entropía/probabilidad posterior del GMM y estabilidad por bootstrap; comparar k=1…6; (c) declarar que difieren en nivel, no en patrón (o probar LPA con BLRT/LMR); (d) reformular la Tabla 3 como descriptiva.

### 4. Sobre-generalización más allá de la muestra
~75,5% del alumnado es de Granada; solo Andalucía y solo pública. Bien declarado en limitaciones, pero los títulos (10.5) y conclusiones saltan a "el sistema formativo" sin calificador.
→ **Fix (redacción):** añadir "en el contexto andaluz estudiado" en hallazgos/conclusiones; presentar la extrapolación a "el sistema" como hipótesis, no resultado.

### 5. Inconsistencias numéricas entre capítulos
- **Alfas distintos** para la MISMA muestra: Cap. III (,729/,690/,820/,783/,868) vs Cap. VII (,749/,710/,833/,783/,875). Decide incluso si "comunicación" pasa el umbral ,70 (,690 vs ,710).
- Media global **7,27** (Cap. VII) vs **7,30** (Caps. X–XI).
- Bibliometría: "España 30% (n=136)" pero 136/495 = 27,5%. Fechas de recogida: "2022–2023" (Cap. VII) vs "marzo–diciembre 2023" (Cap. III).
→ **Fix:** recalcular una sola vez sobre el archivo definitivo y unificar en todos los capítulos; reportar ω y IC 95% de los alfas; pasada de consistencia texto↔tablas.

---

## B. Importantes — un revisor, alta severidad

### 6. Mapeo del CCDFM a niveles A1–C2 no justificado (metodología, Mayor)
Traducir Z=+1 → "B2–C1" es una equivalencia inventada: el CCDFM (0–10, ISTE/DigComp) no está calibrado en la métrica CEFR de DigCompEdu, y menos desde puntuaciones Z relativas a la muestra.
→ **Fix:** retirar las etiquetas A1–C2/B2–C1 del Cap. VII o sustituirlas por descriptores relativos ("perfil alto/medio/bajo en la muestra"); usar A1–C2 solo como referencia narrativa de la literatura.

### 7. Validez estructural en la muestra propia: prometida y no entregada (metodología, Mayor)
Se anuncia "model fit" y ω pero solo se reporta alfa; no hay CFA en la muestra ni invarianza de medida antes de comparar grupos (Infantil/Primaria, género, cursos, perfiles); tampoco se aborda la varianza de método común (autoinforme único).
→ **Fix (reanálisis):** CFA de 5 factores en la muestra (CFI, TLI, RMSEA c/IC90%, SRMR); invarianza al menos por titulación y género; test de Harman/marcador para CMV. Si la invarianza falla, reformular las comparaciones como descriptivas.

### 8. Anclaje de marco inconsistente: MCCDD vs MRCDD (dominio, Mayor)
El objetivo general y el OE1 fijan el **MCCDD (2017, 5 áreas, ya superado)** como referente, mientras el resto de la tesis usa correctamente DigCompEdu/MRCDD (6 áreas/23 comp.).
→ **Fix:** unificar el anclaje en DigCompEdu/MRCDD en todos los objetivos; dejar el MCCDD solo como antecedente histórico; justificar por qué se usa un instrumento pre-MRCDD.

### 9. Sobre-interpretación de las conclusiones estelares (dominio, Mayor)
"Asimetría estructural del sistema" y "acreditar no es cualificar" descansan en 3 docentes (insiders del dispositivo de acreditación) + 14 formadores sensibilizados, pero se enuncian con fuerza de ley general ("el hallazgo que ordena todos los demás").
→ **Fix:** calibrar el registro a "interpretación integradora / hipótesis"; señalar que el perfil insider sobre-representa la crítica al dispositivo (llevar la limitación del Cap. IX a la discusión y conclusiones).

### 10. Fiabilidad intercodificador ausente (metodología, Mayor)
Cap. IV (análisis documental) sin doble codificación ni κ; Cap. II 2.6.2 (cribado sistemático) sin κ reportado.
→ **Fix (reanálisis parcial):** doble-codificar ≥20% del corpus y reportar κ de Cohen / α de Krippendorff por categoría; reportar κ de cribado en la revisión sistemática; publicar ficha y reglas en anexo/OSF.

### 11. Comparaciones múltiples + recodificación ad hoc de "vía de adquisición" (metodología, Menor–Mayor)
Muchos contrastes con corrección solo dentro de cada familia (sin control global). La regla de "vía predominante" (14→3 grupos) es ad hoc y sostiene la conclusión central de que la formación reglada "apenas aporta".
→ **Fix:** control FDR (Benjamini-Hochberg) global o modelo único (MAN(C)OVA); análisis de robustez a la regla de recodificación; enfatizar que los tamaños del efecto son pequeños (ya se reportan).

### 12. Novedad difusa / solapamiento (dominio, Mayor)
El diagnóstico transversal autopercibido es "más de lo mismo" según tu propia revisión; el Cap. IV se solapa con Moreno-Morilla et al. (2026, memorias, nacional). La novedad real (voz del formador de formadores + integración de 4 planos) aparece tarde.
→ **Fix:** llevar la novedad al frente (Cap. I) y afilarla (guías/andaluz vs memorias/nacional; currículo ofertado vs verificado); situar la contribución en el formador de formadores y la lectura integradora.

---

## C. Menores / redacción
- **OE3 infravende** lo que el Cap. VIII entrega → ampliar su redacción.
- **Diseño mixto:** falta un *joint display* (matriz de meta-inferencias por objetivo); precisar el punto de integración; "secuencial" es discutible (las hebras CUAL no derivan de la encuesta) → llamarlo "multifase con integración en la fase interpretativa".
- **Citas ausentes:** Instefjord & Munthe (2017) como precedente del análisis curricular; Real Decreto 1393/2007 en el encuadre normativo.
- **Tamaño muestral:** declarar el N poblacional de la fórmula de Tagliacarne y/o un análisis de potencia.

---

## D. Limitaciones estructurales — solo cabe DECLARARLAS (no corregibles con estos datos)
- **Medición justo tras la asignatura de TIC** (posible inflación) + **confusión curso/universidad/titulación**: retirar todo lenguaje de progresión/causalidad; opcional, modelo con efectos/errores por universidad (ICC).
- **Autoinforme vs desempeño** (transversal a todo el diagnóstico): asegurar que ninguna conclusión sobrepase ese alcance.

---

## Fortalezas a preservar
1. Integración mixta **sustantiva** (Cap. X produce meta-inferencias, no yuxtaposición).
2. Estado de la cuestión doble y actual: bibliométrico (WoS+Scopus) + revisión sistemática PRISMA con recuentos que cuadran y MMAT.
3. Rigor conceptual (distinción alfabetización / CD general / CDD; 22 vs 23 competencias bien manejado).
4. Aportación poco explorada: la voz biográfica del **formador de formadores** ("¿quién forma a los que forman?").
5. Reflexividad y honestidad: posicionamiento insider, cautela autopercepción≠desempeño, comité de ética (2648/CEIH/2022), member checking.

---

## Plan de acción sugerido (orden de coste/impacto)
1. **Rápido (redacción, alto impacto):** reformular OE4 y OE3 (#1, OE3); unificar anclaje MRCDD (#8); calibrar registro de conclusiones y añadir calificadores de alcance (#4, #9); pasada de consistencia numérica (#5).
2. **Medio (reanálisis acotado):** validación externa + estabilidad de los perfiles GMM y retirada del mapeo A1–C2 (#3, #6); crosswalk CCDFM↔áreas (#2); κ intercodificador (#10); FDR + robustez de "vía de adquisición" (#11).
3. **Mayor (si hay tiempo antes de defensa):** CFA + invarianza + CMV en la muestra (#7); joint display (C).
4. **Solo declarar:** limitaciones estructurales (D).
