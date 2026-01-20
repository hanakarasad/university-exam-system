import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
import numpy as np
import hashlib 

# ============================================
# 1. DONNÉES DE DÉMONSTRATION
# ============================================

def get_demo_exams():
    """Retourne des données d'examens de démonstration"""
    exams = [
        {"ID": 1, "Module": "Base de données", "Salle": "Amphi A", "Date": "2024-06-10 09:00", "Durée": 120, "Professeur": "Dr. Benali", "Étudiants": 450, "Département": "Informatique", "Formation": "Licence Info"},
        {"ID": 2, "Module": "Algorithmique", "Salle": "Salle 101", "Date": "2024-06-10 13:00", "Durée": 120, "Professeur": "Dr. Kadri", "Étudiants": 28, "Département": "Informatique", "Formation": "Licence Info"},
        {"ID": 3, "Module": "Réseaux", "Salle": "Amphi B", "Date": "2024-06-11 09:00", "Durée": 120, "Professeur": "Dr. Mansouri", "Étudiants": 320, "Département": "Informatique", "Formation": "Master Info"},
        {"ID": 4, "Module": "Programmation Python", "Salle": "Labo Info 1", "Date": "2024-06-11 13:00", "Durée": 120, "Professeur": "Dr. Bouguerra", "Étudiants": 18, "Département": "Informatique", "Formation": "Licence Info"},
        {"ID": 5, "Module": "Sécurité", "Salle": "Salle 102", "Date": "2024-06-12 09:00", "Durée": 120, "Professeur": "Dr. Saidi", "Étudiants": 22, "Département": "Informatique", "Formation": "Master Sécurité"},
        {"ID": 6, "Module": "Mathématiques", "Salle": "Amphi A", "Date": "2024-06-12 13:00", "Durée": 120, "Professeur": "Dr. Bouguerra", "Étudiants": 420, "Département": "Mathématiques", "Formation": "Licence Maths"},
        {"ID": 7, "Module": "Physique", "Salle": "Amphi B", "Date": "2024-06-13 09:00", "Durée": 120, "Professeur": "Dr. Saidi", "Étudiants": 300, "Département": "Physique", "Formation": "Licence Physique"},
        {"ID": 8, "Module": "Chimie", "Salle": "Labo Chimie 1", "Date": "2024-06-13 13:00", "Durée": 120, "Professeur": "Dr. Cherif", "Étudiants": 25, "Département": "Chimie", "Formation": "Licence Chimie"},
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
        {"Nom": "Labo Chimie 1", "Capacité": 15, "Type": "Laboratoire", "Bâtiment": "Chimie", "Examens": 7},
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
        {"ID": 6, "Nom": "Dr. Cherif Yacine", "Département": "Chimie", "Spécialité": "Chimie Organique", "Examens": 5},
    ]
    return pd.DataFrame(professors)

# ============================================
# 2. SYSTÈME D'AUTHENTIFICATION
# ============================================

def init_session():
    """Initialiser la session"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user_info' not in st.session_state:
        st.session_state.user_info = {}

def hash_password(password):
    """Hasher le mot de passe"""
    return hashlib.sha256(password.encode()).hexdigest()

# Utilisateurs prédéfinis avec rôles
USERS = {
    "ADM001": {
        "password": hash_password("admin123"),
        "role": "admin",
        "nom": "Administrateur",
        "prenom": "Système",
        "departement": "Administration"
    },
    "PROF001": {
        "password": hash_password("prof123"),
        "role": "professeur",
        "nom": "Benali",
        "prenom": "Ahmed",
        "departement": "Informatique"
    },
    "ETUD001": {
        "password": hash_password("etud123"),
        "role": "etudiant",
        "nom": "Kadri",
        "prenom": "Fatima",
        "departement": "Informatique",
        "formation": "Licence Informatique"
    }
}

def authenticate(matricule, password):
    """Authentifier l'utilisateur"""
    hashed_pw = hash_password(password)
    if matricule in USERS and USERS[matricule]["password"] == hashed_pw:
        return USERS[matricule]
    return None

# ============================================
# 3. PAGE DE CONNEXION
# ============================================

