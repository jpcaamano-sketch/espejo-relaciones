-- ============================================================
-- El Espejo de tus Relaciones — Setup DB
-- Ejecutar en Supabase SQL Editor
-- ============================================================

-- ─── Procesos ────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS espejo_procesos (
    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nombre           TEXT NOT NULL,
    correo           TEXT NOT NULL,
    orden_preguntas  TEXT,                    -- JSON array de IDs
    estado           TEXT DEFAULT 'fase1_pendiente',
    herida_primaria  TEXT,
    herida_secundaria TEXT,
    intensidad_primaria TEXT,
    puntajes         TEXT,                    -- JSON
    analisis         TEXT,                    -- JSON
    fase2_activada   BOOLEAN DEFAULT FALSE,
    fecha_creacion   TIMESTAMPTZ DEFAULT now(),
    fecha_completado TIMESTAMPTZ
);

ALTER TABLE espejo_procesos DISABLE ROW LEVEL SECURITY;

-- ─── Respuestas propias ───────────────────────────────────────
CREATE TABLE IF NOT EXISTS espejo_respuestas (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    proceso_id      UUID NOT NULL REFERENCES espejo_procesos(id) ON DELETE CASCADE,
    pregunta_id     INTEGER NOT NULL,
    valor_escala    INTEGER,
    texto_respuesta TEXT,
    UNIQUE (proceso_id, pregunta_id)
);

ALTER TABLE espejo_respuestas DISABLE ROW LEVEL SECURITY;

-- ─── Evaluadores externos ─────────────────────────────────────
CREATE TABLE IF NOT EXISTS espejo_evaluadores (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    proceso_id      UUID NOT NULL REFERENCES espejo_procesos(id) ON DELETE CASCADE,
    nombre          TEXT NOT NULL,
    correo          TEXT NOT NULL,
    token           UUID NOT NULL UNIQUE DEFAULT gen_random_uuid(),
    estado          TEXT DEFAULT 'pendiente',   -- pendiente | completado
    fecha_creacion  TIMESTAMPTZ DEFAULT now(),
    fecha_completado TIMESTAMPTZ
);

ALTER TABLE espejo_evaluadores DISABLE ROW LEVEL SECURITY;

-- ─── Respuestas externas ──────────────────────────────────────
CREATE TABLE IF NOT EXISTS espejo_respuestas_externas (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    evaluador_id    UUID NOT NULL REFERENCES espejo_evaluadores(id) ON DELETE CASCADE,
    pregunta_id     INTEGER NOT NULL,
    valor_escala    INTEGER,
    texto_respuesta TEXT,
    UNIQUE (evaluador_id, pregunta_id)
);

ALTER TABLE espejo_respuestas_externas DISABLE ROW LEVEL SECURITY;
