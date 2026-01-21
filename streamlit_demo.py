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
# 2. SYSTÈME D'AUTHENTIFICATION - AVEC LES 5 ACTEURS EXACTS
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

# Utilisateurs prédéfinis avec les 5 acteurs exacts
USERS = {
    # 1. Doyen ou vice doyen
    "DOYEN001": {
        "password": hash_password("doyen123"),
        "role": "doyen_vice_doyen",
        "nom": "Président",
        "prenom": "Faculté",
        "departement": "Direction",
        "fonction": "Doyen"
    },
    "VDOYEN001": {
        "password": hash_password("vdoyen123"),
        "role": "doyen_vice_doyen",
        "nom": "Vice-Président",
        "prenom": "Faculté",
        "departement": "Direction",
        "fonction": "Vice-Doyen"
    },
    
    # 2. Gestionnaire des examens
    "GEST001": {
        "password": hash_password("gest123"),
        "role": "gestionnaire",
        "nom": "Responsable",
        "prenom": "Examens",
        "departement": "Administration",
        "fonction": "Gestionnaire des Examens"
    },
    
    # 3. Chef de département
    "CHINFO001": {
        "password": hash_password("chef123"),
        "role": "chef_departement",
        "nom": "Alaoui",
        "prenom": "Mohamed",
        "departement": "Informatique",
        "fonction": "Chef de Département"
    },
    "CHMATH001": {
        "password": hash_password("chef123"),
        "role": "chef_departement",
        "nom": "Bouazzi",
        "prenom": "Fatima",
        "departement": "Mathématiques",
        "fonction": "Chef de Département"
    },
    
    # 4. Enseignant
    "PROF001": {
        "password": hash_password("prof123"),
        "role": "enseignant",
        "nom": "Benali",
        "prenom": "Ahmed",
        "departement": "Informatique",
        "fonction": "Professeur"
    },
    "PROF002": {
        "password": hash_password("prof123"),
        "role": "enseignant",
        "nom": "Kadri",
        "prenom": "Fatima",
        "departement": "Informatique",
        "fonction": "Professeur"
    },
    
    # 5. Etudiant
    "ETUD001": {
        "password": hash_password("etud123"),
        "role": "etudiant",
        "nom": "Kadri",
        "prenom": "Fatima",
        "departement": "Informatique",
        "formation": "Licence Informatique",
        "niveau": "L3"
    },
    "ETUD002": {
        "password": hash_password("etud123"),
        "role": "etudiant",
        "nom": "Mansouri",
        "prenom": "Karim",
        "departement": "Informatique",
        "formation": "Master Informatique",
        "niveau": "M2"
    }
}

def authenticate(matricule, password):
    """Authentifier l'utilisateur"""
    hashed_pw = hash_password(password)
    if matricule in USERS and USERS[matricule]["password"] == hashed_pw:
        return USERS[matricule]
    return None

# ============================================
# 3. PAGE DE CONNEXION PROFESSIONNELLE
# ============================================

