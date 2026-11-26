# ============================================================================
#  CHRONO COURSE - chronometre pour un parcours (tunnels d'edit, Piece Control)
#  - Mutator Zone de depart -> lance le chrono du joueur
#  - Mutator Zone d'arrivee -> affiche le temps + record perso, puis teleporte
#    le joueur sur ReturnPoint (optionnel)
#  - Les records sont SAUVEGARDES (persistants) : ils restent apres une
#    deconnexion / une nouvelle partie. Le TOP 5 classe tous les joueurs
#    presents dans la partie avec leur record sauvegarde.
#  Pose un device par parcours. Les zones sont invisibles en jeu.
# ============================================================================

using { /Fortnite.com/Devices }
using { /Fortnite.com/Playspaces }
using { /Verse.org/Simulation }
using { /UnrealEngine.com/Temporary/Diagnostics }

ChronoText<localizes>(Course : string, Time : string, Best : string) : message =
    "{Course}  -  Time: {Time} s   |   Best: {Best} s"

# lignes du tableau des meilleurs temps (le nom du joueur s'affiche via {Who})
LeaderLine<localizes>(Rank : int, Who : agent, Time : string) : message = "{Rank}. {Who}  {Time}"
EmptyLine<localizes>(Rank : int) : message = "{Rank}.  ---"
LeaderTitle<localizes>(Course : string) : message = "TOP 5 - {Course}"
SplitText<localizes>(Index : int, Time : string) : message = "Split {Index} :  {Time} s"
RecordText<localizes>(Course : string, Time : string) : message = "NEW RECORD !   {Course}  -  {Time} s"

split_handler := class:
    Course : chrono_course
    Index : int
    OnEnter(Agent : agent) : void =
        Course.OnSplit(Agent, Index)

# --- records sauvegardes : numero de parcours -> meilleur temps (secondes) ---
course_records := class<final><persistable>:
    Best : [int]float = map{}

var SavedRecords : weak_map(player, course_records) = map{}

GetSavedBest(Player : player, Key : int)<transacts><decides> : float =
    Records := SavedRecords[Player]
    Records.Best[Key]

SaveBest(Player : player, Key : int, Time : float) : void =
    if (Player.IsActive[]):
        var NewBest : [int]float = map{}
        if (Records := SavedRecords[Player]):
            set NewBest = Records.Best
        if (set NewBest[Key] = Time) {}
        if (set SavedRecords[Player] = course_records{Best := NewBest}) {}

