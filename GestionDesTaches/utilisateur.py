import csv

PRIORITE_MAP = {"basse": 2, "normale": 1, "élevée": 0}

class Utilisateur:
    def __init__(self, id_utilisateur, nom, password):
        self.id_utilisateur = id_utilisateur
        self.nom = nom
        self.password = password
        self.taches = []

    def creerNouvelleTache(self, id_tache, description, priorite="normal"):
        nouvelle_tache = {
            'id_tache': id_tache,
            'description': description,
            'priorite': priorite,
            'terminee': False
        }
        self.taches.append(nouvelle_tache)
        self.trier_taches_par_priorite()

    def afficherTaches(self):
        print(f"Taches de l'utilisateur {self.nom}, triées par priorité")
        for tache in self.taches:
            statut = "Terminée" if tache['terminee'] else "En cours"
            print(f"Tâche {tache['id_tache']}, Description: {tache['description']}, Priorité: {tache['priorite']}, Statut: {statut}")

    def modifier_priorite_tache(self, id_tache, nouvelle_priorite):
        for tache in self.taches:
            if tache['id_tache'] == id_tache:
                if not tache['terminee']:
                    tache['priorite'] = nouvelle_priorite
                    print(f"Priorité de la tâche {id_tache} modifiée avec succès.")
                    self.trier_taches_par_priorite()
                else:
                    print(f"La tâche {id_tache} est terminée et ne peut pas être modifiée.")
                return

        print(f"Tâche {id_tache} non trouvée.")

    def trier_taches_par_priorite(self):
        self.taches.sort(key=lambda x: PRIORITE_MAP[x['priorite']])

    @classmethod
    def sauvegarder_donnees(cls, utilisateurs):
        try:
            with open('donnees_utilisateurs.csv', 'w', newline='') as csvfile:
                fieldnames = ['id_utilisateur', 'nom', 'password', 'id_tache', 'description', 'priorite', 'terminee']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()

                for utilisateur in utilisateurs:
                    for tache in utilisateur.taches:
                        writer.writerow({
                            'id_utilisateur': utilisateur.id_utilisateur,
                            'nom': utilisateur.nom,
                            'password': utilisateur.password,
                            'id_tache': tache['id_tache'],
                            'description': tache['description'],
                            'priorite': tache['priorite'],
                            'terminee': tache['terminee']
                        })

                        print(f"Données écrites pour la tâche {tache['id_tache']} de l'utilisateur {utilisateur.nom}")

        except Exception as e:
            print(f"Une erreur s'est produite lors de la sauvegarde des données : {e}")


