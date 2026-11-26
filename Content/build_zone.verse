# ============================================================================
#  BUILD ZONE - zone de construction (RAMP RUSH, 90s, RETAKE)
#  - EntryZone (portail BUILD du lobby) -> teleporte sur Arrival et donne la
#    classe avec materiaux infinis
#  - ReturnZone (dans la zone) -> retour au lobby
#  Les chronos de chaque piste sont des devices chrono_course.
# ============================================================================

using { /Fortnite.com/Devices }
using { /Verse.org/Simulation }

build_zone := class(creative_device):

    @editable
    EntryZone : mutator_zone_device = mutator_zone_device{}

    @editable
    Arrival : creative_prop = creative_prop{}

    @editable
    ReturnZone : mutator_zone_device = mutator_zone_device{}

    @editable
    LobbyPoint : creative_prop = creative_prop{}

    # classe avec ressources de construction infinies
    @editable
    BuildClass : class_and_team_selector_device = class_and_team_selector_device{}

    OnBegin<override>()<suspends> : void =
        set Arrival.CanBeDamaged = false
        EntryZone.AgentEntersEvent.Subscribe(OnEnter)
        ReturnZone.AgentEntersEvent.Subscribe(OnReturn)

    OnEnter(Agent : agent) : void =
        if (player[Agent], TeleportAgentTo[Agent, Arrival]):
            BuildClass.ChangeClass(Agent)

    OnReturn(Agent : agent) : void =
        if (player[Agent], TeleportAgentTo[Agent, LobbyPoint]) {}
