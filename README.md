![Tests](https://github.com/RIENK-Consulting/fr-phonenumbers/actions/workflows/test.yml/badge.svg)
![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue)
[![PyPI version](https://img.shields.io/pypi/v/fr-phonenumbers.svg)](https://pypi.org/project/fr-phonenumbers/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# fr-phonenumbers

Bibliothèque Python ultra-légère et sans dépendance externe pour identifier l'opérateur et la zone des numéros de téléphone français.

## Le Parti Pris

Contrairement aux bibliothèques lourdes et complexes, **fr-phonenumbers** fait le choix de la simplicité et de la robustesse :
* **Zero dépendance :** Utilise exclusivement la bibliothèque standard de Python.
* **100% Autonome (Offline-friendly) :** Les données sont embarquées directement dans le paquet. Aucun téléchargement réseau à l'exécution, ce qui garantit un fonctionnement parfait derrière les proxys d'entreprise.
* **Performance ($O(\log N)$) :** La recherche s'appuie sur le module natif `bisect` appliqué à des plages de numéros triées, offrant des performances instantanées.

## Installation

```bash
pip install fr-phonenumbers
```

## Utilisation rapide

```python
from fr_phonenumbers import get_operator

resultat = get_operator("0105712345")
print(resultat)
# Sortie : {'code': 'FRTE', 'operator': 'Orange', 'zone': 'Métropole'}
```

## Avertissement : Portabilité des numéros
En raison de la portabilité des numéros en France, l'opérateur renvoyé correspond à l'attributaire initial de la tranche de numérotation (fourni par l'ARCEP), et non nécessairement à l'opérateur réel chez qui le client a porté son numéro. Cette bibliothèque permet d'identifier l'affectation théorique d'une ligne, mais ne peut pas refléter les changements individuels liés à la portabilité.

## Sources des Données

Les données de numérotation sont issues des publications officielles de l'ARCEP sur data.gouv.fr :
* [Ressources en numérotation téléphonique](https://www.data.gouv.fr/datasets/ressources-en-numerotation-telephonique)
* [Identifiants de communications électroniques](https://www.data.gouv.fr/datasets/identifiants-de-communications-electroniques)

## Licence

Distribué sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.