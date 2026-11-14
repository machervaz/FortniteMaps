# Team Deathmatch manager
# - Counts eliminations per team
# - Shows the score on screen with a HUD Message device
# - Ends the game when a team reaches ScoreToWin

using { /Fortnite.com/Devices }
using { /Fortnite.com/Characters }
using { /Fortnite.com/Game }
using { /Fortnite.com/Teams }
using { /Verse.org/Simulation }
using { /UnrealEngine.com/Temporary/Diagnostics }

# Text shown on screen. <localizes> is required for text displayed to players.
ScoreMessage<localizes>(Team1 : int, Team2 : int, Goal : int) : message =
    "Team 1: {Team1}   |   Team 2: {Team2}      (first to {Goal})"

tdm_manager := class(creative_device):

    # Number of eliminations a team needs to win (editable in the Details panel)
    @editable
    ScoreToWin : int = 20

    # Drag your HUD Message device here in the Details panel
    @editable
    ScoreHUD : hud_message_device = hud_message_device{}

    # Drag your End Game device here in the Details panel
    @editable
    EndGame : end_game_device = end_game_device{}

    # Score of team 1 (index 0) and team 2 (index 1)
    var TeamScores : []int = array{0, 0}
    var GameOver : logic = false

    # Runs once when the game starts
    OnBegin<override>()<suspends> : void =
        Playspace := GetPlayspace()
        for (Player : Playspace.GetPlayers()):
            TrackPlayer(Player)
        Playspace.PlayerAddedEvent().Subscribe(TrackPlayer)
        UpdateHUD()

    # Listen to eliminations of this player's character
    TrackPlayer(Player : player) : void =
        if (Character := Player.GetFortCharacter[]):
            Character.EliminatedEvent().Subscribe(OnEliminated)

    # Called every time a tracked player is eliminated
    OnEliminated(Result : elimination_result) : void =
        if (GameOver?):
            return

        if:
            Killer := Result.EliminatingCharacter?        # fails for falls / storm
            KillerAgent := Killer.GetAgent[]
            VictimAgent := Result.EliminatedCharacter.GetAgent[]
            KillerAgent <> VictimAgent                      # ignore self-eliminations
            Teams := GetPlayspace().GetTeamCollection()
            KillerTeam := Teams.GetTeam[KillerAgent]
            Index := Teams.GetTeams().Find[KillerTeam]
            NewScore := TeamScores[Index] + 1
            set TeamScores[Index] = NewScore
        then:
            Print("Team {Index + 1} scores! ({NewScore}/{ScoreToWin})")
            UpdateHUD()
            if (NewScore >= ScoreToWin):
                set GameOver = true
                EndGame.Activate(KillerAgent)               # killer's team wins

    UpdateHUD() : void =
        if (S1 := TeamScores[0], S2 := TeamScores[1]):
            ScoreHUD.SetText(ScoreMessage(S1, S2, ScoreToWin))
            ScoreHUD.Show()
