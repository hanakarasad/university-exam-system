-- ============================================
-- INSERTION DES DONNÉES DE BASE
-- ============================================

-- 1. Insertion des départements
INSERT INTO departements (nom) VALUES
('Informatique'),
('Mathématiques'),
('Physique'),
('Chimie'),
('Droit'),
('Sciences Économiques'),
('Biologie');

-- 2. Insertion des formations (30 exemples)
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

-- 3. Insertion des salles (20 exemples)
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

-- 4. Insertion des professeurs (20 exemples)
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

-- Message de confirmation
DO $$
DECLARE
    nb_departements INTEGER;
    nb_formations INTEGER;
    nb_salles INTEGER;
    nb_professeurs INTEGER;
BEGIN
    SELECT COUNT(*) INTO nb_departements FROM departements;
    SELECT COUNT(*) INTO nb_formations FROM formations;
    SELECT COUNT(*) INTO nb_salles FROM lieu_examen;
    SELECT COUNT(*) INTO nb_professeurs FROM professeurs;

    RAISE NOTICE '✅ Données de base insérées avec succès!';
    RAISE NOTICE '   - % départements', nb_departements;
    RAISE NOTICE '   - % formations', nb_formations;
    RAISE NOTICE '   - % salles', nb_salles;
    RAISE NOTICE '   - % professeurs', nb_professeurs;
END $$;
