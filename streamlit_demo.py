import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
import numpy as np

# ============================================
# 1. DONNÉES DE DÉMONSTRATION
# ============================================

def get_demo_exams():
    """Retourne des données d'examens de démonstration"""
    exams = [
        {"ID": 1, "Module": "Base de données", "Salle": "Amphi A", "Date": "2024-06-10 09:00", "Durée": 120, "Professeur": "Dr. Benali", "Étudiants": 450, "Département": "Informatique"},
        {"ID": 2, "Module": "Algorithmique", "Salle": "Salle 101", "Date": "2024-06-10 13:00", "Durée": 120, "Professeur": "Dr. Kadri", "Étudiants": 28, "Département": "Informatique"},
        {"ID": 3, "Module": "Réseaux", "Salle": "Amphi B", "Date": "2024-06-11 09:00", "Durée": 120, "Professeur": "Dr. Mansouri", "Étudiants": 320, "Département": "Informatique"},
        {"ID": 4, "Module": "Programmation Python", "Salle": "Labo Info 1", "Date": "2024-06-11 13:00", "Durée": 120, "Professeur": "Dr. Bouguerra", "Étudiants": 18, "Département": "Informatique"},
        {"ID": 5, "Module": "Sécurité", "Salle": "Salle 102", "Date": "2024-06-12 09:00", "Durée": 120, "Professeur": "Dr. Saidi", "Étudiants": 22, "Département": "Informatique"},
        {"ID": 6, "Module": "Intelligence Artificielle", "Salle": "Amphi A", "Date": "2024-06-12 13:00", "Durée": 120, "Professeur": "Dr. Benali", "Étudiants": 480, "Département": "Informatique"},
        {"ID": 7, "Module": "Développement Web", "Salle": "Salle 201", "Date": "2024-06-13 09:00", "Durée": 120, "Professeur": "Dr. Kadri", "Étudiants": 35, "Département": "Informatique"},
        {"ID": 8, "Module": "Systèmes d'exploitation", "Salle": "Amphi C", "Date": "2024-06-13 13:00", "Durée": 120, "Professeur": "Dr. Mansouri", "Étudiants": 280, "Département": "Informatique"},
        {"ID": 9, "Module": "Mathématiques Avancées", "Salle": "Amphi A", "Date": "2024-06-14 09:00", "Durée": 120, "Professeur": "Dr. Bouguerra", "Étudiants": 420, "Département": "Mathématiques"},
        {"ID": 10, "Module": "Physique Quantique", "Salle": "Amphi B", "Date": "2024-06-14 13:00", "Durée": 120, "Professeur": "Dr. Saidi", "Étudiants": 300, "Département": "Physique"},
        {"ID": 11, "Module": "Chimie Organique", "Salle": "Labo Chimie 1", "Date": "2024-06-15 09:00", "Durée": 120, "Professeur": "Dr. Cherif", "Étudiants": 25, "Département": "Chimie"},
        {"ID": 12, "Module": "Droit Commercial", "Salle": "Salle 301", "Date": "2024-06-15 13:00", "Durée": 120, "Professeur": "Dr. Haddad", "Étudiants": 45, "Département": "Droit"},
        {"ID": 13, "Module": "Économétrie", "Salle": "Amphi D", "Date": "2024-06-16 09:00", "Durée": 120, "Professeur": "Dr. Guendouz", "Étudiants": 380, "Département": "Économie"},
        {"ID": 14, "Module": "Biologie Moléculaire", "Salle": "Labo Bio 1", "Date": "2024-06-16 13:00", "Durée": 120, "Professeur": "Dr. Taleb", "Étudiants": 30, "Département": "Biologie"},
        {"ID": 15, "Module": "Statistiques", "Salle": "Salle 202", "Date": "2024-06-17 09:00", "Durée": 120, "Professeur": "Dr. Mebarki", "Étudiants": 40, "Département": "Mathématiques"},
    ]
    return pd.DataFrame(exams)

