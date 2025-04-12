from automate import Automate

    # 2.2. Concaténation de deux automates
def concatener_automates(automate1, automate2):
    """
    On fait une fonction qui va concaténer deux automates.
    On commencer par récupérer les informations du premier automate, mais on va transformer ses états terminaux en états non-terminaux.
    Ensuite, on va leur ajouter une 𝜖-transition vers un nouvel état que l'on va créer. 
    Le numéro de cet état sera le numéro "suivant" après les états du premier automate.
    Ensuite, ce nouvel état pointera vers les états initiaux du second automate avec une 𝜖-transition.
    On a bien pensé à changer les numéros des états de l'automate 2 pour qu'ils "suivent" le décalage après l'automate 1 et le nouvel état.
    """
    nouvel_automate = Automate()
    # on récupère l'alphabet de chaque automate pour créer l'alphabet du nouvel automate
    nouvel_automate.alphabet = list(set(automate1.alphabet + automate2.alphabet))

    # on copie les états de automate1 et change les anciens états terminaux en états normaux
    nouvel_automate.etats = set(automate1.etats)
    nouvel_automate.etats_initiaux = set(automate1.etats_initiaux)
    nouvel_automate.transitions_symbole = dict(automate1.transitions_symbole)
    anciens_terminaux_a1 = set(automate1.etats_terminaux)
    
    # on crée l'état intermédiaire entre les deux automates
    nouvel_etat = str(max(map(int, nouvel_automate.etats)) + 1)
    nouvel_automate.etats.add(nouvel_etat)

    # on ajoute les 𝜖-transitions des anciens terminaux de l'automate1 vers le nouvel état
    for terminal in anciens_terminaux_a1:
        if (terminal, nouvel_etat) in nouvel_automate.transitions_symbole:
            nouvel_automate.transitions_symbole[(terminal, nouvel_etat)].append("")
        else:
            nouvel_automate.transitions_symbole[(terminal, nouvel_etat)] = []

    # on modifie les états de l'automate2 pour qu'ils aient comme nom la suite des états d'avant avec un décalage puis on ajoute ses transitions avec les noms décalés
    decalage = int(nouvel_etat) + 1
    conversion = {}
    for etat in automate2.etats:
        nouveau_nom = str(int(etat) + decalage)
        conversion[etat] = nouveau_nom
    for nouvel_etat_automate2 in conversion.values():
        nouvel_automate.etats.add(nouvel_etat_automate2)
    for (source, destination), symboles in automate2.transitions_symbole.items():
        nouvelle_source = conversion[source]
        nouvelle_destination = conversion[destination]
        nouvel_automate.transitions_symbole[(nouvelle_source, nouvelle_destination)] = list(symboles)

    # on ajoute les 𝜖-transitions de l'état intermédiaire vers les nouveaux états initiaux de l'automate2
    for etat_initial in automate2.etats_initiaux:
        etat_initial_modifié = conversion[etat_initial]
        nouvel_automate.transitions_symbole[(nouvel_etat, etat_initial_modifié)] = []

    nouvel_automate.etats_terminaux = {conversion[etat] for etat in automate2.etats_terminaux}
    return nouvel_automate

    # 2.3. Répétition d’un automate
def repetition_automate(automate):
    """
    On fait une fonction qui prend un automate en paramètres qui permet de répéter zéro ou plusieurs fois les mots qu'il génère.
    Pour faire cela, on commence par récupérer l'automate donné en paramètres et on va lui rajouter un nouvel état, qui est initial et terminal.
    On ajoute des 𝜖-transitions qui partent de chaque état terminal et qui pointent vers ce nouvel état.
    Ce nouvel état va lui pointer vers chaque état initial avec une 𝜖-transition.    
    """
    nouvel_automate = Automate()
    # on copie les éléments de l'ancien automate
    nouvel_automate.etats = set(automate.etats)
    nouvel_automate.alphabet = list(automate.alphabet)
    nouvel_automate.etats_initiaux = set(automate.etats_initiaux)
    nouvel_automate.etats_terminaux = set(automate.etats_terminaux)
    nouvel_automate.transitions_symbole = dict(automate.transitions_symbole)

    # on trouve l'identitiant qui suit le dernier numéro d'état de l'automate initial et on ajoute le nouvel état
    nouveaux_numeros = []
    for e in nouvel_automate.etats:
        if e.isdigit():
            nouveaux_numeros.append(int(e))
    if nouveaux_numeros:
        nouvel_etat = str(max(nouveaux_numeros) + 1)
    else:
        nouvel_etat = "0"
    nouvel_automate.etats.add(nouvel_etat)
    nouvel_automate.etats_initiaux.add(nouvel_etat)
    nouvel_automate.etats_terminaux.add(nouvel_etat)

    # on ajoute les ε-transitions depuis les états terminaux vers le nouvel état
    for etat_terminal in automate.etats_terminaux:
        cle = (etat_terminal, nouvel_etat)
        if cle not in nouvel_automate.transitions_symbole:
            nouvel_automate.transitions_symbole[cle] = []

    # on ajoute les ε-transitions du nouvel état vers les états initiaux
    for etat_initial in automate.etats_initiaux:
        cle = (nouvel_etat, etat_initial)
        if cle not in nouvel_automate.transitions_symbole:
            nouvel_automate.transitions_symbole[cle] = []

    return nouvel_automate