# ============================================================================
#  AMBIANCE - musique de la map
#  - Radios : une radio par zone (lobby, aim, build...). Chaque joueur entend
#    la musique tant qu'il ne l'a pas coupee.
#  - Bouton MUSIC (lobby) : coupe / remet la musique pour CE joueur.
# ============================================================================

using { /Fortnite.com/Devices }
using { /Fortnite.com/Playspaces }
using { /Verse.org/Simulation }

MusicOnText<localizes>() : message = "Music : ON"
MusicOffText<localizes>() : message = "Music : OFF"

ambiance := class(creative_device):

    @editable
    Radios : []radio_device = array{}

    @editable
    MusicButton : button_device = button_device{}

    @editable
    MusicHUD : hud_message_device = hud_message_device{}

    var Muted : [agent]logic = map{}

    OnBegin<override>()<suspends> : void =
        MusicButton.InteractedWithEvent.Subscribe(OnMusic)
        GetPlayspace().PlayerAddedEvent().Subscribe(OnPlayerAdded)
        Sleep(2.0)
        for (Player : GetPlayspace().GetPlayers()):
            Listen(Player)
        for (Radio : Radios):
            Radio.Play()
        # reinscrit regulierement les joueurs (arrivees tardives, reapparitions)
        loop:
            Sleep(5.0)
            for (Player : GetPlayspace().GetPlayers(), not Muted[Player]?):
                Listen(Player)

    OnPlayerAdded(Player : player) : void =
        Listen(Player)

    Listen(Agent : agent) : void =
        for (Radio : Radios):
            Radio.Register(Agent)

    OnMusic(Agent : agent) : void =
        if (Muted[Agent]?):
            if (set Muted[Agent] = false) {}
            Listen(Agent)
            MusicHUD.SetText(MusicOnText())
        else:
            if (set Muted[Agent] = true) {}
            for (Radio : Radios):
                Radio.Unregister(Agent)
            MusicHUD.SetText(MusicOffText())
        MusicHUD.Show(Agent)
