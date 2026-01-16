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
        {"ID": 9, "Module": "Mathématiques", "Salle": "Amphi A", "Date": "2024-06-14 09:00", "Durée": 120, "Professeur": "Dr. Bouguerra", "Étudiants": 420, "Département": "Mathématiques"},
        {"ID": 10, "Module": "Physique", "Salle": "Amphi B", "Date": "2024-06-14 13:00", "Durée": 120, "Professeur": "Dr. Saidi", "Étudiants": 300, "Département": "Physique"},
    ]
    return pd.DataFrame(exams)

def get_demo_rooms():
    """Retourne des données de salles de démonstration"""
    rooms = [
        {"Nom": "Amphi A", "Capacité": 500, "Type": "Amphithéâtre", "Bâtiment": "Principal", "Examens": 12},
        {"Nom": "Amphi B", "Capacité": 350, "Type": "Amphithéâtre", "Bâtiment": "Principal", "Examens": 8},
        {"Nom": "Amphi C", "Capacité": 300, "Type": "Amphithéâtre", "Bâtiment": "Sciences", "Examens": 6},
        {"Nom": "Salle 101", "Capacité": 30, "Type": "Salle", "Bâtiment": "Bâtiment A", "Examens": 15},
        {"Nom": "Salle 102", "Capacité": 25, "Type": "Salle", "Bâtiment": "Bâtiment A", "Examens": 10},
        {"Nom": "Salle 201", "Capacité": 40, "Type": "Salle", "Bâtiment": "Bâtiment B", "Examens": 18},
        {"Nom": "Labo Info 1", "Capacité": 20, "Type": "Laboratoire", "Bâtiment": "Informatique", "Examens": 22},
        {"Nom": "Labo Info 2", "Capacité": 20, "Type": "Laboratoire", "Bâtiment": "Informatique", "Examens": 20},
    ]
    return pd.DataFrame(rooms)