def get_demo_rooms():
    """Retourne des données de salles de démonstration"""
    rooms = [
        {"Nom": "Amphi A", "Capacité": 500, "Type": "Amphithéâtre", "Bâtiment": "Principal", "Examens": 12},
        {"Nom": "Amphi B", "Capacité": 350, "Type": "Amphithéâtre", "Bâtiment": "Principal", "Examens": 8},
        {"Nom": "Amphi C", "Capacité": 300, "Type": "Amphithéâtre", "Bâtiment": "Sciences", "Examens": 6},
        {"Nom": "Amphi D", "Capacité": 400, "Type": "Amphithéâtre", "Bâtiment": "Nouveau", "Examens": 5},
        {"Nom": "Salle 101", "Capacité": 30, "Type": "Salle", "Bâtiment": "Bâtiment A", "Examens": 15},
        {"Nom": "Salle 102", "Capacité": 25, "Type": "Salle", "Bâtiment": "Bâtiment A", "Examens": 10},
        {"Nom": "Salle 201", "Capacité": 40, "Type": "Salle", "Bâtiment": "Bâtiment B", "Examens": 18},
        {"Nom": "Salle 202", "Capacité": 35, "Type": "Salle", "Bâtiment": "Bâtiment B", "Examens": 12},
        {"Nom": "Salle 301", "Capacité": 50, "Type": "Salle", "Bâtiment": "Bâtiment C", "Examens": 14},
        {"Nom": "Salle 302", "Capacité": 45, "Type": "Salle", "Bâtiment": "Bâtiment C", "Examens": 11},
        {"Nom": "Labo Info 1", "Capacité": 20, "Type": "Laboratoire", "Bâtiment": "Informatique", "Examens": 22},
        {"Nom": "Labo Info 2", "Capacité": 20, "Type": "Laboratoire", "Bâtiment": "Informatique", "Examens": 20},
        {"Nom": "Labo Physique 1", "Capacité": 15, "Type": "Laboratoire", "Bâtiment": "Physique", "Examens": 8},
        {"Nom": "Labo Chimie 1", "Capacité": 15, "Type": "Laboratoire", "Bâtiment": "Chimie", "Examens": 7},
        {"Nom": "Labo Bio 1", "Capacité": 18, "Type": "Laboratoire", "Bâtiment": "Biologie", "Examens": 9},
    ]
    return pd.DataFrame(rooms)

def get_demo_professors():
    """Retourne des données de professeurs de démonstration"""
    professors = [
        {"ID": 1, "Nom": "Dr. Benali Ahmed", "Département": "Informatique", "Spécialité": "Base de données", "Examens": 15, "Heures": 45},
        {"ID": 2, "Nom": "Dr. Kadri Fatima", "Département": "Informatique", "Spécialité": "Algorithmique", "Examens": 12, "Heures": 36},
        {"ID": 3, "Nom": "Dr. Mansouri Karim", "Département": "Informatique", "Spécialité": "Réseaux", "Examens": 10, "Heures": 30},
        {"ID": 4, "Nom": "Dr. Bouguerra Nadia", "Département": "Mathématiques", "Spécialité": "Analyse", "Examens": 8, "Heures": 24},
        {"ID": 5, "Nom": "Dr. Saidi Mohamed", "Département": "Physique", "Spécialité": "Mécanique", "Examens": 6, "Heures": 18},
        {"ID": 6, "Nom": "Dr. Boukhatem Leïla", "Département": "Physique", "Spécialité": "Optique", "Examens": 7, "Heures": 21},
        {"ID": 7, "Nom": "Dr. Cherif Yacine", "Département": "Chimie", "Spécialité": "Chimie Organique", "Examens": 5, "Heures": 15},
        {"ID": 8, "Nom": "Dr. Zitouni Samira", "Département": "Chimie", "Spécialité": "Chimie Analytique", "Examens": 4, "Heures": 12},
        {"ID": 9, "Nom": "Dr. Haddad Rachid", "Département": "Droit", "Spécialité": "Droit Civil", "Examens": 9, "Heures": 27},
        {"ID": 10, "Nom": "Dr. Belkacem Soraya", "Département": "Droit", "Spécialité": "Droit Commercial", "Examens": 8, "Heures": 24},
        {"ID": 11, "Nom": "Dr. Guendouz Ali", "Département": "Économie", "Spécialité": "Microéconomie", "Examens": 7, "Heures": 21},
        {"ID": 12, "Nom": "Dr. Bencherif Hafsa", "Département": "Économie", "Spécialité": "Macroéconomie", "Examens": 6, "Heures": 18},
        {"ID": 13, "Nom": "Dr. Taleb Mustapha", "Département": "Biologie", "Spécialité": "Biologie Cellulaire", "Examens": 5, "Heures": 15},
        {"ID": 14, "Nom": "Dr. Khelifati Yasmine", "Département": "Biologie", "Spécialité": "Génétique", "Examens": 4, "Heures": 12},
        {"ID": 15, "Nom": "Dr. Mebarki Hocine", "Département": "Mathématiques", "Spécialité": "Statistiques", "Examens": 10, "Heures": 30},
    ]
    return pd.DataFrame(professors)

