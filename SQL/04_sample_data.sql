-- ============================================
-- GÉNÉRATION DES DONNÉES D'EXEMPLE - VERSION FINALE
-- ============================================

DO $$
DECLARE
    student_counter INTEGER;
    formation_count INTEGER;
    promo_base INTEGER := 2021;
    nb_etudiants INTEGER;
    nb_professeurs INTEGER;
    nb_salles INTEGER;
    nb_modules INTEGER;
    nb_inscriptions BIGINT;
    etudiant_record RECORD;
    modules_formation INTEGER[];
    nb_modules_inscrire INTEGER;
    module_idx INTEGER;
    selected_module_id INTEGER;
    salle_counter INTEGER;
BEGIN
    RAISE NOTICE '============================================';
    RAISE NOTICE 'GÉNÉRATION DES DONNÉES D''EXEMPLE';
    RAISE NOTICE '============================================';

    -- 1. CRÉATION DE DONNÉES MASSIVES POUR LES ÉTUDIANTS
    RAISE NOTICE '1. Insertion de 130,000 étudiants...';

    -- Compter le nombre de formations disponibles
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
            RAISE NOTICE '   Étudiants insérés: %', student_counter;
        END IF;
    END LOOP;

    RAISE NOTICE '✅ 130,000 étudiants insérés avec succès!';

    -- 2. CRÉATION DES MODULES POUR CHAQUE FORMATION
    RAISE NOTICE '2. Création des modules pour chaque formation...';

    INSERT INTO modules (nom, credits, formation_id)
    SELECT
        'Module ' || num || ' - ' ||
        (ARRAY['Fondamentaux', 'Avancé', 'Spécialisé', 'Pratique'])[1 + floor(random() * 4)],
        5 + floor(random() * 3),
        f.id
    FROM formations f
    CROSS JOIN generate_series(1, f.nb_modules) AS num;

    RAISE NOTICE '✅ Modules créés pour toutes les formations';

    -- 3. INSCRIPTIONS DES ÉTUDIANTS AUX MODULES
    RAISE NOTICE '3. Inscriptions des étudiants aux modules...';

    -- Insertion avec gestion des conflits
    INSERT INTO inscriptions (etudiant_id, module_id, note)
    SELECT
        e.id,
        m.id,
        CASE WHEN random() > 0.3 THEN 10 + floor(random() * 11)::numeric END
    FROM etudiants e
    CROSS JOIN LATERAL (
        SELECT id
        FROM modules
        WHERE formation_id = e.formation_id
        ORDER BY random()
        LIMIT (6 + floor(random() * 3))
    ) m
    WHERE e.id <= 50000
    ON CONFLICT (etudiant_id, module_id) DO NOTHING;

    RAISE NOTICE '✅ Inscriptions terminées';

    -- 4. PROFESSEURS SUPPLÉMENTAIRES
    RAISE NOTICE '4. Ajout de 100 professeurs supplémentaires...';

    INSERT INTO professeurs (nom, prenom, dept_id, specialite)
    SELECT
        (ARRAY['Bouchenak', 'Taleb', 'Bencherif', 'Khelifati', 'Benslimane', 'Guendouz', 'Amrouche', 'Mebarki', 'Mokhtari', 'Lounis'])[1 + floor(random() * 10)],
        (ARRAY['Abdelkader', 'Mustapha', 'Omar', 'Hocine', 'Houria', 'Malika', 'Salima', 'Dalila', 'Soraya', 'Hafsa'])[1 + floor(random() * 10)],
        1 + floor(random() * 7),
        'Spécialité_' || prof_num
    FROM generate_series(1, 100) AS prof_num
    ON CONFLICT DO NOTHING;

    RAISE NOTICE '✅ 100 professeurs supplémentaires ajoutés';

    -- 5. SALLES SUPPLÉMENTAIRES
    RAISE NOTICE '5. Ajout de 30 salles supplémentaires...';

    -- Ajouter des salles supplémentaires
    FOR salle_counter IN 1..30 LOOP
        INSERT INTO lieu_examen (nom, capacite, type, batiment)
        VALUES (
            'Salle_Supp_' || (1000 + salle_counter),
            20 + floor(random() * 81),
            CASE
                WHEN random() < 0.3 THEN 'amphi'
                WHEN random() < 0.6 THEN 'salle'
                ELSE 'labo'
            END,
            'Bâtiment ' || chr(65 + floor(random() * 5)::integer)
        ) ON CONFLICT (nom) DO NOTHING;

        IF salle_counter % 10 = 0 THEN
            RAISE NOTICE '   Salles créées: %', salle_counter;
        END IF;
    END LOOP;

    RAISE NOTICE '✅ Salles ajoutées avec succès';

    -- 6. STATISTIQUES FINALES
    SELECT COUNT(*) INTO nb_etudiants FROM etudiants;
    SELECT COUNT(*) INTO nb_professeurs FROM professeurs;
    SELECT COUNT(*) INTO nb_salles FROM lieu_examen;
    SELECT COUNT(*) INTO nb_modules FROM modules;
    SELECT COUNT(*) INTO nb_inscriptions FROM inscriptions;

    RAISE NOTICE '============================================';
    RAISE NOTICE 'STATISTIQUES FINALES DE LA BASE DE DONNÉES:';
    RAISE NOTICE '============================================';
    RAISE NOTICE 'Étudiants: %', nb_etudiants;
    RAISE NOTICE 'Professeurs: %', nb_professeurs;
    RAISE NOTICE 'Salles: %', nb_salles;
    RAISE NOTICE 'Modules: %', nb_modules;
    RAISE NOTICE 'Inscriptions: %', nb_inscriptions;
    RAISE NOTICE '============================================';

END $$;
