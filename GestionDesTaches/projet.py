import json
import tkinter as tk
from tkinter import simpledialog, messagebox

class Tache:
    def _init_(self, id_tache, description, priorite="normale", terminee=False):
        self.id_tache = id_tache
        self.description = description
        self.priorite = priorite
        self.terminee = terminee

    def marquer_comme_terminee(self):
        self.terminee = True

    def modifier_priorite(self, nouvelle_priorite):
        if not self.terminee:
            self.priorite = nouvelle_priorite
            print(f"Priorité de la tâche {self.id_tache} modifiée avec succès.")
        else:
            print(f"La tâche {self.id_tache} est terminée et ne peut pas être modifiée.")

    def afficher_details(self):
        statut = "Terminée" if self.terminee else "En cours"
        return f"ID: {self.id_tache}, Description: {self.description}, Priorité: {self.priorite}, Statut: {statut}"

class Utilisateur:
    def _init_(self, id_utilisateur, nom, mot_de_passe):
        self.id_utilisateur = id_utilisateur
        self.nom = nom
        self.mot_de_passe = mot_de_passe
        self.taches = []

    def creer_nouvelle_tache(self, id_tache, description, priorite="normale"):
        nouvelle_tache = Tache(id_tache, description, priorite)
        self.taches.append(nouvelle_tache)
        self.trier_taches_par_priorite()

    def afficher_taches(self):
        taches_str = [tache.afficher_details() for tache in self.taches]
        return "\n".join(taches_str)

    def modifier_priorite_tache(self, id_tache, nouvelle_priorite):
        for tache in self.taches:
            if tache.id_tache == id_tache:
                tache.modifier_priorite(nouvelle_priorite)
                self.trier_taches_par_priorite()
                return f"Priorité de la tâche {id_tache} modifiée avec succès."

        return f"Tâche {id_tache} non trouvée ou déjà terminée."

    def marquer_tache_comme_terminee(self, id_tache):
        for tache in self.taches:
            if tache.id_tache == id_tache:
                tache.marquer_comme_terminee()
                self.trier_taches_par_priorite()
                return f"Tâche {id_tache} marquée comme terminée avec succès."

        return f"Tâche {id_tache} non trouvée."

    def trier_taches_par_priorite(self):
        self.taches.sort(key=lambda x: {"basse": 2, "normale": 1, "élevée": 0}[x.priorite])

    def sauvegarder_en_json(self):
        utilisateur_data = {
            "id_utilisateur": self.id_utilisateur,
            "nom": self.nom,
            "mot_de_passe": self.mot_de_passe,
            "taches": [
                {
                    "id_tache": tache.id_tache,
                    "description": tache.description,
                    "priorite": tache.priorite,
                    "terminee": tache.terminee
                }
                for tache in self.taches
            ]
        }

        with open(f"utilisateur_{self.id_utilisateur}.json", "w") as fichier_json:
            json.dump(utilisateur_data, fichier_json)

    def charger_depuis_json(self):
        try:
            with open(f"utilisateur_{self.id_utilisateur}.json", "r") as fichier_json:
                utilisateur_data = json.load(fichier_json)

            self.id_utilisateur = utilisateur_data["id_utilisateur"]
            self.nom = utilisateur_data["nom"]
            self.mot_de_passe = utilisateur_data["mot_de_passe"]

            self.taches = [
                Tache(
                    tache["id_tache"],
                    tache["description"],
                    tache["priorite"],
                    tache["terminee"]
                )
                for tache in utilisateur_data["taches"]
            ]

        except FileNotFoundError:
            print("Aucun fichier JSON trouvé pour cet utilisateur.")

# Interface graphique avec Tkinter
class InterfaceUtilisateur(tk.Tk):
    def _init_(self):
        super()._init_()

        self.title("Gestionnaire de tâches")
        self.geometry("600x400")

        self.utilisateur_actuel = None
        self.creer_widgets_connexion()

    def creer_widgets_connexion(self):
        self.label_instruction = tk.Label(self, text="Options:")
        self.label_instruction.pack(pady=10)

        self.bouton_creer_compte = tk.Button(self, text="Créer un compte utilisateur", command=self.creer_compte)
        self.bouton_creer_compte.pack()

        self.bouton_se_connecter = tk.Button(self, text="Se connecter", command=self.se_connecter)
        self.bouton_se_connecter.pack()

    def creer_widgets_utilisateur(self):
        self.label_utilisateur = tk.Label(self, text=f"Bienvenue, {self.utilisateur_actuel.nom}!")
        self.label_utilisateur.pack(pady=10)

        self.bouton_creer_tache = tk.Button(self, text="Créer une nouvelle tâche", command=self.creer_tache)
        self.bouton_creer_tache.pack()

        self.bouton_afficher_taches = tk.Button(self, text="Afficher les tâches", command=self.afficher_taches)
        self.bouton_afficher_taches.pack()

        self.bouton_deconnexion = tk.Button(self, text="Déconnexion", command=self.deconnexion)
        self.bouton_deconnexion.pack()

    def creer_compte(self):
        nom_utilisateur = self.demander_saisie("Nom d'utilisateur:")
        mot_de_passe = self.demander_saisie("Mot de passe:")
        nouvel_utilisateur = Utilisateur(len(utilisateurs) + 1, nom_utilisateur, mot_de_passe)
        utilisateurs.append(nouvel_utilisateur)
        self.utilisateur_actuel = nouvel_utilisateur
        messagebox.showinfo("Succès", f"Compte utilisateur créé avec succès. ID: {nouvel_utilisateur.id_utilisateur}")
        self.creer_widgets_utilisateur()

    def se_connecter(self):
        id_utilisateur = self.demander_saisie("Entrez votre ID utilisateur:")
        mot_de_passe = self.demander_saisie("Entrez votre mot de passe:")
        utilisateur_actuel = next((u for u in utilisateurs if str(u.id_utilisateur) == id_utilisateur and u.mot_de_passe == mot_de_passe), None)

        if utilisateur_actuel:
            utilisateur_actuel.charger_depuis_json()
            self.utilisateur_actuel = utilisateur_actuel
            self.creer_widgets_utilisateur()
        else:
            messagebox.showerror("Erreur", "Utilisateur non trouvé ou mot de passe incorrect.")

    def creer_tache(self):
        id_tache = len(self.utilisateur_actuel.taches) + 1
        description = self.demander_saisie("Description de la tâche:")
        priorite = self.demander_saisie("Priorité de la tâche (Basse/Normal/Elevée):").lower()
        if priorite not in ["basse", "normale", "élevée"]:
            priorite = "normale"
        self.utilisateur_actuel.creer_nouvelle_tache(id_tache, description, priorite)
        messagebox.showinfo("Succès", "Nouvelle tâche créée avec succès.")

    def afficher_taches(self):
        taches = self.utilisateur_actuel.afficher_taches()
        messagebox.showinfo("Tâches de l'utilisateur", taches)

    def deconnexion(self):
        self.utilisateur_actuel.sauvegarder_en_json()
        self.utilisateur_actuel = None
        self.destroy()

    def demander_saisie(self, message):
        return simpledialog.askstring("Saisie", message)

if __name__ == "__main__":
    utilisateurs = []
    app = InterfaceUtilisateur()
    app.mainloop()