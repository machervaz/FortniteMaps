# Guide – Map d'entraînement (UEFN)

Plan de la map :

```
                 [ ZONE PIECE CONTROL ]
                          ▲
 [ ZONE EDIT ] ◄──  LOBBY (noir + LED bleu/blanc)  ──► [ ZONE AIM ]
                          ▼
                 [ ZONE 1V1 BUILDFIGHT ]
```

Place les zones **à au moins 150 m** du lobby (et entre elles) pour que les joueurs ne se voient pas d'une zone à l'autre.

Scripts Verse fournis :
- `Content/training_hub.verse` → device **training_hub_manager** (téléportations, retour lobby, vitesse 1v1, rotation des hologrammes)
- `Content/chrono_course.verse` → device **chrono_course** (chrono pour les parcours piece control / edit)

Après avoir ajouté les fichiers : **Verse → Build Verse Code** (Ctrl+Shift+B). Les deux devices apparaissent ensuite dans le Content Browser, dans le dossier du projet.

---

## 1. Lobby noir avec LED bleu électrique et blanc

**Ambiance générale**
1. Pose un **Day Sequence Device** : heure = nuit, désactive le soleil et la lune, nuages à 0.
2. Ajoute un **Post Process Volume** (Unbound = true) : exposition légèrement plus basse, Bloom ≈ 1.5 pour que les LED « bavent ».
3. Si tu veux, ajoute un peu de **Exponential Height Fog** bleu foncé (#020814) pour donner de la profondeur.

**Structure**
- Sol, murs et plafond : props cubes/plaques (galerie *Shape Primitives*) avec un matériau **noir mat** (Base Color #050505, Roughness 0.8).
- Sol légèrement brillant si tu veux des reflets : Roughness 0.2.

**LED**
- Bandes LED : longues plaques fines (≈ 5 cm d'épaisseur) le long des arêtes du sol, des murs et du plafond, avec un **matériau émissif** :
  - Bleu électrique : couleur `#00AAFF` (ou `#0066FF`), Emissive × 20
  - Blanc : `#FFFFFF`, Emissive × 10
  - Alterne : bleu sur les arêtes du sol/plafond, blanc en lignes verticales sur les murs.
- **Customizable Light Device** au plafond (couleur `#0080FF`, intensité moyenne) + quelques spots blancs dirigés vers les cylindres.

## 2. Cylindres holographiques (un par zone)

Pour chaque zone (Piece Control, Edit, Aim, 1v1) :

1. **Le visuel** : un prop *Cylinder* (Shape Primitives), ≈ 3 m de diamètre, 4 m de haut, **collision désactivée**.
   Matériau hologramme (Material Editor) :
   - Blend Mode : *Translucent*, Shading Model : *Unlit*
   - Emissive = couleur (bleu `#00CFFF` ou blanc) × **Fresnel** (exposant ≈ 3) × 15
   - Opacity = Fresnel × 0.6 + bandes horizontales (*Panner* vertical sur une texture de lignes) pour l'effet scan
2. **Le socle** : un disque fin émissif bleu au sol sous le cylindre.
3. **Le nom de la zone** : un **Billboard Device** au-dessus (« PIECE CONTROL », « EDIT », « AIM », « 1V1 »), texte blanc.
4. **Option** : un **Beacon Device** couleur bleu au centre pour un faisceau lumineux vertical.
5. **Le déclencheur** : une **Mutator Zone** de la taille du cylindre (≈ 3 × 3 × 4 m) placée dedans.
6. **L'arrivée** : dans la zone d'entraînement, un petit prop (pad) avec **collision désactivée** → c'est la `Destination`. Les joueurs arrivent 1,5 m au-dessus.

Dans chaque zone d'entraînement, place aussi un cylindre **« RETOUR LOBBY »** (même visuel, blanc) avec sa Mutator Zone.
Pose aussi un petit pad (collision off) dans le lobby → `LobbyPoint`.

> Les cylindres d'arrivée/retour doivent être à quelques mètres du point d'arrivée, sinon le joueur est renvoyé direct.

## 3. Zone Piece Control

Idées d'exercices (construits avec des props ou en mode Créatif) :
- **Cône + mur** : parcours de pièces à reproduire rapidement (90s, tunnels, side-jumps).
- **Couloir de retakes** : rampe adverse au-dessus du joueur à reprendre.
- **Parcours chrono** : un **Trigger** au départ, un **Trigger** à l'arrivée, un **HUD Message Device** → reliés à un device **chrono_course** (`CourseName` = « Piece Control 1 »).

Donne des matériaux à l'arrivée : **Item Granter** (bois/brique/métal 999) dans `Loadouts` du portail.
Paramètres de l'île : *Infinite Building Materials = On*, *Building Can Destroy Environment = Off*.

## 4. Zone Edit

- Rangées de murs / sols / escaliers / cônes **éditables** (pièces construites en Créatif ou props de construction joueur).
- Panneaux (Billboard) avec les edits à faire : fenêtre, porte, demi-mur, triangle, arche…
- **Parcours chrono edit** : une ligne de murs à éditer pour passer, Trigger départ/arrivée + **chrono_course**.
- Pour remettre les murs à zéro : un **Button Device** « RESET » relié à un **Prop Manipulator** / ou rejoue la séquence avec un **Barrier Device**.
  (Le plus simple : utiliser des murs placés en Créatif et le paramètre *Respawn des builds* de la zone si disponible.)

## 5. Zone Aim

- **Shooting Gallery Target** (cibles fixes et mobiles) + **Shooting Gallery Target Track** pour les cibles qui bougent.
- **Training Dummy / Guard Spawner** (gardes en mode passif) pour le tracking.
- **Score Manager** + **Timer Device** : défi « 60 secondes, combien de cibles ? »
- Armes données à l'arrivée : **Item Granter** (AR, SMG, pompe, sniper) dans `Loadouts`.
- Réglage : munitions infinies, *Infinite Reload*.

## 6. Zone 1v1 Buildfight + ralentissement

1. Une arène fermée (≈ 60 × 60 m) avec 2 **Player Spawn Pads**, mats infinis, un **Item Granter** pour le kit.
2. **Vitesse réglable** :
   - Pose 4 **Class Designer** : classe 1 = `Movement Multiplier 1.0`, classe 2 = `0.75`, classe 3 = `0.5`, classe 4 = `0.25`.
   - Pose 4 **Class and Team Selector** (un par classe, *Class to Switch to* = 1, 2, 3, 4).
   - Pose 4 **Button Device** au bord de l'arène : « 100 % », « 75 % », « 50 % », « 25 % ».
   - Dans `SpeedOptions` du manager : associe chaque bouton à son selector.
3. Le Class Selector **100 %** va dans `DefaultClass` du manager (retour à la vitesse normale en revenant au lobby).

> ⚠️ Limite Fortnite : on ne peut pas ralentir le *temps du jeu* (slow-motion) ni la vitesse de construction/edit. Ce qu'on ralentit ici, c'est la **vitesse de déplacement** du joueur, ce qui laisse plus de temps pour placer ses pièces et analyser les situations.

## 7. Brancher le device `training_hub_manager`

Glisse **training_hub_manager** dans la map (n'importe où, il est invisible), puis dans le panneau *Details* :

| Champ | Quoi mettre |
|---|---|
| `Portals` | 4 entrées (une par zone) : `ZoneName`, `EntryZone` (Mutator Zone du cylindre), `Destination` (pad d'arrivée), `Loadouts` (Item Granters), `WelcomeMessages` (HUD Message, optionnel), `ClassOnEnter` (optionnel) |
| `ReturnZones` | les Mutator Zones des cylindres « RETOUR LOBBY » |
| `LobbyPoint` | le pad d'arrivée du lobby |
| `DefaultClass` | le Class Selector 100 % |
| `SpeedOptions` | 4 entrées bouton → selector |
| `Holograms` | les props cylindres à faire tourner (optionnel) |
| `HologramQuarterTurnTime` | vitesse de rotation (3 s par quart de tour) |

Pour chaque **Item Granter** : *Receiving Players* = *Instigating Player*, et pour chaque **HUD Message** : texte de bienvenue de la zone.

Pour les **Mutator Zones** : désactive tous les effets (pas de dégâts, pas de modification), elles servent juste de détecteur.

## 8. Tester

1. **Build Verse Code** → corrige les éventuelles erreurs affichées dans le *Verse Log*.
2. **Launch Session**, entre dans chaque cylindre, vérifie téléport, kit, retour lobby, boutons de vitesse.

---

## 9. (Plan B) Décor du lobby généré automatiquement – `lobby_builder.verse`

Le device **lobby_builder** fait apparaître au lancement : sol/murs/plafond noirs, LED bleues (bords + grille au sol), lignes LED blanches sur les murs, et un hologramme flottant + socle sur chaque Mutator Zone de portail.

1. **Crée 5 props** (Content Browser → clic droit → *Blueprint Class* → *Creative Prop*), chacun avec un *Static Mesh* :
   | Nom | Mesh | Matériau | Collision |
   |---|---|---|---|
   | `BP_BlackBlock` | Cube 1 m | noir mat | normale |
   | `BP_BlueLed` | Cube 1 m | émissif `#00AAFF` × 20 | **NoCollision** |
   | `BP_WhiteLed` | Cube 1 m | émissif blanc × 10 | **NoCollision** |
   | `BP_HoloCylinder` | Cylindre 1 m | hologramme (section 2) | **NoCollision** |
   | `BP_BlueDisc` | Cylindre 1 m | émissif `#00AAFF` | **NoCollision** |
2. Pose **lobby_builder** au centre du lobby, au niveau du sol, et assigne les 5 props dans *Details*.
3. Pose les 4 **Mutator Zones** des portails dans le lobby (ex. à 12 m du centre : +X, −X, +Y, −Y) → `PortalZones`. Les Mutator Zones « retour » → `ReturnZones`.
4. Pose un petit sol réel sous le **Player Spawner** (le décor apparaît une fraction de seconde après le début).
5. Le décor n'est visible qu'en jeu (*Launch Session*), pas dans l'éditeur.
