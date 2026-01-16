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
        {"ID": 1, "Module": "Base de données", "Salle": "Amphi A", "Date": "2024-06-10 09:00", "Durée": 120, "Professeur": "Dr. Benali", "Étudiants": 450},
        {"ID": 2, "Module": "Algorithmique", "Salle": "Salle 101", "Date": "2024-06-10 13:00", "Durée": 120, "Professeur": "Dr. Kadri", "Étudiants": 28},
        {"ID": 3, "Module": "Réseaux", "Salle": "Amphi B", "Date": "2024-06-11 09:00", "Durée": 120, "Professeur": "Dr. Mansouri", "Étudiants": 320},
        {"ID": 4, "Module": "Programmation Python", "Salle": "Labo Info 1", "Date": "2024-06-11 13:00", "Durée": 120, "Professeur": "Dr. Bouguerra", "Étudiants": 18},
        {"ID": 5, "Module": "Sécurité", "Salle": "Salle 102", "Date": "2024-06-12 09:00", "Durée": 120, "Professeur": "Dr. Saidi", "Étudiants": 22},
        {"ID": 6, "Module": "Intelligence Artificielle", "Salle": "Amphi A", "Date": "2024-06-12 13:00", "Durée": 120, "Professeur": "Dr. Benali", "Étudiants": 480},
        {"ID": 7, "Module": "Développement Web", "Salle": "Salle 201", "Date": "2024-06-13 09:00", "Durée": 120, "Professeur": "Dr. Kadri", "Étudiants": 35},
        {"ID": 8, "Module": "Systèmes d'exploitation", "Salle": "Amphi C", "Date": "2024-06-13 13:00", "Durée": 120, "Professeur": "Dr. Mansouri", "Étudiants": 280},
        {"ID": 9, "Module": "Mathématiques", "Salle": "Amphi A", "Date": "2024-06-14 09:00", "Durée": 120, "Professeur": "Dr. Bouguerra", "Étudiants": 420},
        {"ID": 10, "Module": "Physique", "Salle": "Amphi B", "Date": "2024-06-14 13:00", "Durée": 120, "Professeur": "Dr. Saidi", "Étudiants": 300},
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
        {"Nom": "Salle 301", "Capacité": 50, "Type": "Salle", "Bâtiment": "Bâtiment C", "Examens": 14},
        {"Nom": "Amphi D", "Capacité": 400, "Type": "Amphithéâtre", "Bâtiment": "Nouveau", "Examens": 5},
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
        {"ID": 9, "Nom": "Dr. Haddad Rachid", "Département": "Droit", "Spécialité": "Droit Civil", "Examens": 9},
        {"ID": 10, "Nom": "Dr. Belkacem Soraya", "Département": "Droit", "Spécialité": "Droit Commercial", "Examens": 8},
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
        st.success("Emploi du temps généré avec succès! (Simulation)")
    
    if st.button("🔍 Vérifier les Conflits", use_container_width=True):
        st.info("✅ Aucun conflit détecté (Mode démonstration)")
    
    if st.button("📤 Exporter Toutes les Données", use_container_width=True):
        st.success("Données exportées! (Simulation)")
    
    st.divider()
    
    st.info("""
    **💡 À propos de cette démo:**
    Cette version utilise des données simulées.
    La version complète nécessite PostgreSQL.
    
    **🕐 Données actualisées en temps réel**
    """)

# Onglets
tab1, tab2, tab3, tab4 = st.tabs(["📅 Examens", "🏛️ Salles", "👨‍🏫 Professeurs", "📈 Statistiques"])

# Onglet 1: Examens
with tab1:
    st.header("📋 Calendrier des Examens")
    
    # Filtres
    col1, col2, col3 = st.columns(3)
    with col1:
        date_filter = st.date_input("📅 Date", datetime.date(2024, 6, 10))
    with col2:
        salle_filter = st.selectbox("🏛️ Salle", ["Toutes", "Amphi A", "Amphi B", "Amphi C", "Salle 101", "Salle 102", "Labo Info 1"])
    with col3:
        prof_filter = st.selectbox("👨‍🏫 Professeur", ["Tous", "Dr. Benali Ahmed", "Dr. Kadri Fatima", "Dr. Mansouri Karim"])
    
    # Données
    df_exams = get_demo_exams()
    
    # Application des filtres
    if salle_filter != "Toutes":
        df_exams = df_exams[df_exams["Salle"] == salle_filter]
    
    if prof_filter != "Tous":
        df_exams = df_exams[df_exams["Professeur"] == prof_filter]
    
    # Affichage
    if not df_exams.empty:
        st.dataframe(df_exams, use_container_width=True, height=350)
        
        # Graphiques
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.subheader("📊 Examens par Jour")
            df_exams["Jour"] = pd.to_datetime(df_exams["Date"]).dt.date
            daily_counts = df_exams["Jour"].value_counts().sort_index()
            st.bar_chart(daily_counts)
        
        with col_chart2:
            st.subheader("🎯 Occupation des Salles")
            room_counts = df_exams["Salle"].value_counts()
            st.bar_chart(room_counts)
        
        # Export
        csv = df_exams.to_csv(index=False).encode('utf-8-sig')
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
    
    # Filtre par type
    type_filter = st.selectbox("Filtrer par Type", ["Tous", "Amphithéâtre", "Salle", "Laboratoire"])
    
    if type_filter != "Tous":
        df_rooms = df_rooms[df_rooms["Type"] == type_filter]
    
    st.dataframe(df_rooms, use_container_width=True)
    
    # Graphiques
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📏 Capacité des Salles")
        fig1 = px.bar(df_rooms, x='Nom', y='Capacité', 
                     color='Type', title="Distribution des Capacités")
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
                              ["Tous", "Informatique", "Mathématiques", "Physique", "Chimie", "Droit"])
    
    if dept_filter != "Tous":
        df_profs = df_profs[df_profs["Département"] == dept_filter]
    
    st.dataframe(df_profs, use_container_width=True)
    
    # Graphiques
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Répartition par Département")
        if not df_profs.empty:
            dept_counts = df_profs["Département"].value_counts()
            st.bar_chart(dept_counts)
    
    with col2:
        st.subheader("🎯 Charge de Travail")
        if not df_profs.empty:
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
    
    # Données pour les graphiques
    df_exams = get_demo_exams()
    df_rooms = get_demo_rooms()
    df_profs = get_demo_professors()
    
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        # Heatmap simplifié (بدون matplotlib)
        st.subheader("🗓️ Calendrier d'Occupation")
        
        # جدول بسيط بدلاً من heatmap
        dates = ["2024-06-10", "2024-06-11", "2024-06-12", "2024-06-13"]
        rooms = ["Amphi A", "Amphi B", "Salle 101", "Salle 102", "Labo Info 1"]
        
        # إنشاء جدول بيانات بسيط
        import random
        schedule_data = []
        for room in rooms:
            row = {"Salle": room}
            for date in dates:
                row[date] = random.randint(0, 3)
            schedule_data.append(row)
        
        schedule_df = pd.DataFrame(schedule_data)
        st.dataframe(schedule_df.set_index("Salle"), use_container_width=True)
    
    with col_chart2:
        # Distribution des durées (بدون matplotlib)
        st.subheader("⏱️ Distribution des Durées")
        
        durations_data = pd.DataFrame({
            "Durée (min)": [90, 120, 150, 180],
            "Nombre d'examens": [15, 45, 25, 5]
        })
        
        fig = px.bar(durations_data, x="Durée (min)", y="Nombre d'examens",
                    title="Répartition des Durées d'Examen")
        st.plotly_chart(fig, use_container_width=True)

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