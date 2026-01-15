-- Supprimer les tables si elles existent (ordre inverse des dépendances)
DROP TABLE IF EXISTS surveillances CASCADE;
DROP TABLE IF EXISTS examens CASCADE;
DROP TABLE IF EXISTS inscriptions CASCADE;
DROP TABLE IF EXISTS modules CASCADE;
DROP TABLE IF EXISTS etudiants CASCADE;
DROP TABLE IF EXISTS professeurs CASCADE;
DROP TABLE IF EXISTS lieu_examen CASCADE;
DROP TABLE IF EXISTS formations CASCADE;
DROP TABLE IF EXISTS departements CASCADE;

-- 1. Table des départements (7 départements)
CREATE TABLE departements (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL UNIQUE
);

-- 2. Table des formations (200+ formations)
CREATE TABLE formations (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(150) NOT NULL,
    dept_id INTEGER REFERENCES departements(id) ON DELETE CASCADE,
    nb_modules INTEGER DEFAULT 8
);

-- 3. Table des étudiants (130,000 étudiants)
CREATE TABLE etudiants (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    formation_id INTEGER REFERENCES formations(id) ON DELETE SET NULL,
    promo INTEGER DEFAULT 2024
);

-- 4. Table des modules (6-9 modules par formation)
CREATE TABLE modules (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(150) NOT NULL,
    credits INTEGER DEFAULT 5,
    formation_id INTEGER REFERENCES formations(id) ON DELETE CASCADE,
    pre_req_id INTEGER REFERENCES modules(id)
);

-- 5. Table des professeurs (500 professeurs)
CREATE TABLE professeurs (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(150) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    dept_id INTEGER REFERENCES departements(id),
    specialite VARCHAR(100),
    max_surveillances INTEGER DEFAULT 10
);

-- 6. Table des salles d'examen (100 salles)
CREATE TABLE lieu_examen (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL UNIQUE,
    capacite INTEGER NOT NULL CHECK (capacite > 0),
    type VARCHAR(20) CHECK (type IN ('amphi', 'salle', 'labo')),
    batiment VARCHAR(50),
    equipement TEXT
);

-- 7. Table des inscriptions (900,000 inscriptions)
CREATE TABLE inscriptions (
    etudiant_id INTEGER REFERENCES etudiants(id) ON DELETE CASCADE,
    module_id INTEGER REFERENCES modules(id) ON DELETE CASCADE,
    note DECIMAL(4,2),
    PRIMARY KEY (etudiant_id, module_id)
);

-- 8. Table des examens (cœur du système)
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

-- 9. Table des surveillances
CREATE TABLE surveillances (
    id SERIAL PRIMARY KEY,
    examen_id INTEGER REFERENCES examens(id) ON DELETE CASCADE,
    prof_id INTEGER REFERENCES professeurs(id),
    role VARCHAR(50) DEFAULT 'surveillant',
    UNIQUE(examen_id, prof_id)
);

-- Message de confirmation
DO $$ BEGIN
    RAISE NOTICE '✅ Toutes les tables créées avec succès!';
END $$;
