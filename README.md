# Project PE
## Proposal Performance Evaluation : Study and comparison of genetic algorithms applied on a road network congestion problem

Gabin Calmet, Solal Stern, Justine Cauvi

Tâche à faire en vrac :

- Faire une simulation de voitures (fichier simulation_voiture)
- Faire un fichier class graph
- Implémenter algo génétique (fichier algo_génétique)
- Partie modélisation du problème et résolution
- Déterminer la fonction de fitness pour notre premier modèle (ax+b)
- Réfléchir au paramètre qu'on ajuste, au metrics qu'on mesure qui sont pertinentes pour notre problème
- Faire les mesures et analyser
- Faire des grapiques explicatifs pour que ce soit clair (notamment un individu c'est une chaîne de Markov...)
- Rédiger le rapport
- Faire la présentation finale
- Respirer, c'est important

Agencement du rapport :

1. State of the art /!\ Notamment quand on a dit congestion is a phenomenon that is purely non-linear, which disqualifies linear programming as soon as we want to make the model more complex : discuss it
2. Modélisation : -description du problème, sa modélisation (chaîne de Markov blabla), résolution si possible
3. Simulation de voitures (pour la fonction de fitness)
4. Après on dit que c'est long donc on va essayer de déterminer une fonction analytique qui permet d'éviter la simulation
5. On teste pour voir si ça fonctionne
6. Simulation : algo génétique
7. Evaluation des performances
