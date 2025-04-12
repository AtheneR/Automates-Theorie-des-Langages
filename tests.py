from automate import Automate
from fonctions import concatener_automates, repetition_automate

        # Partie 1 : Modélisation d’un automate
print("***PARTIE 1 : MODÉLISATION D'UN AUTOMATE***\n")
    # 1.1. Modélisation d’un automate
automate = Automate(['a', 'b', 'c', 'd'])

automate.ajouter_etat('1', est_initial=True)
automate.ajouter_etat('2')
automate.ajouter_etat('3', est_terminal=True)
automate.ajouter_etat('4')

automate.ajouter_transition('1', 'a', '2')
automate.ajouter_transition('1', 'b', '4')
automate.ajouter_transition('2', 'a', '2')
automate.ajouter_transition('2', 'b', '2')
automate.ajouter_transition('2', 'c', '3')
automate.ajouter_transition('2', 'd', '3')
automate.ajouter_transition('4', 'c', '3')
automate.ajouter_transition('4', 'd', '3')

print("---1.1. Modélisation d’un automate---\n")
print(automate)


    # 1.2. Génération d’un fichier image
# on attend ici :
# digraph {
# rankdir=LR
# 3 [shape=doublecircle]
# 4 [shape=circle]
# __1__ [shape=point]
# 1 [shape=circle]
# 2 [shape=circle]
# __1__ -> 1
# 1 -> 2 [label=a]
# 1 -> 4 [label=b]
# 2 -> 2 [label="b,a"]
# 2 -> 3 [label="c,d"]
# 4 -> 3 [label="c,d"]
# }

print("\n---1.2. Génération d’un fichier image---\n")
print(automate.to_dot().source)
automate.to_png("résultats/generation_fichier_image")


    # 1.3. Sauvegarde et chargement d’un automate
automate.sauvegarder('résultats/sauvegarde')

automate_a_charger = Automate()
automate_a_charger.charger('supports/automate_a_charger.txt')
print("\n---1.3. Sauvegarde et chargement d’un automate---\n")
print("    Automate chargé :")
print(automate_a_charger)



        # Partie 2 : Opérations sur les automates
print("\n\n***PARTIE 2 : OPÉRATIONS SUR LES AUTOMATES***")
    # 2.1. L’union de deux automates
automate1 = Automate()
automate1.etats = {"0", "1", "2", "3"}
automate1.alphabet = ["a", "b"]
automate1.etats_initiaux = {"0","2"}
automate1.etats_terminaux = {"3"}
automate1.transitions_symbole = {
    ("0", "0"): ["b"],
    ("0", "1"): ["a"],
    ("1", "2"): ["a,b"],
    ("2", "3"): ["b"],
}

automate2 = Automate()
automate2.etats = {"0", "1"}
automate2.alphabet = ["a", "b"]
automate2.etats_initiaux = {"0"}
automate2.etats_terminaux = {"1"}
automate2.transitions_symbole = {
    ("0", "1"): ["a"],
    ("1", "1"): ["b"],
}
automate_union = automate1.union(automate2)
print("\n---2.1. L’union de deux automates---\n")
print("    Automate après union :")
print(automate_union)
automate_union.to_png("résultats/union")


    # 2.2. Concaténation de deux automates
automate1 = Automate()
automate1.etats = {"0", "1", "2"}
automate1.alphabet = ["a", "b"]
automate1.etats_initiaux = {"0"}
automate1.etats_terminaux = {"1", "2"}
automate1.transitions_symbole = {
    ("0", "1"): ["a"],
    ("0", "2"): ["b"],
    ("1", "1"): ["b"],
}

automate2 = Automate()
automate2.etats = {"0", "1", "2"}
automate2.alphabet = ["a", "b"]
automate2.etats_initiaux = {"0", "1"}
automate2.etats_terminaux = {"2"}
automate2.transitions_symbole = {
    ("0", "2"): ["a"],
    ("1", "2"): ["b"],
}

automate_concatene = concatener_automates(automate1, automate2)
print("\n---2.2. Concaténation de deux automates---\n")
print("   Automate 1 :")
print(automate1)
print("\n   Automate 2 :")
print(automate2)
print("\n   Automate concaténé :")
print(automate_concatene)
automate_concatene.to_png('résultats/concatenation')


    # 2.3. Répétition d’un automate
automate_a_repeter = Automate()
automate_a_repeter.etats = {"0", "1", "2"}
automate_a_repeter.alphabet = ["a", "b"]
automate_a_repeter.etats_initiaux = {"0", "1"}
automate_a_repeter.etats_terminaux = {"2"}
automate_a_repeter.transitions_symbole = {
    ("0", "2"): ["a"],
    ("1", "2"): ["b"],
}

