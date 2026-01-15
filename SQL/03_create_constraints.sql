-- ============================================
-- 03_create_constraints.sql
-- CRÉATION DES CONTRAINTES ET INDEX
-- VERSION CORRIGÉE ET STABLE
-- ============================================

-- ==================================================
-- 1. Création des index pour améliorer la performance
-- ==================================================

CREATE INDEX IF NOT EXISTS idx_etudiants_formation
ON etudiants(formation_id);

CREATE INDEX IF NOT EXISTS idx_inscriptions_etudiant
ON inscriptions(etudiant_id);

CREATE INDEX IF NOT EXISTS idx_inscriptions_module
ON inscriptions(module_id);

CREATE INDEX IF NOT EXISTS idx_examens_date
ON examens(date_heure);

CREATE INDEX IF NOT EXISTS idx_examens_salle_date
ON examens(salle_id, date_heure);

CREATE INDEX IF NOT EXISTS idx_examens_module
ON examens(module_id);

-- ==================================================
-- 2. Contrainte : Un étudiant ne peut pas avoir
--    deux examens le même jour
-- ==================================================

CREATE OR REPLACE FUNCTION check_student_conflict()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM examens e
        JOIN inscriptions i ON e.module_id = i.module_id
        WHERE i.etudiant_id IN (
            SELECT etudiant_id
            FROM inscriptions
            WHERE module_id = NEW.module_id
        )
        AND DATE(e.date_heure) = DATE(NEW.date_heure)
        AND e.id <> COALESCE(NEW.id, -1)
    ) THEN
        RAISE EXCEPTION
            'Conflit étudiant : un étudiant a déjà un examen le même jour';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trig_student_conflict ON examens;

CREATE TRIGGER trig_student_conflict
BEFORE INSERT OR UPDATE ON examens
FOR EACH ROW
EXECUTE FUNCTION check_student_conflict();

-- ==================================================
-- 3. Contrainte : Un professeur ne peut pas
--    surveiller plus de 3 examens par jour
-- ==================================================

CREATE OR REPLACE FUNCTION check_professor_limit()
RETURNS TRIGGER AS $$
BEGIN
    -- Si aucun professeur n'est affecté
    IF NEW.prof_id IS NULL THEN
        RETURN NEW;
    END IF;

    IF (
        SELECT COUNT(*)
        FROM examens
        WHERE prof_id = NEW.prof_id
          AND DATE(date_heure) = DATE(NEW.date_heure)
          AND id <> COALESCE(NEW.id, -1)
    ) >= 3 THEN
        RAISE EXCEPTION
            'Un professeur ne peut pas avoir plus de 3 examens par jour';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trig_professor_limit ON examens;

CREATE TRIGGER trig_professor_limit
BEFORE INSERT OR UPDATE ON examens
FOR EACH ROW
EXECUTE FUNCTION check_professor_limit();

-- ==================================================
-- 4. Contrainte : Capacité de la salle suffisante
-- ==================================================

CREATE OR REPLACE FUNCTION check_capacity()
RETURNS TRIGGER AS $$
DECLARE
    student_count INTEGER;
    room_capacity INTEGER;
BEGIN
    -- Nombre d'étudiants inscrits au module
    SELECT COUNT(*)
    INTO student_count
    FROM inscriptions
    WHERE module_id = NEW.module_id;

    -- Capacité de la salle
    SELECT capacite
    INTO room_capacity
    FROM lieu_examen
    WHERE id = NEW.salle_id;

    IF student_count > room_capacity THEN
        RAISE EXCEPTION
            'Capacité insuffisante : salle % places, % étudiants inscrits',
            room_capacity, student_count;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trig_capacity ON examens;

CREATE TRIGGER trig_capacity
BEFORE INSERT OR UPDATE ON examens
FOR EACH ROW
EXECUTE FUNCTION check_capacity();

-- ==================================================
-- Message de confirmation
-- ==================================================

DO $$
BEGIN
    RAISE NOTICE '✅ Contraintes et index créés avec succès (version corrigée)';
END;
$$;