def login_page():
    """Page de connexion professionnelle"""
    st.set_page_config(page_title="Connexion", page_icon="🔐", layout="wide")
    
    # CSS professionnel SANS ESPACE BLANC
    st.markdown("""
    <style>
    /* Supprimer TOUS les espaces blancs */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        min-height: 100vh !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* Cacher le header Streamlit */
    header {
        visibility: hidden !important;
        height: 0 !important;
    }
    
    /* Supprimer les marges par défaut */
    .main .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
    }
    
    .login-card {
        max-width: 480px;
        margin: 100px auto 30px auto;
        padding: 50px 40px;
        background: rgba(255, 255, 255, 0.98);
        border-radius: 24px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.4);
    }
    
    .login-title {
        text-align: center;
        color: #2c3e50;
        margin-bottom: 40px;
        font-size: 32px;
        font-weight: 700;
    }
    
    .stTextInput > div > div > input {
        border-radius: 12px;
        border: 2px solid #e0e0e0;
        padding: 14px 20px;
        font-size: 16px;
        transition: all 0.3s;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    .stButton > button {
        width: 100%;
        border-radius: 12px;
        height: 52px;
        font-weight: 600;
        font-size: 16px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        margin-top: 20px;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
    }
    
    .account-card {
        background: #f8f9fa;
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
        border-left: 4px solid #667eea;
        transition: all 0.3s;
    }
    
    .account-card:hover {
        transform: translateX(5px);
        background: #eef2ff;
    }
    
    .university-info {
        text-align: center;
        color: white;
        padding: 40px 0 20px 0;
        margin: 0;
    }
    
    .university-name {
        font-size: 36px;
        font-weight: 700;
        margin-bottom: 10px;
    }
    
    .university-slogan {
        font-size: 18px;
        opacity: 0.9;
    }
    
    .role-header {
        color: #2c3e50;
        border-bottom: 2px solid #667eea;
        padding-bottom: 10px;
        margin-top: 30px;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # En-tête universitaire
    st.markdown("""
    <div class="university-info">
        <div class="university-name">🎓 Université Excellence</div>
        <div class="university-slogan">Système Intelligent de Planification des Examens Universitaires</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Carte de connexion
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    
    # Logo
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("https://cdn-icons-png.flaticon.com/512/2232/2232688.png", width=100)
    
    # Titre
    st.markdown('<h1 class="login-title">🔐 Portail d\'Authentification</h1>', unsafe_allow_html=True)
    
    # Formulaire de connexion
    with st.form("login_form", clear_on_submit=True):
        matricule = st.text_input("**🎓 Numéro Matricule**", 
                                placeholder="Votre numéro d'identification",
                                help="Exemple: DOYEN001, GEST001, CHINFO001, PROF001, ETUD001")
        
        password = st.text_input("**🔑 Mot de Passe**", 
                               type="password",
                               placeholder="Votre mot de passe confidentiel",
                               help="Votre mot de passe personnel")
        
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            submit = st.form_submit_button("**🚀 Accéder au Système**", 
                                         use_container_width=True,
                                         type="primary")
    
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
                st.success(f"### ✅ Bienvenue {user['prenom']} {user['nom']}!")
                st.balloons()
                st.rerun()
            else:
                st.error("### ❌ Identifiants incorrects")
                st.warning("Veuillez vérifier votre matricule et mot de passe")
        else:
            st.warning("### ⚠️ Champs requis")
            st.info("Tous les champs doivent être remplis")
    
    # Comptes de démonstration - Organisés par les 5 acteurs
    with st.expander("### 📋 Comptes de Démonstration (5 Acteurs)", expanded=True):
        
        # 1. Doyen ou vice doyen
        st.markdown('<h4 class="role-header">👑 1. Doyen ou Vice-Doyen</h4>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div class="account-card">
            <h4>🎓 Doyen</h4>
            <p><strong>Matricule:</strong> DOYEN001</p>
            <p><strong>Mot de passe:</strong> doyen123</p>
            <p><em>Vue d'ensemble, rapports stratégiques</em></p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="account-card">
            <h4>👔 Vice-Doyen</h4>
            <p><strong>Matricule:</strong> VDOYEN001</p>
            <p><strong>Mot de passe:</strong> vdoyen123</p>
            <p><em>Supervision, coordination</em></p>
            </div>
            """, unsafe_allow_html=True)
        
        # 2. Gestionnaire des examens
        st.markdown('<h4 class="role-header">📊 2. Gestionnaire des Examens</h4>', unsafe_allow_html=True)
        st.markdown("""
        <div class="account-card">
        <h4>📊 Gestionnaire des Examens</h4>
        <p><strong>Matricule:</strong> GEST001</p>
        <p><strong>Mot de passe:</strong> gest123</p>
        <p><em>Organisation, planification des examens</em></p>
        </div>
        """, unsafe_allow_html=True)
        
        # 3. Chef de département
        st.markdown('<h4 class="role-header">👨‍💼 3. Chef de Département</h4>', unsafe_allow_html=True)
        col3, col4 = st.columns(2)
        with col3:
            st.markdown("""
            <div class="account-card">
            <h4>👨‍💼 Chef Info</h4>
            <p><strong>Matricule:</strong> CHINFO001</p>
            <p><strong>Mot de passe:</strong> chef123</p>
            <p><em>Gestion du département informatique</em></p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class="account-card">
            <h4>👩‍💼 Chef Maths</h4>
            <p><strong>Matricule:</strong> CHMATH001</p>
            <p><strong>Mot de passe:</strong> chef123</p>
            <p><em>Gestion du département mathématiques</em></p>
            </div>
            """, unsafe_allow_html=True)
        
        # 4. Enseignant
        st.markdown('<h4 class="role-header">👨‍🏫 4. Enseignant</h4>', unsafe_allow_html=True)
        col5, col6 = st.columns(2)
        with col5:
            st.markdown("""
            <div class="account-card">
            <h4>👨‍🏫 Enseignant 1</h4>
            <p><strong>Matricule:</strong> PROF001</p>
            <p><strong>Mot de passe:</strong> prof123</p>
            <p><em>Gestion des examens et étudiants</em></p>
            </div>
            """, unsafe_allow_html=True)
        
        with col6:
            st.markdown("""
            <div class="account-card">
            <h4>👩‍🏫 Enseignant 2</h4>
            <p><strong>Matricule:</strong> PROF002</p>
            <p><strong>Mot de passe:</strong> prof123</p>
            <p><em>Gestion des examens et étudiants</em></p>
            </div>
            """, unsafe_allow_html=True)
        
        # 5. Etudiant
        st.markdown('<h4 class="role-header">👨‍🎓 5. Etudiant</h4>', unsafe_allow_html=True)
        col7, col8 = st.columns(2)
        with col7:
            st.markdown("""
            <div class="account-card">
            <h4>👨‍🎓 Étudiant 1</h4>
            <p><strong>Matricule:</strong> ETUD001</p>
            <p><strong>Mot de passe:</strong> etud123</p>
            <p><em>Consultation des examens et résultats</em></p>
            </div>
            """, unsafe_allow_html=True)
        
        with col8:
            st.markdown("""
            <div class="account-card">
            <h4>👩‍🎓 Étudiant 2</h4>
            <p><strong>Matricule:</strong> ETUD002</p>
            <p><strong>Mot de passe:</strong> etud123</p>
            <p><em>Consultation des examens et résultats</em></p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer avec l'année 2026 et version 1.0
    st.markdown(f"""
    <div style="text-align:center; margin-top:50px; color:white; opacity:0.8;">
    <p>© 2026 Université Excellence - Tous droits réservés</p>
    <p style="font-size:14px;">Version 1.0 | Système Intelligent de Planification des Examens Universitaires</p>
    <p style="font-size:12px;">5 Acteurs: Doyen/Vice-Doyen | Gestionnaire | Chef de Département | Enseignant | Étudiant</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# 4. APPLICATION PRINCIPALE
# ============================================

def main_app():
    """Application principale après authentification"""
    
    st.set_page_config(
        page_title="Système Intelligent de Planification des Examens Universitaires",
        page_icon="🎓",
        layout="wide"
    )
    
    # CSS personnalisé
    st.markdown("""
    <style>
    .user-info-card {
        background: linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%);
        color: white;
        padding: 25px;
        border-radius: 15px;
        margin-bottom: 25px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .role-badge {
        display: inline-block;
        padding: 6px 18px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 14px;
        margin-top: 10px;
    }
    
    .badge-doyen_vice_doyen { background: #9c27b0; color: white; }
    .badge-gestionnaire { background: #2196f3; color: white; }
    .badge-chef_departement { background: #ff9800; color: white; }
    .badge-enseignant { background: #4ecdc4; color: white; }
    .badge-etudiant { background: #45b7d1; color: white; }
    
    .stat-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        border-left: 6px solid #4CAF50;
        margin: 12px 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    
    .tab-content {
        padding: 20px;
        background: white;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }
    
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 3px 10px rgba(0,0,0,0.05);
    }
    
    .actor-section {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid #667eea;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Récupérer les infos utilisateur
    user_info = st.session_state.user_info
    role = user_info.get('role', 'etudiant')
    
    # Mapper le rôle pour l'affichage
    role_display_map = {
        'doyen_vice_doyen': 'Doyen/Vice-Doyen',
        'gestionnaire': 'Gestionnaire des Examens',
        'chef_departement': 'Chef de Département',
        'enseignant': 'Enseignant',
        'etudiant': 'Étudiant'
    }
    
    role_display = role_display_map.get(role, role)
    badge_class = f"badge-{role}"
    
    # En-tête avec informations utilisateur
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        st.title(f"🎓 Système Intelligent de Planification des Examens Universitaires")
        st.markdown(f"""
        <div class="user-info-card">
        <h3>👤 {user_info['prenom']} {user_info['nom']}</h3>
        <p><strong>🎓 Matricule:</strong> {user_info['matricule']}</p>
        <p><strong>🏢 Fonction:</strong> {role_display}</p>
        <p><strong>📋 Département:</strong> {user_info.get('departement', 'Non spécifié')}</p>
        <span class="role-badge {badge_class}">{role_display.upper()}</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        if st.button("🚪 Déconnexion", type="secondary", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user_info = {}
            st.rerun()
    
    # ============================================
    # BARRE LATÉRALE SELON LE RÔLE (5 ACTEURS)
    # ============================================
    
    with st.sidebar:
        st.header(f"⚙️ Panneau {role_display}")
        
        # Statistiques communes
        if role in ['doyen_vice_doyen', 'gestionnaire']:
            st.markdown('<div class="stat-card">', unsafe_allow_html=True)
            col_s1, col_s2 = st.columns(2)
            with col_s1:
                st.metric("👨‍🎓 Étudiants", "130,000")
                st.metric("📝 Examens", "1,850")
            with col_s2:
                st.metric("🏛️ Salles", "65")
                st.metric("👨‍🏫 Enseignants", "120")
            st.markdown('</div>', unsafe_allow_html=True)
            
        elif role == 'chef_departement':
            st.markdown('<div class="stat-card">', unsafe_allow_html=True)
            col_s1, col_s2 = st.columns(2)
            with col_s1:
                st.metric("👨‍🎓 Étudiants", "12,500")
                st.metric("📝 Examens", "280")
            with col_s2:
                st.metric("👨‍🏫 Enseignants", "45")
                st.metric("🎓 Promotions", "6")
            st.markdown('</div>', unsafe_allow_html=True)
            
        elif role == 'enseignant':
            st.markdown('<div class="stat-card">', unsafe_allow_html=True)
            st.metric("📅 Mes Examens", "15")
            st.metric("⏰ Heures/Semaine", "25")
            st.metric("👥 Étudiants", "450")
            st.markdown('</div>', unsafe_allow_html=True)
            
        elif role == 'etudiant':
            st.markdown('<div class="stat-card">', unsafe_allow_html=True)
            st.metric("📅 Mes Examens", "8")
            st.metric("📊 Moyenne", "14.5/20")
            st.metric("🎯 Crédits", "45/60")
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.divider()
        
        # Actions spécifiques selon les 5 acteurs
        if role == 'doyen_vice_doyen':
            st.subheader("Actions Direction")
            if st.button("📋 Rapport Annuel", use_container_width=True):
                st.success("📄 Rapport généré")
            if st.button("📊 Tableau de Bord", use_container_width=True):
                st.info("📈 Tableau de bord affiché")
            if st.button("👥 Réunion Faculté", use_container_width=True):
                st.warning("📅 Réunion programmée")
                
        elif role == 'gestionnaire':
            st.subheader("Actions Gestionnaire")
            if st.button("🚀 Générer Planning", type="primary", use_container_width=True):
                st.success("✅ Planning généré!")
            if st.button("🔍 Vérifier Conflits", use_container_width=True):
                st.info("✅ Aucun conflit détecté!")
            if st.button("📊 Exporter Rapports", use_container_width=True):
                st.success("📁 Rapports exportés!")
                
        elif role == 'chef_departement':
            st.subheader("Actions Chef Département")
            if st.button("📋 Planification Département", use_container_width=True):
                st.success("📅 Planification effectuée")
            if st.button("👥 Gestion Enseignants", use_container_width=True):
                st.info("👨‍🏫 Gestion activée")
            if st.button("📊 Statistiques Département", use_container_width=True):
                st.warning("📈 Statistiques affichées")
                
        elif role == 'enseignant':
            st.subheader("Actions Enseignant")
            if st.button("📋 Voir Mes Examens", use_container_width=True):
                st.success("✅ Liste chargée")
            if st.button("📈 Mes Statistiques", use_container_width=True):
                st.info("📊 Statistiques affichées")
            if st.button("✏️ Saisir Notes", use_container_width=True):
                st.warning("📝 Module de saisie")
                
        elif role == 'etudiant':
            st.subheader("Actions Étudiant")
            if st.button("📅 Mon Calendrier", use_container_width=True):
                st.success("🗓️ Calendrier affiché")
            if st.button("📄 Mes Résultats", use_container_width=True):
                st.info("📈 Résultats consultés")
            if st.button("📚 Mes Cours", use_container_width=True):
                st.warning("📖 Liste des cours")
        
        st.divider()
        st.caption(f"📍 Connecté en tant que {role_display}")
        st.caption(f"🕐 {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}")

    # ============================================
    # ONGLETS SELON LES 5 ACTEURS
    # ============================================
    
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    
    # 1. DOYEN OU VICE-DOYEN
    if role == 'doyen_vice_doyen':
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Tableau de Bord", "📈 Statistiques", "📋 Rapports", "⚙️ Configuration"])
        
        with tab1:
            st.header("📊 Tableau de Bord de Direction")
            
            # Métriques stratégiques
            col1, col2, col3, col4 = st.columns(4)
            with col1: 
                st.metric("Budget Total", "15.2M €", "+2.3%")
            with col2: 
                st.metric("Taux Réussite", "87.5%", "+1.2%")
            with col3: 
                st.metric("Satisfaction", "92%", "+3%")
            with col4: 
                st.metric("Nouveaux Étudiants", "4,200", "+5%")
            
            # Graphiques stratégiques
            col_chart1, col_chart2 = st.columns(2)
            with col_chart1:
                st.subheader("📈 Évolution des Effectifs")
                effectifs = pd.DataFrame({
                    "Année": ["2022", "2023", "2024", "2025"],
                    "Étudiants": [115000, 120000, 125000, 130000],
                    "Enseignants": [105, 110, 115, 120]
                })
                fig = px.line(effectifs, x='Année', y=['Étudiants', 'Enseignants'], 
                             title="Croissance sur 4 ans")
                st.plotly_chart(fig, use_container_width=True)
            
            with col_chart2:
                st.subheader("🎯 Répartition des Départements")
                depts = pd.DataFrame({
                    "Département": ["Informatique", "Mathématiques", "Physique", "Chimie", "Droit", "Économie"],
                    "Effectifs": [45000, 28000, 22000, 18000, 15000, 10000]
                })
                fig = px.pie(depts, values='Effectifs', names='Département', 
                            title="Distribution des effectifs")
                st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            st.header("📈 Statistiques Institutionnelles")
            
            # Analyse comparative
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("📊 Performance par Faculté")
                performance = pd.DataFrame({
                    "Faculté": ["Sciences", "Droit", "Médecine", "Lettres", "Économie"],
                    "Taux Réussite": [87, 85, 90, 82, 88],
                    "Satisfaction": [92, 88, 94, 85, 90],
                    "Budget Utilisé": [96, 94, 98, 92, 95]
                })
                st.dataframe(performance, use_container_width=True)
            
            with col2:
                st.subheader("📈 Tendance des Admissions")
                admissions = pd.DataFrame({
                    "Année": ["2022", "2023", "2024", "2025"],
                    "Admissions": [4200, 4300, 4400, 4500],
                    "Diplômés": [3800, 3900, 4000, 4100]
                })
                fig = px.line(admissions, x='Année', y=['Admissions', 'Diplômés'], 
                             title="Évolution des admissions et diplômés")
                st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            st.header("📋 Rapports Institutionnels")
            
            # Génération de rapports
            col_rap1, col_rap2 = st.columns(2)
            with col_rap1:
                with st.expander("📄 Rapport Annuel 2025-2026", expanded=True):
                    st.write("""
                    **Synthèse des performances:**
                    - Taux de réussite global: 87.5%
                    - Nombre d'étudiants: 130,000
                    - Budget exécuté: 98.2%
                    - Satisfaction étudiante: 92%
                    
                    **Recommandations:**
                    1. Augmenter les capacités d'accueil
                    2. Moderniser les infrastructures
                    3. Renforcer la formation continue
                    """)
                    if st.button("📥 Télécharger", key="rap1"):
                        st.success("✅ Rapport téléchargé")
            
            with col_rap2:
                with st.expander("📊 Rapport Financier", expanded=True):
                    st.write("""
                    **Analyse financière:**
                    - Budget total: 15.2M €
                    - Dépenses pédagogiques: 8.5M €
                    - Investissements: 3.2M €
                    - Frais de fonctionnement: 3.5M €
                    """)
                    if st.button("📥 Télécharger", key="rap2"):
                        st.success("✅ Rapport téléchargé")
            
            # Rapports statistiques
            st.subheader("📈 Rapports Statistiques")
            rapports = ["Performance académique", "Taux d'emploi des diplômés", 
                       "Satisfaction des parties prenantes", "Impact social"]
            
            for i, rapport in enumerate(rapports):
                col_gen1, col_gen2, col_gen3 = st.columns([3, 1, 1])
                with col_gen1:
                    st.write(f"**{rapport}**")
                with col_gen2:
                    if st.button("📊 Générer", key=f"gen_{i}"):
                        st.success(f"✅ Rapport '{rapport}' généré")
                with col_gen3:
                    if st.button("📥 Exporter", key=f"exp_{i}"):
                        st.success(f"✅ Rapport '{rapport}' exporté")
        
        with tab4:
            st.header("⚙️ Configuration Institutionnelle")
            
            with st.form("config_direction"):
                st.subheader("🏛️ Paramètres Institutionnels")
                
                col_c1, col_c2 = st.columns(2)
                with col_c1:
                    annee_academique = st.selectbox("Année académique", 
                                                   ["2025-2026", "2026-2027", "2027-2028"])
                    objectif_reussite = st.slider("Objectif taux de réussite (%)", 70, 100, 90)
                    budget_total = st.number_input("Budget total (M€)", 10.0, 50.0, 15.2)
                
                with col_c2:
                    priorites = st.multiselect("Priorités stratégiques",
                                              ["Infrastructure", "Recherche", "International", 
                                               "Innovation pédagogique", "Employabilité"],
                                              default=["Infrastructure", "Innovation pédagogique"])
                    comite_direction = st.text_area("Comité de direction", 
                                                   "Président: Doyen\nMembres: Vice-Doyens, Directeurs")
                
                if st.form_submit_button("💾 Enregistrer les paramètres"):
                    st.success("✅ Configuration sauvegardée")
    
    # 2. GESTIONNAIRE DES EXAMENS
    elif role == 'gestionnaire':
        tab1, tab2, tab3, tab4 = st.tabs(["📅 Planification", "🏛️ Salles", "👨‍🏫 Ressources", "⚙️ Paramètres"])
        
        with tab1:
            st.header("📅 Planification des Examens")
            
            # Filtres
            col_f1, col_f2, col_f3 = st.columns(3)
            with col_f1:
                date_filter = st.date_input("Filtrer par date", datetime.date(2024, 6, 10))
            with col_f2:
                dept_filter = st.selectbox("Filtrer par département", 
                                         ["Tous", "Informatique", "Mathématiques", "Physique", "Chimie"])
            with col_f3:
                salle_filter = st.selectbox("Filtrer par salle", 
                                          ["Toutes", "Amphi A", "Amphi B", "Amphi C", "Salle 101", "Salle 102"])
            
            df_exams = get_demo_exams()
            
            # Appliquer les filtres
            if dept_filter != "Tous":
                df_exams = df_exams[df_exams["Département"] == dept_filter]
            
            if salle_filter != "Toutes":
                df_exams = df_exams[df_exams["Salle"] == salle_filter]
            
            # Afficher le tableau
            st.dataframe(df_exams, use_container_width=True, height=400)
            
            # Boutons d'action
            col_act1, col_act2, col_act3 = st.columns(3)
            with col_act1:
                if st.button("➕ Ajouter Examen", use_container_width=True):
                    st.success("✅ Formulaire d'ajout ouvert")
            with col_act2:
                if st.button("✏️ Modifier", use_container_width=True):
                    st.info("✏️ Mode édition activé")
            with col_act3:
                if st.button("🗑️ Supprimer", use_container_width=True):
                    st.warning("🗑️ Sélectionnez un examen à supprimer")
        
        with tab2:
            st.header("🏛️ Gestion des Salles")
            df_rooms = get_demo_rooms()
            
            st.dataframe(df_rooms, use_container_width=True)
            
            # Graphique des capacités
            st.subheader("📏 Capacité des Salles")
            fig = px.bar(df_rooms, x='Nom', y='Capacité', 
                        color='Type', title="Distribution des Capacités",
                        hover_data=['Bâtiment', 'Examens'])
            st.plotly_chart(fig, use_container_width=True)
            
            # Gestion des salles
            with st.expander("➕ Ajouter/Modifier une salle"):
                col_s1, col_s2 = st.columns(2)
                with col_s1:
                    nom_salle = st.text_input("Nom de la salle")
                    capacite = st.number_input("Capacité", 1, 1000, 50)
                with col_s2:
                    type_salle = st.selectbox("Type", ["Amphithéâtre", "Salle", "Laboratoire"])
                    batiment = st.text_input("Bâtiment")
                
                if st.button("💾 Enregistrer la salle"):
                    st.success(f"✅ Salle '{nom_salle}' enregistrée")
        
        with tab3:
            st.header("👨‍🏫 Gestion des Ressources")
            
            # Enseignants
            st.subheader("👨‍🏫 Liste des Enseignants")
            df_profs = get_demo_professors()
            st.dataframe(df_profs, use_container_width=True)
            
            # Affectation des surveillants
            st.subheader("👁️ Affectation des Surveillances")
            surveillance = pd.DataFrame({
                "Examen": ["Base de données", "Algorithmique", "Réseaux", "Mathématiques"],
                "Date": ["2024-06-10", "2024-06-10", "2024-06-11", "2024-06-12"],
                "Salle": ["Amphi A", "Salle 101", "Amphi B", "Amphi A"],
                "Surveillants": ["Dr. Benali + 2", "Dr. Kadri + 1", "Dr. Mansouri + 2", "Dr. Bouguerra + 3"],
                "Statut": ["✓ Affecté", "✓ Affecté", "🔄 En cours", "⏳ À affecter"]
            })
            st.dataframe(surveillance, use_container_width=True)
        
        with tab4:
            st.header("⚙️ Paramètres de Planification")
            
            with st.form("config_gestionnaire"):
                st.subheader("📅 Paramètres de Planification")
                
                col_c1, col_c2 = st.columns(2)
                with col_c1:
                    start_date = st.date_input("Date de début des examens",
                                             datetime.date(2024, 6, 10))
                    max_daily = st.slider("Examens maximum par jour", 1, 10, 4)
                    min_interval = st.number_input("Intervalle minimum (minutes)", 30, 180, 60)
                
                with col_c2:
                    duration = st.selectbox("Durée par défaut (minutes)",
                                          [90, 120, 150, 180], index=1)
                    time_slots = ["08:00", "09:00", "10:30", "13:00", "15:00", "17:00"]
                    selected_times = st.multiselect("Créneaux horaires disponibles",
                                                  time_slots, default=["09:00", "13:00", "15:00"])
                    auto_schedule = st.checkbox("Planification automatique", value=True)
                
                st.divider()
                
                st.subheader("🔔 Paramètres de Notification")
                notify_students = st.checkbox("Notifications aux étudiants", value=True)
                notify_professors = st.checkbox("Notifications aux enseignants", value=True)
                
                if st.form_submit_button("💾 Sauvegarder la configuration"):
                    st.success("✅ Configuration sauvegardée avec succès!")
    
    # 3. CHEF DE DÉPARTEMENT
    elif role == 'chef_departement':
        tab1, tab2, tab3 = st.tabs(["📅 Examens Département", "👨‍🏫 Enseignants", "📊 Statistiques"])
        
        with tab1:
            st.header(f"📅 Examens du Département {user_info['departement']}")
            
            df_all = get_demo_exams()
            df_dept_exams = df_all[df_all["Département"] == user_info['departement']]
            
            if not df_dept_exams.empty:
                st.dataframe(df_dept_exams, use_container_width=True)
                
                # Statistiques du département
                col_dept1, col_dept2, col_dept3 = st.columns(3)
                with col_dept1:
                    st.metric("Examens total", len(df_dept_exams))
                with col_dept2:
                    total_students = df_dept_exams["Étudiants"].sum()
                    st.metric("Étudiants concernés", f"{total_students:,}")
                with col_dept3:
                    enseignants = df_dept_exams["Professeur"].nunique()
                    st.metric("Enseignants impliqués", enseignants)
                
                # Planning par formation
                st.subheader("📊 Répartition par Formation")
                formation_counts = df_dept_exams["Formation"].value_counts()
                fig = px.pie(values=formation_counts.values, names=formation_counts.index,
                            title=f"Examens par formation - {user_info['departement']}")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info(f"ℹ️ Aucun examen programmé pour le département {user_info['departement']}")
        
        with tab2:
            st.header(f"👨‍🏫 Enseignants du Département {user_info['departement']}")
            
            # Liste des enseignants du département
            enseignants_dept = [
                {"Nom": "Dr. Benali Ahmed", "Grade": "Professeur", "Spécialité": "Base de données", "Charge Horaire": "192h"},
                {"Nom": "Dr. Kadri Fatima", "Grade": "Maître de Conférences", "Spécialité": "Algorithmique", "Charge Horaire": "192h"},
                {"Nom": "Dr. Mansouri Karim", "Grade": "Maître de Conférences", "Spécialité": "Réseaux", "Charge Horaire": "192h"},
                {"Nom": "Dr. Saidi Mohamed", "Grade": "Professeur", "Spécialité": "Sécurité", "Charge Horaire": "192h"},
            ]
            
            df_enseignants = pd.DataFrame(enseignants_dept)
            st.dataframe(df_enseignants, use_container_width=True)
            
            # Gestion des charges
            st.subheader("📋 Gestion des Charges")
            with st.form("gestion_charges"):
                col_charge1, col_charge2, col_charge3 = st.columns(3)
                with col_charge1:
                    enseignant = st.selectbox("Enseignant", [e["Nom"] for e in enseignants_dept])
                with col_charge2:
                    charge_actuelle = st.number_input("Charge actuelle (heures)", 0, 300, 192)
                with col_charge3:
                    charge_souhaitee = st.number_input("Charge souhaitée (heures)", 0, 300, 192)
                
                if st.form_submit_button("💾 Mettre à jour la charge"):
                    st.success(f"✅ Charge de {enseignant} mise à jour")
        
        with tab3:
            st.header(f"📊 Statistiques du Département {user_info['departement']}")
            
            # Tableau de bord complet
            col_stat1, col_stat2, col_stat3 = st.columns(3)
            with col_stat1:
                st.metric("Budget alloué", "3.2M €", "+5%")
                st.metric("Publications", "125", "+12")
            with col_stat2:
                st.metric("Projets recherche", "18", "+3")
                st.metric("Partenariats", "24", "+2")
            with col_stat3:
                st.metric("Satisfaction étudiants", "4.2/5", "+0.3")
                st.metric("Insertion professionnelle", "86%", "+4%")
            
            st.divider()
            
            # Évolution des indicateurs
            st.subheader("📈 Évolution des indicateurs")
            evolution = pd.DataFrame({
                "Année": ["2022", "2023", "2024", "2025"],
                "Effectifs": [11000, 11500, 12000, 12500],
                "Taux Réussite": [84, 86, 87, 88.5],
                "Budget (M€)": [2.8, 2.9, 3.0, 3.2]
            })
            
            fig = px.line(evolution, x='Année', y=['Effectifs', 'Taux Réussite', 'Budget (M€)'],
                         title="Évolution sur 4 ans")
            st.plotly_chart(fig, use_container_width=True)
    
    # 4. ENSEIGNANT
    elif role == 'enseignant':
        tab1, tab2, tab3 = st.tabs(["📅 Mes Examens", "👥 Mes Étudiants", "📊 Mes Statistiques"])
        
        with tab1:
            st.header("📅 Mes Examens Programmés")
            
            # Filtrer les examens du professeur
            df_all = get_demo_exams()
            df_my_exams = df_all[df_all["Professeur"].str.contains(user_info['nom'])]
            
            if not df_my_exams.empty:
                # Afficher le tableau
                st.dataframe(df_my_exams, use_container_width=True)
                
                # Prochain examen
                next_exam = df_my_exams.iloc[0] if len(df_my_exams) > 0 else None
                if next_exam is not None:
                    st.info(f"""
                    **📌 Prochain examen:**
                    - **Module:** {next_exam['Module']}
                    - **Date:** {next_exam['Date']}
                    - **Salle:** {next_exam['Salle']}
                    - **Étudiants:** {next_exam['Étudiants']}
                    """)
                
                # Statistiques rapides
                col_prof1, col_prof2, col_prof3 = st.columns(3)
                with col_prof1:
                    st.metric("Total examens", len(df_my_exams))
                with col_prof2:
                    total_students = df_my_exams["Étudiants"].sum()
                    st.metric("Étudiants total", f"{total_students:,}")
                with col_prof3:
                    st.metric("Heures d'examen", f"{len(df_my_exams) * 2}h")
            else:
                st.info("ℹ️ Aucun examen programmé pour le moment.")
        
        with tab2:
            st.header("👥 Mes Étudiants")
            
            # Simulation d'étudiants
            etudiants = [
                {"Matricule": "ETUD001", "Nom": "Kadri", "Prénom": "Fatima", "Note": "16/20", "Statut": "✓"},
                {"Matricule": "ETUD002", "Nom": "Mansouri", "Prénom": "Karim", "Note": "14/20", "Statut": "✓"},
                {"Matricule": "ETUD003", "Nom": "Bouguerra", "Prénom": "Nadia", "Note": "18/20", "Statut": "✓"},
                {"Matricule": "ETUD004", "Nom": "Saidi", "Prénom": "Mohamed", "Note": "12/20", "Statut": "⚠️"},
                {"Matricule": "ETUD005", "Nom": "Cherif", "Prénom": "Yacine", "Note": "15/20", "Statut": "✓"},
            ]
            
            df_etudiants = pd.DataFrame(etudiants)
            st.dataframe(df_etudiants, use_container_width=True)
            
            # Statistiques des étudiants
            col_etud1, col_etud2, col_etud3 = st.columns(3)
            with col_etud1:
                moyenne = df_etudiants["Note"].str.replace("/20", "").astype(float).mean()
                st.metric("Moyenne générale", f"{moyenne:.1f}/20")
            with col_etud2:
                st.metric("Nombre d'étudiants", len(df_etudiants))
            with col_etud3:
                reussite = (df_etudiants["Note"].str.replace("/20", "").astype(float) >= 10).sum()
                st.metric("Taux de réussite", f"{(reussite/len(df_etudiants))*100:.0f}%")
        
        with tab3:
            st.header("📊 Mes Statistiques Personnelles")
            
            col_stat1, col_stat2 = st.columns(2)
            with col_stat1:
                st.metric("Heures d'examens", "45h")
                st.metric("Nombre d'étudiants", "450")
                st.metric("Moyenne des notes", "14.8/20")
            
            with col_stat2:
                st.metric("Taux de réussite", "92%")
                st.metric("Examens corrigés", "15/15")
                st.metric("Satisfaction étudiants", "4.5/5")
            
            st.divider()
            
            # Graphique d'évolution
            st.subheader("📈 Évolution des résultats")
            evolution_data = pd.DataFrame({
                "Semestre": ["S1", "S2", "S3", "S4", "S5", "S6"],
                "Moyenne": [14.2, 14.5, 14.8, 15.1, 14.9, 15.2],
                "Taux réussite": [88, 90, 91, 93, 92, 94]
            })
            
            fig = px.line(evolution_data, x='Semestre', y=['Moyenne', 'Taux réussite'],
                         title="Évolution sur les 3 dernières années")
            st.plotly_chart(fig, use_container_width=True)
    
    # 5. ETUDIANT
    elif role == 'etudiant':
        tab1, tab2, tab3 = st.tabs(["📅 Mes Examens", "📊 Mes Résultats", "ℹ️ Mon Profil"])
        
        with tab1:
            st.header("📅 Mon Calendrier d'Examens")
            
            # Simulation d'examens pour l'étudiant
            mes_examens = [
                {"Module": "Base de données", "Date": "2024-06-10 09:00", "Salle": "Amphi A", "Professeur": "Dr. Benali", "Statut": "🟢"},
                {"Module": "Algorithmique", "Date": "2024-06-10 13:00", "Salle": "Salle 101", "Professeur": "Dr. Kadri", "Statut": "🟢"},
                {"Module": "Réseaux", "Date": "2024-06-11 09:00", "Salle": "Amphi B", "Professeur": "Dr. Mansouri", "Statut": "🟡"},
                {"Module": "Programmation Python", "Date": "2024-06-11 13:00", "Salle": "Labo Info 1", "Professeur": "Dr. Bouguerra", "Statut": "🔴"},
                {"Module": "Sécurité", "Date": "2024-06-12 09:00", "Salle": "Salle 102", "Professeur": "Dr. Saidi", "Statut": "🟡"},
            ]
            
            df_mes_examens = pd.DataFrame(mes_examens)
            st.dataframe(df_mes_examens, use_container_width=True)
            
            # Prochain examen
            if not df_mes_examens.empty:
                prochain = df_mes_examens.iloc[0]
                
                # Calculer le temps restant
                exam_date = datetime.datetime.strptime(prochain['Date'], "%Y-%m-%d %H:%M")
                now = datetime.datetime.now()
                time_left = exam_date - now
                
                days = time_left.days
                hours = time_left.seconds // 3600
                minutes = (time_left.seconds % 3600) // 60
                
                st.success(f"""
                **📌 Prochain examen:**
                - **Module:** {prochain['Module']}
                - **Date:** {prochain['Date']}
                - **Salle:** {prochain['Salle']}
                - **Temps restant:** {days} jours, {hours} heures, {minutes} minutes
                """)
            
            # Statistiques
            col_exam1, col_exam2, col_exam3 = st.columns(3)
            with col_exam1:
                st.metric("Examens restants", len(df_mes_examens))
            with col_exam2:
                passed = (df_mes_examens["Statut"] == "🟢").sum()
                st.metric("Examens passés", passed)
            with col_exam3:
                pending = (df_mes_examens["Statut"] != "🟢").sum()
                st.metric("À venir", pending)
        
        with tab2:
            st.header("📊 Mes Résultats Académiques")
            
            # Notes de l'étudiant
            notes = [
                {"Module": "Base de données", "Note": "16/20", "Crédits": "6", "Statut": "✓ Validé"},
                {"Module": "Algorithmique", "Note": "14/20", "Crédits": "5", "Statut": "✓ Validé"},
                {"Module": "Réseaux", "Note": "15/20", "Crédits": "6", "Statut": "✓ Validé"},
                {"Module": "Mathématiques", "Note": "13/20", "Crédits": "4", "Statut": "✓ Validé"},
                {"Module": "Physique", "Note": "11/20", "Crédits": "4", "Statut": "⚠️ Rattrapage"},
                {"Module": "Anglais", "Note": "17/20", "Crédits": "3", "Statut": "✓ Validé"},
            ]
            
            df_notes = pd.DataFrame(notes)
            st.dataframe(df_notes, use_container_width=True)
            
            # Calcul des statistiques
            notes_numeriques = df_notes["Note"].str.replace("/20", "").astype(float)
            moyenne = notes_numeriques.mean()
            credits_valides = df_notes[df_notes["Statut"] == "✓ Validé"]["Crédits"].astype(int).sum()
            credits_totaux = df_notes["Crédits"].astype(int).sum()
            
            col_note1, col_note2, col_note3 = st.columns(3)
            with col_note1:
                st.metric("Moyenne générale", f"{moyenne:.2f}/20")
            with col_note2:
                st.metric("Crédits validés", f"{credits_valides}/{credits_totaux}")
            with col_note3:
                taux_reussite = (df_notes["Statut"] == "✓ Validé").sum() / len(df_notes) * 100
                st.metric("Taux de réussite", f"{taux_reussite:.0f}%")
            
            # Graphique des notes
            st.subheader("📈 Visualisation des Notes")
            fig = px.bar(df_notes, x='Module', y=notes_numeriques, 
                        title="Distribution des Notes par Module",
                        color=notes_numeriques,
                        color_continuous_scale='RdYlGn')
            st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            st.header("ℹ️ Mon Profil Étudiant")
            
            col_profil1, col_profil2 = st.columns(2)
            
            with col_profil1:
                st.info(f"""
                **📋 Informations Personnelles:**
                
                **Nom:** {user_info['nom']}
                **Prénom:** {user_info['prenom']}
                **Matricule:** {user_info['matricule']}
                **Formation:** {user_info.get('formation', 'Licence Informatique')}
                **Département:** {user_info.get('departement', 'Informatique')}
                **Niveau:** {user_info.get('niveau', 'L3')}
                **Année académique:** 2025-2026
                """)
            
            with col_profil2:
                st.subheader("🔒 Changer le mot de passe")
                with st.form("change_pass"):
                    current = st.text_input("Mot de passe actuel", type="password")
                    new = st.text_input("Nouveau mot de passe", type="password")
                    confirm = st.text_input("Confirmer le nouveau mot de passe", type="password")
                    
                    if st.form_submit_button("💾 Mettre à jour le mot de passe"):
                        if new == confirm and len(new) >= 6:
                            st.success("✅ Mot de passe mis à jour avec succès!")
                        else:
                            st.error("❌ Les mots de passe ne correspondent pas ou sont trop courts")
            
            # Informations académiques
            st.subheader("🎓 Progression Académique")
            
            col_prog1, col_prog2, col_prog3 = st.columns(3)
            with col_prog1:
                st.metric("Crédits obtenus", "45/60")
                st.progress(45/60)
            
            with col_prog2:
                st.metric("Modules validés", "8/10")
                st.progress(0.8)
            
            with col_prog3:
                st.metric("Moyenne générale", "14.5/20")
                st.progress(14.5/20)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ============================================
    # PIED DE PAGE
    # ============================================
    
    st.divider()
    
    # Messages de pied de page selon les 5 acteurs
    if role == 'doyen_vice_doyen':
        st.caption(f"""
        👑 **Interface Doyen/Vice-Doyen - Système Intelligent de Planification des Examens Universitaires**  
        📊 Tableau de bord stratégique | 📈 Statistiques institutionnelles | 📋 Rapports de direction  
        🏛️ Université Excellence | Année académique 2025-2026
        """)
    elif role == 'gestionnaire':
        st.caption(f"""
        📊 **Interface Gestionnaire des Examens - Système Intelligent de Planification des Examens Universitaires**  
        🏛️ Gestion de 65 salles | 👨‍🏫 Coordination de 120 enseignants | 📅 Planification de 1,850 examens  
        🎯 Université Excellence | Année académique 2025-2026
        """)
    elif role == 'chef_departement':
        st.caption(f"""
        👨‍💼 **Interface Chef de Département - Système Intelligent de Planification des Examens Universitaires**  
        📅 Gestion départementale | 👨‍🏫 Supervision des enseignants | 👨‍🎓 Suivi des étudiants  
        🏛️ Département: {user_info.get('departement', 'Informatique')} | Année académique 2025-2026
        """)
    elif role == 'enseignant':
        st.caption(f"""
        👨‍🏫 **Interface Enseignant - Système Intelligent de Planification des Examens Universitaires**  
        📅 Planification d'examens | 👥 Gestion d'étudiants | 📊 Suivi des résultats  
        🎯 Université Excellence | Année académique 2025-2026
        """)
    elif role == 'etudiant':
        st.caption(f"""
        👨‍🎓 **Interface Étudiant - Système Intelligent de Planification des Examens Universitaires**  
        📅 Consultation du calendrier | 📊 Visualisation des notes | ℹ️ Profil personnel  
        🎓 Université Excellence | Formation: {user_info.get('formation', 'Licence Informatique')} | Niveau: {user_info.get('niveau', 'L3')}
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