chrono_course := class(creative_device):

    @editable
    CourseName : string = "Parcours"

    # (Optionnel) numero de parcours Piece Control : 1..9 -> nom pris dans PieceControlNames
    # (les textes Verse ne se reglent pas depuis Python, les entiers si)
    # Sert aussi de cle pour la sauvegarde des records (un numero different par parcours)
    @editable
    CourseLabel : int = 0

    PieceControlNames : []string = array{"Corridor 1", "Corridor 2", "Corridor 3", "Climb 1", "Climb 2", "Climb 3", "Descent 1", "Descent 2", "Descent 3", "Climb 4", "Easy", "Medium", "Hard", "Impossible", "Ramp Rush", "90s", "Retake"}

    # Zone de depart (Mutator Zone a l'entree)
    @editable
    StartTrigger : mutator_zone_device = mutator_zone_device{}

    # Zone d'arrivee (Mutator Zone a la fin)
    @editable
    FinishTrigger : mutator_zone_device = mutator_zone_device{}

    # HUD Message device qui affiche le resultat
    @editable
    ResultHUD : hud_message_device = hud_message_device{}

    # (Optionnel) Pad ou le joueur est teleporte a l'arrivee (ex: entree des tunnels)
    @editable
    ReturnPoint : []creative_prop = array{}

    # (Optionnel) reset des constructions a l'arrivee : explosifs + sequences qui
    # rechargent le Data Layer des pieces d'origine (Piece Control)
    @editable
    ResetExplosives : []explosive_device = array{}

    @editable
    ResetSequences : []cinematic_sequence_device = array{}

    # (Optionnel) tableau des 5 meilleurs temps : 1er billboard = titre, puis 5 lignes
    @editable
    Leaderboard : []billboard_device = array{}

    # taille du texte des lignes du TOP 5 (petit pour que le temps reste sur la meme ligne)
    @editable
    LineTextSize : int = 16

    # taille du titre "TOP 5 - ..." (assez petit pour tenir sur une ligne, meme "Impossible")
    @editable
    TitleTextSize : int = 18

    # (Optionnel) zones intermediaires : temps de passage affiche au joueur
    @editable
    Checkpoints : []mutator_zone_device = array{}

    var Resetting : logic = false

    var StartTimes : [agent]float = map{}

    OnBegin<override>()<suspends> : void =
        # les points de retour sont dans le rayon des explosifs du reset : s'ils etaient
        # detruits, la teleportation suivante enverrait le joueur sous la map
        for (Point : ReturnPoint):
            set Point.CanBeDamaged = false
        StartTrigger.AgentEntersEvent.Subscribe(OnStart)
        FinishTrigger.AgentEntersEvent.Subscribe(OnFinish)
        for (I -> Zone : Checkpoints):
            Zone.AgentEntersEvent.Subscribe(split_handler{Course := Self, Index := I}.OnEnter)
        GetPlayspace().PlayerAddedEvent().Subscribe(OnPlayerChanged)
        GetPlayspace().PlayerRemovedEvent().Subscribe(OnPlayerChanged)
        for (I -> Board : Leaderboard):
            Board.SetTextSize(if (I = 0) then TitleTextSize else LineTextSize)
        RefreshLeaderboard()
        # les records sauvegardes des joueurs arrivent avec eux : on re-affiche un peu apres
        Sleep(3.0)
        RefreshLeaderboard()

    OnPlayerChanged(Player : player) : void =
        spawn{ DelayedRefresh() }

    DelayedRefresh()<suspends> : void =
        Sleep(1.0)
        RefreshLeaderboard()


    OnStart(Agent : agent) : void =
        if (set StartTimes[Agent] = GetSimulationElapsedTime()) {}

    OnSplit(Agent : agent, Index : int) : void =
        if (Start := StartTimes[Agent], Start >= 0.0):
            ResultHUD.SetText(SplitText(Index + 1, FormatSeconds(GetSimulationElapsedTime() - Start)))
            ResultHUD.Show(Agent)

    OnFinish(Agent : agent) : void =
        if:
            Start := StartTimes[Agent]
            Start >= 0.0
            set StartTimes[Agent] = -1.0
        then:
            Elapsed := GetSimulationElapsedTime() - Start
            var Best : float = Elapsed
            var NewRecord : logic = false
            if (Player := player[Agent]):
                if (Previous := GetSavedBest[Player, CourseLabel], Previous <= Elapsed):
                    set Best = Previous
                else:
                    SaveBest(Player, CourseLabel, Elapsed)
                    set NewRecord = true
            if (NewRecord?):
                ResultHUD.SetText(RecordText(DisplayName(), FormatSeconds(Elapsed)))
            else:
                ResultHUD.SetText(ChronoText(DisplayName(), FormatSeconds(Elapsed), FormatSeconds(Best)))
            ResultHUD.Show(Agent)
            RefreshLeaderboard()
            for (Point : ReturnPoint):
                if (TeleportAgentTo[Agent, Point]) {}
            if (ResetExplosives.Length > 0 or ResetSequences.Length > 0, not Resetting?):
                set Resetting = true
                spawn{ ResetBuilds(Agent) }

    # casse toutes les constructions puis recharge les pieces d'origine
    ResetBuilds(Agent : agent)<suspends> : void =
        Print("Reset des constructions ({CourseName})")
        for (Explosive : ResetExplosives):
            Explosive.Explode(Agent)
        Sleep(0.6)
        for (Sequence : ResetSequences):
            Sequence.Play()
        Sleep(3.0)
        for (Explosive : ResetExplosives):
            Explosive.Reset()
        set Resetting = false

    DisplayName() : string =
        if (CourseLabel > 0, N := PieceControlNames[CourseLabel - 1]) then N else CourseName

    # classe les joueurs presents selon leur record sauvegarde
    RefreshLeaderboard() : void =
        var Sorted : []tuple(player, float) = array{}
        for (Player : GetPlayspace().GetPlayers(), Player.IsActive[], Time := GetSavedBest[Player, CourseLabel]):
            set Sorted = InsertSorted(Sorted, Player, Time)
        for (I -> Board : Leaderboard):
            if (I = 0):
                Board.SetText(LeaderTitle(DisplayName()))
            else if (Entry := Sorted[I - 1]):
                Board.SetText(LeaderLine(I, Entry(0), FormatSeconds(Entry(1))))
            else:
                Board.SetText(EmptyLine(I))

    InsertSorted(List : []tuple(player, float), Player : player, Time : float) : []tuple(player, float) =
        var Out : []tuple(player, float) = array{}
        var Placed : logic = false
        for (Entry : List):
            if (not Placed?, Time < Entry(1)):
                set Out += array{(Player, Time)}
                set Placed = true
            set Out += array{Entry}
        if (not Placed?):
            set Out += array{(Player, Time)}
        Out

    # 12.345 -> "12.34"
    FormatSeconds(Seconds : float) : string =
        if:
            Centis := Round[Seconds * 100.0]
            Whole := Quotient[Centis, 100]
            Rest := Mod[Centis, 100]
        then:
            if (Rest < 10) then "{Whole}.0{Rest}" else "{Whole}.{Rest}"
        else:
            "?"