# ============================================
# 2. APPLICATION STREAMLIT
# ============================================

st.set_page_config(
    page_title="Système de Gestion des Examens",
    page_icon="🎓",
    layout="wide"
)

# CSS personnalisé
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 30px;
    }
    .demo-badge {
        background-color: #ff6b6b;
        color: white;
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
    }
    .stat-card {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #4CAF50;
        margin-bottom: 10px;
    }
    .config-section {
        background-color: #f0f8ff;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #d1e7ff;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# En-tête
st.markdown('<div class="main-header"><h1>🎓 Système Intelligent de Gestion des Examens Universitaires</h1><p>Version Démonstration - Projet Académique</p><span class="demo-badge">MODE DÉMO</span></div>', unsafe_allow_html=True)

# Barre latérale
with st.sidebar:
    st.header("📊 Tableau de Bord")
    
    st.markdown('<div class="stat-card">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.metric("👨‍🎓 Étudiants", "130,000")
        st.metric("📝 Examens", "1,850")
    with col2:
        st.metric("🏛️ Salles", "65")
        st.metric("👨‍🏫 Professeurs", "120")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()
    
    st.header("⚙️ Actions")
    
    if st.button("🔄 Générer Nouvel Emploi du Temps", type="primary", use_container_width=True):
        st.success("✅ Emploi du temps généré avec succès! (Simulation)")
    
    if st.button("🔍 Vérifier les Conflits", use_container_width=True):
        st.info("✅ Aucun conflit détecté (Mode démonstration)")
    
    if st.button("📤 Exporter Toutes les Données", use_container_width=True):
        st.success("📁 Données exportées! (Simulation)")
    
    st.divider()
    
    st.info("""
    **💡 À propos de cette démo:**
    Cette version utilise des données simulées.
    La version complète nécessite PostgreSQL.
    
    **🕐 Données actualisées en temps réel**
    """)

# Onglets
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📅 Examens", 
    "🏛️ Salles", 
    "👨‍🏫 Professeurs", 
    "📈 Statistiques",
    "⚙️ Configuration"
])

# Onglet 1: Examens
with tab1:
    st.header("📋 Calendrier des Examens")
    
    # Filtres
    col1, col2, col3 = st.columns(3)
    with col1:
        date_filter = st.date_input("📅 Date", datetime.date(2024, 6, 10))
    with col2:
        salle_filter = st.selectbox("🏛️ Salle", ["Toutes", "Amphi A", "Amphi B", "Amphi C", "Amphi D", 
                                                 "Salle 101", "Salle 102", "Salle 201", "Salle 202", 
                                                 "Salle 301", "Salle 302", "Labo Info 1", "Labo Info 2"])
    with col3:
        dept_filter = st.selectbox("🏢 Département", ["Tous", "Informatique", "Mathématiques", "Physique", 
                                                     "Chimie", "Droit", "Économie", "Biologie"])
    
    # Données
    df_exams = get_demo_exams()
    
    # Application des filtres
    if salle_filter != "Toutes":
        df_exams = df_exams[df_exams["Salle"] == salle_filter]
    
    if dept_filter != "Tous":
        df_exams = df_exams[df_exams["Département"] == dept_filter]
    
    # Affichage
    if not df_exams.empty:
        # Formatage des colonnes
        display_cols = ["ID", "Module", "Département", "Salle", "Date", "Durée", "Professeur", "Étudiants"]
        df_display = df_exams.rename(columns={
            "Date": "Date et Heure",
            "Durée": "Durée (min)",
            "Étudiants": "Nb. Étudiants"
        })[display_cols]
        
        st.dataframe(df_display, use_container_width=True, height=400)
        
        # Graphiques
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.subheader("📊 Examens par Jour")
            df_exams["Jour"] = pd.to_datetime(df_exams["Date"]).dt.date
            daily_counts = df_exams["Jour"].value_counts().sort_index()
            st.bar_chart(daily_counts)
        
        with col_chart2:
            st.subheader("🎯 Répartition par Département")
            dept_counts = df_exams["Département"].value_counts()
            st.bar_chart(dept_counts)
        
        # Export
        csv = df_display.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            "📥 Télécharger le Calendrier (CSV)",
            csv,
            "calendrier_examens.csv",
            "text/csv",
            key='download-exams'
        )
    else:
        st.warning("Aucun examen trouvé avec ces critères.")

