# ============================================================================
#  TRAINING HUB - Lobby avec cylindres holographiques
#  - Chaque cylindre (mutator zone) teleporte vers une zone d'entrainement
#  - Chaque zone a un portail "retour lobby"
#  - Zone 1v1 : boutons pour choisir la vitesse de deplacement (100/75/50/25 %)
#  - Les hologrammes tournent lentement sur eux-memes
# ============================================================================

using { /Fortnite.com/Devices }
using { /Fortnite.com/Characters }
using { /Verse.org/Simulation }
using { /UnrealEngine.com/Temporary/SpatialMath }
using { /UnrealEngine.com/Temporary/Diagnostics }

# ----------------------------------------------------------------------------
#  Un portail = un cylindre holographique dans le lobby
# ----------------------------------------------------------------------------
hub_portal := class<concrete>:

    # Nom de la zone (pour les logs)
    @editable
    ZoneName : string = "Zone"

    # Mutator Zone placee DANS le cylindre holographique (declencheur)
    @editable
    EntryZone : mutator_zone_device = mutator_zone_device{}

    # Prop "marqueur" a l'endroit d'arrivee (petit pad, collision desactivee)
    @editable
    Destination : creative_prop = creative_prop{}

    # (Optionnel) Item Granters a declencher en arrivant (armes, materiaux...)
    @editable
    Loadouts : []item_granter_device = array{}

    # (Optionnel) HUD Message a afficher au joueur en arrivant
    @editable
    WelcomeMessages : []hud_message_device = array{}

    # (Optionnel) Class Selector a appliquer en arrivant (ex: classe vitesse 100 %)
    @editable
    ClassOnEnter : []class_and_team_selector_device = array{}

    Init() : void =
        set Destination.CanBeDamaged = false     # jamais detruit par un explosif de reset
        EntryZone.AgentEntersEvent.Subscribe(OnEnter)

    OnEnter(Agent : agent) : void =
        if (TeleportAgentTo[Agent, Destination]):
            Print("Teleporte vers : {ZoneName}")
            for (Selector : ClassOnEnter):
                Selector.ChangeClass(Agent)
            for (Granter : Loadouts):
                Granter.GrantItem(Agent)
            for (Hud : WelcomeMessages):
                Hud.Show(Agent)

# ----------------------------------------------------------------------------
#  Un bouton de vitesse dans la zone 1v1
#  Chaque bouton est relie a un Class Selector -> Class Designer
#  dont le "Movement Multiplier" est regle (1.0 / 0.75 / 0.5 / 0.25)
# ----------------------------------------------------------------------------
speed_option := class<concrete>:

    @editable
    Button : button_device = button_device{}

    @editable
    ClassSelector : class_and_team_selector_device = class_and_team_selector_device{}

    Init() : void =
        Button.InteractedWithEvent.Subscribe(OnPressed)

    OnPressed(Agent : agent) : void =
        ClassSelector.ChangeClass(Agent)

# ----------------------------------------------------------------------------
#  Teleportation commune (au-dessus du marqueur pour ne pas rester coince)
# ----------------------------------------------------------------------------
TeleportAgentTo(Agent : agent, Target : creative_prop)<transacts><decides> : void =
    Character := Agent.GetFortCharacter[]
    T := Target.GetTransform()
    Character.TeleportTo[T.Translation + vector3{X := 0.0, Y := 0.0, Z := 150.0}, T.Rotation]

# ----------------------------------------------------------------------------
#  Device principal a poser dans la map
# ----------------------------------------------------------------------------
training_hub_manager := class(creative_device):

    # Les cylindres du lobby (Piece Control, Edit, Aim, 1v1...)
    @editable
    Portals : []hub_portal = array{}

    # Mutator Zones "retour lobby" placees dans chaque zone d'entrainement
    @editable
    ReturnZones : []mutator_zone_device = array{}

    # Marqueur d'arrivee dans le lobby
    @editable
    LobbyPoint : creative_prop = creative_prop{}

    # Class Selector "normal" (vitesse 100 %) applique au retour lobby
    @editable
    DefaultClass : []class_and_team_selector_device = array{}

    # Boutons de vitesse de la zone 1v1
    @editable
    SpeedOptions : []speed_option = array{}

    # Props du cylindre holographique a faire tourner (optionnel)
    @editable
    Holograms : []creative_prop = array{}

    # Duree d'un quart de tour des hologrammes (secondes)
    @editable
    HologramQuarterTurnTime : float = 3.0

    OnBegin<override>()<suspends> : void =
        for (Portal : Portals):
            Portal.Init()
        for (Zone : ReturnZones):
            Zone.AgentEntersEvent.Subscribe(OnReturnToLobby)
        for (Option : SpeedOptions):
            Option.Init()
        for (Holo : Holograms):
            spawn{ AnimateHologram(Holo) }

    OnReturnToLobby(Agent : agent) : void =
        if (TeleportAgentTo[Agent, LobbyPoint]):
            for (Selector : DefaultClass):
                Selector.ChangeClass(Agent)

    # Rotation infinie d'un hologramme autour de son axe vertical
    AnimateHologram(Holo : creative_prop)<suspends> : void =
        loop:
            T := Holo.GetTransform()
            NewRotation := T.Rotation.ApplyYaw(DegreesToRadians(90.0))
            Holo.MoveTo(T.Translation, NewRotation, HologramQuarterTurnTime)
