SYSTEME DE PLANIFICATION DES EXAMENS UNIVERSITAIRES
===================================================

📋 Prérequis:
- Python 3.8 ou supérieur
- PostgreSQL 14 ou supérieur
- 4GB RAM minimum

🚀 Étapes d'Installation Rapide:

1. Installer PostgreSQL depuis postgresql.org
2. Démarrer pgAdmin et créer une base de données nommée "university_exams"
3. Exécuter les fichiers SQL dans l'ordre dans Query Tool:
   - 01_database_setup.sql
   - 02_insert_basic_data.sql
   - 03_create_constraints.sql

4. Ouvrir Command Prompt dans le dossier du projet et exécuter:
   pip install -r requirements.txt

5. Modifier le mot de passe dans config.py pour correspondre à votre PostgreSQL

6. Démarrer l'application:
   streamlit run app.py

7. Ouvrir le navigateur à l'adresse: http://localhost:8501

📊 Fonctionnalités du Système:
- Planification intelligente pour 130,000 étudiants
- Détection automatique des conflits
- Interface web interactive
- Rapports et statistiques avancés
- Export des données en CSV et Excel

📞 Support: Consultez les fichiers SQL pour modifier les données
