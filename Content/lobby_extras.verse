# ============================================================================
#  LOBBY EXTRAS
#  - Classement global : pour chaque parcours chronometre (tunnels, Piece
#    Control), le meilleur joueur present et son record sauvegarde.
#  - Statistiques sauvegardees par joueur : temps de jeu, kills / morts en 1v1.
#    Bouton "MY STATS" -> message HUD au joueur.
# ============================================================================

using { /Fortnite.com/Devices }
using { /Fortnite.com/Characters }
using { /Fortnite.com/Game }
using { /Fortnite.com/Playspaces }
using { /Verse.org/Simulation }
using { /UnrealEngine.com/Temporary/Diagnostics }
using { /UnrealEngine.com/Temporary/SpatialMath }

GlobalTitle<localizes>() : message = "WORLD RECORDS (players online)"
GlobalLine<localizes>(Course : string, Who : agent, Time : string) : message = "{Course} :  {Who}  {Time} s"
GlobalEmpty<localizes>(Course : string) : message = "{Course} :  ---"
StatsText<localizes>(Minutes : int, Kills : int, Deaths : int, Bots : int, Records : int, Total : int) : message =
    "MY STATS   |   Play time: {Minutes} min   |   1v1 kills: {Kills}   |   1v1 deaths: {Deaths}   |   Bots killed: {Bots}   |   Records: {Records}/{Total}"

# --- statistiques sauvegardees (persistantes) ---
player_stats := class<final><persistable>:
    PlaySeconds : float = 0.0
    Kills1v1 : int = 0
    Deaths1v1 : int = 0
    BotKills : int = 0

var SavedStats : weak_map(player, player_stats) = map{}

GetStats(Player : player) : player_stats =
    if (Stats := SavedStats[Player]) then Stats else player_stats{}

SetStats(Player : player, Stats : player_stats) : void =
    if (Player.IsActive[], set SavedStats[Player] = Stats) {}

AddPlayTime(Player : player, Seconds : float) : void =
    Old := GetStats(Player)
    SetStats(Player, player_stats{PlaySeconds := Old.PlaySeconds + Seconds, Kills1v1 := Old.Kills1v1, Deaths1v1 := Old.Deaths1v1, BotKills := Old.BotKills})

AddKill1v1(Player : player) : void =
    Old := GetStats(Player)
    SetStats(Player, player_stats{PlaySeconds := Old.PlaySeconds, Kills1v1 := Old.Kills1v1 + 1, Deaths1v1 := Old.Deaths1v1, BotKills := Old.BotKills})

AddDeath1v1(Player : player) : void =
    Old := GetStats(Player)
    SetStats(Player, player_stats{PlaySeconds := Old.PlaySeconds, Kills1v1 := Old.Kills1v1, Deaths1v1 := Old.Deaths1v1 + 1, BotKills := Old.BotKills})

# un bot (PNJ ou sentinelle) tue par ce joueur
AddBotKill(Player : player) : void =
    Old := GetStats(Player)
    SetStats(Player, player_stats{PlaySeconds := Old.PlaySeconds, Kills1v1 := Old.Kills1v1, Deaths1v1 := Old.Deaths1v1, BotKills := Old.BotKills + 1})

AddBotKillByChar(Result : elimination_result) : void =
    if (Killer := Result.EliminatingCharacter?, Killer <> Result.EliminatedCharacter, Agent := Killer.GetAgent[], Player := player[Agent]):
        AddBotKill(Player)

# Vrai si la position est dans l'arene 1v1
In1v1Arena(P : vector3)<transacts><decides> : void =
    P.X > -22800.0
    P.X < -17200.0
    P.Y > -2800.0
    P.Y < 2800.0

lobby_extras := class(creative_device):

    # Tous les chronos de la map (tunnels + Piece Control)
    @editable
    Courses : []chrono_course = array{}

    # Classement global : 1er billboard = titre, puis une ligne par parcours (meme ordre que Courses)
    @editable
    GlobalBoard : []billboard_device = array{}

    @editable
    GlobalTextSize : int = 16

    # Bouton "MY STATS" et HUD qui affiche les stats au joueur
    @editable
    StatsButton : button_device = button_device{}

    @editable
    StatsHUD : hud_message_device = hud_message_device{}

    var Watched : [agent]logic = map{}

    OnBegin<override>()<suspends> : void =
        for (I -> Board : GlobalBoard):
            Board.SetTextSize(if (I = 0) then GlobalTextSize + 4 else GlobalTextSize)
        StatsButton.InteractedWithEvent.Subscribe(OnStats)
        GetPlayspace().PlayerAddedEvent().Subscribe(OnPlayerAdded)
        GetPlayspace().PlayerRemovedEvent().Subscribe(OnPlayerRemoved)
        for (Player : GetPlayspace().GetPlayers()):
            Watch(Player)
        spawn{ PlayTimeLoop() }
        loop:
            RefreshGlobal()
            Sleep(5.0)

    OnPlayerAdded(Player : player) : void =
        Watch(Player)

    OnPlayerRemoved(Player : player) : void =
        if (set Watched[Player] = false) {}

    # suit les eliminations du joueur (kills / morts dans l'arene 1v1)
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
            if (VictimPlayer := player[Victim.GetAgent[]]):
                AddDeath1v1(VictimPlayer)
            if:
                Killer := Result.EliminatingCharacter?
                Killer <> Victim
                KillerPlayer := player[Killer.GetAgent[]]
            then:
                AddKill1v1(KillerPlayer)

    PlayTimeLoop()<suspends> : void =
        loop:
            Sleep(30.0)
            for (Player : GetPlayspace().GetPlayers(), Player.IsActive[]):
                AddPlayTime(Player, 30.0)

    OnStats(Agent : agent) : void =
        if (Player := player[Agent]):
            Stats := GetStats(Player)
            var Records : int = 0
            for (Course : Courses, GetSavedBest[Player, Course.CourseLabel]):
                set Records += 1
            Minutes := if (M := Floor[Stats.PlaySeconds / 60.0]) then M else 0
            StatsHUD.SetText(StatsText(Minutes, Stats.Kills1v1, Stats.Deaths1v1, Stats.BotKills, Records, Courses.Length))
            StatsHUD.Show(Agent)

    RefreshGlobal() : void =
        if (Title := GlobalBoard[0]):
            Title.SetText(GlobalTitle())
        for (I -> Course : Courses, Board := GlobalBoard[I + 1]):
            var BestPlayer : ?player = false
            var BestTime : float = 0.0
            for (Player : GetPlayspace().GetPlayers(), Player.IsActive[], Time := GetSavedBest[Player, Course.CourseLabel]):
                if (not BestPlayer?):
                    set BestPlayer = option{Player}
                    set BestTime = Time
                else if (Time < BestTime):
                    set BestPlayer = option{Player}
                    set BestTime = Time
            if (Who := BestPlayer?):
                Board.SetText(GlobalLine(Course.DisplayName(), Who, Course.FormatSeconds(BestTime)))
            else:
                Board.SetText(GlobalEmpty(Course.DisplayName()))
