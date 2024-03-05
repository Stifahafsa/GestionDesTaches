class Tache:
    def __init__(self, id_tache, description, priorite="normal"):
        self.id_tache = id_tache
        self.description = description
        self.priorite = priorite
        self.terminee = False

    def marquerCommeTerminee(self):
        self.terminee = True

    def afficherDetails(self):
        statut = "Terminée" if self.terminee else "En cours"
        print(f"Tâche {self.id_tache}, Description: {self.description}, Priorité: {self.priorite}, Statut: {statut}")