print("\n--- 2.3. Répétition d’un automate --- \n")
print("   Automate à répéter :")
print(automate_a_repeter)
automate_repete=repetition_automate(automate_a_repeter)
print("\n   Automate répété :")
print(automate_concatene)
automate_repete.to_png('résultats/repetition')



        # Partie 4 : Finalisation
print("\n\n***PARTIE 4 : FINALISATION***")
    # 4.1. Compléter un automate
print("\n--- 4.1. Compléter un automate ---\n")
print("    Automate non complété :")
print(automate)
automate.completer()
print("\n    Automate complété :")
print(automate)
automate.to_png("résultats/compléter")


    # 4.2. Déterminisation d’un automate
automate_non_deterministe = Automate()
automate_non_deterministe.etats = {"0", "1", "2", "3"}
automate_non_deterministe.alphabet = ["a", "b"]
automate_non_deterministe.etats_initiaux = {"0", "1"}
automate_non_deterministe.etats_terminaux = {"3"}
automate_non_deterministe.transitions_symbole = {
    ("0", "1"): ["a"],
    ("0", "2"): ["a"],
    ("1", "2"): ["a", "b"],
    ("2", "3"): ["b"]
}

print("\n--- 4.2. Déterminisation d’un automate ---\n")
print("    Automate non déterminisé :")
print("Est déterministe : ", automate_non_deterministe.est_deterministe())
print(automate_non_deterministe)
automate_non_deterministe.to_png("résultats/non_deterministe")

print("\n    Automate déterminisé :")
automate_deterministe = automate_non_deterministe.determiniser()
print("Est déterministe : ", automate_deterministe.est_deterministe())
print(automate_deterministe)
automate_deterministe.to_png("résultats/deterministe")


    # 4.3. Minimisation d’un automate
print("\n--- 4.3. Minimisation d’un automate ---\n")
automate_a_minimiser = Automate()
automate_a_minimiser.etats = {"1", "2", "3", "4"}
automate_a_minimiser.alphabet = ["a", "b"]
automate_a_minimiser.etats_initiaux = {"1"}
automate_a_minimiser.etats_terminaux = {"3","4"}
automate_a_minimiser.transitions_symbole = {
    ("1", "1"): ["b"],
    ("1", "2"): ["a"],
    ("2", "2"): ["a"],
    ("2", "3"): ["b"],
    ("3", "3"): ["b"],
    ("3", "4"): ["a"],
    ("4", "3"): ["b"],
    ("4", "4"): ["a"],
}

print("    Automate non minimisé :")
print(automate_a_minimiser)
automate_a_minimiser.to_png("résultats/non_minimise")

automate_minimise=automate_a_minimiser.minimiser()
print("\n    Automate minimisé :")
print(automate_minimise)
automate_minimise.to_png("résultats/minimise")


    # 4.4. Vérification d’un mot
print("\n--- 4.4. Vérification d’un mot ---\n")
automate_a_verifier = Automate(alphabet=['a', 'b', 'c'])
automate_a_verifier.ajouter_etat('q0', est_initial=True)
automate_a_verifier.ajouter_etat('q1', est_terminal=True)
automate_a_verifier.ajouter_transition('q0', 'a', 'q1')
automate_a_verifier.ajouter_transition('q1', 'b', 'q1')
automate_a_verifier.ajouter_transition('q1', 'c', 'q1')

print("Mot demandé : abc\nRésultat attendu : True\nRésultat : ",automate_a_verifier.accepte_mot('abc'))
print("Mot demandé : aa\nRésultat attendu : False\nRésultat : ",automate_a_verifier.accepte_mot('aa'))


    # 4.5. Application
print("\n--- 4.5. Application ---\n")

automate_email = Automate()
automate_email.charger('supports/automate_lacatholille.txt')

print("lucien.mousin@lacatholille.fr (résultat attendu True) :", automate_email.accepte_mot("lucien.mousin@lacatholille.fr"))
print("jean.dupont2@lacatholille.fr (résultat attendu True) :", automate_email.accepte_mot("jean.dupont2@lacatholille.fr"))

print("123.truc@lacatholille.fr (résultat attendu False) :", automate_email.accepte_mot("123.truc@lacatholille.fr"))
print("dark.sasuke@gmail.com (résultat attendu False) :", automate_email.accepte_mot("dark.sasuke@gmail.com"))