import graphviz

class Automate:
            ## Partie 1 : Modélisation d’un automate
        # 1.1. Modélisation d’un automate
    def __init__(self, alphabet=None):
        """
        On a un constructeur qui prend en paramètre un alphabet.
        On initialise d'abord l’alphabet de l’automate, qui est un ensemble de chaînes de caractères.
        L'alphabet peut être vide, ça nous sert pour le chargement d'un automate car dans ce cas on aura aucune information sur l'automate avant d'avoir chargé le fichier.
        On a ensuite l’ensemble des états de l’automate, l’ensemble des états initiaux de l’automate et l’ensemble des états terminaux de l’automate.
        Pour les transitions, on fait deux dictionnaires :
            - Le premier dictionnaire lie un tuple à un symbole. Dans le tuple, on aura l'état de départ et l'état d'arrivée. 
            Pour une transition (source, destination) -> symbole, on aura donc [source,destination]:symbole.
            Par exemple, on aura [A:B]=1 pour la transition A->(1)->B.
            - Le second dictionnaire lie un tuple à l'état de destination. Dans le tuple, on aura l'état de départ et le symbole.
            Pour une transition (source, destination) -> symbole, on aura donc [source,symbole]:destination.
            Par exemple, on aura [A:1]=B pour la transition A->(1)->B.
        """
        if alphabet is None:
            alphabet = []
        else :
            self.alphabet = set(alphabet)

        self.etats = set()
        self.etats_initiaux = set()
        self.etats_terminaux = set()

        self.transitions_symbole = {}
        self.transitions_destination = {}


    def ajouter_etat(self, id, est_initial=False, est_terminal=False):
        """
        On a une fonction qui ajoute un état à l'automate.
        L'état est identifié par un identifiant unique, son id.
        L'état peut être initial et peut être terminal.
        """
        self.etats.add(id)
        if est_initial:
            self.etats_initiaux.add(id)
        if est_terminal:
            self.etats_terminaux.add(id)


    def ajouter_transition(self, source, symbole, destination):
        """
        On a une fonction qui ajoute une transition à l'automate.
        On pense à ajouter la transition à l'attribut transitions_symbole et à l'attribut transitions_destination.
        On pense aussi à lever une exception si la transition est invalide.
        """
        if source not in self.etats:
            raise ValueError(f"L’état source '{source}' n’existe pas.")
        if destination not in self.etats:
            raise ValueError(f"L’état destination '{destination}' n’existe pas.")
        if symbole not in self.alphabet:
            raise ValueError(f"Le symbole '{symbole}' n’est pas dans l’alphabet.")

        if (source, destination) not in self.transitions_symbole:
            self.transitions_symbole[(source, destination)] = []
        self.transitions_symbole[(source, destination)].append(symbole)

        if (source, symbole) not in self.transitions_destination:
            self.transitions_destination[(source, symbole)] = []
        self.transitions_destination[(source, symbole)].append(destination)

    
    def symbole_transition(self, source, destination):
        """
        On retourne le symbole de la transition entre deux états.
        """
        return self.transitions_symbole.get((source, destination))
    
    
    def destination_transition(self, source, symbole):
        """
        On retourne l’état destination pour une transition donnée (source, symbole).
        """
        return self.transitions_destination.get((source, symbole))
    

    def __str__(self):
        """
        On affiche la représentation demandée dans le sujet, c'est-à-dire suivant ce format :
        Alphabet: {'d', 'a', 'c', 'b'}
        Etats: {'4', '3', '2', '1'}
        Etats initiaux: {'1'}
        Etats terminaux: {'3'}
        Transitions:
            1 --(a)--> 2
            1 --(b)--> 4
            2 --(a,b)--> 2
            2 --(d,c)--> 3
            4 --(d,c)--> 3
        """
        # on va récupérer dans résultat tous les éléments pour construire notre affichage à la fin
        resultat = []
        resultat.append(f"Alphabet: {self.alphabet}")
        resultat.append(f"Etats: {self.etats}")
        resultat.append(f"Etats initiaux: {self.etats_initiaux}")
        resultat.append(f"Etats terminaux: {self.etats_terminaux}")
        resultat.append("Transitions:")

        transitions_regroupees = {}
        for (source, destination), symboles in self.transitions_symbole.items():
            # si une transition a plusieurs stmboles on les regroupe et pour éviter les doublons on les trie
            symboles_unique = sorted(set(symboles))
            transitions_regroupees[(source, destination)] = symboles_unique
        
        # on récupère toutes les transitions en faisant bien attention à traiter les cas où plusieurs symboles relient les deux mêmes états
        for (source, destination), symboles in transitions_regroupees.items():
            symbole_affichage = ",".join(symboles)
            resultat.append(f"{source} --({symbole_affichage})--> {destination}")

        texte_final = "\n".join(resultat)
        return texte_final.strip()

    
        # 1.2. Génération d’un fichier image
    def to_dot(self):
        """
        On fait une fonction qui va sauvegarder le graphe créé sous format dot.
        On va donc construire une chapine de caractères représentant la rédaction suivant le format dot.
        Une fois cela créé, on va le sauvegarder dans un fichier texte au format dot.
        Voici un exemple de chapine de caractères renvoyés :
        digraph {
            rankdir=LR
            3 [shape=doublecircle]
            4 [shape=circle]
            __1__ [shape=point]
            1 [shape=circle]
            2 [shape=circle]
            __1__ -> 1
            1 -> 2 [label=a]
            1 -> 4 [label=b]
            2 -> 2 [label="b,a"]
            2 -> 3 [label="c,d"]
            4 -> 3 [label="c,d"]
        }
        """
        dot = graphviz.Digraph()
        dot.attr(rankdir="LR")

        # on ajoute les premiers états, ceux qui ne sont pas terminaux ou initaux
        for etat in self.etats:
            if etat not in self.etats_terminaux and etat not in self.etats_initiaux:
                dot.node(etat, shape="circle")

        # on ajoute les flèches vers les états initiaux
        for etat in self.etats_initiaux:
            nom_fictif = "__" + etat + "__"
            dot.node(nom_fictif, shape="point")
            dot.edge(nom_fictif, etat)

        # on ajoute les états initiaux
        for etat in self.etats_initiaux:
            dot.node(etat, shape="circle")

        # on ajoute les états finaux
        # on a bien pensé à mettre cette étape après la mise en place des autres états car si l'on a un état initial terminal, si on ne mets pas l'ajout de l'état terminal en dernier, son cercle sera simple et non double
        for etat in self.etats_terminaux:
            dot.node(etat, shape="doublecircle")
        
        # on va traiter l'affichage de chaque transition
        transitions_groupées = {}
        for (source, destination), symboles in self.transitions_symbole.items():
            clé = (source, destination)
            if clé not in transitions_groupées:
                transitions_groupées[clé] = set()

            for s in symboles:
                transitions_groupées[clé].add(s)

        # on ajoute les transitions en regroupant les symboles
        for (source, destination), symboles in transitions_groupées.items():
            # on trie les symboles
            # s'il n'y a pas de symbole, c'est qu'on a une epsilon-transition, donc on ajoute le symbole epsilon
            if not symboles:
                symboles_str = "Ɛ"
            else:
                symboles_str = ",".join(sorted(symboles))

            # si on a plusieurs symboles, on les affiche avec des guillemets autour et une virgule entre les symboles
            if len(symboles_str.split(",")) > 1:
                dot.edge(str(source), str(destination), label=symboles_str)
            else:
                dot.edge(str(source), str(destination), label=symboles_str)

        return dot
    

    def to_png(self, nom_fichier):
        """
        On crée l'image PNG de l'automate et on la sauvegarde dans le fichier nom_fichier.
        """
        dot = self.to_dot()
        dot.render(nom_fichier, format="png", cleanup=True)


        # 1.3. Sauvegarde et chargement d’un automate
    def sauvegarder(self, nom_fichier):
        """
        On sauvegarde l'automate dans un fichier texte.
        On suit l'exemple donné dans le sujet, dont voici un exemple :
        0 1 2 3
        a b c d
        1
        3
        1 a 2
        1 b 4
        2 a 2
        2 b 2
        2 d 3
        2 c 3
        4 d 3
        4 c 3
        On commence donc par enregistrer les états, puis on ajoute l'alphabet.
        On ajoute les états initiaux et les états finaux.
        On ajoute ensuite chaque transition.
        """
        with open(nom_fichier, "w") as file:
            file.write(" ".join(map(str, self.etats)) + "\n")
            file.write(" ".join(self.alphabet) + "\n")
            file.write(" ".join(map(str, self.etats_initiaux)) + "\n")
            file.write(" ".join(map(str, self.etats_terminaux)) + "\n")
            for (source, destination), symboles in self.transitions_symbole.items():
                symboles_str = ",".join(sorted(symboles))
                for symbole in symboles_str.split(","):
                    file.write(f"{source} {symbole} {destination}\n")


    def charger(self, nom_fichier):
        """
        On va charger un automate à partir d'un fichier texte.
        On va commencer par lire les états, puis l'alphabet.
        Ensuite, on va récupérer les états initiaux, puis les états finaux.
        On va finir avec les transitions et pour chaque transition lue, on va l'ajouter dans chacun des deux dictionnaires de transition.
        """
        with open(nom_fichier, "r") as file:
            self.etats = file.readline().strip().split()
            self.alphabet = file.readline().strip().split()
            self.etats_initiaux = file.readline().strip().split()
            self.etats_terminaux = file.readline().strip().split()

            self.transitions_symbole = {}
            self.transitions_destination = {}

            for line in file:
                source, symbole, destination = line.strip().split()
                
                if (source, destination) not in self.transitions_symbole:
                    self.transitions_symbole[(source, destination)] = set()
                self.transitions_symbole[(source, destination)].add(symbole)

                if (source, symbole) not in self.transitions_destination:
                    self.transitions_destination[(source, symbole)] = set()
                self.transitions_destination[(source, symbole)].add(destination)


            ## Partie 2 : Opérations sur les automates
        # 2.1. Union de deux automates
    def union(self, autre_automate):
        """
        On va créer un nouvel automate qui va créer la fusion de deux automates.
        La méthodologie est la suivante :
        1. on ajoute un nouvel automate avec un état initial nommé 0
        2. on rajoute le nouvel état initial aux états initiaux des deux automates par des epsilon-transitions
        3. on ajoute les états, alphabet, transitions et états terminaux du premier automate en pensant bien à renommer les états avec un décalage de 1, car on a utilisé le nom "état 0" pour la racine
        4. on met à jour le décalage avec le nombre d'états du premier automate, et on ajoute les informations du second automate à notre nouvel automate, en renommant les états avec la suite des nombres non utilisés
        """
        nouvel_automate = Automate()
        nouvel_automate.etats.add("0")
        nouvel_automate.etats_initiaux = {"0"}
        
        for etat in self.etats_initiaux:
            nouvel_automate.transitions_symbole[("0", str(int(etat) + 1))] = []
        for etat in autre_automate.etats_initiaux:
            nouvel_automate.transitions_symbole[("0", str(int(etat) + len(self.etats) + 1))] = []

        # on ajoute le premier automate
        décalage = 1
        nouvel_automate.alphabet = list(set(self.alphabet + autre_automate.alphabet))
        for etat in self.etats:
            nouveau_numero = int(etat) + décalage
            nouvel_automate.etats.add(str(nouveau_numero))
        for (source, destination), symboles in self.transitions_symbole.items():
            nouvel_automate.transitions_symbole[(str(int(source) + décalage), str(int(destination) + décalage))] = symboles
        for etat in self.etats_terminaux:
            nouvel_etat = str(int(etat) + décalage)
            nouvel_automate.etats_terminaux.add(nouvel_etat)

        # on ajoute le second automate
        décalage = len(self.etats) + 1
        for etat in autre_automate.etats:
            nouveau_numero = int(etat) + décalage
            nouvel_automate.etats.add(str(nouveau_numero))
        for (source, destination), symboles in autre_automate.transitions_symbole.items():
            nouvel_automate.transitions_symbole[(str(int(source) + décalage), str(int(destination) + décalage))] = symboles
        
        for etat in autre_automate.etats_terminaux:
            nouvel_etat = str(int(etat) + décalage)
            nouvel_automate.etats_terminaux.add(nouvel_etat)
        return nouvel_automate
    

            ## Partie 4 : Finalisation
    def enlever_etats_puits(self):
        """
        Avant de réaliser cette partie là, on met en place une fonction pour enlever les états puits.
        Cette fonction sera utilisée dans plusieurs fonctions de cette partie.
        Cette fonction permet de supprimer les états puits de l'automate.
        Un état puits est un état qui boucle uniquement sur lui-même pour tous les symboles de l'alphabet.
        On fait bien attention à ne pas supprimer un état puit s'il est terminal.
        On va utiliser transitions_symbole, car dès que l'on voit une absence de transition à partir de l'état que l'on regarde ou que les seules destinations sont l'état lui-même, on a un puit.
        """
        etats_puits = set()

        for etat in self.etats:
            # on garde les états terminaux
            if etat in self.etats_terminaux:
                continue

            est_puit = True
            # on fait le parcours de toutes les transitions où l'état est la source
            for (source, destination), symboles in self.transitions_symbole.items():
                if source == etat:
                    if destination != etat:
                        est_puit = False
                        break
            if est_puit:
                etats_puits.add(etat)

        if not etats_puits:
            return self

        # on supprime les états puits
        self.etats -= etats_puits
        self.etats_initiaux -= etats_puits
        self.etats_terminaux -= etats_puits

        # on enlève les transitions qui partent ou vont vers un état puits
        nouvelles_transitions_symbole = {}
        for (source, destination), symboles in self.transitions_symbole.items():
            if source not in etats_puits and destination not in etats_puits:
                nouvelles_transitions_symbole[(source, destination)] = symboles
        self.transitions_symbole = nouvelles_transitions_symbole

        # on fait la même chose pour l'autre dictionnaire de transitions
        nouvelles_transitions_destination = {}
        for (source, symbole), destinations in self.transitions_destination.items():
            garder = True
            if source in etats_puits:
                garder = False
            else:
                for destination in destinations:
                    if destination in etats_puits:
                        garder = False
                        break
            if garder:
                nouvelles_transitions_destination[(source, symbole)] = destinations
        self.transitions_destination = nouvelles_transitions_destination
        return self

    
        # 4.1. Compléter un automate
    def completer(self):
        """
        On fait une fonction qui va compléter l'automate s'il n'est pas déjà complet.
        On va regarder chaque état, puis chaque symbole.
        On regarde s'il existe une transition pour chaque symbole, si ce n'est pas le cas on ajoute une transition vers le nouvel état puit que l'on a nommé puit.
        On renvoie à la fin d'automate complété.
        """
        # pour éviter d'avoir plusieurs puits et compléxifier l'algo, on va commencer par enlever les potentiels puits qu'il pourrait exister
        self.enlever_etats_puits()
        # on ajoute un état "puit" s'il n'existe pas déjà
        etat_puit = "puit"
        if etat_puit not in self.etats:
            self.etats.add(etat_puit)

        for etat in self.etats:
            for symbole in self.alphabet:
                transition_existe = False
                # on parcourt toutes les transitions
                for (source, destination), symboles in self.transitions_symbole.items():
                    if source == etat:
                        # on regarde si le symbole est déjà utilisé pour cette transition
                        if symbole in symboles:
                            transition_existe = True
                            break
                # si aucune transition avec ce symbole n'existe, on en ajoute une vers l'état puit
                if not transition_existe:
                    if (etat, etat_puit) in self.transitions_symbole:
                        self.transitions_symbole[(etat, etat_puit)].append(symbole)
                    else:
                        self.transitions_symbole[(etat, etat_puit)] = [symbole]

        # on ajoute à l'état puit une transition vers lui-même pour tous les symboles de l'alphabet
        for symbole in self.alphabet:
            if (etat_puit, etat_puit) in self.transitions_symbole:
                if symbole not in self.transitions_symbole[(etat_puit, etat_puit)]:
                    self.transitions_symbole[(etat_puit, etat_puit)].append(symbole)
            else:
                self.transitions_symbole[(etat_puit, etat_puit)] = [symbole]


        # 4.2. Déterminisation d’un automate
    def est_deterministe(self):
        """
        On va vérifier les deux critères principaux pour être déterministe.
        On va donc faire en deux temps :
        - on regarde d'abord si l'automate a plus d'un état initial, si c'est le cas, il n'est pas déterministe.
        - on va regarder pour chaque état s'il pointe vers seulement un seul état pour un symbole donné. 
        Si ce n'est pas le cas et que l'état pointe vers plusieurs états avec un seul symbole, il n'est pas déterministe.
        On renverra à la fin True ou False.
        """
        # s'il y a plus d'un état initial l'automate n'est pas déterministe
        if len(self.etats_initiaux) != 1:
            return False

        # on va ajouter chaque transition à une liste de relations
        transitions_par_etat_et_symbole = {}
        for (etat_depart, etat_arrivee), symboles in self.transitions_symbole.items():
            for symbole in symboles:
                cle = (etat_depart, symbole)
                if cle in transitions_par_etat_et_symbole:
                    # on est dans le cas où il y a déjà une relation qui part de cet état de départ avec ce symbole, donc l'automate n'est pas déterministe
                    return False
                else:
                    transitions_par_etat_et_symbole[cle] = etat_arrivee

        # on a jamais eu de contradiction donc l'automate est déterministe
        return True
    
    
    def determiniser(self):
        """
        Pour faire la déterminisation d'un automate, on va faire les étapes que l'on a apprises en cours.
        1. On va créer un unique état initial regroupant tous les états initiaux de l'automate de départ.
        2. On va ajouter ensuite les transitions de ce nouvel état initial vers les anciens états des états initiaux qui le composent.
        3. On va répéter l'ajout des états du nouvel automate tant que l'on a des nouveaux états qui apparaissent et qui sont donc à traiter.
        """
        nouvel_automate = Automate()
        nouvel_automate.alphabet = self.alphabet[:]

        # on crée le nouvel état initial à partir des états initiaux de l'automate de départ
        #on donne par défaut le nom de tous les états qui le composent avec des tirets entre les noms d'états
        etats_initiaux_fusionnes = sorted(self.etats_initiaux)
        etat_initial_nom = "-".join(etats_initiaux_fusionnes)
        nouvel_automate.etats_initiaux = {etat_initial_nom}
        nouvel_automate.etats.add(etat_initial_nom)

        # on fera une liste des états à traiter
        # dès que l'on récupère un état, on regarde s'il a déjà été traité ou s'il a été traité
        # si ce n'est pas le cas, on l'ajoute à la liste des états de l'automate initial à traiter
        etats_a_traiter = [etats_initiaux_fusionnes]
        # ici, la clé sera le nom de l'état concaténé et la valeur la liste des états originaux qui compose le nouvel état
        etats_vus = {}
        etats_vus[etat_initial_nom] = etats_initiaux_fusionnes

        # on va traiter chaque état les uns après les autres tant qu'on a des nouveaux états à traiter
        while etats_a_traiter:
            etats_courants = etats_a_traiter.pop(0)
            # on donne le nom de tous les états qui le composent avec des tirets entre les états
            nom_courant = "-".join(sorted(etats_courants))

            for symbole in self.alphabet:
                nouveaux_etats = set()
                for etat in etats_courants:
                    for (source, cible), symboles in self.transitions_symbole.items():
                        if source == etat and symbole in symboles:
                            nouveaux_etats.add(cible)

                if nouveaux_etats:
                    nouveaux_etats_tries = sorted(nouveaux_etats)
                    nom_nouvel_etat = "-".join(nouveaux_etats_tries)

                    # on ajoute l’état s’il est nouveau
                    if nom_nouvel_etat not in etats_vus:
                        etats_vus[nom_nouvel_etat] = nouveaux_etats_tries
                        etats_a_traiter.append(nouveaux_etats_tries)
                        nouvel_automate.etats.add(nom_nouvel_etat)

                    # on ajoute la transition
                    cle = (nom_courant, nom_nouvel_etat)
                    if cle not in nouvel_automate.transitions_symbole:
                        nouvel_automate.transitions_symbole[cle] = []
                    if symbole not in nouvel_automate.transitions_symbole[cle]:
                        nouvel_automate.transitions_symbole[cle].append(symbole)

        # les états terminaux sont ceux qui sont composés d'au moins un état de l'automate initial qui est terminal
        for nom_etat, anciens_etats in etats_vus.items():
            for etat in anciens_etats:
                if etat in self.etats_terminaux:
                    nouvel_automate.etats_terminaux.add(nom_etat)
                    break

        return nouvel_automate


        # 4.2. Minimisation d’un automate
    def minimiser(self):
        """
        Pour minimiser, on va appliquer l'algorithme de Moore que l'on a vu en cours.

        1. On crée un premier dictionnaire avec l'affectation d'une classe pour chaque état ainsi qu'une matrice de référence avec les transitions.
        Cette matrice sera sous cette forme :
        ['a', '4', '2', 'puit', '2', '4']
        ['b', '3', '3', 'puit', '1', '3']
        Cette technique imite celle que l'on met en place à la main.

        2. on va faire une répétition d'étape tant que l'on arrive à notre condition d'arrêt :
        - on crée la classe correspondant aux transitions en fonction de la partition des états originaux.
        - on met à jour la matrice de transitions associées pour qu'elle corresponde à la nouvelle classe.
        - avant de passer à l'itération suivante, on va calculer temporairement la classe qui viendra à la nouvelle itération. si c'est la même que la classe actuelle, cela veut dire que l'on a trouvé l'automate minimal.
        
        3. une fois l'automate minimal trouvé, on va le créer pour passer de notre structure avec des dictionnaires et des matrices à la classe automate.
        Pour cela on va réaliser plusieurs étapes :
        1. On va parcourir la liste des signatures, qui est la combinaison suivant l'algorithme de moore d'un état associé à un état initial.
        Pour chaque signature, qui sera par exemple sous la forme ("0","1","2","4"), le premier symbole représente l'état, les suivants les états vers lesquels pointe cet état.
        2. On va regarder si le nouvel automate a déjà cet état là.
        Si oui, on passe à la signature suivante, sinon on ajoute à l'automate l'état.
        En reprenant notre exemple, on ajouterait par exemple l'état "0". On va regarder dans le dictionnaire classe_actuelle qui lie les états de départ aux états de l'automate minimal, qui peut ressembler à ceci {'2-3': '0', '0-1': '1', '1-2': '2', '3': '3', '2': '4', 'puit': '5'}, si l'état associé est un état initial et/ou un état terminal.
        Si par exemple on ajoute l'état "0" et que '2-3' est initial, on ajoutera un pointeur initial vers "0".
        3. On va récupérer ensuite les éléments qui forment la suite de la signature. Ils représentent les états vers lesquels pointe l'état que l'on ajoute.
        """
        # on initialise nos variables
        automate = self.determiniser()
        automate.completer()

        etats = list(automate.etats)
        alphabet = list(automate.alphabet)
        etats_initiaux = automate.etats_initiaux
        etats_terminaux = automate.etats_terminaux

        # on récupère les états de l'automate de départ 
        # on va créer un dictionnaire avec une première répartition des états, entre les états terminaux et non-terminaux
        dict_classe_initial = {}
        premier_etat = etats[0]
        if premier_etat in etats_terminaux:
            for etat in etats:
                if etat in etats_terminaux:
                    dict_classe_initial[etat] = "0"
                else:
                    dict_classe_initial[etat] = "1"
        else:
            for etat in etats:
                if etat in etats_terminaux:
                    dict_classe_initial[etat] = "1"
                else:
                    dict_classe_initial[etat] = "0"
        # print("Premiers états répartis entre terminaux et non-terminaux stockés dans un dictionnaire:", dict_classe_initial)

        # on initialise la première matrice de transition
        # ça sera notre matrice de référence pour les itérations de classe
        matrice_transition_initiale = []
        for symbole in alphabet:
            ligne = [symbole]
            for etat in etats:
                destination_trouvee = None
                for (source, destination), symboles in automate.transitions_symbole.items():
                    if source == etat and symbole in symboles:
                        destination_trouvee = destination
                        break
                ligne.append(destination_trouvee)
            matrice_transition_initiale.append(ligne)
        # print("Matrice initiale des transitions de l'automate :")
        # for ligne in matrice_transition_initiale:
        #     print(ligne)

        # on crée la première matrice de transition en initialisant avec les premières valeurs
        liste_classe_temporaire = []
        for etat, groupe in dict_classe_initial.items():
            liste_classe_temporaire.append([etat, groupe])
        # print("Matrice des premiers états :", liste_classe_temporaire)
        
            # on initialise avec la première répartition des classes
        classe_actuelle = dict_classe_initial.copy()
        non_minimal = True
        cpt = 0
        # on va maintenant répéter les étapes plus haut tant que l'on a pas l'automate minimal
        while non_minimal:
            # print(f"\n--- ITERATION {cpt} ---")

            # on construit la matrice de transitions à partir de la classe actuelle
            matrice_transition_temporaire = []
            for symbole in alphabet:
                ligne = [symbole]
                for etat in etats:
                    transition_trouvee = False
                    for (source, destination), symboles in automate.transitions_symbole.items():
                        if source == etat and symbole in symboles:
                            ligne.append(classe_actuelle[destination])
                            transition_trouvee = True
                            break
                    if not transition_trouvee:
                        ligne.append(None)
                matrice_transition_temporaire.append(ligne)

            # print("Matrice transition temporaire :")
            # for ligne in matrice_transition_temporaire:
            #     print(ligne)

            # on génère la nouvelle classe à partir de la signature de l'état
            # on désigne comme signature la combinaisons qui composent un état à la fin de cette étape
            # par exmeple, on pourrait avoit ("0","1","2")
            # on aurait ici le cas de l'état qui a actuellement comme classe "0" (attention, ce n'est pas nécessairment l'état "0" de l'automate initial), qui ira en l'état "1" (temporaire, pas initial) avec le symbole de la première ligne de la matrice (disons "a" par exemple)
            # en suivant cette même logique, "0" irait donc en "2" avec le symbole d'après, disons "b"
            # une fois qu'on a ces signatures (qu'on aurait pu appeler aussi partition), on va créer la classe associée à cette répartition
            # à chaque fois qu'on crée une signature, on fait le changement de classe pour tous les états qui obtiennent à cette étape la même signature
            signatures = {}
            nouvelle_classe = {}
            classe_par_signature = {}
            compteur = 0
            liste_signatures=[]
            for i, etat in enumerate(etats):
                signature = [classe_actuelle[etat]]
                for ligne in matrice_transition_temporaire:
                    signature.append(ligne[i + 1])
                signature_tuple = tuple(signature)
                liste_signatures.append(signature_tuple)

                if signature_tuple not in classe_par_signature:
                    classe_par_signature[signature_tuple] = str(compteur)
                    compteur += 1
                nouvelle_classe[etat] = classe_par_signature[signature_tuple]

            # print("Nouvelle répartition des classes :")
            # for e in etats:
            #     print(f"{e}: {nouvelle_classe[e]}")

            # on vérifie la condition de sortie
            # print("Classe actuelle : ",classe_actuelle)
            if nouvelle_classe == classe_actuelle:
                non_minimal = False
            else:
                # si la classe n'est pas la même que celle de l'étape d'avant, la classe que l'on vient de calculer devient la classe de la prochaine itération
                classe_actuelle = nouvelle_classe
                cpt += 1
        
        # on construit maintenant l'automate minimal
        # print("\n--- CONSTRUCTION DE L'AUTOMATE MINIMAL ---")
        automate_minimal = Automate(alphabet=alphabet)

        for signature in classe_par_signature:
            nom_etat = classe_par_signature[signature]
            if nom_etat in automate_minimal.etats:
                # cela veut dire qu'on aura deux états qui auront fusionné, on ne va pas ajouter le nouvel état plusieurs fois
                continue

            # si l'état n'est pas ajouté, on l'ajoute et ses transitions avec , que l'on récupère dans la matrice
            for cle, val in classe_actuelle.items():
                if val == nom_etat:
                    ancien_etat = cle
                    break
            est_initial = ancien_etat in etats_initiaux
            est_terminal = ancien_etat in etats_terminaux
            automate_minimal.ajouter_etat(nom_etat, est_initial=est_initial, est_terminal=est_terminal)

        for signature in classe_par_signature:
            source = classe_par_signature[signature]
            destinations = signature[1:]
            for i, symbole in enumerate(alphabet):
                destination_classe = destinations[i]
                if destination_classe is not None:
                    automate_minimal.ajouter_transition(source, symbole, destination_classe)

        # on pense bien à enlever les potentiels états puis qu'il pourrait y avoir, pour avoir l'automate minimal sans puit, donc le plus minimal possible
        automate_minimal=automate_minimal.enlever_etats_puits()
        return automate_minimal


        # 4.2. Vérification d’un mot
    def accepte_mot(self, mot):
        """
        Cette fonction vérifie si l'automate accepte le mot donné.
        Le mot est accepté si on peut arriver à un état terminal à la fin du mot en partant de l'un des états initiaux.
        Pour cela, on va parcourir l'automate.
        Si on arrive à un état qui n'a pas de transition avec le symbole à étudier à cette étape, c'est qu'il n'est pas accepté.
        Si on s'arrête au bout du mot sur un état qui n'est pas final, le mot n'est pas non plus accepté.
        """
        # on commence à partir des états initiaux
        etats_actuels = self.etats_initiaux.copy()

        # on parcourt chaque symbole du mot
        for symbole in mot:
            nouveaux_etats = set()
            
            for etat in etats_actuels:
                # si une transition existe pour l'état et le symbole, on ajoute l'état de destination aux nouveaux états
                if (etat, symbole) in self.transitions_destination:
                    nouveaux_etats.update(self.transitions_destination[(etat, symbole)])

            # si aucun nouvel état n'est trouvé, le mot n'est pas accepté
            if not nouveaux_etats:
                return False

            # les nouveaux états deviennent les états actuels pour le prochain symbole
            etats_actuels = nouveaux_etats

        # à la fin, on vérifie si l'un des états actuels est terminal
        if len(etats_actuels & set(self.etats_terminaux)) > 0:
            return True
        else:
            return False