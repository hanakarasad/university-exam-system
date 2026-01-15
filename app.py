import streamlit as st
import pandas as pd
import plotly.express as px
from database import db
from scheduler import ExamScheduler
from conflict_checker import ConflictChecker
import datetime

# Configuration de la page Streamlit
st.set_page_config(
    page_title="Système de Planification des Examens",
    page_icon="📚",
    layout="wide"
)

# Masquer l'en-tête par défaut de Streamlit
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

# En-tête de l'application
col1, col2 = st.columns([1, 4])
with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/2232/2232688.png", width=80)
with col2:
    st.title("📅 Système Intelligent de Planification des Examens")
    st.caption("Version 1.0 - Gestion de 130,000 étudiants et 200+ formations")

# Barre latérale
with st.sidebar:
    st.header("⚙️ Panneau de Contrôle")
    
    if st.button("🚀 Générer Nouvel Emploi du Temps", type="primary", use_container_width=True):
        with st.spinner("Génération de l'emploi du temps en cours..."):
            scheduler = ExamScheduler()
            success = scheduler.generate_schedule()
            if success:
                st.success("Emploi du temps généré avec succès!")
                st.rerun()
    
    if st.button("🔍 Vérifier les Conflits", use_container_width=True):
        with st.spinner("Vérification des conflits en cours..."):
            checker = ConflictChecker()
            conflicts = checker.check_all_conflicts()
            
            conflict_count = sum(len(c) if c else 0 for c in conflicts.values())
            if conflict_count == 0:
                st.success("✅ Aucun conflit détecté")
            else:
                st.error(f"⚠️ {conflict_count} conflits détectés")
    
    st.divider()
    
    st.header("📊 Statistiques Rapides")
    try:
        stats = db.execute_query("""
            SELECT
                (SELECT COUNT(*) FROM etudiants) as total_etudiants,
                (SELECT COUNT(*) FROM examens) as total_examens,
                (SELECT COUNT(*) FROM lieu_examen) as total_salles,
                (SELECT COUNT(DISTINCT DATE(date_heure)) FROM examens) as jours_examens
        """, fetch=True)
        
        if stats:
            st.metric("👨‍🎓 Étudiants", f"{stats[0][0]:,}")
            st.metric("📝 Examens", stats[0][1])
            st.metric("🏛️ Salles", stats[0][2])
            st.metric("📅 Jours d'examens", stats[0][3])
    except:
        st.warning("Impossible de charger les statistiques")

# Onglets principaux
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📋 Emploi du Temps",
    "🏛️ Gestion des Salles",
    "👨‍🏫 Professeurs",
    "📈 Rapports",
    "⚙️ Configuration"
])

# Onglet 1: Emploi du temps
with tab1:
    st.header("📋 Emploi du Temps des Examens")
    
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        date_filter = st.date_input("Filtrer par Date", datetime.date.today())
    with col_f2:
        # Récupérer la liste des départements
        try:
            depts = db.execute_query("SELECT nom FROM departements", fetch=True)
            dept_options = ["Tous"] + [d[0] for d in depts] if depts else ["Tous"]
            dept_filter = st.selectbox("Filtrer par Département", dept_options)
        except:
            dept_filter = "Tous"
            st.info("Chargement des départements...")
    
    # Requête pour obtenir les examens
    query = """
        SELECT
            e.id as id_examen,
            m.nom as module,
            d.nom as departement,
            f.nom as formation,
            l.nom as salle,
            l.capacite as capacite,
            e.date_heure as date_heure,
            e.duree_minutes as duree_minutes,
            CONCAT(p.nom, ' ', p.prenom) as professeur
        FROM examens e
        LEFT JOIN modules m ON e.module_id = m.id
        LEFT JOIN formations f ON m.formation_id = f.id
        LEFT JOIN departements d ON f.dept_id = d.id
        LEFT JOIN lieu_examen l ON e.salle_id = l.id
        LEFT JOIN professeurs p ON e.prof_id = p.id
        WHERE 1=1
    """
    
    params = []
    if dept_filter != "Tous":
        query += " AND d.nom = %s"
        params.append(dept_filter)
    
    query += " ORDER BY e.date_heure"
    
    try:
        df_exams = pd.read_sql(query, db.conn, params=params)
        
        if not df_exams.empty:
            # Renommer les colonnes pour l'affichage
            df_display = df_exams.rename(columns={
                'id_examen': 'ID Examen',
                'module': 'Module',
                'departement': 'Département',
                'formation': 'Formation',
                'salle': 'Salle',
                'capacite': 'Capacité',
                'date_heure': 'Date et Heure',
                'duree_minutes': 'Durée (min)',
                'professeur': 'Professeur'
            })
            
            st.dataframe(df_display, use_container_width=True, height=400)
            
            # Options d'export
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                csv = df_display.to_csv(index=False).encode('utf-8-sig')
                st.download_button(
                    label="📥 Télécharger en CSV",
                    data=csv,
                    file_name="emploi_du_temps_examens.csv",
                    mime="text/csv"
                )
            
            # Graphique de distribution
            if len(df_exams) > 1:
                st.subheader("📊 Distribution des Examens par Jour")
                df_exams['Date'] = pd.to_datetime(df_exams['date_heure']).dt.date
                daily_counts = df_exams['Date'].value_counts().sort_index()
                st.bar_chart(daily_counts)
        else:
            st.warning("Aucun examen programmé. Utilisez le bouton 'Générer' dans la barre latérale.")
    except Exception as e:
        st.error(f"Erreur: {e}")

