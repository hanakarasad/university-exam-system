import psycopg2
from config import DB_CONFIG
import time

class Database:
    def __init__(self):
        self.conn = None
        self.max_retries = 3
        self.retry_delay = 2
        self.connect()
    
    def connect(self):
        """Établir la connexion à la base de données avec retry"""
        for attempt in range(self.max_retries):
            try:
                self.conn = psycopg2.connect(**DB_CONFIG)
                print("✅ Connexion à la base de données établie avec succès")
                return
            except Exception as e:
                print(f"❌ Tentative {attempt + 1}/{self.max_retries} échouée: {e}")
                if attempt < self.max_retries - 1:
                    print(f"⏳ Nouvelle tentative dans {self.retry_delay} secondes...")
                    time.sleep(self.retry_delay)
                else:
                    print("⚠️ Connexion échouée, mode démo activé")
                    self.conn = None
    
    def execute_query(self, query, params=None, fetch=False):
        """Exécuter une requête SQL"""
        if self.conn is None:
            print("⚠️ Pas de connexion BD, requête ignorée")
            return [] if fetch else 0
        
        cursor = self.conn.cursor()
        try:
            cursor.execute(query, params or ())
            if fetch:
                result = cursor.fetchall()
                cursor.close()
                return result
            self.conn.commit()
            rowcount = cursor.rowcount
            cursor.close()
            return rowcount
        except Exception as e:
            print(f"❌ Erreur dans la requête: {e}")
            print(f"Requête: {query[:100]}...")
            if params:
                print(f"Paramètres: {params}")
            self.conn.rollback()
            return [] if fetch else 0
        finally:
            if cursor:
                cursor.close()
    
    def close(self):
        """Fermer la connexion"""
        if self.conn:
            self.conn.close()
            print("📤 Connexion fermée")

# Créer une instance globale de la base de données
try:
    db = Database()
except:
    print("⚠️ Impossible de créer l'instance DB")
    db = None