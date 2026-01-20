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
# 3. PAGE DE CONNEXION PROFESSIONNELLE
# ============================================

def login_page():
    """Page de connexion professionnelle"""
    st.set_page_config(page_title="Connexion", page_icon="🔐", layout="wide")
    
    # CSS professionnel SANS ESPACE BLANC
    st.markdown("""
    <style>
    /* Supprimer les espaces blancs */
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
        margin: 100px auto;
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
    </style>
    """, unsafe_allow_html=True)
    
    # En-tête universitaire
    st.markdown("""
    <div class="university-info">
        <div class="university-name">🎓 Université Excellence</div>
        <div class="university-slogan">Système Intelligent de Gestion des Examens</div>
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
                                help="Exemple: ADM001, PROF001, ETUD001")
        
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
    
    # Comptes de démonstration
    with st.expander("### 📋 Comptes de Démonstration", expanded=True):
        st.markdown("""
        <div class="account-card">
        <h4>👨‍💼 Administrateur</h4>
        <p><strong>Matricule:</strong> ADM001</p>
        <p><strong>Mot de passe:</strong> admin123</p>
        <p><em>Accès complet au système</em></p>
        </div>
        
        <div class="account-card">
        <h4>👨‍🏫 Professeur</h4>
        <p><strong>Matricule:</strong> PROF001</p>
        <p><strong>Mot de passe:</strong> prof123</p>
        <p><em>Gestion des examens et étudiants</em></p>
        </div>
        
        <div class="account-card">
        <h4>👨‍🎓 Étudiant</h4>
        <p><strong>Matricule:</strong> ETUD001</p>
        <p><strong>Mot de passe:</strong> etud123</p>
        <p><em>Consultation des examens et résultats</em></p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer avec l'année 2026 et version 1
    st.markdown(f"""
    <div style="text-align:center; margin-top:50px; color:white; opacity:0.8;">
    <p>© 2026 Université Excellence - Tous droits réservés</p>
    <p style="font-size:14px;">Version 1.0 | Système de Gestion des Examens</p>
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
    
    .badge-admin { background: #ff6b6b; color: white; }
    .badge-prof { background: #4ecdc4; color: white; }
    .badge-etud { background: #45b7d1; color: white; }
    
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
            
            if st.button("📊 Exporter Rapports", use_container_width=True):
                st.success("📁 Rapports exportés! (Simulation)")
        
        elif role == 'professeur':
            st.markdown('<div class="stat-card">', unsafe_allow_html=True)
            st.metric("📅 Mes Examens", "15")
            st.metric("⏰ Heures/Semaine", "25")
            st.metric("👥 Étudiants", "450")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.divider()
            
            if st.button("📋 Voir Mes Examens", use_container_width=True):
                st.success("✅ Liste chargée")
            
            if st.button("📈 Mes Statistiques", use_container_width=True):
                st.info("📊 Statistiques affichées")
            
            if st.button("✏️ Saisir Notes", use_container_width=True):
                st.warning("📝 Module de saisie (simulation)")
        
        elif role == 'etudiant':
            st.markdown('<div class="stat-card">', unsafe_allow_html=True)
            st.metric("📅 Mes Examens", "8")
            st.metric("📊 Moyenne", "14.5/20")
            st.metric("🎯 Crédits", "45/60")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.divider()
            
            if st.button("📅 Mon Calendrier", use_container_width=True):
                st.success("🗓️ Calendrier affiché")
            
            if st.button("📄 Mes Résultats", use_container_width=True):
                st.info("📈 Résultats consultés")
            
            if st.button("📚 Mes Cours", use_container_width=True):
                st.warning("📖 Liste des cours (simulation)")
        
        st.divider()
        st.caption(f"📍 Connecté en tant que {role.title()}")
        st.caption(f"🕐 {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}")

    # ============================================
    # ONGLETS SELON LE RÔLE
    # ============================================
    
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    
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
            
            # Statistiques
            col_stat1, col_stat2, col_stat3 = st.columns(3)
            with col_stat1:
                st.metric("Examens filtrés", len(df_exams))
            with col_stat2:
                total_students = df_exams["Étudiants"].sum() if not df_exams.empty else 0
                st.metric("Étudiants concernés", f"{total_students:,}")
            with col_stat3:
                st.metric("Jours d'examen", df_exams["Date"].apply(lambda x: x.split()[0]).nunique())
            
            # Graphiques
            col_chart1, col_chart2 = st.columns(2)
            with col_chart1:
                st.subheader("📊 Distribution par Département")
                dept_counts = df_exams["Département"].value_counts()
                st.bar_chart(dept_counts)
            
            with col_chart2:
                st.subheader("🎯 Capacité des salles")
                room_data = df_exams.groupby("Salle")["Étudiants"].sum().reset_index()
                fig = px.bar(room_data, x='Salle', y='Étudiants', title="Nombre d'étudiants par salle")
                st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            st.header("🏛️ Gestion des Salles d'Examen")
            df_rooms = get_demo_rooms()
            
            # Filtre par type
            type_filter = st.selectbox("Type de salle", ["Tous", "Amphithéâtre", "Salle", "Laboratoire"])
            
            if type_filter != "Tous":
                df_rooms = df_rooms[df_rooms["Type"] == type_filter]
            
            st.dataframe(df_rooms, use_container_width=True)
            
            # Graphique des capacités
            st.subheader("📏 Capacité des Salles")
            fig = px.bar(df_rooms, x='Nom', y='Capacité', 
                        color='Type', title="Distribution des Capacités",
                        hover_data=['Bâtiment', 'Examens'])
            st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            st.header("👨‍🏫 Gestion des Professeurs")
            df_profs = get_demo_professors()
            
            # Filtre par département
            dept_filter = st.selectbox("Département", 
                                      ["Tous", "Informatique", "Mathématiques", "Physique", "Chimie"])
            
            if dept_filter != "Tous":
                df_profs = df_profs[df_profs["Département"] == dept_filter]
            
            st.dataframe(df_profs, use_container_width=True)
            
            # Statistiques
            col_prof1, col_prof2 = st.columns(2)
            with col_prof1:
                st.metric("Nombre de professeurs", len(df_profs))
            with col_prof2:
                total_exams = df_profs["Examens"].sum() if not df_profs.empty else 0
                st.metric("Examens attribués", total_exams)
        
        with tab4:
            st.header("📈 Tableau de Bord Administratif")
            
            # Métriques principales
            col1, col2, col3, col4 = st.columns(4)
            with col1: 
                st.metric("Examens aujourd'hui", "15", "+2", delta_color="normal")
            with col2: 
                st.metric("Salles occupées", "87%", "+3%")
            with col3: 
                st.metric("Alertes système", "3", "-1", delta_color="inverse")
            with col4: 
                st.metric("Taux satisfaction", "94%", "+2%")
            
            st.divider()
            
            # Graphiques avancés
            col_chart1, col_chart2 = st.columns(2)
            
            with col_chart1:
                st.subheader("📅 Charge d'examens par jour")
                exam_days = pd.DataFrame({
                    "Jour": ["10/06", "11/06", "12/06", "13/06", "14/06"],
                    "Examens": [15, 18, 12, 20, 16],
                    "Étudiants": [4500, 5200, 3800, 6000, 4800]
                })
                fig1 = px.line(exam_days, x='Jour', y='Examens', title="Évolution quotidienne")
                st.plotly_chart(fig1, use_container_width=True)
            
            with col_chart2:
                st.subheader("🎯 Répartition des formations")
                formations_data = pd.DataFrame({
                    "Formation": ["Informatique", "Mathématiques", "Physique", "Chimie", "Droit"],
                    "Étudiants": [45000, 28000, 22000, 18000, 15000]
                })
                fig2 = px.pie(formations_data, values='Étudiants', names='Formation', 
                             title="Répartition par formation")
                st.plotly_chart(fig2, use_container_width=True)
        
        with tab5:
            st.header("⚙️ Configuration du Système")
            
            with st.form("admin_config"):
                st.subheader("Paramètres de planification")
                
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
                
                st.subheader("Paramètres de notification")
                notify_students = st.checkbox("Notifications aux étudiants", value=True)
                notify_professors = st.checkbox("Notifications aux professeurs", value=True)
                notify_admin = st.checkbox("Alertes administrateur", value=True)
                
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    save_btn = st.form_submit_button("💾 Sauvegarder la configuration", 
                                                   use_container_width=True)
                with col_btn2:
                    test_btn = st.form_submit_button("🧪 Tester les paramètres", 
                                                   use_container_width=True)
                
                if save_btn:
                    st.success("✅ Configuration sauvegardée avec succès!")
                if test_btn:
                    st.info("🧪 Test des paramètres en cours...")
    
    elif role == 'professeur':
        # Professeur: Onglets spécifiques
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
    
    elif role == 'etudiant':
        # Étudiant: Onglets simples
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
                **Année:** 2025-2026
                **Niveau:** L3
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
    
    if role == 'admin':
        st.caption("""
        ⚠️ **Système de Gestion des Examens - Version Admin 1.0**  
        📊 Gestion complète de 130,000 étudiants | 🏛️ 65 salles | 👨‍🏫 120 professeurs  
        🔧 Développé avec: Python • Streamlit • PostgreSQL | 🕐 Dernière mise à jour: Aujourd'hui
        """)
    elif role == 'professeur':
        st.caption("""
        👨‍🏫 **Interface Professeur - Système de Gestion des Examens**  
        📅 Planification d'examens | 👥 Gestion d'étudiants | 📊 Suivi des résultats
        🎯 Université Excellence | Année académique 2025-2026
        """)
    elif role == 'etudiant':
        st.caption("""
        👨‍🎓 **Interface Étudiant - Système de Gestion des Examens**  
        📅 Consultation du calendrier | 📊 Visualisation des notes | ℹ️ Profil personnel
        🎓 Université Excellence | Formation: Licence Informatique | Niveau: L3
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