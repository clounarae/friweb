# friweb

School project related to the course of Céline Hudelot, on Web Research and Indexation

### Prérequis

Depuis la racine du projet, lancer  `pip3 install -r requirements.txt` pour installer les packages nécessaires à son fonctionnement. \
Il faut ensuite mettre le dossier *Data* à la racine du dossier, en vérifiant bien qu'il contient bien un dossier nommé *CACM*. 
\
Enfin pour lancer le script en lui même il faut tout d'abord lancer `python3 import-export.py` puis `python3 main.py`

### Réponses aux questions

Les réponses aux questions s'affichent dans l'ordre quand le programme est lancé, mais en voici un rappel :
 1. Le vocabulaire contient **16512** éléments distincts : comme le stemming a été implémenté, le vocabulaire ne contient plus que les "root words"
 2. On trouve les coefficients de la Loi de Heap en réalisant une régression linéaire sur les résultats trouvés pour la moitié de la collection et sur son entièreté : **K = 9.951621** et **b= 0.577647**. Pour un millions de
 3. Pour un million de token, on trouve une taille de vocabulaire de **29092** éléments
 4. On peut tracer le diagramme de fréquence de la collection mais nous déconseillons de le faire si ce n'est pas nécessaire car cela prend du temps. 

On peut ensuite choisir dans le script si on veut choisir une méthode booléenne de recherche, en tapant *b* ou une méthode vectorielle en tapant *v*.
La méthode vectorielle prend en compte la pertinence lors du classement des documents, ce qui n'est pas le cas pour la recherche booléenne.


### Description des fichiers 1
 
- Le fichier `import-export.py` s'occupe d'importer et de traiter les données : les différentes fonctions crééent à partir de la collection les tokens, puis le vocabulaire, puis l'index inversé. Ce fichier permet aussi de créer la représentation vectorielle des fichiers de la collection.
-  le fichier `text-processing.py` contient des fonctions permettant le préprocessing de la collection
- Le fichier `utils.py` contient des fonctions "utilitaires", certains pour répondre aux premières questions et dans le fichier d'import-export (tracer le graphe, faire une régression linéaire pour obtenir les coefficients de la loi de Heap...), mais aussi d'autres qui permettent de réaliser la recherche vectorielle (calcul de la cos similarité, calcul des poids)
- le fichier `search-methods.py` contient les deux méthodes de recherche implémentées, vectorielles et booléennes
- le fichier `main.py` permet de lancer le script.

