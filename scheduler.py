import datetime
import random
from database import db

class ExamScheduler:
    def __init__(self):
        self.start_date = datetime.datetime(2024, 6, 10, 9, 0)
        self.time_slots = ["09:00", "11:00", "14:00", "16:00"]
    
    def generate_schedule(self, max_exams_per_day=4, days_range=10):
        """Générer automatiquement l'emploi du temps des examens"""
        print("🚀 Début de la génération de l'emploi du temps...")
        
        # 1. Récupérer tous les modules
        modules = db.execute_query(
            "SELECT id, formation_id FROM modules ORDER BY formation_id",
            fetch=True
        )
        
        if not modules:
            print("❌ Aucun module trouvé dans la base de données")
            return False
        
        # 2. Récupérer les salles
        salles = db.execute_query(
            "SELECT id, capacite, type FROM lieu_examen ORDER BY type, capacite",
            fetch=True
        )
        
        # 3. Récupérer les professeurs
        profs = db.execute_query(
            "SELECT id, dept_id FROM professeurs",
            fetch=True
        )
        
        exam_count = 0
        current_date = self.start_date
        day_exam_count = 0
        
        print(f"📊 Nombre de modules à programmer: {len(modules)}")
        
        for i, module_data in enumerate(modules):
            module_id, formation_id = module_data
            
            # Nouveau jour si limite atteinte
            if day_exam_count >= max_exams_per_day:
                current_date += datetime.timedelta(days=1)
                day_exam_count = 0
                print(f"📅 Passage au jour: {current_date.date()}")
            
            # Choisir un créneau horaire
            time_slot = random.choice(self.time_slots)
            hour, minute = map(int, time_slot.split(':'))
            exam_datetime = current_date.replace(hour=hour, minute=minute, second=0)
            
            # Choisir une salle appropriée
            suitable_salle = None
            if salles:
                suitable_salle = salles[i % len(salles)][0]  # Rotation des salles
            
            # Choisir un professeur du même département
            prof_id = None
            dept_result = db.execute_query(
                "SELECT dept_id FROM formations WHERE id = %s",
                (formation_id,),
                fetch=True
            )
            
            if dept_result and profs:
                dept_id = dept_result[0][0]
                for prof_data in profs:
                    prof, prof_dept = prof_data
                    if prof_dept == dept_id:
                        # Vérifier que le professeur n'a pas déjà 3 examens ce jour-là
                        exam_today = db.execute_query(
                            "SELECT COUNT(*) FROM examens WHERE prof_id = %s AND DATE(date_heure) = %s",
                            (prof, exam_datetime.date()),
                            fetch=True
                        )
                        if exam_today and exam_today[0][0] < 3:
                            prof_id = prof
                            break
            
            # Insérer l'examen dans la base de données
            try:
                db.execute_query("""
                    INSERT INTO examens
                    (module_id, prof_id, salle_id, date_heure, duree_minutes)
                    VALUES (%s, %s, %s, %s, %s)
                """, (module_id, prof_id, suitable_salle, exam_datetime, 120))
                
                exam_count += 1
                day_exam_count += 1
                
                if exam_count % 10 == 0:
                    print(f"📝 Examens programmés: {exam_count}")
                    
            except Exception as e:
                print(f"⚠️ Erreur pour le module {module_id}: {e}")
                continue
        
        print(f"✅ {exam_count} examens programmés avec succès!")
        return True
    
    def optimize_schedule(self):
        """Optimiser l'emploi du temps existant"""
        print("🔧 Début de l'optimisation de l'emploi du temps...")
        
        # Vérifier les conflits de salles
        conflicts = db.execute_query("""
            SELECT e1.id, e1.salle_id, l.nom, e1.date_heure, e2.date_heure
            FROM examens e1
            JOIN examens e2 ON e1.salle_id = e2.salle_id
            JOIN lieu_examen l ON e1.salle_id = l.id
            WHERE e1.id != e2.id
            AND DATE(e1.date_heure) = DATE(e2.date_heure)
            AND ABS(EXTRACT(EPOCH FROM (e1.date_heure - e2.date_heure))) < 7200
            ORDER BY e1.salle_id, e1.date_heure
        """, fetch=True)
        
        if conflicts:
            print(f"⚠️ {len(conflicts)} conflits de salles détectés")
            for conflict in conflicts[:5]:  # Afficher les 5 premiers conflits
                print(f"   - Salle {conflict[2]}: conflit entre examens {conflict[0]} et un autre")
        else:
            print("✅ Aucun conflit de salles détecté")
        
        return len(conflicts)

# Exécuter directement si le fichier est lancé
if __name__ == "__main__":
    scheduler = ExamScheduler()
    success = scheduler.generate_schedule()
    if success:
        scheduler.optimize_schedule()