# Onglet 2: Salles
with tab2:
    st.header("🏛️ Gestion des Salles d'Examen")
    
    df_rooms = get_demo_rooms()
    
    # Filtres
    col1, col2 = st.columns(2)
    with col1:
        type_filter = st.selectbox("Filtrer par Type", ["Tous", "Amphithéâtre", "Salle", "Laboratoire"])
    with col2:
        batiment_filter = st.selectbox("Filtrer par Bâtiment", ["Tous", "Principal", "Sciences", "Nouveau", 
                                                               "Bâtiment A", "Bâtiment B", "Bâtiment C",
                                                               "Informatique", "Physique", "Chimie", "Biologie"])
    
    # Application des filtres
    if type_filter != "Tous":
        df_rooms = df_rooms[df_rooms["Type"] == type_filter]
    
    if batiment_filter != "Tous":
        df_rooms = df_rooms[df_rooms["Bâtiment"] == batiment_filter]
    
    # Affichage
    st.dataframe(df_rooms, use_container_width=True)
    
    # Graphiques
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📏 Capacité des Salles")
        fig1 = px.bar(df_rooms, x='Nom', y='Capacité', 
                     color='Type', title="Distribution des Capacités",
                     hover_data=['Bâtiment', 'Examens'])
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.subheader("📊 Occupation par Bâtiment")
        building_counts = df_rooms.groupby('Bâtiment')['Examens'].sum().reset_index()
        fig2 = px.pie(building_counts, values='Examens', names='Bâtiment',
                     title="Répartition des Examens par Bâtiment")
        st.plotly_chart(fig2, use_container_width=True)

# Onglet 3: Professeurs
with tab3:
    st.header("👨‍🏫 Gestion des Professeurs")
    
    df_profs = get_demo_professors()
    
    # Filtre par département
    dept_filter = st.selectbox("Filtrer par Département", 
                              ["Tous", "Informatique", "Mathématiques", "Physique", 
                               "Chimie", "Droit", "Économie", "Biologie"])
    
    if dept_filter != "Tous":
        df_profs = df_profs[df_profs["Département"] == dept_filter]
    
    # Affichage
    st.dataframe(df_profs, use_container_width=True)
    
    # Graphiques
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Répartition par Département")
        if not df_profs.empty:
            dept_counts = df_profs["Département"].value_counts()
            st.bar_chart(dept_counts)
    
    with col2:
        st.subheader("🎯 Charge de Travail (Heures)")
        if not df_profs.empty:
            workload = df_profs[["Nom", "Heures"]].set_index("Nom")
            st.bar_chart(workload)

