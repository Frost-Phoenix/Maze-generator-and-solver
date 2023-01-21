Le jeu fonctionne avec le clavier, pour naviguer dans les menus et lancer les algos 
il faut utiliser la touche correspondante. 

Comprend :
    -> 3 algorithmes de générations de labyrinthes (avec un seul chemin possible): 
        - DFS qui creuse le labyrinthes avec une pile
        - kruskal qui crée un quadrillage est casse aléatoirement des mur selon certaines règles
        - prism qui s’étend dans toutes les directions à la fois

        - le départ est toujours placer dans un des 4 coins, et l'arrivé sur une case vide alléatoire 

    -> 3 algorithmes de résolution de labyrinthes (avec indication du chemin si arrivé accessible): 
        - DFS (depth first search) parcours en profondeur aves une pile 
        - BFS (depth first search) parcours en largeur aves une file 
        - A* qui connait la position de l'arrivé et trouve le plus court chemin 
                (ne se déplace que dans les 4 direction cardinale)

    -> Un éditeur pour pouvoir s'amuser avec des obstacles custom :)
        - A* est l'algorithmes le plus approprier pour ce mode 


PS: Veuliez m'excuser de l'absence de commentaires, je n'ai pas eu le temps pour m'en occuper.