def get_demo_professors():
    """Retourne des données de professeurs de démonstration"""
    professors = [
        {"ID": 1, "Nom": "Dr. Benali Ahmed", "Département": "Informatique", "Spécialité": "Base de données", "Examens": 15},
        {"ID": 2, "Nom": "Dr. Kadri Fatima", "Département": "Informatique", "Spécialité": "Algorithmique", "Examens": 12},
        {"ID": 3, "Nom": "Dr. Mansouri Karim", "Département": "Informatique", "Spécialité": "Réseaux", "Examens": 10},
        {"ID": 4, "Nom": "Dr. Bouguerra Nadia", "Département": "Mathématiques", "Spécialité": "Analyse", "Examens": 8},
        {"ID": 5, "Nom": "Dr. Saidi Mohamed", "Département": "Physique", "Spécialité": "Mécanique", "Examens": 6},
        {"ID": 6, "Nom": "Dr. Boukhatem Leïla", "Département": "Physique", "Spécialité": "Optique", "Examens": 7},
        {"ID": 7, "Nom": "Dr. Cherif Yacine", "Département": "Chimie", "Spécialité": "Chimie Organique", "Examens": 5},
        {"ID": 8, "Nom": "Dr. Zitouni Samira", "Département": "Chimie", "Spécialité": "Chimie Analytique", "Examens": 4},
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
    
    if st.button("🔄 Générer Emploi du Temps", type="primary", use_container_width=True):
        st.success("✅ Emploi du temps généré avec succès! (Simulation)")
    
    if st.button("🔍 Vérifier les Conflits", use_container_width=True):
        st.info("✅ Aucun conflit détecté (Mode démonstration)")
    
    if st.button("📤 Exporter les Données", use_container_width=True):
        st.success("📁 Données exportées! (Simulation)")
    
    st.divider()
    
    st.info("""
    **💡 À propos de cette démo:**
    Cette version utilise des données simulées.
    La version complète nécessite PostgreSQL.
    
    **Données actualisées en temps réel**
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
        salle_filter = st.selectbox("🏛️ Salle", ["Toutes", "Amphi A", "Amphi B", "Amphi C", "Salle 101", "Salle 102", "Salle 201", "Labo Info 1"])
    with col3:
        dept_filter = st.selectbox("🏢 Département", ["Tous", "Informatique", "Mathématiques", "Physique", "Chimie"])
    
    # Données
    df_exams = get_demo_exams()
    
    # Application des filtres
    if salle_filter != "Toutes":
        df_exams = df_exams[df_exams["Salle"] == salle_filter]
    
    if dept_filter != "Tous":
        df_exams = df_exams[df_exams["Département"] == dept_filter]
    
    # Affichage
    if not df_exams.empty:
        # Formatage
        df_display = df_exams.copy()
        df_display = df_display.rename(columns={
            "Date": "Date et Heure",
            "Durée": "Durée (min)",
            "Étudiants": "Nb. Étudiants"
        })
        
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
            "📥 Télécharger CSV",
            csv,
            "calendrier_examens.csv",
            "text/csv"
        )
    else:
        st.warning("Aucun examen trouvé avec ces critères.")

# Onglet 2: Salles
with tab2:
    st.header("🏛️ Gestion des Salles d'Examen")
    
    df_rooms = get_demo_rooms()
    
    # Filtre par type
    type_filter = st.selectbox("Filtrer par Type", ["Tous", "Amphithéâtre", "Salle", "Laboratoire"])
    
    if type_filter != "Tous":
        df_rooms = df_rooms[df_rooms["Type"] == type_filter]
    
    # Affichage
    st.dataframe(df_rooms, use_container_width=True)
    
    # Graphiques
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📏 Capacité des Salles")
        fig1 = px.bar(df_rooms, x='Nom', y='Capacité', 
                     color='Type', title="Distribution des Capacités")
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.subheader("📊 Occupation")
        room_usage = df_rooms[["Nom", "Examens"]].set_index("Nom")
        st.bar_chart(room_usage)

# Onglet 3: Professeurs
with tab3:
    st.header("👨‍🏫 Gestion des Professeurs")
    
    df_profs = get_demo_professors()
    
    # Filtre par département
    dept_filter = st.selectbox("Filtrer par Département", 
                              ["Tous", "Informatique", "Mathématiques", "Physique", "Chimie"])
    
    if dept_filter != "Tous":
        df_profs = df_profs[df_profs["Département"] == dept_filter]
    
    # Affichage
    st.dataframe(df_profs, use_container_width=True)
    
    # Graphiques
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Répartition par Département")
        dept_counts = df_profs["Département"].value_counts()
        st.bar_chart(dept_counts)
    
    with col2:
        st.subheader("🎯 Charge de Travail")
        workload = df_profs[["Nom", "Examens"]].set_index("Nom")
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
    
    # Graphiques avancés
    st.subheader("📊 Visualisations Avancées")
    
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        # Distribution des étudiants
        st.subheader("👥 Répartition des Étudiants")
        student_data = pd.DataFrame({
            "Tranche": ["< 50", "50-100", "100-200", "200-300", "300-400", "> 400"],
            "Examens": [5, 8, 10, 12, 8, 2]
        })
        fig1 = px.bar(student_data, x="Tranche", y="Examens", title="Nombre d'étudiants par examen")
        st.plotly_chart(fig1, use_container_width=True)
    
    with col_chart2:
        # Répartition des durées
        st.subheader("⏱️ Durées des Examens")
        duration_data = pd.DataFrame({
            "Durée (min)": [90, 120, 150, 180],
            "Examens": [15, 45, 25, 5]
        })
        fig2 = px.pie(duration_data, values="Examens", names="Durée (min)", title="Répartition des Durées")
        st.plotly_chart(fig2, use_container_width=True)
    
    # Résumé
    st.subheader("📋 Résumé Général")
    
    summary_data = {
        "Métrique": ["Examens programmés", "Salles utilisées", "Professeurs mobilisés", "Jours d'examen"],
        "Valeur": [len(get_demo_exams()), len(get_demo_rooms()), len(get_demo_professors()), 5]
    }
    
    st.table(pd.DataFrame(summary_data))

# Onglet 5: Configuration
with tab5:
    st.header("⚙️ Configuration du Système")
    
    # Section 1: Paramètres
    st.markdown('<div class="config-section">', unsafe_allow_html=True)
    st.subheader("📅 Paramètres de Planification")
    
    with st.form("config_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            start_date = st.date_input("Date de Début des Examens", datetime.date(2024, 6, 10))
            max_daily = st.slider("Examens Max par Jour", 1, 10, 4)
        
        with col2:
            duration = st.selectbox("Durée par Défaut (min)", [90, 120, 150, 180], index=1)
            time_options = ["08:00", "09:00", "10:30", "13:00", "15:00", "17:00"]
            selected_times = st.multiselect("Créneaux Horaires", time_options, default=["09:00", "13:00", "15:00"])
        
        # Boutons
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            save_btn = st.form_submit_button("💾 Sauvegarder", use_container_width=True)
        with col_btn2:
            reset_btn = st.form_submit_button("🔄 Réinitialiser", use_container_width=True)
    
    if save_btn:
        st.success("✅ Configuration sauvegardée!")
    if reset_btn:
        st.info("🔄 Configuration réinitialisée")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Section 2: Maintenance
    st.markdown('<div class="config-section">', unsafe_allow_html=True)
    st.subheader("🔧 Maintenance")
    
    col_m1, col_m2 = st.columns(2)
    
    with col_m1:
        if st.button("🧹 Effacer données", type="secondary", use_container_width=True):
            st.warning("⚠️ Fonction désactivée en mode démo")
    
    with col_m2:
        if st.button("💾 Sauvegarde", use_container_width=True):
            st.success("✅ Sauvegarde créée (simulation)")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Section 3: Informations
    st.markdown('<div class="config-section">', unsafe_allow_html=True)
    st.subheader("ℹ️ Informations Système")
    
    st.info("""
    **📊 Environnement:**
    - Mode: Démonstration
    - Version: 1.0
    - Plateforme: Streamlit Cloud
    
    **🔧 Dépendances:**
    - Python 3.10+
    - Streamlit 1.28+
    - Pandas 2.1+
    - Plotly 5.17+
    
    **📅 Données:**
    - Type: Simulées
    - Période: Juin 2024
    - Mise à jour: Manuel
    """)
    
    # Bouton rafraîchir
    if st.button("🔄 Rafraîchir l'application", type="primary", use_container_width=True):
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Section 4: À propos
    st.markdown('<div class="config-section">', unsafe_allow_html=True)
    st.subheader("📖 À propos")
    
    st.markdown("""
    **🎯 Système de Planification des Examens Universitaires**
    
    Projet académique démontrant les capacités de gestion d'examens à grande échelle.
    
    **Fonctionnalités:**
    - Gestion de 130,000 étudiants
    - Planification intelligente
    - Détection de conflits
    - Interface web moderne
    
    **Version complète sur GitHub avec PostgreSQL**
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
        ⚠️ <strong>Note:</strong> Version démo avec données simulées.<br>
        Version complète nécessite PostgreSQL local.
    </p>
</div>
""", unsafe_allow_html=True)

# Section version complète
with st.expander("📖 À propos de la Version Complète"):
    st.markdown("""
    ### 🎯 Version Complète du Projet
    
    **Fonctionnalités Complètes:**
    1. Base de données PostgreSQL
    2. 130,000 étudiants réels
    3. Génération automatique
    4. Détection de conflits
    
    **Installation:**
    ```bash
    git clone https://github.com/VOTRE_NOM/university-exam-system.git
    pip install -r requirements.txt
    # Installer PostgreSQL
    streamlit run app.py
    ```
    """)

st.success("✅ Application chargée avec succès!")