# ============================================================================
#  TUNNEL RESET - remet les pieces des tunnels d'edit a neuf, sans relancer
#  la partie.
#  1. Les Explosive Devices (invisibles, 0 degat aux joueurs) detruisent les
#     pieces editees.
#  2. Le Cinematic Sequence Device joue une sequence qui decharge puis
#     recharge le Data Layer "DL_TunnelBuilds" : les pieces d'origine
#     reapparaissent.
# ============================================================================

using { /Fortnite.com/Devices }
using { /Verse.org/Simulation }

tunnel_reset := class(creative_device):

    # Boutons "RESET TUNNELS"
    @editable
    Buttons : []button_device = array{}

    # Explosifs qui nettoient les pieces editees
    @editable
    Explosives : []explosive_device = array{}

    # Sequence qui recharge le Data Layer des pieces
    @editable
    ReloadSequence : cinematic_sequence_device = cinematic_sequence_device{}

    # Attente entre l'explosion et le rechargement (secondes)
    @editable
    ReloadDelay : float = 0.5

    var Busy : logic = false

    OnBegin<override>()<suspends> : void =
        for (Button : Buttons):
            Button.InteractedWithEvent.Subscribe(OnReset)

    OnReset(Agent : agent) : void =
        if (not Busy?):
            set Busy = true
            spawn{ DoReset(Agent) }

    DoReset(Agent : agent)<suspends> : void =
        for (Explosive : Explosives):
            Explosive.Explode(Agent)
        Sleep(ReloadDelay)
        ReloadSequence.Play()
        Sleep(3.0)
        for (Explosive : Explosives):
            Explosive.Reset()
        set Busy = false
