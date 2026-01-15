from database import db

class ConflictChecker:
    def check_all_conflicts(self):
        """Vérifier tous les types de conflits"""
        print("🔍 Vérification des conflits...")
        
        conflicts = {
            "conflits_salles": self.check_room_conflicts(),
            "conflits_etudiants": self.check_student_conflicts(),
            "conflits_professeurs": self.check_professor_conflicts(),
            "conflits_capacite": self.check_capacity_conflicts()
        }
        
        total_conflicts = 0
        for conflict_list in conflicts.values():
            if conflict_list:
                total_conflicts += len(conflict_list)
        
        print(f"📊 Total des conflits détectés: {total_conflicts}")
        
        return conflicts
    
    def check_room_conflicts(self):
        """Conflits de salles (même salle à même heure)"""
        result = db.execute_query("""
            SELECT DISTINCT e1.salle_id, l.nom, DATE(e1.date_heure) as date,
                   COUNT(*) as nb_conflits
            FROM examens e1
            JOIN examens e2 ON e1.salle_id = e2.salle_id 
                AND e1.id < e2.id
                AND DATE(e1.date_heure) = DATE(e2.date_heure)
                AND ABS(EXTRACT(EPOCH FROM (e1.date_heure - e2.date_heure))) < 7200
            JOIN lieu_examen l ON e1.salle_id = l.id
            GROUP BY e1.salle_id, l.nom, DATE(e1.date_heure)
            HAVING COUNT(*) > 0
        """, fetch=True)
        return result if result else []
    
    def check_student_conflicts(self):
        """Étudiants avec plusieurs examens le même jour"""
        result = db.execute_query("""
            SELECT e.etudiant_id, et.nom, et.prenom, 
                   DATE(ex.date_heure) as date_examen,
                   COUNT(DISTINCT ex.id) as nb_examens
            FROM inscriptions e
            JOIN examens ex ON e.module_id = ex.module_id
            JOIN etudiants et ON e.etudiant_id = et.id
            GROUP BY e.etudiant_id, et.nom, et.prenom, DATE(ex.date_heure)
            HAVING COUNT(DISTINCT ex.id) > 1
            ORDER BY nb_examens DESC
            LIMIT 20
        """, fetch=True)
        return result if result else []
    
    def check_professor_conflicts(self):
        """Professeurs avec plus de 3 examens par jour"""
        result = db.execute_query("""
            SELECT p.id, p.nom, p.prenom, 
                   DATE(e.date_heure) as date_examen,
                   COUNT(*) as nb_examens
            FROM professeurs p
            JOIN examens e ON p.id = e.prof_id
            GROUP BY p.id, p.nom, p.prenom, DATE(e.date_heure)
            HAVING COUNT(*) > 3
            ORDER BY nb_examens DESC
        """, fetch=True)
        return result if result else []
    
    def check_capacity_conflicts(self):
        """Examens avec plus d'étudiants que la capacité de la salle"""
        result = db.execute_query("""
            SELECT e.id, m.nom as module, l.nom as salle, 
                   l.capacite, COUNT(i.etudiant_id) as nb_etudiants
            FROM examens e
            JOIN modules m ON e.module_id = m.id
            JOIN lieu_examen l ON e.salle_id = l.id
            JOIN inscriptions i ON m.id = i.module_id
            GROUP BY e.id, m.nom, l.nom, l.capacite
            HAVING COUNT(i.etudiant_id) > l.capacite
        """, fetch=True)
        return result if result else []

# Exemple d'utilisation
if __name__ == "__main__":
    checker = ConflictChecker()
    conflicts = checker.check_all_conflicts()
    
    for type_conflit, resultats in conflicts.items():
        print(f"\n{type_conflit.upper()}:")
        if resultats:
            for ligne in resultats[:3]:
                print(f"   - {ligne}")
        else:
            print("   ✅ Aucun conflit")