# Onglet 4: Statistiques
with tab4:
    st.header("📈 Tableau de Bord Complet")
    
    # Métriques principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Examens", "1,850", "+5%")
    
    with col2:
        st.metric("Taux d'Occupation", "87%", "+3%")
    
    with col3:
        st.metric("Conflits Résolus", "42", "-12%")
    
    with col4:
        st.metric("Satisfaction", "94%", "+2%")
    
    st.divider()
    
    # Données
    df_exams = get_demo_exams()
    df_rooms = get_demo_rooms()
    df_profs = get_demo_professors()
    
    # Graphiques avancés
    st.subheader("📊 Visualisations Avancées")
    
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        # Distribution des étudiants par examen
        st.subheader("👥 Distribution des Étudiants")
        
        student_dist = pd.DataFrame({
            "Tranche": ["< 50", "50-100", "100-200", "200-300", "300-400", "> 400"],
            "Nombre d'examens": [5, 8, 10, 12, 8, 2]
        })
        
        fig1 = px.bar(student_dist, x="Tranche", y="Nombre d'examens",
                      title="Nombre d'étudiants par examen",
                      color="Nombre d'examens")
        st.plotly_chart(fig1, use_container_width=True)
    
    with col_chart2:
        # Répartition des durées
        st.subheader("⏱️ Durées des Examens")
        
        durations_data = pd.DataFrame({
            "Durée (min)": [90, 120, 150, 180],
            "Nombre d'examens": [15, 45, 25, 5]
        })
        
        fig2 = px.pie(durations_data, values="Nombre d'examens", names="Durée (min)",
                      title="Répartition des Durées d'Examen",
                      hole=0.3)
        st.plotly_chart(fig2, use_container_width=True)
    
    # Tableau récapitulatif
    st.subheader("📋 Résumé Général")
    
    summary_data = {
        "Métrique": ["Examens programmés", "Salles utilisées", "Professeurs mobilisés", 
                     "Jours d'examen", "Heures totales", "Étudiants concernés"],
        "Valeur": [len(df_exams), len(df_rooms), len(df_profs), 
                   df_exams["Date"].apply(lambda x: pd.to_datetime(x).date()).nunique(),
                   df_exams["Durée"].sum() / 60,
                   df_exams["Étudiants"].sum()],
        "Unité": ["examens", "salles", "professeurs", "jours", "heures", "étudiants"]
    }
    
    summary_df = pd.DataFrame(summary_data)
    st.dataframe(summary_df, use_container_width=True)

# Onglet 5: Configuration
with tab5:
    st.header("⚙️ Configuration du Système")
    
    # Section 1: Paramètres de planification
    st.markdown('<div class="config-section">', unsafe_allow_html=True)
    st.subheader("📅 Paramètres de Planification")
    
    with st.form("config_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            start_date = st.date_input("Date de Début des Examens",
                                     datetime.date(2024, 6, 10))
            max_daily = st.slider("Examens Max par Jour", 1, 10, 4)
            min_interval = st.number_input("Intervalle Minimum (min)", 30, 180, 60)
        
        with col2:
            duration = st.selectbox("Durée par Défaut (min)",
                                  [90, 120, 150, 180], index=1)
            time_options = ["08:00", "09:00", "10:30", "13:00", "15:00", "17:00", "19:00"]
            selected_times = st.multiselect("Créneaux Horaires",
                                          time_options, default=["09:00", "13:00", "15:00"])
            auto_schedule = st.checkbox("Planification automatique", value=True)
        
        # Boutons d'action
        col_btn1, col_btn2, col_btn3 = st.columns(3)
        with col_btn1:
            save_btn = st.form_submit_button("💾 Sauvegarder", use_container_width=True)
        with col_btn2:
            reset_btn = st.form_submit_button("🔄 Réinitialiser", use_container_width=True)
        with col_btn3:
            test_btn = st.form_submit_button("🧪 Tester", use_container_width=True)
    
    if save_btn:
        st.success("✅ Configuration sauvegardée avec succès!")
    if reset_btn:
        st.info("🔄 Configuration réinitialisée aux valeurs par défaut")
    if test_btn:
        st.warning("🧪 Test en cours... (mode démonstration)")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Section 2: Maintenance
    st.markdown('<div class="config-section">', unsafe_allow_html=True)
    st.subheader("🔧 Maintenance")
    
    col_m1, col_m2 = st.columns(2)
    
    with col_m1:
        st.markdown("**Nettoyage des données**")
        
        if st.button("🧹 Effacer tous les examens", type="secondary", use_container_width=True):
            if st.checkbox("Je confirme la suppression de tous les examens"):
                st.warning("⚠️ Fonction désactivée en mode démo")
                st.info("Dans la version complète, cette action supprimerait tous les examens programmés.")
        
        if st.button("🗑️ Supprimer données obsolètes", use_container_width=True):
            st.info("📅 Suppression des données antérieures à 2023 (simulation)")
    
    with col_m2:
        st.markdown("**Sauvegarde et restauration**")
        
        if st.button("💾 Sauvegarde complète", use_container_width=True):
            st.success("✅ Sauvegarde créée: backup_2024-01-16.zip (simulation)")
        
        if st.button("📥 Restaurer sauvegarde", use_container_width=True):
            st.warning("🔄 Restauration à partir de backup_2024-01-10.zip (simulation)")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Section 3: Informations système
    st.markdown('<div class="config-section">', unsafe_allow_html=True)
    st.subheader("ℹ️ Informations Système")
    
    info_col1, info_col2 = st.columns(2)
    
    with info_col1:
        st.markdown("""
        **📊 Environnement:**
        - Mode: Démonstration
        - Version: 1.0
        - Plateforme: Streamlit Cloud
        
        **🔧 Dépendances:**
        - Python 3.10+
        - Streamlit 1.28+
        - Pandas 2.1+
        - Plotly 5.17+
        """)
    
    with info_col2:
        st.markdown("""
        **📅 Données:**
        - Type: Simulées
        - Période: Juin 2024
        - Mise à jour: Manuel
        
        **🔄 Performances:**
        - Temps chargement: < 2s
        - Données: 15 examens
        - Mémoire: Optimisée
        """)
    
    # Bouton pour rafraîchir
    if st.button("🔄 Rafraîchir toutes les données", type="primary", use_container_width=True):
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Section 4: À propos
    st.markdown('<div class="config-section">', unsafe_allow_html=True)
    st.subheader("📖 À propos")
    
    st.markdown("""
    **🎯 Système de Planification des Examens Universitaires**
    
    Ce système a été développé dans le cadre d'un projet académique pour démontrer 
    les capacités de gestion d'examens à grande échelle.
    
    **Fonctionnalités clés:**
    - Gestion de 130,000 étudiants
    - Planification intelligente
    - Détection de conflits
    - Interface web moderne
    
    **Version complète disponible sur GitHub avec:**
    - Base de données PostgreSQL
    - Scripts SQL complets
    - Authentification multi-utilisateur
    - Export PDF/Excel
    """)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Pied de page
