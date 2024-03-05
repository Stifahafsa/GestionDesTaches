import csv
from utilisateur import Utilisateur
from tache import Tache

# Programme principal
def programme_principal():
    utilisateurs = []

    try:
        with open('donnees_utilisateurs.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                id_utilisateur = int(row['id_utilisateur'])
                nom = row['nom']
                password = row['password']
                id_tache = int(row['id_tache'])
                description = row['description']
                priorite = row['priorite']
                terminee = row['terminee'] == 'True'

                utilisateur_existant = next((u for u in utilisateurs if u.id_utilisateur == id_utilisateur), None)
                if utilisateur_existant is None:
                    utilisateur_existant = Utilisateur(id_utilisateur, nom, password)
                    utilisateurs.append(utilisateur_existant)

                utilisateur_existant.creerNouvelleTache(id_tache, description, priorite)
                tache = utilisateur_existant.taches[-1]
                tache.terminee = terminee

    except FileNotFoundError:
        pass

    while True:
        print("\nOptions:")
        print("1. Créer un compte utilisateur")
        print("2. Se connecter")
        print("3. Quitter")

        choix = input("Choisissez une option (1-3): ")

        if choix == "1":
            nom_utilisateur = input("Nom d'utilisateur: ")
            password_utilisateur = input("Mot de passe: ")
            nouveau_utilisateur = Utilisateur(len(utilisateurs) + 1, nom_utilisateur, password_utilisateur)
            utilisateurs.append(nouveau_utilisateur)
            print(f"Compte utilisateur créé avec succès. ID: {nouveau_utilisateur.id_utilisateur}")

        elif choix == "2":
            id_utilisateur = int(input("Entrez votre ID utilisateur: "))
            password_utilisateur = input("Entrez votre mot de passe: ")
            utilisateur_actuel = next(
                (u for u in utilisateurs if u.id_utilisateur == id_utilisateur and u.password == password_utilisateur),
                None)

            if utilisateur_actuel:
                interaction_utilisateur(utilisateur_actuel)
            else:
                print("Utilisateur non trouvé ou mot de passe incorrect. Veuillez créer un compte.")

        elif choix == "3":
            print("Au revoir!")
            Utilisateur.sauvegarder_donnees(utilisateurs)
            break

        else:
            print("Option invalide. Veuillez choisir une option valide.")

def interaction_utilisateur(utilisateur):
    while True:
        print("\nOptions utilisateur:")
        print("1. Créer une nouvelle tâche")
        print("2. Afficher les tâches")
        print("3. Modifier la priorité d'une tâche")
        print("4. Marquer une tâche comme terminée")
        print("5. Déconnexion")

        choix_utilisateur = input("Choisissez une option (1-5): ")

        if choix_utilisateur == "1":
            id_tache = len(utilisateur.taches) + 1
            description = input("Description de la tâche: ")
            priorite = input("Priorité de la tâche (Basse/Normal/Elevée), appuyez sur entré pour normale: ").lower()
            if priorite not in ["basse", "normale", "élevée"]:
                priorite = "normale"
            utilisateur.creerNouvelleTache(id_tache, description, priorite)

        elif choix_utilisateur == "2":
            utilisateur.afficherTaches()

        elif choix_utilisateur == "3":
            id_tache = int(input("ID de la tâche à modifier: "))
            nouvelle_priorite = input("Nouvelle priorité (Basse/Normal/Elevée): ").lower()
            utilisateur.modifier_priorite_tache(id_tache, nouvelle_priorite)

        elif choix_utilisateur == "4":
            id_tache = int(input("ID de la tâche à marquer comme terminée: "))
            for tache in utilisateur.taches:
                if tache.id_tache == id_tache:
                    tache.marquerCommeTerminee()
                    print(f"Tâche {id_tache} marquée comme terminée avec succès.")
                    utilisateur.trier_taches_par_priorite()
                    break
            else:
                print(f"Tâche {id_tache} non trouvée.")

        elif choix_utilisateur == "5":
            print("Déconnexion...")
            break

        else:
            print("Option invalide. Veuillez choisir une option valide.")

if __name__ == "__main__":
    programme_principal()
