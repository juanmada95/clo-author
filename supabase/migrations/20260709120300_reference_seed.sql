-- ============================================================================
-- Migration 004 — MRCDD reference data (canonical, idempotent)
-- Source: Marco de Referencia de la Competencia Digital Docente,
--         Resolución de 4 de mayo de 2022 (BOE-A-2022-8042).
--         6 areas, 23 competences (Area 1 gains one vs DigCompEdu's 22).
-- Area names (ES/EN) are the canonical DigCompEdu/MRCDD labels.
--
-- NOTE: competence `name_es` labels below follow the published MRCDD wording
-- to the best available transcription. Verify verbatim against BOE-A-2022-8042
-- (pp. 7 ff.) before quoting them in the manuscript.
-- ============================================================================

insert into mrcdd_area (area_id, name_es, name_en) values
    (1, 'Compromiso profesional',                                'Professional Engagement'),
    (2, 'Recursos digitales',                                    'Digital Resources'),
    (3, 'Enseñanza y aprendizaje',                               'Teaching and Learning'),
    (4, 'Evaluación y retroalimentación',                        'Assessment and Feedback'),
    (5, 'Empoderamiento del alumnado',                           'Empowering Learners'),
    (6, 'Desarrollo de la competencia digital del alumnado',     'Facilitating Learners'' Digital Competence')
on conflict (area_id) do update
    set name_es = excluded.name_es,
        name_en = excluded.name_en;

insert into mrcdd_competence (competence_id, area_id, code, name_es) values
    -- Área 1 — Compromiso profesional (5)
    ( 1, 1, '1.1', 'Comunicación organizativa'),
    ( 2, 1, '1.2', 'Participación, colaboración y coordinación profesional'),
    ( 3, 1, '1.3', 'Práctica reflexiva'),
    ( 4, 1, '1.4', 'Desarrollo profesional digital continuo'),
    ( 5, 1, '1.5', 'Protección de datos personales, privacidad, seguridad y bienestar digital'),
    -- Área 2 — Recursos digitales (3)
    ( 6, 2, '2.1', 'Selección de recursos digitales'),
    ( 7, 2, '2.2', 'Creación y modificación de recursos digitales'),
    ( 8, 2, '2.3', 'Gestión, protección y distribución de recursos digitales'),
    -- Área 3 — Enseñanza y aprendizaje (4)
    ( 9, 3, '3.1', 'Enseñanza'),
    (10, 3, '3.2', 'Orientación y apoyo en el aprendizaje'),
    (11, 3, '3.3', 'Aprendizaje colaborativo'),
    (12, 3, '3.4', 'Aprendizaje autorregulado'),
    -- Área 4 — Evaluación y retroalimentación (3)
    (13, 4, '4.1', 'Estrategias de evaluación'),
    (14, 4, '4.2', 'Análisis de evidencias de aprendizaje'),
    (15, 4, '4.3', 'Retroalimentación y toma de decisiones'),
    -- Área 5 — Empoderamiento del alumnado (3)
    (16, 5, '5.1', 'Accesibilidad e inclusión'),
    (17, 5, '5.2', 'Atención a las diferencias personales en el aprendizaje'),
    (18, 5, '5.3', 'Compromiso activo del alumnado con su propio aprendizaje'),
    -- Área 6 — Desarrollo de la competencia digital del alumnado (5)
    (19, 6, '6.1', 'Alfabetización mediática y en el tratamiento de la información y los datos'),
    (20, 6, '6.2', 'Comunicación y colaboración ciudadana'),
    (21, 6, '6.3', 'Creación de contenidos digitales'),
    (22, 6, '6.4', 'Uso responsable y bienestar digital'),
    (23, 6, '6.5', 'Resolución de problemas')
on conflict (competence_id) do update
    set area_id = excluded.area_id,
        code    = excluded.code,
        name_es = excluded.name_es;
