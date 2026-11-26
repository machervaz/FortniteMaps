# ============================================================================
#  ARENA EXTRAS (zone 1v1)
#  - Score de la session : kills dans l'arene, les 2 meilleurs joueurs presents
#    s'affichent au-dessus du panneau. Bouton RESET SCORE.
#  - Mode de vie (bouton HEALTH) : 100/100, 100/0, 200/200, 1 HP. Applique a
#    l'arrivee dans l'arene, apres chaque kill et a chaque retour.
#  - Le gagnant d'un duel est soigne ; le perdant revient automatiquement dans
#    l'arene apres un compte a rebours.
# ============================================================================

using { /Fortnite.com/Devices }
using { /Fortnite.com/Characters }
using { /Fortnite.com/Game }
using { /Fortnite.com/Playspaces }
using { /Verse.org/Simulation }
using { /UnrealEngine.com/Temporary/Diagnostics }
using { /UnrealEngine.com/Temporary/SpatialMath }

ScoreTwo<localizes>(A : agent, KA : int, B : agent, KB : int) : message = "SCORE   {A}  {KA}   -   {KB}  {B}"
ScoreOne<localizes>(A : agent, KA : int) : message = "SCORE   {A}  {KA}"
ScoreNone<localizes>() : message = "SCORE   ---"
HealthModeText<localizes>(Mode : string) : message = "HEALTH : {Mode}"
BackIn<localizes>(Seconds : int) : message = "Back to the 1v1 arena in {Seconds}..."

arena_extras := class(creative_device):

    @editable
    ScoreBoard : billboard_device = billboard_device{}

    @editable
    ResetScoreButton : button_device = button_device{}

    @editable
    HealthButton : button_device = button_device{}

    @editable
    HealthBoard : billboard_device = billboard_device{}

    # Pad d'arrivee de l'arene (les joueurs y reviennent apres une mort)
    @editable
    ArrivalPoint : creative_prop = creative_prop{}

    @editable
    CountdownHUD : hud_message_device = hud_message_device{}

    @editable
    RespawnDelay : int = 3

    ModeNames : []string = array{"100 / 100", "100 / 0", "200 / 200", "1 HP"}
    ModeHealth : []float = array{100.0, 100.0, 200.0, 1.0}
    ModeShield : []float = array{100.0, 0.0, 200.0, 0.0}

    var Kills : [agent]int = map{}
    var Mode : int = 0
    var Watched : [agent]logic = map{}
    var InArena : [agent]logic = map{}

    OnBegin<override>()<suspends> : void =
        ResetScoreButton.InteractedWithEvent.Subscribe(OnResetScore)
        HealthButton.InteractedWithEvent.Subscribe(OnHealthMode)
        GetPlayspace().PlayerAddedEvent().Subscribe(OnPlayerAdded)
        for (Player : GetPlayspace().GetPlayers()):
            Watch(Player)
        ShowMode()
        RefreshScore()
        # applique le mode de vie aux joueurs qui entrent dans l'arene
        loop:
            Sleep(0.5)
            for (Player : GetPlayspace().GetPlayers(), Player.IsActive[], Char := Player.GetFortCharacter[]):
                Inside := if (Char.IsActive[], In1v1Arena[Char.GetTransform().Translation]) then true else false
                Was := if (InArena[Player]?) then true else false
                if (Inside? and not Was?):
                    ApplyMode(Char)
                if (set InArena[Player] = Inside) {}

    OnPlayerAdded(Player : player) : void =
        Watch(Player)

    Watch(Player : player) : void =
        if (not Watched[Player]?, Char := Player.GetFortCharacter[]):
            if (set Watched[Player] = true) {}
            Char.EliminatedEvent().Subscribe(OnEliminated)
        else if (not Watched[Player]?):
            spawn{ WatchLater(Player) }

    WatchLater(Player : player)<suspends> : void =
        Sleep(2.0)
        if (Player.IsActive[]):
            Watch(Player)

    OnEliminated(Result : elimination_result) : void =
        Victim := Result.EliminatedCharacter
        if (In1v1Arena[Victim.GetTransform().Translation]):
            if:
                Killer := Result.EliminatingCharacter?
                Killer <> Victim
                KillerAgent := Killer.GetAgent[]
            then:
                Current := if (K := Kills[KillerAgent]) then K else 0
                if (set Kills[KillerAgent] = Current + 1) {}
                ApplyMode(Killer)
                RefreshScore()
            if (VictimAgent := Victim.GetAgent[]):
                if (set InArena[VictimAgent] = false) {}
                spawn{ BringBack(VictimAgent) }

    # attend que le joueur reapparaisse puis le renvoie dans l'arene
    BringBack(Agent : agent)<suspends> : void =
        var Tries : int = 0
        loop:
            Sleep(0.5)
            set Tries += 1
            if (Char := Agent.GetFortCharacter[], Char.IsActive[]):
                break
            if (Tries > 40):
                break
        var S : int = RespawnDelay
        loop:
            if (S <= 0):
                break
            CountdownHUD.SetText(BackIn(S))
            CountdownHUD.Show(Agent)
            Sleep(1.0)
            set S -= 1
        CountdownHUD.Hide(Agent)
        if (Char := Agent.GetFortCharacter[], Char.IsActive[]):
            Target := ArrivalPoint.GetTransform().Translation + vector3{X := 0.0, Y := 0.0, Z := 120.0}
            if (Char.TeleportTo[Target, IdentityRotation()]) {}
            ApplyMode(Char)

    ApplyMode(Char : fort_character) : void =
        if (H := ModeHealth[Mode], Sh := ModeShield[Mode]):
            Char.SetMaxHealth(if (H > 100.0) then H else 100.0)
            Char.SetMaxShield(if (Sh > 100.0) then Sh else 100.0)
            Char.SetHealth(H)
            Char.SetShield(Sh)

    OnHealthMode(Agent : agent) : void =
        set Mode = if (Mode + 1 < ModeNames.Length) then Mode + 1 else 0
        ShowMode()
        for (Player : GetPlayspace().GetPlayers(), InArena[Player]?, Char := Player.GetFortCharacter[], Char.IsActive[]):
            ApplyMode(Char)

    ShowMode() : void =
        if (Name := ModeNames[Mode]):
            HealthBoard.SetText(HealthModeText(Name))

    OnResetScore(Agent : agent) : void =
        set Kills = map{}
        RefreshScore()

    RefreshScore() : void =
        var First : ?agent = false
        var FirstK : int = -1
        var Second : ?agent = false
        var SecondK : int = -1
        for (Player : GetPlayspace().GetPlayers(), Player.IsActive[]):
            K := if (KV := Kills[Player]) then KV else 0
            if (K > FirstK):
                set Second = First
                set SecondK = FirstK
                set First = option{Player}
                set FirstK = K
            else if (K > SecondK):
                set Second = option{Player}
                set SecondK = K
        if (A := First?, B := Second?):
            ScoreBoard.SetText(ScoreTwo(A, FirstK, B, SecondK))
        else if (A := First?):
            ScoreBoard.SetText(ScoreOne(A, FirstK))
        else:
            ScoreBoard.SetText(ScoreNone())
