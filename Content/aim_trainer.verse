# ============================================================================
#  AIM TRAINER - zone Aim : 3 failles -> 3 exercices de tir sur de VRAIS bots
#  Les bots sont des PNJ (NPC Spawner + definition NPC_TrainingBot, comportement
#  vide) avec de vrais PV. Ils sont mis en stase (pas de gravite) et deplaces
#  par Verse (TeleportTo a chaque image) :
#   1. LANCER  (200 PV) : propulse par un matelas dans la direction de ses
#                fleches ; s'il touche le sol il meurt ; mort -> un autre part
#                d'un autre matelas.
#   2. REBOND  (200 PV) : rebondit sur le meme matelas ; uniquement quand il
#                est tue il reapparait sur un autre.
#   3. CIRCUIT (1000 PV) : rebondit sans arret de pad en pad, en zigzag ; au bout du
#                circuit il meurt ; mort -> un autre repart du debut.
#  Failles : Rifts[i] (mutator zone) teleporte vers RiftTargets[i].
# ============================================================================

using { /Fortnite.com/Devices }
using { /Fortnite.com/Characters }
using { /Fortnite.com/Game }
using { /Fortnite.com/Playspaces }
using { /Verse.org/Simulation }
using { /Verse.org/Random }
using { /UnrealEngine.com/Temporary/SpatialMath }
using { /Verse.org/Input }
using { /Fortnite.com/Input/Character }

ExScoreText<localizes>(Name : string, Kills : int, Total : int, Acc : int) : message =
    "{Name}  -  {Kills} / {Total} bots killed  ({Acc}%)"