def login_page():
    """Page de connexion"""
    st.set_page_config(page_title="Connexion", page_icon="🔐", layout="centered")
    
    st.markdown("""
    <style>
    .login-container {
        max-width: 450px;
        margin: 50px auto;
        padding: 40px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        color: white;
        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
    }
    .login-title {
        text-align: center;
        margin-bottom: 30px;
        font-size: 28px;
    }
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        height: 45px;
        font-weight: bold;
    }
    .demo-accounts {
        background: rgba(255,255,255,0.1);
        padding: 15px;
        border-radius: 10px;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    
    # Logo et titre
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("https://cdn-icons-png.flaticon.com/512/2232/2232688.png", width=80)
    
    st.markdown('<h2 class="login-title">🔐 Connexion au Système</h2>', unsafe_allow_html=True)
    
    # Formulaire de connexion
    with st.form("login_form"):
        matricule = st.text_input("🎓 Numéro Matricule", placeholder="Ex: ADM001, PROF001, ETUD001")
        password = st.text_input("🔑 Mot de passe", type="password", placeholder="Votre mot de passe")
        
        submit = st.form_submit_button("🚀 Se Connecter", use_container_width=True)
    
    # Validation
    if submit:
        if matricule and password:
            user = authenticate(matricule, password)
            if user:
                st.session_state.authenticated = True
                st.session_state.user_info = {
                    "matricule": matricule,
                    **user
                }
                st.success(f"✅ Bienvenue {user['prenom']} {user['nom']}!")
                st.rerun()
            else:
                st.error("❌ Matricule ou mot de passe incorrect")
        else:
            st.warning("⚠️ Veuillez remplir tous les champs")
    
    # Comptes de démonstration
    with st.expander("📋 Comptes de démonstration", expanded=True):
        st.markdown("""
        <div class="demo-accounts">
        <table style="width:100%; color:white;">
        <tr>
            <th>Matricule</th>
            <th>Mot de passe</th>
            <th>Rôle</th>
        </tr>
        <tr><td>ADM001</td><td>admin123</td><td>Administrateur</td></tr>
        <tr><td>PROF001</td><td>prof123</td><td>Professeur</td></tr>
        <tr><td>ETUD001</td><td>etud123</td><td>Étudiant</td></tr>
        </table>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div style="text-align:center; margin-top:30px; color:#666;">
    <p>Système de Gestion des Examens Universitaires - Version 2.0</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# 4. APPLICATION PRINCIPALE
# ============================================

def main_app():
    """Application principale après authentification"""
    
    st.set_page_config(
        page_title="Système de Gestion des Examens",
        page_icon="🎓",
        layout="wide"
    )
    
    # CSS personnalisé
    st.markdown("""
    <style>
    .user-info-card {
        background: linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    .role-badge {
        display: inline-block;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 14px;
    }
    .badge-admin { background: #ff6b6b; color: white; }
    .badge-prof { background: #4ecdc4; color: white; }
    .badge-etud { background: #45b7d1; color: white; }
    .stat-card {
        background: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #4CAF50;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Récupérer les infos utilisateur
    user_info = st.session_state.user_info
    role = user_info.get('role', 'etudiant')
    badge_class = f"badge-{role}"
    
    # En-tête avec informations utilisateur
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        st.title(f"🎓 Système de Gestion des Examens")
        st.markdown(f"""
        <div class="user-info-card">
        <h3>👤 {user_info['prenom']} {user_info['nom']}</h3>
        <p><strong>🎓 Matricule:</strong> {user_info['matricule']}</p>
        <p><strong>🏢 Département:</strong> {user_info.get('departement', 'Non spécifié')}</p>
        <span class="role-badge {badge_class}">{role.upper()}</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        if st.button("🚪 Déconnexion", type="secondary", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user_info = {}
            st.rerun()
    
    # ============================================
    # BARRE LATÉRALE SELON LE RÔLE
    # ============================================
    
    with st.sidebar:
        st.header(f"⚙️ Panneau {role.title()}")
        
        if role == 'admin':
            st.markdown('<div class="stat-card">', unsafe_allow_html=True)
            col_s1, col_s2 = st.columns(2)
            with col_s1:
                st.metric("👨‍🎓 Étudiants", "130,000")
                st.metric("📝 Examens", "1,850")
            with col_s2:
                st.metric("🏛️ Salles", "65")
                st.metric("👨‍🏫 Profs", "120")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.divider()
            
            if st.button("🚀 Générer Emploi du Temps", type="primary", use_container_width=True):
                st.success("✅ Emploi du temps généré! (Simulation)")
            
            if st.button("🔍 Vérifier Conflits", use_container_width=True):
                st.info("✅ Aucun conflit détecté! (Simulation)")
        
        elif role == 'professeur':
            st.markdown('<div class="stat-card">', unsafe_allow_html=True)
            st.metric("Mes Examens", "15")
            st.metric("Heures/Semaine", "25")
            st.metric("Étudiants", "450")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.divider()
            
            if st.button("📋 Mes Examens", use_container_width=True):
                st.success("✅ Affichage de vos examens")
            
            if st.button("📊 Mes Statistiques", use_container_width=True):
                st.info("📈 Statistiques chargées")
        
        elif role == 'etudiant':
            st.markdown('<div class="stat-card">', unsafe_allow_html=True)
            st.metric("Mes Examens", "8")
            st.metric("Moyenne", "14.5/20")
            st.metric("Crédits", "45/60")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.divider()
            
            if st.button("📅 Mon Calendrier", use_container_width=True):
                st.success("📅 Calendrier chargé")
            
            if st.button("📊 Mes Résultats", use_container_width=True):
                st.info("📄 Résultats affichés")
        
        st.divider()
        st.caption(f"Connecté en tant que {role.title()}")

    # ============================================
    # ONGLETS SELON LE RÔLE
    # ============================================
    
    if role == 'admin':
        # Admin: Tous les onglets
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📅 Tous les Examens", 
            "🏛️ Gestion Salles", 
            "👨‍🏫 Gestion Profs", 
            "📈 Statistiques",
            "⚙️ Configuration"
        ])
        
        with tab1:
            st.header("📋 Calendrier Complet des Examens")
            df_exams = get_demo_exams()
            st.dataframe(df_exams, use_container_width=True, height=400)
            
            # Graphique
            st.subheader("📊 Distribution par Département")
            dept_counts = df_exams["Département"].value_counts()
            st.bar_chart(dept_counts)
        
        with tab2:
            st.header("🏛️ Gestion des Salles")
            df_rooms = get_demo_rooms()
            st.dataframe(df_rooms, use_container_width=True)
        
        with tab3:
            st.header("👨‍🏫 Gestion des Professeurs")
            df_profs = get_demo_professors()
            st.dataframe(df_profs, use_container_width=True)
        
        with tab4:
            st.header("📈 Tableau de Bord Admin")
            col1, col2, col3, col4 = st.columns(4)
            with col1: st.metric("Examens Aujourd'hui", "15", "+2")
            with col2: st.metric("Salles Occupées", "87%", "+3%")
            with col3: st.metric("Alertes", "3", "-1")
            with col4: st.metric("Satisfaction", "94%", "+2%")
        
        with tab5:
            st.header("⚙️ Configuration Système")
            with st.form("admin_config"):
                start_date = st.date_input("Date Début Examens", datetime.date(2024, 6, 10))
                max_daily = st.slider("Examens Max/Jour", 1, 10, 4)
                if st.form_submit_button("💾 Sauvegarder"):
                    st.success("Configuration sauvegardée!")
    
    elif role == 'professeur':
        # Professeur: Onglets spécifiques
        tab1, tab2, tab3 = st.tabs(["📅 Mes Examens", "👥 Mes Étudiants", "📊 Mes Statistiques"])
        
        with tab1:
            st.header("📅 Mes Examens Programmés")
            # Filtrer les examens du professeur
            df_all = get_demo_exams()
            df_my_exams = df_all[df_all["Professeur"].str.contains(user_info['nom'])]
            
            if not df_my_exams.empty:
                st.dataframe(df_my_exams, use_container_width=True)
                
                # Prochain examen
                next_exam = df_my_exams.iloc[0] if len(df_my_exams) > 0 else None
                if next_exam is not None:
                    st.info(f"**Prochain examen:** {next_exam['Module']} le {next_exam['Date']}")
            else:
                st.info("Aucun examen programmé pour vous.")
        
        with tab2:
            st.header("👥 Mes Étudiants")
            # Simulation d'étudiants
            etudiants = [
                {"Matricule": "ETUD001", "Nom": "Kadri", "Prénom": "Fatima", "Note": "16/20"},
                {"Matricule": "ETUD002", "Nom": "Mansouri", "Prénom": "Karim", "Note": "14/20"},
                {"Matricule": "ETUD003", "Nom": "Bouguerra", "Prénom": "Nadia", "Note": "18/20"},
            ]
            st.dataframe(pd.DataFrame(etudiants), use_container_width=True)
        
        with tab3:
            st.header("📊 Mes Statistiques")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Heures d'examens", "45h")
                st.metric("Nombre d'étudiants", "450")
            with col2:
                st.metric("Moyenne des notes", "14.8/20")
                st.metric("Taux de réussite", "92%")
    
    elif role == 'etudiant':
        # Étudiant: Onglets simples
        tab1, tab2, tab3 = st.tabs(["📅 Mes Examens", "📊 Mes Notes", "ℹ️ Mon Profil"])
        
        with tab1:
            st.header("📅 Mon Calendrier d'Examens")
            # Simulation d'examens pour l'étudiant
            mes_examens = [
                {"Module": "Base de données", "Date": "2024-06-10 09:00", "Salle": "Amphi A", "Professeur": "Dr. Benali"},
                {"Module": "Algorithmique", "Date": "2024-06-10 13:00", "Salle": "Salle 101", "Professeur": "Dr. Kadri"},
                {"Module": "Réseaux", "Date": "2024-06-11 09:00", "Salle": "Amphi B", "Professeur": "Dr. Mansouri"},
            ]
            
            df_mes_examens = pd.DataFrame(mes_examens)
            st.dataframe(df_mes_examens, use_container_width=True)
            
            # Prochain examen
            if not df_mes_examens.empty:
                prochain = df_mes_examens.iloc[0]
                st.success(f"**Prochain examen:** {prochain['Module']} - {prochain['Date']}")
        
        with tab2:
            st.header("📊 Mes Résultats")
            notes = [
                {"Module": "Base de données", "Note": "16/20", "Crédits": "6"},
                {"Module": "Algorithmique", "Note": "14/20", "Crédits": "5"},
                {"Module": "Réseaux", "Note": "15/20", "Crédits": "6"},
                {"Module": "Mathématiques", "Note": "13/20", "Crédits": "4"},
            ]
            
            df_notes = pd.DataFrame(notes)
            st.dataframe(df_notes, use_container_width=True)
            
            # Graphique
            st.subheader("📈 Évolution des Notes")
            fig = px.bar(df_notes, x='Module', y='Note', title="Mes Notes par Module")
            st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            st.header("ℹ️ Mon Profil")
            col1, col2 = st.columns(2)
            
            with col1:
                st.info(f"""
                **Informations Personnelles:**
                - Nom: {user_info['nom']}
                - Prénom: {user_info['prenom']}
                - Matricule: {user_info['matricule']}
                - Formation: {user_info.get('formation', 'Licence Informatique')}
                - Département: {user_info.get('departement', 'Informatique')}
                """)
            
            with col2:
                st.subheader("Changer le mot de passe")
                with st.form("change_pass"):
                    current = st.text_input("Mot de passe actuel", type="password")
                    new = st.text_input("Nouveau mot de passe", type="password")
                    confirm = st.text_input("Confirmer", type="password")
                    
                    if st.form_submit_button("💾 Mettre à jour"):
                        st.success("✅ Mot de passe changé (simulation)")
    
    # ============================================
    # PIED DE PAGE
    # ============================================
    
    st.divider()
    
    if role == 'admin':
        st.caption("""
        ⚠️ **Système de Gestion des Examens - Version Admin 2.0**  
        📊 Gestion complète de 130,000 étudiants | 🏛️ 65 salles | 👨‍🏫 120 professeurs  
        🔧 Développé avec: Python • Streamlit • PostgreSQL
        """)
    elif role == 'professeur':
        st.caption("""
        👨‍🏫 **Interface Professeur - Système de Gestion des Examens**  
        📅 Planification d'examens | 👥 Gestion d'étudiants | 📊 Suivi des résultats
        """)
    elif role == 'etudiant':
        st.caption("""
        👨‍🎓 **Interface Étudiant - Système de Gestion des Examens**  
        📅 Consultation du calendrier | 📊 Visualisation des notes | ℹ️ Profil personnel
        """)

# ============================================
# 5. POINT D'ENTRÉE PRINCIPAL
# ============================================

def main():
    """Point d'entrée principal"""
    # Initialiser la session
    init_session()
    
    # Vérifier l'authentification
    if not st.session_state.authenticated:
        login_page()
    else:
        main_app()

if __name__ == "__main__":
    main()