# ============================================================================
#  BUILD AIR BOTS - zone BUILD : deux rampes + bots immobiles en l'air
#  Un bot apparait au centre d'une case de la grille de construction, au-dessus
#  des rampes (en stase, il ne tombe pas). Le joueur construit autour (full
#  piece) et le tue ; le suivant apparait ailleurs, UN ETAGE PLUS HAUT
#  (jusqu'a MaxLevel). Une balise (fleche) montre ou est le bot.
#  Bouton RESET : casse les constructions et redescend les bots au depart.
#  Les bots n'existent que si un joueur est dans la zone (limite de PNJ).
# ============================================================================

using { /Fortnite.com/Devices }
using { /Fortnite.com/Characters }
using { /Fortnite.com/Game }
using { /Fortnite.com/Playspaces }
using { /Verse.org/Simulation }
using { /Verse.org/Random }
using { /UnrealEngine.com/Temporary/SpatialMath }

LevelText<localizes>(Level : int) : message = "Bot level {Level}"

build_air_bots := class(creative_device):

    @editable
    Spawner : npc_spawner_device = npc_spawner_device{}

    @editable
    ResetButton : button_device = button_device{}

    @editable
    ResetExplosives : []explosive_device = array{}

    # fleche au-dessus du bot
    @editable
    Indicator : beacon_device = beacon_device{}

    # zone ou un joueur doit etre pour que les bots existent
    @editable
    ZoneMinX : float = 13500.0
    @editable
    ZoneMaxX : float = 26500.0
    @editable
    ZoneMinY : float = 21500.0
    @editable
    ZoneMaxY : float = 28500.0

    # grille de construction : centre de la zone (centre d'une case) et sol
    @editable
    GridX : float = 19968.0
    @editable
    GridY : float = 25088.0
    @editable
    FloorZ : float = 1920.0
    # nombre de cases autour du centre ou un bot peut apparaitre (X et Y)
    @editable
    SpreadX : int = 10
    @editable
    SpreadY : int = 5
    # distance minimale (en cases) entre deux bots de suite
    @editable
    MinCellsApart : int = 5
    # etage du premier bot, puis +1 a chaque bot tue, jusqu'a MaxLevel
    @editable
    StartLevel : int = 5
    @editable
    MaxLevel : int = 30

    @editable
    BotHealth : float = 200.0

    # hauteur du centre du personnage au-dessus de ses pieds
    @editable
    CharZ : float = 95.0

    var Resetting : logic = false
    var Level : int = 0
    var PrevCX : int = 100
    var PrevCY : int = 100

    OnBegin<override>()<suspends> : void =
        Spawner.DespawnAll(false)
        ResetButton.InteractedWithEvent.Subscribe(OnReset)
        Indicator.Disable()
        set Level = StartLevel
        Sleep(1.0)
        loop:
            WaitPlayerIn()
            # case au hasard, assez loin du bot precedent
            var CX : int = GetRandomInt(-SpreadX, SpreadX)
            var CY : int = GetRandomInt(-SpreadY, SpreadY)
            for (Try := 1..10, Abs(CX - PrevCX) + Abs(CY - PrevCY) < MinCellsApart):
                set CX = GetRandomInt(-SpreadX, SpreadX)
                set CY = GetRandomInt(-SpreadY, SpreadY)
            set PrevCX = CX
            set PrevCY = CY
            Pos := vector3:
                X := GridX + 512.0 * CX
                Y := GridY + 512.0 * CY
                Z := FloorZ + 384.0 * Level + 5.0
            Rot := MakeRotationFromYawPitchRollDegrees(90.0 * GetRandomInt(0, 3), 0.0, 0.0)
            MaybeChar := SpawnBot(Pos, Rot)
            if (Char := MaybeChar?):
                if (Indicator.TeleportTo[vector3{X := Pos.X, Y := Pos.Y, Z := Pos.Z + 400.0}, IdentityRotation()]) {}
                Indicator.Enable()
                Killed := race:
                    block:
                        R := Char.EliminatedEvent().Await()
                        AddBotKillByChar(R)
                        true
                    block:
                        WaitNoPlayerIn()
                        false
                    loop:
                        # le bot reste a sa place meme si on le pousse
                        Sleep(0.5)
                        if (Char.TeleportTo[vector3{X := Pos.X, Y := Pos.Y, Z := Pos.Z + CharZ}, Rot]) {}
                Indicator.Disable()
                if (Killed?):
                    set Level = if (Level < MaxLevel) then Level + 1 else MaxLevel
                else:
                    set Level = StartLevel
                Sleep(1.0)
                Spawner.DespawnAll(false)
            else:
                Sleep(2.0)
            Sleep(0.5)

    SpawnBot(Pos : vector3, Rot : rotation)<suspends> : ?fort_character =
        Spawner.Reset()
        Away := Spawner.GetTransform().Translation
        MaybeAgent := Spawner.SpawnAt(FromVector3(vector3{X := Away.X, Y := Away.Y, Z := Away.Z + 30.0}), ?Rotation := option{FromRotation(Rot)})
        if (Agent := MaybeAgent?, Char := Agent.GetFortCharacter[]):
            Char.SetMaxHealth(BotHealth)
            Char.SetHealth(BotHealth)
            Char.PutInStasis(stasis_args{AllowTurning := false, AllowFalling := false, AllowEmotes := false})
            if (Char.TeleportTo[vector3{X := Pos.X, Y := Pos.Y, Z := Pos.Z + CharZ}, Rot]) {}
            option{Char}
        else:
            false

    AnyPlayerIn()<transacts><decides> : void =
        Inside := for (Player : GetPlayspace().GetPlayers(), Char := Player.GetFortCharacter[], P := Char.GetTransform().Translation, P.X >= ZoneMinX, P.X <= ZoneMaxX, P.Y >= ZoneMinY, P.Y <= ZoneMaxY) { Player }
        Inside.Length > 0

    WaitPlayerIn()<suspends> : void =
        loop:
            if (AnyPlayerIn[]):
                break
            Sleep(0.5)

    WaitNoPlayerIn()<suspends> : void =
        loop:
            Sleep(0.5)
            if (not AnyPlayerIn[]):
                break

    OnReset(Agent : agent) : void =
        set Level = StartLevel
        if (not Resetting?):
            set Resetting = true
            spawn{ DoReset(Agent) }

    DoReset(Agent : agent)<suspends> : void =
        for (Explosive : ResetExplosives):
            Explosive.Explode(Agent)
        Sleep(1.5)
        for (Explosive : ResetExplosives):
            Explosive.Reset()
        set Resetting = false
