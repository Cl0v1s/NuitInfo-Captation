# Captation

Captation est un projet réalisé par l'équipe de la compagnie des fiers à bras magiques, mangeurs de sandwich, tueurs d'ennemis à la hache à l'occasion de l'édition 2015 de la nuit de l'info à Bordeaux.

## Sujet

L'objectif du concours était de réaliser une application répondant au sujet "Catastrophes et réseaux sociaux".   
Un ensemble de défis étaient proposés, le but étant, pour les participants, de les remplir, tout en restant dans le cadre du sujet exposé ci-dessus.

## L'application 

Captation est un ensemble de scripts serveurs, couplés à une interface web chargé d'identifier l'existence de menances à partir de twitter, de les géolocaliser et de prévenir les détenteurs de l'application mobile de la proximité d'un danger.
Une fois ceux-ci avertit, il est est possible de signaler leur état de santé afin de fournir un compte-rendu aux ONG humanitaires compétentes.

## Limites

Afin de géolocaliser les catastrophes, le système se base sur la position des tweets associés.
Ceci pose deux problèmes majeurs:

* Très peu de tweets présentent une localisation
* On se base sur la moyenne des positions des tweets pour localiser une catastrophe, elle même identifiée par son nom. De fait si une personne au pole nord, tweet à propos d'une tempête de neige, tandis qu'un autre individu fait de même au pole sud, la tempête sera localisée au niveau de l'équateur.  