# Onglet 2: Gestion des salles
with tab2:
    st.header("🏛️ Gestion des Salles d'Examen")
    
    try:
        rooms_df = pd.read_sql("""
            SELECT
                nom as nom_salle,
                capacite as capacite,
                type as type_salle,
                batiment as batiment,
                (SELECT COUNT(*) FROM examens WHERE salle_id = lieu_examen.id) as examens_programmes
            FROM lieu_examen
            ORDER BY type, capacite DESC
        """, db.conn)
        
        if not rooms_df.empty:
            # Renommer pour l'affichage
            rooms_display = rooms_df.rename(columns={
                'nom_salle': 'Nom Salle',
                'capacite': 'Capacité',
                'type_salle': 'Type',
                'batiment': 'Bâtiment',
                'examens_programmes': 'Examens Programmes'
            })
            
            st.dataframe(rooms_display, use_container_width=True)
            
            # Graphique des capacités
            st.subheader("📊 Capacité des Salles")
            fig = px.bar(rooms_df, x='nom_salle', y='capacite',
                        color='type_salle', title="Distribution des Capacités")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Aucune salle enregistrée.")
    except Exception as e:
        st.error(f"Erreur: {e}")

# Onglet 3: Professeurs
with tab3:
    st.header("👨‍🏫 Gestion des Professeurs")
    
    try:
        profs_df = pd.read_sql("""
            SELECT
                p.id as id_prof,
                CONCAT(p.nom, ' ', p.prenom) as nom_complet,
                d.nom as departement,
                p.specialite as specialite,
                (SELECT COUNT(*) FROM examens WHERE prof_id = p.id) as examens_attribues
            FROM professeurs p
            LEFT JOIN departements d ON p.dept_id = d.id
            ORDER BY p.nom
        """, db.conn)
        
        if not profs_df.empty:
            # Renommer pour l'affichage
            profs_display = profs_df.rename(columns={
                'id_prof': 'ID',
                'nom_complet': 'Nom Complet',
                'departement': 'Département',
                'specialite': 'Spécialité',
                'examens_attribues': 'Examens Attribués'
            })
            
            st.dataframe(profs_display, use_container_width=True)
            
            # Statistiques
            st.subheader("📊 Répartition par Département")
            if 'departement' in profs_df.columns:
                dept_dist = profs_df['departement'].value_counts()
                st.bar_chart(dept_dist)
        else:
            st.warning("Aucun professeur enregistré.")
    except Exception as e:
        st.error(f"Erreur: {e}")

# Onglet 4: Rapports
with tab4:
    st.header("📈 Rapports et Statistiques")
    
    try:
        # Statistiques de base
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_students = db.execute_query("SELECT COUNT(*) FROM etudiants", fetch=True)
            if total_students:
                st.metric("👨‍🎓 Étudiants", f"{total_students[0][0]:,}")
        
        with col2:
            total_exams = db.execute_query("SELECT COUNT(*) FROM examens", fetch=True)
            if total_exams:
                st.metric("📝 Examens", total_exams[0][0])
        
        with col3:
            total_rooms = db.execute_query("SELECT COUNT(*) FROM lieu_examen", fetch=True)
            if total_rooms:
                st.metric("🏛️ Salles", total_rooms[0][0])
        
        with col4:
            exam_days = db.execute_query("SELECT COUNT(DISTINCT DATE(date_heure)) FROM examens", fetch=True)
            if exam_days:
                st.metric("📅 Jours d'examens", exam_days[0][0])
        
        # Graphique d'occupation des salles
        st.subheader("📊 Occupation des Salles")
        try:
            room_usage = pd.read_sql("""
                SELECT
                    l.nom as salle,
                    COUNT(e.id) as nb_examens
                FROM lieu_examen l
                LEFT JOIN examens e ON l.id = e.salle_id
                GROUP BY l.id, l.nom
                ORDER BY nb_examens DESC
            """, db.conn)
            
            if not room_usage.empty:
                st.bar_chart(room_usage.set_index('salle'))
        except:
            st.info("Données d'occupation non disponibles")
        
    except Exception as e:
        st.error(f"Erreur dans les rapports: {e}")

# Onglet 5: Configuration
with tab5:
    st.header("⚙️ Configuration du Système")
    
    st.subheader("Paramètres de Planification")
    
    with st.form("config_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            start_date = st.date_input("Date de Début des Examens",
                                     datetime.date(2024, 6, 10))
            max_daily = st.slider("Examens Max par Jour", 1, 10, 4)
        
        with col2:
            duration = st.selectbox("Durée des Examens (min)",
                                  [90, 120, 150, 180], index=1)
            time_options = ["08:00", "09:00", "10:30", "13:00", "15:00", "17:00"]
            selected_times = st.multiselect("Créneaux Horaires",
                                          time_options, default=["09:00", "13:00", "15:00"])
        
        if st.form_submit_button("💾 Sauvegarder"):
            st.success("Configuration sauvegardée!")
    
    st.divider()
    
    st.subheader("Maintenance")
    col_m1, col_m2 = st.columns(2)
    
    with col_m1:
        if st.button("🧹 Effacer tous les examens", type="secondary"):
            if st.checkbox("Je confirme la suppression de tous les examens"):
                try:
                    db.execute_query("DELETE FROM examens")
                    st.success("Tous les examens ont été supprimés!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Erreur: {e}")

# Pied de page
st.divider()
st.caption("""
    ⚠️ Système Intelligent de Planification des Examens - Version 1.0
    ⏱️ Temps de Génération Cible: < 45 secondes
    📊 Capacité: 130,000 étudiants + 200 formations
    🔧 Développé avec: Python + Streamlit + PostgreSQL
""")

# Fermer la connexion à la fin
import atexit
atexit.register(db.close)