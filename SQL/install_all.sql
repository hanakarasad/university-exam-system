-- ============================================
-- INSTALLATION COMPLÈTE - TOUT EN UN
-- ============================================

DO $$
BEGIN
    RAISE NOTICE '🚀 DÉBUT DE L''INSTALLATION...';
    RAISE NOTICE '============================================';
END $$;

-- 1. NETTOYAGE COMPLET
DROP TABLE IF EXISTS surveillances CASCADE;
DROP TABLE IF EXISTS examens CASCADE;
DROP TABLE IF EXISTS inscriptions CASCADE;
DROP TABLE IF EXISTS modules CASCADE;
DROP TABLE IF EXISTS etudiants CASCADE;
DROP TABLE IF EXISTS professeurs CASCADE;
DROP TABLE IF EXISTS lieu_examen CASCADE;
DROP TABLE IF EXISTS formations CASCADE;
DROP TABLE IF EXISTS departements CASCADE;

DO $$ BEGIN
    RAISE NOTICE '✅ 1. Nettoyage terminé';
END $$;

-- 2. CRÉATION DES TABLES
CREATE TABLE departements (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE formations (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(150) NOT NULL,
    dept_id INTEGER REFERENCES departements(id) ON DELETE CASCADE,
    nb_modules INTEGER DEFAULT 8
);

CREATE TABLE etudiants (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    formation_id INTEGER REFERENCES formations(id) ON DELETE SET NULL,
    promo INTEGER DEFAULT 2024
);

CREATE TABLE modules (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(150) NOT NULL,
    credits INTEGER DEFAULT 5,
    formation_id INTEGER REFERENCES formations(id) ON DELETE CASCADE,
    pre_req_id INTEGER REFERENCES modules(id)
);

CREATE TABLE professeurs (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(150) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    dept_id INTEGER REFERENCES departements(id),
    specialite VARCHAR(100),
    max_surveillances INTEGER DEFAULT 10
);

CREATE TABLE lieu_examen (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL UNIQUE,
    capacite INTEGER NOT NULL CHECK (capacite > 0),
    type VARCHAR(20) CHECK (type IN ('amphi', 'salle', 'labo')),
    batiment VARCHAR(50),
    equipement TEXT
);

CREATE TABLE inscriptions (
    etudiant_id INTEGER REFERENCES etudiants(id) ON DELETE CASCADE,
    module_id INTEGER REFERENCES modules(id) ON DELETE CASCADE,
    note DECIMAL(4,2),
    PRIMARY KEY (etudiant_id, module_id)
);

CREATE TABLE examens (
    id SERIAL PRIMARY KEY,
    module_id INTEGER NOT NULL REFERENCES modules(id),
    prof_id INTEGER REFERENCES professeurs(id),
    salle_id INTEGER NOT NULL REFERENCES lieu_examen(id),
    date_heure TIMESTAMP NOT NULL,
    duree_minutes INTEGER NOT NULL CHECK (duree_minutes > 0),
    surveillants_requis INTEGER DEFAULT 1,
    UNIQUE(module_id, date_heure)
);

CREATE TABLE surveillances (
    id SERIAL PRIMARY KEY,
    examen_id INTEGER REFERENCES examens(id) ON DELETE CASCADE,
    prof_id INTEGER REFERENCES professeurs(id),
    role VARCHAR(50) DEFAULT 'surveillant',
    UNIQUE(examen_id, prof_id)
);

DO $$ BEGIN
    RAISE NOTICE '✅ 2. Toutes les tables créées';
END $$;

-- 3. DONNÉES DE BASE
INSERT INTO departements (nom) VALUES
('Informatique'),
('Mathématiques'),
('Physique'),
('Chimie'),
('Droit'),
('Sciences Économiques'),
('Biologie');

INSERT INTO formations (nom, dept_id, nb_modules) VALUES
('Licence Informatique', 1, 8),
('Master Data Science', 1, 9),
('Ingénieur Logiciel', 1, 7),
('Licence Mathématiques', 2, 8),
('Master Mathématiques Appliquées', 2, 9),
('Licence Physique', 3, 8),
('Master Physique Quantique', 3, 9),
('Licence Chimie', 4, 8),
('Master Chimie Organique', 4, 9),
('Licence Droit', 5, 8),
('Master Droit des Affaires', 5, 9),
('Licence Sciences Économiques', 6, 8),
('Master Économétrie', 6, 9),
('Licence Biologie', 7, 8),
('Master Biologie Moléculaire', 7, 9),
('Licence Informatique Graphique', 1, 8),
('Master Intelligence Artificielle', 1, 9),
('Licence Statistiques', 2, 8),
('Licence Électronique', 3, 8),
('Master Nanotechnologies', 3, 9),
('Licence Biochimie', 4, 8),
('Licence Droit International', 5, 8),
('Master Finance', 6, 9),
('Licence Biotechnologie', 7, 8),
('Licence Réseaux Informatiques', 1, 8),
('Master Sécurité Informatique', 1, 9),
('Licence Physique Chimie', 3, 8),
('Master Droit Fiscal', 5, 9),
('Licence Économie Gestion', 6, 8),
('Master Biologie Cellulaire', 7, 9);

INSERT INTO lieu_examen (nom, capacite, type, batiment) VALUES
('Amphi A', 500, 'amphi', 'Bâtiment Principal'),
('Amphi B', 350, 'amphi', 'Bâtiment Principal'),
('Amphi C', 300, 'amphi', 'Bâtiment Sciences'),
('Salle 101', 20, 'salle', 'Bâtiment A'),
('Salle 102', 20, 'salle', 'Bâtiment A'),
('Salle 103', 25, 'salle', 'Bâtiment A'),
('Salle 201', 30, 'salle', 'Bâtiment B'),
('Salle 202', 30, 'salle', 'Bâtiment B'),
('Salle 203', 35, 'salle', 'Bâtiment B'),
('Salle 301', 40, 'salle', 'Bâtiment C'),
('Salle 302', 40, 'salle', 'Bâtiment C'),
('Labo Info 1', 15, 'labo', 'Bâtiment Informatique'),
('Labo Info 2', 15, 'labo', 'Bâtiment Informatique'),
('Labo Info 3', 20, 'labo', 'Bâtiment Informatique'),
('Labo Physique 1', 15, 'labo', 'Bâtiment Physique'),
('Labo Physique 2', 15, 'labo', 'Bâtiment Physique'),
('Labo Chimie 1', 15, 'labo', 'Bâtiment Chimie'),
('Labo Chimie 2', 15, 'labo', 'Bâtiment Chimie'),
('Salle de Conférence', 100, 'salle', 'Bâtiment Administratif'),
('Amphi D', 400, 'amphi', 'Bâtiment Nouveau');

-- Noms algériens pour les professeurs
INSERT INTO professeurs (nom, prenom, dept_id, specialite) VALUES
('Benali', 'Ahmed', 1, 'Algorithmique'),
('Kadri', 'Fatima', 1, 'Bases de données'),
('Mansouri', 'Karim', 2, 'Analyse'),
('Bouguerra', 'Nadia', 2, 'Algèbre'),
('Saidi', 'Mohamed', 3, 'Mécanique'),
('Boukhatem', 'Leïla', 3, 'Optique'),
('Cherif', 'Yacine', 4, 'Chimie Organique'),
('Zitouni', 'Samira', 4, 'Chimie Analytique'),
('Haddad', 'Rachid', 5, 'Droit Civil'),
('Belkacem', 'Soraya', 5, 'Droit Commercial'),
('Guendouz', 'Ali', 6, 'Microéconomie'),
('Bencherif', 'Hafsa', 6, 'Macroéconomie'),
('Taleb', 'Mustapha', 7, 'Biologie Cellulaire'),
('Khelifati', 'Yasmine', 7, 'Génétique'),
('Benslimane', 'Omar', 1, 'Réseaux'),
('Amrouche', 'Dalila', 1, 'Sécurité'),
('Mebarki', 'Hocine', 2, 'Statistiques'),
('Bouchenak', 'Salima', 3, 'Physique Quantique'),
('Mokhtari', 'Abdelkader', 4, 'Biochimie'),
('Lounis', 'Malika', 5, 'Droit International');

DO $$ BEGIN
    RAISE NOTICE '✅ 3. Données de base insérées';
END $$;

-- 4. INDEX ET CONTRAINTES
CREATE INDEX idx_etudiants_formation ON etudiants(formation_id);
CREATE INDEX idx_inscriptions_etudiant ON inscriptions(etudiant_id);
CREATE INDEX idx_inscriptions_module ON inscriptions(module_id);
CREATE INDEX idx_examens_date ON examens(date_heure);
CREATE INDEX idx_examens_salle ON examens(salle_id, date_heure);
CREATE INDEX idx_examens_module ON examens(module_id);

DO $$ BEGIN
    RAISE NOTICE '✅ 4. Index créés';
END $$;

-- 5. GÉNÉRATION DES 130,000 ÉTUDIANTS
DO $$
DECLARE
    student_counter INTEGER;
    formation_count INTEGER;
    promo_base INTEGER := 2021;
BEGIN
    RAISE NOTICE '5. Génération de 130,000 étudiants...';

    SELECT COUNT(*) INTO formation_count FROM formations;

    FOR student_counter IN 1..130000 LOOP
        INSERT INTO etudiants (nom, prenom, formation_id, promo)
        VALUES (
            (ARRAY['Benali', 'Kadri', 'Mansouri', 'Bouguerra', 'Saidi', 'Boukhatem', 'Cherif', 'Zitouni', 'Haddad', 'Belkacem'])[1 + floor(random() * 10)],
            (ARRAY['Mohamed', 'Karim', 'Yacine', 'Ahmed', 'Rachid', 'Mustapha', 'Omar', 'Hocine', 'Abdelkader', 'Ali'])[1 + floor(random() * 10)],
            1 + floor(random() * formation_count),
            promo_base + floor(random() * 4)
        );

        IF student_counter % 10000 = 0 THEN
            RAISE NOTICE '   % étudiants créés...', student_counter;
        END IF;
    END LOOP;

    RAISE NOTICE '✅ 130,000 étudiants créés';
END $$;

-- 6. CRÉATION DES MODULES
DO $$ BEGIN
    RAISE NOTICE '6. Création des modules...';
END $$;

INSERT INTO modules (nom, credits, formation_id)
SELECT
    'Module ' || num || ' - ' ||
    (ARRAY['Fondamentaux', 'Avancé', 'Spécialisé', 'Pratique'])[1 + floor(random() * 4)],
    5 + floor(random() * 3),
    f.id
FROM formations f
CROSS JOIN generate_series(1, f.nb_modules) AS num;

DO $$ BEGIN
    RAISE NOTICE '✅ Modules créés';
END $$;

-- 7. CRÉATION DES INSCRIPTIONS
DO $$
DECLARE
    student RECORD;
    formation_modules INTEGER[];
    modules_to_insert INTEGER;
    j INTEGER;
    selected_module INTEGER;
BEGIN
    RAISE NOTICE '7. Création des inscriptions...';

    FOR student IN SELECT id, formation_id FROM etudiants LIMIT 50000 LOOP
        -- Récupérer tous les modules de la formation
        SELECT ARRAY_AGG(id) INTO formation_modules
        FROM modules WHERE formation_id = student.formation_id;

        IF formation_modules IS NOT NULL AND array_length(formation_modules, 1) > 0 THEN
            -- Choisir 6-8 modules aléatoires
            modules_to_insert := 6 + floor(random() * 3);

            FOR j IN 1..modules_to_insert LOOP
                -- Sélectionner un module aléatoire
                selected_module := formation_modules[1 + floor(random() * array_length(formation_modules, 1))];

                -- Insérer l'inscription
                INSERT INTO inscriptions (etudiant_id, module_id, note)
                VALUES (student.id, selected_module,
                        CASE WHEN random() > 0.3 THEN 10 + floor(random() * 11)::numeric END)
                ON CONFLICT (etudiant_id, module_id) DO NOTHING;
            END LOOP;
        END IF;

        IF student.id % 10000 = 0 THEN
            RAISE NOTICE '   % étudiants traités', student.id;
        END IF;
    END LOOP;

    RAISE NOTICE '✅ Inscriptions créées';
END $$;

-- 8. AJOUT DE PROFESSEURS SUPPLÉMENTAIRES
DO $$ BEGIN
    RAISE NOTICE '8. Ajout de professeurs supplémentaires...';
END $$;

INSERT INTO professeurs (nom, prenom, dept_id, specialite)
SELECT
    (ARRAY['Bouchenak', 'Taleb', 'Bencherif', 'Khelifati', 'Benslimane', 'Guendouz', 'Amrouche', 'Mebarki', 'Mokhtari', 'Lounis'])[1 + floor(random() * 10)],
    (ARRAY['Abdelkader', 'Mustapha', 'Omar', 'Hocine', 'Houria', 'Malika', 'Salima', 'Dalila', 'Soraya', 'Hafsa'])[1 + floor(random() * 10)],
    1 + floor(random() * 7),
    'Spécialité_' || prof_num
FROM generate_series(1, 50) AS prof_num
ON CONFLICT DO NOTHING;

DO $$ BEGIN
    RAISE NOTICE '✅ 50 professeurs supplémentaires ajoutés';
END $$;

-- 9. AJOUT DE SALLES SUPPLÉMENTAIRES
DO $$
DECLARE
    salle_counter INTEGER;
    salle_nom TEXT;
BEGIN
    RAISE NOTICE '9. Ajout de salles supplémentaires...';

    FOR salle_counter IN 1..30 LOOP
        salle_nom := 'Salle_Supp_' || (1000 + salle_counter);

        INSERT INTO lieu_examen (nom, capacite, type, batiment)
        VALUES (
            salle_nom,
            20 + floor(random() * 81),
            CASE
                WHEN random() < 0.3 THEN 'amphi'
                WHEN random() < 0.6 THEN 'salle'
                ELSE 'labo'
            END,
            'Bâtiment ' || chr(65 + floor(random() * 5)::integer)
        ) ON CONFLICT (nom) DO NOTHING;

        IF salle_counter % 10 = 0 THEN
            RAISE NOTICE '   % salles créées', salle_counter;
        END IF;
    END LOOP;

    RAISE NOTICE '✅ 30 salles supplémentaires ajoutées';
END $$;

-- 10. VÉRIFICATION FINALE
DO $$
DECLARE
    nb_departements INTEGER;
    nb_formations INTEGER;
    nb_etudiants INTEGER;
    nb_professeurs INTEGER;
    nb_salles INTEGER;
    nb_modules INTEGER;
    nb_inscriptions BIGINT;
BEGIN
    SELECT COUNT(*) INTO nb_departements FROM departements;
    SELECT COUNT(*) INTO nb_formations FROM formations;
    SELECT COUNT(*) INTO nb_etudiants FROM etudiants;
    SELECT COUNT(*) INTO nb_professeurs FROM professeurs;
    SELECT COUNT(*) INTO nb_salles FROM lieu_examen;
    SELECT COUNT(*) INTO nb_modules FROM modules;
    SELECT COUNT(*) INTO nb_inscriptions FROM inscriptions;

    RAISE NOTICE '============================================';
    RAISE NOTICE 'INSTALLATION TERMINÉE AVEC SUCCÈS!';
    RAISE NOTICE '============================================';
    RAISE NOTICE 'Départements: %', nb_departements;
    RAISE NOTICE 'Formations: %', nb_formations;
    RAISE NOTICE 'Étudiants: %', nb_etudiants;
    RAISE NOTICE 'Professeurs: %', nb_professeurs;
    RAISE NOTICE 'Salles: %', nb_salles;
    RAISE NOTICE 'Modules: %', nb_modules;
    RAISE NOTICE 'Inscriptions: %', nb_inscriptions;
    RAISE NOTICE '============================================';
END $$;