st.divider()
st.markdown("""
<div style='text-align: center; padding: 20px; background-color: #f0f2f6; border-radius: 10px;'>
    <h3>🔧 Système de Planification des Examens Universitaires</h3>
    <p><strong>Version Démonstration 1.0</strong> | Projet Académique</p>
    <p>📊 Gestion de 130,000 étudiants | 🏛️ 65 salles d'examen | 👨‍🏫 120 professeurs</p>
    <p>🚀 <strong>Développé avec:</strong> Python • Streamlit • Plotly • Pandas</p>
    <hr style='margin: 10px 0;'>
    <p style='font-size: 14px; color: #666;'>
        ⚠️ <strong>Note importante:</strong> Cette version utilise des données simulées pour la démonstration.<br>
        La version complète du projet nécessite l'installation de PostgreSQL localement.
    </p>
</div>
""", unsafe_allow_html=True)

# Section pour la version complète
with st.expander("📖 À propos de la Version Complète", expanded=False):
    st.markdown("""
    ### 🎯 Version Complète du Projet
    
    **🌟 Fonctionnalités Complètes:**
    
    1. **Base de données PostgreSQL avancée:**
       - 130,000 étudiants réels
       - 200+ formations
       - 900,000 inscriptions
       - Planification intelligente
    
    2. **Fonctionnalités intelligentes:**
       - Génération automatique des emplois du temps
       - Détection de conflits en temps réel
       - Optimisation des ressources
       - Alertes intelligentes
    
    3. **Interface web complète:**
       - Tableau de bord interactif
       - Rapports détaillés
       - Export Excel/CSV/PDF
       - Authentification multi-niveaux
    
    **🔧 Installation de la Version Complète:**
    
    ```bash
    # 1. Cloner le projet
    git clone https://github.com/VOTRE_NOM/university-exam-system.git
    
    # 2. Installer PostgreSQL
    # Télécharger depuis: https://www.postgresql.org/download/
    
    # 3. Créer la base de données
    psql -U postgres -c "CREATE DATABASE university_exams;"
    
    # 4. Exécuter les scripts SQL
    psql -U postgres -d university_exams -f SQL/install_all.sql
    
    # 5. Installer les dépendances
    pip install -r requirements.txt
    
    # 6. Lancer l'application
    streamlit run app.py
    ```
    
    **📞 Support et Documentation:**
    - Documentation complète dans README.md
    - Scripts SQL prêts à l'emploi
    - Interface administrateur complète
    - Système de sauvegarde automatique
    
    **🔗 Lien GitHub:** `https://github.com/VOTRE_NOM/university-exam-system`
    """)

st.success("✅ Application de démonstration chargée avec succès!")