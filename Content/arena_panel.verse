# ============================================================================
#  ARENA PANEL - panneau de la zone 1v1 : on TIRE sur les formes
#  Chaque forme est un prop surveille par un Prop Manipulator (DamagedEvent
#  donne le joueur qui a tire). Les props sont rendus endommageables au debut.
#  - formes "<" / ">" : vitesse du tireur 100 / 75 / 50 / 25 % (Class Selectors)
#  - forme RESET : un explosif invisible casse tous les builds de l'arene
#  - carres de couleur : un Skydome par couleur (regle dans l'editeur, en mode
#    volume sur l'arene) ; on active celui du carre touche, on coupe les autres
# ============================================================================

using { /Fortnite.com/Devices }
using { /Verse.org/Simulation }
using { /UnrealEngine.com/Temporary/Diagnostics }
using { /Verse.org/Assets }

SpeedText<localizes>(Percent : int) : message = "{Percent}%"

# Tir sur un carre de couleur -> ciel Index
sky_handler := class:
    Panel : arena_panel
    Index : int
    OnHit(Agent : agent) : void =
        Panel.OnSkyHit(Agent, Index)

arena_panel := class(creative_device):

    # ---- Vitesse ----
    @editable
    SpeedDownShape : prop_manipulator_device = prop_manipulator_device{}

    @editable
    SpeedUpShape : prop_manipulator_device = prop_manipulator_device{}

    @editable
    SpeedDisplay : billboard_device = billboard_device{}

    # Class Selectors 100 %, 75 %, 50 %, 25 % (dans cet ordre)
    @editable
    SpeedSelectors : []class_and_team_selector_device = array{}

    # ---- Reset des builds ----
    @editable
    ResetShape : prop_manipulator_device = prop_manipulator_device{}

    # Plusieurs explosifs utilises a tour de role : pendant qu'un se rearme,
    # le suivant est pret (reset reutilisable tout de suite)
    @editable
    ResetExplosives : []explosive_device = array{}

    # ---- Ciel ----
    @editable
    SkyShapes : []prop_manipulator_device = array{}

    # Voute celeste (demi-sphere au-dessus de l'arene) : on lui change de
    # materiau au tir -> changement de ciel instantane
    @editable
    SkyVault : creative_prop = creative_prop{}

    # Materiaux du ciel (meme ordre que SkyShapes : violet, jour, nuit, rose)
    SkyMaterials : []material = array:
        Lobby.Materials.M_SkyVault2_Violet{}
        Lobby.Materials.M_SkyVault2_Jour{}
        Lobby.Materials.M_SkyVault2_Nuit{}
        Lobby.Materials.M_SkyVault2_Rose{}

    # ---- Sol autour de l arene (change de couleur avec le ciel) ----
    @editable
    SkyFloor : creative_prop = creative_prop{}

    FloorMaterials : []material = array:
        Lobby.Materials.M_SkyFloor_Violet{}
        Lobby.Materials.M_SkyFloor_Jour{}
        Lobby.Materials.M_SkyFloor_Nuit{}
        Lobby.Materials.M_SkyFloor_Rose{}

    # Zone fine au ras du sol : la toucher = retour sur le disque principal
    @editable
    FallZone : mutator_zone_device = mutator_zone_device{}

    # Repere (cache en jeu) sur le disque principal
    @editable
    RespawnPoint : creative_prop = creative_prop{}

    # Props des formes : rendus endommageables au demarrage
    @editable
    ShapeProps : []creative_prop = array{}

    # Delai minimum entre deux tirs pris en compte pour la vitesse et le ciel
    @editable
    HitCooldown : float = 0.4

    Percents : []int = array{100, 75, 50, 25}

    var SpeedIndex : [agent]int = map{}
    var LastHit : [agent]float = map{}
    var NextExplosive : int = 0

    OnBegin<override>()<suspends> : void =
        for (Prop : ShapeProps):
            set Prop.CanBeDamaged = true
        SpeedDownShape.DamagedEvent.Subscribe(OnSpeedDown)
        SpeedUpShape.DamagedEvent.Subscribe(OnSpeedUp)
        ResetShape.DamagedEvent.Subscribe(OnResetHit)
        for (I -> Shape : SkyShapes):
            Shape.DamagedEvent.Subscribe(sky_handler{Panel := Self, Index := I}.OnHit)
        SpeedDisplay.SetText(SpeedText(100))
        set SkyVault.CanBeDamaged = false      # la voute ne casse pas si on tire en l'air
        set SkyFloor.CanBeDamaged = false
        RespawnPoint.Hide()
        FallZone.AgentEntersEvent.Subscribe(OnFall)
        ApplySky(0)

    # Vrai si le tir de Agent doit etre pris en compte (anti-rafale)
    Accept(Agent : agent)<transacts><decides> : void =
        Now := GetSimulationElapsedTime()
        Previous := if (P := LastHit[Agent]) then P else -100.0
        Now - Previous >= HitCooldown
        set LastHit[Agent] = Now

    Heal() : void =
        SpeedDownShape.RestoreHealth()
        SpeedUpShape.RestoreHealth()
        ResetShape.RestoreHealth()
        for (Shape : SkyShapes):
            Shape.RestoreHealth()

    # ---------------- vitesse ----------------
    OnSpeedDown(Agent : agent) : void =
        Heal()
        if (Accept[Agent]):
            ChangeSpeed(Agent, 1)

    OnSpeedUp(Agent : agent) : void =
        Heal()
        if (Accept[Agent]):
            ChangeSpeed(Agent, -1)

    ChangeSpeed(Agent : agent, Step : int) : void =
        Current := if (C := SpeedIndex[Agent]) then C else 0
        var Next : int = Current + Step
        if (Next < 0):
            set Next = 0
        if (Next > Percents.Length - 1):
            set Next = Percents.Length - 1
        if (set SpeedIndex[Agent] = Next) {}
        if (Selector := SpeedSelectors[Next]):
            Selector.ChangeClass(Agent)
        if (Percent := Percents[Next]):
            SpeedDisplay.SetText(SpeedText(Percent))

    # ---------------- reset ----------------
    OnResetHit(Agent : agent) : void =
        Heal()
        if (Accept[Agent]):
            if (Explosive := ResetExplosives[NextExplosive]):
                Explosive.Explode(Agent)
                spawn{ Rearm(Explosive) }
            set NextExplosive = if (NextExplosive + 1 < ResetExplosives.Length) then NextExplosive + 1 else 0

    # L'explosif a besoin d'environ 1,5 s avant de pouvoir etre reinitialise
    Rearm(Explosive : explosive_device)<suspends> : void =
        Sleep(1.5)
        Explosive.Reset()
        Heal()

    # ---------------- ciel ----------------
    OnSkyHit(Agent : agent, Index : int) : void =
        Heal()
        if (Accept[Agent]):
            ApplySky(Index)

    ApplySky(Index : int) : void =
        if (Material := SkyMaterials[Index]):
            SkyVault.SetMaterial(Material)
        if (FloorMat := FloorMaterials[Index]):
            SkyFloor.SetMaterial(FloorMat)

    # ---------------- chute sur le sol ----------------
    OnFall(Agent : agent) : void =
        if (TeleportAgentTo[Agent, RespawnPoint]) {}

