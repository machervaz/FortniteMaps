# ============================================================================
#  AIM TARGETS - salle TARGETS de la zone Aim
#  - FLICKS (30 s) : une cible apparait au hasard, elle reste TargetWindow
#    secondes ; touchee = +1. Score = cibles touchees / cibles apparues.
#  - TRACKING (20 s) : une cible se deplace sur un rail ; chaque balle qui la
#    touche = +1.
#  Les meilleurs scores sont sauvegardes (cles 101 et 102 des records).
# ============================================================================

using { /Fortnite.com/Devices }
using { /Verse.org/Simulation }
using { /Verse.org/Random }
using { /UnrealEngine.com/Temporary/Diagnostics }

FlickResult<localizes>(Hits : int, Shown : int, Acc : int, Best : int) : message =
    "FLICKS  -  {Hits} / {Shown} targets  ({Acc}%)   |   Best: {Best}"
TrackResult<localizes>(Hits : int, Best : int) : message =
    "TRACKING  -  {Hits} hits   |   Best: {Best}"
StartIn<localizes>(S : int) : message = "Get ready... {S}"
GoText<localizes>() : message = "GO !"
BusyText<localizes>() : message = "Someone is already playing, wait a few seconds"

FlickKey : int = 101
TrackKey : int = 102

aim_targets := class(creative_device):

    @editable
    FlickButton : button_device = button_device{}

    @editable
    TrackButton : button_device = button_device{}

    @editable
    FlickTargets : []shooting_range_target_device = array{}

    @editable
    Track : shooting_range_target_track_device = shooting_range_target_track_device{}

    @editable
    Board : billboard_device = billboard_device{}

    @editable
    HUD : hud_message_device = hud_message_device{}

    @editable
    FlickTime : float = 30.0

    # temps pendant lequel une cible reste visible
    @editable
    TargetWindow : float = 1.4

    @editable
    TrackTime : float = 20.0

    # duree d'un aller du rail (la cible fait des allers-retours)
    @editable
    TrackLegTime : float = 2.5

    var Running : logic = false
    var TrackActive : logic = false
    var TrackHits : int = 0

    OnBegin<override>()<suspends> : void =
        FlickButton.InteractedWithEvent.Subscribe(OnFlick)
        TrackButton.InteractedWithEvent.Subscribe(OnTrack)
        Track.HitEvent.Subscribe(OnTrackHit)
        for (T : FlickTargets):
            T.PopDown()
        Track.PopDown()

    OnFlick(Agent : agent) : void =
        if (Running?):
            HUD.SetText(BusyText())
            HUD.Show(Agent)
        else:
            set Running = true
            spawn{ RunFlicks(Agent) }

    OnTrack(Agent : agent) : void =
        if (Running?):
            HUD.SetText(BusyText())
            HUD.Show(Agent)
        else:
            set Running = true
            spawn{ RunTracking(Agent) }

    OnTrackHit() : void =
        if (TrackActive?):
            set TrackHits += 1

    Countdown(Agent : agent)<suspends> : void =
        for (I := 0..2):
            HUD.SetText(StartIn(3 - I))
            HUD.Show(Agent)
            Sleep(1.0)
        HUD.SetText(GoText())
        HUD.Show(Agent)

    RunFlicks(Agent : agent)<suspends> : void =
        Countdown(Agent)
        var Hits : int = 0
        var Shown : int = 0
        var Prev : int = -1
        EndTime := GetSimulationElapsedTime() + FlickTime
        loop:
            if (GetSimulationElapsedTime() >= EndTime or FlickTargets.Length = 0):
                break
            var I : int = GetRandomInt(0, FlickTargets.Length - 1)
            if (I = Prev):
                set I = if (I + 1 < FlickTargets.Length) then I + 1 else 0
            set Prev = I
            if (T := FlickTargets[I]):
                T.Reset()
                T.PopUp()
                set Shown += 1
                Hit := race:
                    block:
                        T.HitEvent.Await()
                        true
                    block:
                        Sleep(TargetWindow)
                        false
                if (Hit?):
                    set Hits += 1
                T.PopDown()
                Sleep(0.15)
        Acc := if (Shown > 0, A := Floor[Hits * 100.0 / (Shown * 1.0)]) then A else 0
        Best := SaveIfBetter(Agent, FlickKey, Hits)
        Result := FlickResult(Hits, Shown, Acc, Best)
        Board.SetText(Result)
        HUD.SetText(Result)
        HUD.Show(Agent)
        set Running = false

    RunTracking(Agent : agent)<suspends> : void =
        Countdown(Agent)
        Track.Reset()
        Track.PopUp()
        Track.EnableTrackMovement()
        set TrackHits = 0
        set TrackActive = true
        race:
            Sleep(TrackTime)
            loop:
                Track.MoveToEnd()
                Sleep(TrackLegTime)
                Track.MoveToStart()
                Sleep(TrackLegTime)
        set TrackActive = false
        Track.DisableTrackMovement()
        Track.PopDown()
        Best := SaveIfBetter(Agent, TrackKey, TrackHits)
        Result := TrackResult(TrackHits, Best)
        Board.SetText(Result)
        HUD.SetText(Result)
        HUD.Show(Agent)
        set Running = false

    # sauvegarde le score s'il bat le record (plus grand = mieux), renvoie le record
    SaveIfBetter(Agent : agent, Key : int, Score : int) : int =
        if (Player := player[Agent]):
            Old := if (B := GetSavedBest[Player, Key]) then B else -1.0
            if (Score * 1.0 > Old):
                SaveBest(Player, Key, Score * 1.0)
                return Score
            if (O := Round[Old]):
                return O
        Score
