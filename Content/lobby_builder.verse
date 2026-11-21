# ============================================================================
#  LOBBY BUILDER - genere automatiquement le decor du lobby au lancement
#  - Sol, murs et plafond noirs
#  - Bandes LED bleu electrique (bords sol/plafond + grille au sol)
#  - Lignes LED blanches verticales sur les murs
#  - Un cylindre holographique (qui flotte et tourne) sur chaque Mutator Zone
#    de portail, avec un socle bleu (portails) ou blanc (retour lobby)
#
#  Pose ce device AU CENTRE du lobby, au niveau du sol.
#  Toutes les tailles sont en centimetres (100 = 1 m).
# ============================================================================

using { /Fortnite.com/Devices }
using { /Verse.org/Simulation }
using { /UnrealEngine.com/Temporary/SpatialMath }

# Raccourci pour ecrire un vecteur
V(X : float, Y : float, Z : float)<computes> : vector3 = vector3{X := X, Y := Y, Z := Z}

lobby_builder := class(creative_device):

    # ---- Props a creer dans le Content Browser (voir le guide) ----
    # Cube 1 m, materiau noir mat, collision normale
    @editable
    BlackBlock : creative_prop_asset = DefaultCreativePropAsset

    # Cube 1 m, materiau emissif bleu electrique, sans collision
    @editable
    BlueLed : creative_prop_asset = DefaultCreativePropAsset

    # Cube 1 m, materiau emissif blanc, sans collision
    @editable
    WhiteLed : creative_prop_asset = DefaultCreativePropAsset

    # Cylindre 1 m, materiau hologramme translucide, SANS collision
    @editable
    HoloCylinder : creative_prop_asset = DefaultCreativePropAsset

    # Cylindre 1 m, materiau emissif bleu, sans collision (socle des portails)
    @editable
    BlueDisc : creative_prop_asset = DefaultCreativePropAsset

    # ---- Dimensions du lobby ----
    @editable
    LobbySize : float = 4000.0          # 40 m x 40 m

    @editable
    LobbyHeight : float = 1200.0        # 12 m

    @editable
    WallThickness : float = 50.0

    @editable
    LedThickness : float = 10.0

    @editable
    WhiteLinesPerWall : int = 4

    @editable
    FloorGridSpacing : float = 1000.0   # une ligne bleue au sol tous les 10 m

    # ---- Portails ----
    # Mutator Zones des cylindres du lobby (socle bleu)
    @editable
    PortalZones : []mutator_zone_device = array{}

    # Mutator Zones "retour lobby" dans les zones d'entrainement (socle blanc)
    @editable
    ReturnZones : []mutator_zone_device = array{}

    @editable
    HoloDiameter : float = 300.0

    @editable
    HoloHeight : float = 400.0

    # Hauteur du flottement et duree d'un demi-cycle (secondes)
    @editable
    HoloBob : float = 30.0

    @editable
    HoloCycleTime : float = 2.0

    OnBegin<override>()<suspends> : void =
        O := GetTransform().Translation
        BuildRoom(O)
        BuildLeds(O)
        for (Zone : PortalZones):
            BuildHologram(Zone, BlueDisc)
        for (Zone : ReturnZones):
            BuildHologram(Zone, WhiteLed)

    # ------------------------------------------------------------------------
    #  Sol, plafond, 4 murs
    # ------------------------------------------------------------------------
    BuildRoom(O : vector3)<transacts> : void =
        H := LobbySize / 2.0
        W := WallThickness
        Outer := LobbySize + 2.0 * W
        Box(BlackBlock, O + V(0.0, 0.0, -W / 2.0), V(Outer, Outer, W))
        Box(BlackBlock, O + V(0.0, 0.0, LobbyHeight + W / 2.0), V(Outer, Outer, W))
        Box(BlackBlock, O + V(H + W / 2.0, 0.0, LobbyHeight / 2.0), V(W, Outer, LobbyHeight))
        Box(BlackBlock, O + V(-H - W / 2.0, 0.0, LobbyHeight / 2.0), V(W, Outer, LobbyHeight))
        Box(BlackBlock, O + V(0.0, H + W / 2.0, LobbyHeight / 2.0), V(Outer, W, LobbyHeight))
        Box(BlackBlock, O + V(0.0, -H - W / 2.0, LobbyHeight / 2.0), V(Outer, W, LobbyHeight))

    # ------------------------------------------------------------------------
    #  LED
    # ------------------------------------------------------------------------
    BuildLeds(O : vector3)<transacts> : void =
        H := LobbySize / 2.0
        L := LedThickness
        Normals := array{V(1.0, 0.0, 0.0), V(-1.0, 0.0, 0.0), V(0.0, 1.0, 0.0), V(0.0, -1.0, 0.0)}

        for (N : Normals):
            Tangent := V(-N.Y, N.X, 0.0)
            Inner := O + N * (H - L / 2.0)

            # Bandes bleues en bas et en haut des murs (sur toute la longueur)
            Box(BlueLed, Inner + V(0.0, 0.0, L), Size(N, Tangent, L, LobbySize, 2.0 * L))
            Box(BlueLed, Inner + V(0.0, 0.0, LobbyHeight - L), Size(N, Tangent, L, LobbySize, 2.0 * L))

            # Lignes blanches verticales
            Count := WhiteLinesPerWall + 1
            for (I := 1..WhiteLinesPerWall):
                Offset := -H + LobbySize * (1.0 * I) / (1.0 * Count)
                Box(WhiteLed, Inner + Tangent * Offset + V(0.0, 0.0, LobbyHeight / 2.0),
                    Size(N, Tangent, L, 2.0 * L, LobbyHeight - 4.0 * L))

        # Grille bleue au sol
        if (FloorGridSpacing > 0.0):
            var Pos : float = -H + FloorGridSpacing
            loop:
                if (Pos >= H):
                    break
                Box(BlueLed, O + V(Pos, 0.0, 1.0), V(L, LobbySize, 2.0))
                Box(BlueLed, O + V(0.0, Pos, 1.0), V(LobbySize, L, 2.0))
                set Pos += FloorGridSpacing

    # Taille d'une bande : Depth = epaisseur vers le mur, Length = le long du mur
    Size(N : vector3, Tangent : vector3, Depth : float, Len : float, Tall : float)<computes> : vector3 =
        Along := V(Abs(N.X) * Depth + Abs(Tangent.X) * Len, Abs(N.Y) * Depth + Abs(Tangent.Y) * Len, Tall)
        Along

    # ------------------------------------------------------------------------
    #  Hologramme pose sur une Mutator Zone
    # ------------------------------------------------------------------------
    BuildHologram(Zone : mutator_zone_device, BaseAsset : creative_prop_asset) : void =
        P := Zone.GetTransform().Translation
        Box(BaseAsset, P + V(0.0, 0.0, 3.0), V(HoloDiameter * 1.3, HoloDiameter * 1.3, 6.0))
        Center := P + V(0.0, 0.0, HoloHeight / 2.0 + 20.0)
        if (Holo := Box(HoloCylinder, Center, V(HoloDiameter, HoloDiameter, HoloHeight))?):
            spawn{ Animate(Holo, Center) }

    Animate(Holo : creative_prop, Base : vector3)<suspends> : void =
        Quarter := DegreesToRadians(90.0)
        loop:
            R1 := Holo.GetTransform().Rotation.ApplyYaw(Quarter)
            Holo.MoveTo(Base + V(0.0, 0.0, HoloBob), R1, HoloCycleTime)
            R2 := Holo.GetTransform().Rotation.ApplyYaw(Quarter)
            Holo.MoveTo(Base, R2, HoloCycleTime)

    # ------------------------------------------------------------------------
    #  Fait apparaitre un cube/cylindre de 1 m mis a l'echelle
    # ------------------------------------------------------------------------
    Box(Asset : creative_prop_asset, Center : vector3, Dimensions : vector3)<transacts> : ?creative_prop =
        Result := SpawnProp(Asset, transform{Translation := Center, Rotation := IdentityRotation(), Scale := Dimensions * 0.01})
        Result(0)