aim_trainer := class(creative_device):

    # ---- score des exercices (affiche aux joueurs de l'arene) ----
    @editable
    ScoreHUD : hud_message_device = hud_message_device{}

    ExNames : []string = array{"LAUNCH", "BOUNCE", "CIRCUIT"}
    var ExKills : []int = array{0, 0, 0}
    var ExTotal : []int = array{0, 0, 0}

    # ---- Failles (hub -> exercices, et retours) ----
    @editable
    Rifts : []mutator_zone_device = array{}

    @editable
    RiftTargets : []creative_prop = array{}

    # ---- 1. Lancer ----
    @editable
    LaunchSpawner : npc_spawner_device = npc_spawner_device{}

    @editable
    LaunchPads : []creative_prop = array{}

    # ---- 2. Rebond ----
    @editable
    BounceSpawner : npc_spawner_device = npc_spawner_device{}

    @editable
    BouncePads : []creative_prop = array{}

    # ---- 3. Circuit ----
    @editable
    CircuitSpawner : npc_spawner_device = npc_spawner_device{}

    # points du circuit, dans l'ordre
    @editable
    CircuitPath : []creative_prop = array{}

    # ---- 4. Double pump ----
    # zone qui couvre la salle : entree = donne les 2 pompes, emote = retour lobby
    @editable
    PumpRoom : mutator_zone_device = mutator_zone_device{}

    # bots "sentinelle" (Sentry device), un par coin ; Verse les fait apparaitre un a un
    @editable
    PumpSentries : []sentry_device = array{}

    # bouton "NO DELAY" : donne la classe sans delai de changement d'arme (Class Designer 9) ;
    # en quittant la salle, le joueur repasse sur la classe normale
    @editable
    PumpButton : button_device = button_device{}

    @editable
    PumpClassOn : class_and_team_selector_device = class_and_team_selector_device{}

    @editable
    PumpClassOff : class_and_team_selector_device = class_and_team_selector_device{}

    var PumpBoosted : []agent = array{}

    # donneur d'objets : 2 pompes (vide l'inventaire avant)
    @editable
    PumpLoadout : item_granter_device = item_granter_device{}

    # point d'arrivee du lobby (retour par emote)
    @editable
    LobbyPoint : creative_prop = creative_prop{}

    @editable
    PumpHealth : float = 100.0

    # distance d'apparition des mannequins autour du joueur
    @editable
    PumpMinDistance : float = 140.0

    @editable
    PumpMaxDistance : float = 220.0

    # interieur de la salle (les mannequins restent dedans)
    @editable
    PumpAreaMinX : float = -190.0

    @editable
    PumpAreaMaxX : float = 190.0

    @editable
    PumpAreaMinY : float = 59810.0

    @editable
    PumpAreaMaxY : float = 60190.0

    @editable
    PumpFloorZ : float = 1270.0

    var PumpPlayers : []agent = array{}

    # ---- Reglages ----
    @editable
    LaunchHealth : float = 200.0

    @editable
    BounceHealth : float = 200.0

    @editable
    CircuitHealth : float = 1000.0

    @editable
    LaunchApex : float = 2200.0

    @editable
    LaunchMinDistance : float = 5500.0

    @editable
    LaunchMaxDistance : float = 7500.0

    @editable
    LaunchTime : float = 4.2

    # zone ou le bot peut atterrir (interieur de l'arene LANCER) : un vol trop long est raccourci
    @editable
    LaunchAreaMinX : float = -4500.0

    @editable
    LaunchAreaMaxX : float = 4500.0

    @editable
    LaunchAreaMinY : float = 30600.0

    @editable
    LaunchAreaMaxY : float = 38500.0

    @editable
    BounceHeight : float = 3000.0

    @editable
    BounceTime : float = 1.3

    @editable
    CircuitSpeed : float = 750.0

    # hauteur des rebonds du bot du circuit (de pad en pad)
    @editable
    CircuitHop : float = 180.0

    # hauteur du centre du personnage au-dessus de ses pieds
    @editable
    CharZ : float = 95.0

    OnBegin<override>()<suspends> : void =
        for (I -> Zone : Rifts):
            Zone.AgentEntersEvent.Subscribe(rift_handler{Trainer := Self, Index := I}.OnEnter)
        for (Pad : LaunchPads):
            set Pad.CanBeDamaged = false
        for (Pad : BouncePads):
            set Pad.CanBeDamaged = false
        for (Point : CircuitPath):
            set Point.CanBeDamaged = false
        LaunchSpawner.DespawnAll(false)
        BounceSpawner.DespawnAll(false)
        CircuitSpawner.DespawnAll(false)
        set LobbyPoint.CanBeDamaged = false
        for (Sentry : PumpSentries):
            Sentry.DestroySentry()
        PumpRoom.AgentBeginsEmotingEvent.Subscribe(OnPumpEmote)
        PumpButton.InteractedWithEvent.Subscribe(OnPumpButton)
        Sleep(1.0)
        spawn{ RunLaunch() }
        spawn{ RunBounce() }
        spawn{ RunCircuit() }
        spawn{ RunPump() }

    # ---------------- 4. double pump ----------------
    # le joueur est-il dans la salle ? (par sa position : etre teleporte directement
    # dans la zone ne declenche pas toujours l'evenement d'entree)
    InPumpRoom(Agent : agent)<transacts><decides> : void =
        Char := Agent.GetFortCharacter[]
        P := Char.GetTransform().Translation
        P.X >= PumpAreaMinX - 150.0
        P.X <= PumpAreaMaxX + 150.0
        P.Y >= PumpAreaMinY - 150.0
        P.Y <= PumpAreaMaxY + 150.0
        P.Z >= PumpFloorZ - 200.0
        P.Z <= PumpFloorZ + 1200.0

    # met a jour la liste des joueurs presents ; ceux qui arrivent recoivent les 2 pompes
    UpdatePumpPlayers() : void =
        var Inside : []agent = array{}
        for (Player : GetPlayspace().GetPlayers(), InPumpRoom[Player]):
            set Inside += array{Player}
            if (not PumpPlayers.Find[Player]):
                Print("Double pump : joueur dans la salle")
                PumpLoadout.GrantItem(Player)
        # ceux qui sont sortis : on enleve le reglage "sans delai"
        for (Gone : PumpBoosted, not Inside.Find[Gone]):
            PumpClassOff.ChangeClass(Gone)
            Print("Double pump : reglage sans delai desactive")
        set PumpBoosted = for (Kept : PumpBoosted, Inside.Find[Kept]) { Kept }
        set PumpPlayers = Inside

    # bouton dans la salle -> classe sans delai de changement d'arme
    OnPumpButton(Agent : agent) : void =
        if (InPumpRoom[Agent]):
            PumpClassOn.ChangeClass(Agent)
            if (not PumpBoosted.Find[Agent]):
                set PumpBoosted += array{Agent}
            Print("Double pump : reglage sans delai active")
            if (Player := player[Agent]):
                WatchPumpFire(Player)

    # ---- double pompe auto : apres chaque tir (mode NO DELAY), une pompe neuve est
    # redonnee et equipee -> plus de temps de pompage, chargeur toujours plein ----
    var PumpFireWatched : []player = array{}

    WatchPumpFire(Player : player) : void =
        if (not PumpFireWatched.Find[Player], Input := GetPlayerInput[Player]):
            set PumpFireWatched += array{Player}
            Input.AddInputMapping(RangedWeaponMapping)
            Input.GetInputEvents(WeaponPrimary).BeginDetectEvent.Subscribe(OnPumpFire)

    OnPumpFire(Data : tuple(player, logic)) : void =
        Player := Data(0)
        if (PumpBoosted.Find[Player], InPumpRoom[Player]):
            spawn{ RefreshPump(Player) }

    RefreshPump(Player : player)<suspends> : void =
        Sleep(PumpRefreshDelay)
        if (InPumpRoom[Player]):
            PumpLoadout.GrantItem(Player)

    # delai entre le tir et la pompe neuve (laisse partir le coup)
    @editable
    PumpRefreshDelay : float = 0.08

    # emote dans la salle -> retour au lobby
    OnPumpEmote(Agent : agent) : void =
        Print("Double pump : emote vue")
        if (player[Agent]):
            if (TeleportAgentTo[Agent, LobbyPoint]) {}

    # la zone ne "voit" pas un joueur teleporte dedans : on l'eloigne puis on la remet
    # en place sur lui -> elle le detecte comme s'il etait entre a pied
    RefreshPumpRoom()<suspends> : void =
        Home := PumpRoom.GetTransform()
        Away := Home.Translation + vector3{X := 0.0, Y := 0.0, Z := 5000.0}
        if (PumpRoom.TeleportTo[Away, Home.Rotation]):
            Sleep(0.25)
            if (PumpRoom.TeleportTo[Home.Translation, Home.Rotation]):
                Print("Double pump : zone de la salle relancee")
            else:
                Print("Double pump : zone non remise en place")
        else:
            Print("Double pump : la zone ne peut pas bouger")

    # une seule sentinelle a la fois, dans un des 4 coins (jamais 2 fois le meme de
    # suite), pacifique (ne tire pas) ; eliminee -> une autre apparait dans un autre coin
    RunPump()<suspends> : void =
        var PrevCorner : int = -1
        loop:
            UpdatePumpPlayers()
            if (PumpPlayers.Length > 0):
                set PrevCorner = PickOther(PumpSentries.Length, PrevCorner)
                if (Sentry := PumpSentries[PrevCorner]):
                    Sentry.Enable()
                    Sentry.Spawn()
                    Sentry.Pacify()
                    Killed := race:
                        block:
                            SentryKiller := Sentry.EliminatedEvent.Await()
                            if (KA := SentryKiller?, KP := player[KA]):
                                AddBotKill(KP)
                            true
                        block:
                            WaitPumpEmpty()
                            false
                    if (not Killed?):
                        Sentry.DestroySentry()
                    Sleep(0.4)
                else:
                    Sleep(0.5)
            else:
                Sleep(0.5)

    # attend que plus aucun joueur ne soit dans la salle
    WaitPumpEmpty()<suspends> : void =
        loop:
            Sleep(0.5)
            UpdatePumpPlayers()
            if (PumpPlayers.Length = 0):
                break

    # ---- les bots d'un exercice n'existent que si un joueur est dans son arene ----
    # (Fortnite limite le nombre de PNJ en meme temps : sans ca, 3 bots tournent en
    # permanence et le 4e exercice ne peut plus en faire apparaitre)
    AnyPlayerIn(MinX : float, MaxX : float, MinY : float, MaxY : float)<transacts><decides> : void =
        Inside := for (Player : GetPlayspace().GetPlayers(), Char := Player.GetFortCharacter[], P := Char.GetTransform().Translation, P.X >= MinX, P.X <= MaxX, P.Y >= MinY, P.Y <= MaxY) { Player }
        Inside.Length > 0

    WaitPlayerIn(MinX : float, MaxX : float, MinY : float, MaxY : float)<suspends> : void =
        loop:
            if (AnyPlayerIn[MinX, MaxX, MinY, MaxY]):
                break
            Sleep(0.5)

    WaitNoPlayerIn(MinX : float, MaxX : float, MinY : float, MaxY : float)<suspends> : void =
        loop:
            Sleep(0.5)
            if (not AnyPlayerIn[MinX, MaxX, MinY, MaxY]):
                break

    # ---- score des exercices : bots tues / bots apparus (0 lancer, 1 rebond, 2 circuit) ----
    # Les compteurs repartent a zero quand l'arene se vide.
    RecordBot(Ex : int, Result : elimination_result, MinX : float, MaxX : float, MinY : float, MaxY : float) : void =
        Victim := Result.EliminatedCharacter
        Killed := if (Killer := Result.EliminatingCharacter?, Killer <> Victim) then true else false
        AddBotKillByChar(Result)
        if (K := ExKills[Ex], T := ExTotal[Ex]):
            if (set ExTotal[Ex] = T + 1) {}
            if (Killed?, set ExKills[Ex] = K + 1) {}
        if (K := ExKills[Ex], T := ExTotal[Ex], Name := ExNames[Ex]):
            Acc := if (T > 0, A := Floor[K * 100.0 / (T * 1.0)]) then A else 0
            ScoreHUD.SetText(ExScoreText(Name, K, T, Acc))
            for (Player : GetPlayspace().GetPlayers(), Char := Player.GetFortCharacter[], P := Char.GetTransform().Translation, P.X >= MinX, P.X <= MaxX, P.Y >= MinY, P.Y <= MaxY):
                ScoreHUD.Show(Player)

    ResetScoreIfEmpty(Ex : int, MinX : float, MaxX : float, MinY : float, MaxY : float) : void =
        if (not AnyPlayerIn[MinX, MaxX, MinY, MaxY]):
            if (set ExKills[Ex] = 0, set ExTotal[Ex] = 0) {}

    UseRift(Agent : agent, Index : int) : void =
        # joueurs seulement (les bots PNJ ne doivent pas etre teleportes)
        if (player[Agent], Target := RiftTargets[Index], TeleportAgentTo[Agent, Target]) {}

    # indice au hasard different du precedent
    PickOther(Count : int, Previous : int) : int =
        if (Count <= 1):
            0
        else:
            I := GetRandomInt(0, Count - 2)
            if (I >= Previous) then I + 1 else I

    # fait apparaitre un bot sur Pos ; PV, stase (ni gravite ni deplacement IA)
    SpawnBot(Spawner : npc_spawner_device, Pos : vector3, Rot : rotation, Health : float)<suspends> : ?fort_character =
        Spawner.Reset()
        MaybeAgent := Spawner.SpawnAt(FromVector3(Pos), ?Rotation := option{FromRotation(Rot)})
        if (Agent := MaybeAgent?, Char := Agent.GetFortCharacter[]):
            Char.SetMaxHealth(Health)
            Char.SetHealth(Health)
            Char.PutInStasis(stasis_args{AllowTurning := false, AllowFalling := false, AllowEmotes := false})
            MoveChar(Char, Pos, Rot)
            option{Char}
        else:
            false

    # comme SpawnBot, mais le bot apparait sur le spawner (loin des joueurs : le spawner
    # refuse d'apparaitre tout pres d'un joueur) puis est teleporte sur Pos
    SpawnBotAway(Spawner : npc_spawner_device, Pos : vector3, Rot : rotation, Health : float)<suspends> : ?fort_character =
        Spawner.Reset()
        Away := Spawner.GetTransform().Translation
        MaybeAgent := Spawner.SpawnAt(FromVector3(vector3{X := Away.X, Y := Away.Y, Z := Away.Z + 30.0}), ?Rotation := option{FromRotation(Rot)})
        if (not MaybeAgent?):
            Print("Double pump : SpawnAt a refuse (limite de PNJ ?)")
        if (Agent := MaybeAgent?, Char := Agent.GetFortCharacter[]):
            Char.SetMaxHealth(Health)
            Char.SetHealth(Health)
            Char.PutInStasis(stasis_args{AllowTurning := false, AllowFalling := false, AllowEmotes := false})
            MoveChar(Char, Pos, Rot)
            option{Char}
        else:
            false

    MoveChar(Char : fort_character, P : vector3, Rot : rotation) : void =
        if (Char.TeleportTo[vector3{X := P.X, Y := P.Y, Z := P.Z + CharZ}, Rot]) {}

    # deplacement en cloche de From a To (sommet a ApexZ), mis a jour a chaque image
    ArcChar(Char : fort_character, From : vector3, To : vector3, ApexZ : float, Duration : float, Rot : rotation)<suspends> : void =
        H := ApexZ - (From.Z + To.Z) / 2.0
        T0 := GetSimulationElapsedTime()
        loop:
            T := (GetSimulationElapsedTime() - T0) / Max(0.05, Duration)
            if (T >= 1.0):
                MoveChar(Char, To, Rot)
                break
            P := vector3{X := From.X + (To.X - From.X) * T, Y := From.Y + (To.Y - From.Y) * T, Z := From.Z + (To.Z - From.Z) * T + 4.0 * H * T * (1.0 - T)}
            MoveChar(Char, P, Rot)
            Sleep(0.0)

    # ---------------- 1. lancer ----------------
    # distance max dans la direction (Dx, Dy) avant de sortir de la zone d'atterrissage
    MaxFlight(Start : vector3, Dx : float, Dy : float) : float =
        var Best : float = 100000.0
        if (Dx > 0.001):
            set Best = Min(Best, (LaunchAreaMaxX - Start.X) / Dx)
        else if (Dx < -0.001):
            set Best = Min(Best, (LaunchAreaMinX - Start.X) / Dx)
        if (Dy > 0.001):
            set Best = Min(Best, (LaunchAreaMaxY - Start.Y) / Dy)
        else if (Dy < -0.001):
            set Best = Min(Best, (LaunchAreaMinY - Start.Y) / Dy)
        Max(0.0, Best)

    RunLaunch()<suspends> : void =
        var PrevPad : int = -1
        loop:
            WaitPlayerIn(-5000.0, 5000.0, 29000.0, 39000.0)
            set PrevPad = PickOther(LaunchPads.Length, PrevPad)
            if (Pad := LaunchPads[PrevPad]):
                Start := Pad.GetTransform().Translation
                Rot := Pad.GetTransform().Rotation
                # le matelas pousse dans SA direction (fleches), devie de +/- 12 degres
                Fwd := Rot.GetLocalForward()
                A := GetRandomFloat(-12.0, 12.0) * PiFloat / 180.0
                Dx := Fwd.X * Cos(A) - Fwd.Y * Sin(A)
                Dy := Fwd.X * Sin(A) + Fwd.Y * Cos(A)
                Dist := Min(GetRandomFloat(LaunchMinDistance, LaunchMaxDistance), MaxFlight(Start, Dx, Dy))
                Land := vector3{X := Start.X + Dx * Dist, Y := Start.Y + Dy * Dist, Z := Start.Z}
                MaybeChar := SpawnBot(LaunchSpawner, Start, Rot, LaunchHealth)
                if (Char := MaybeChar?):
                    race:
                        block:
                            R := Char.EliminatedEvent().Await()
                            RecordBot(0, R, -5000.0, 5000.0, 29000.0, 39000.0)
                        WaitNoPlayerIn(-5000.0, 5000.0, 29000.0, 39000.0)
                        block:
                            # vol raccourci par le mur -> un peu plus court en temps aussi
                            Duration := Max(2.6, LaunchTime * Dist / ((LaunchMinDistance + LaunchMaxDistance) / 2.0))
                            ArcChar(Char, Start, Land, Start.Z + LaunchApex, Duration, Rot)
                            Char.Damage(100000.0)     # touche le sol -> meurt
                            Sleep(3.0)
                    LaunchSpawner.DespawnAll(false)
                    ResetScoreIfEmpty(0, -5000.0, 5000.0, 29000.0, 39000.0)
                else:
                    Sleep(1.0)
            Sleep(0.6)

    # ---------------- 2. rebond ----------------
    RunBounce()<suspends> : void =
        var PrevPad : int = -1
        loop:
            WaitPlayerIn(-4000.0, 4000.0, 40000.0, 48000.0)
            set PrevPad = PickOther(BouncePads.Length, PrevPad)
            if (Pad := BouncePads[PrevPad]):
                Base := Pad.GetTransform().Translation
                Rot := Pad.GetTransform().Rotation
                MaybeChar := SpawnBot(BounceSpawner, Base, Rot, BounceHealth)
                if (Char := MaybeChar?):
                    race:
                        block:
                            R := Char.EliminatedEvent().Await()
                            RecordBot(1, R, -4000.0, 4000.0, 40000.0, 48000.0)
                        WaitNoPlayerIn(-4000.0, 4000.0, 40000.0, 48000.0)
                        loop:
                            ArcChar(Char, Base, Base, Base.Z + BounceHeight, 2.0 * BounceTime, Rot)
                    BounceSpawner.DespawnAll(false)
                    ResetScoreIfEmpty(1, -4000.0, 4000.0, 40000.0, 48000.0)
                else:
                    Sleep(1.0)
            Sleep(0.6)

    # ---------------- 3. circuit ----------------
    RunCircuit()<suspends> : void =
        loop:
            WaitPlayerIn(-3500.0, 3500.0, 48500.0, 55500.0)
            if (First := CircuitPath[0]):
                Start := First.GetTransform().Translation
                MaybeChar := SpawnBot(CircuitSpawner, Start, First.GetTransform().Rotation, CircuitHealth)
                if (Char := MaybeChar?):
                    race:
                        block:
                            R := Char.EliminatedEvent().Await()
                            RecordBot(2, R, -3500.0, 3500.0, 48500.0, 55500.0)
                        WaitNoPlayerIn(-3500.0, 3500.0, 48500.0, 55500.0)
                        block:
                            WalkPath(Char, Start)
                            Char.Damage(100000.0)     # bout du circuit -> meurt
                            Sleep(3.0)
                    CircuitSpawner.DespawnAll(false)
                    ResetScoreIfEmpty(2, -3500.0, 3500.0, 48500.0, 55500.0)
                else:
                    Sleep(1.0)
            Sleep(0.6)

    WalkPath(Char : fort_character, Start : vector3)<suspends> : void =
        var From : vector3 = Start
        for (I := 1..CircuitPath.Length - 1, Point := CircuitPath[I]):
            To := Point.GetTransform().Translation
            Rot := Point.GetTransform().Rotation
            Dz := To.Z - From.Z
            if (Dz > 100.0):
                # pad d'impulsion : grand saut vers l'etagere du dessus
                ArcChar(Char, From, To, To.Z + 170.0, 0.8, Rot)
            else:
                # rebond de pad en pad le long de l'etagere
                ArcChar(Char, From, To, Max(From.Z, To.Z) + CircuitHop, Max(0.35, Distance(From, To) / CircuitSpeed), Rot)
            set From = To

rift_handler := class:
    Trainer : aim_trainer
    Index : int
    OnEnter(Agent : agent) : void =
        Trainer.UseRift(Agent, Index)
