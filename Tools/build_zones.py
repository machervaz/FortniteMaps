# ============================================================================
#  build_zones.py - construit les 4 zones d'entrainement (UEFN, console Python)
#     C:/Users/marca/Documents/Fortnite Projects/testMoudon01/Tools/build_zones.py
#  Relancable : supprime d'abord tous les acteurs dont le label commence par ZONE_
#  Zones a 200 m du lobby :  Piece Control +X | Edit -Y | Aim +Y | 1v1 -X
# ============================================================================
import unreal, math, traceback

LOG_FILE = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\build_zones_log.txt"
ROOT = "/5622d7d7-d1ca-438f-8a48-1286a48e2471"
MAT_DIR = ROOT + "/Lobby/Materials"

FLOOR_Z = 1270.0       # meme niveau que le lobby
ZONE_DIST = 20000.0    # 200 m
ZONE_SIZE = 6000.0     # 60 x 60 m
LED = 10.0

CLS = {
    "mutator": "/CRD_VolumetricRegion/Device_MutatorVolume_V2.Device_MutatorVolume_V2_C",
    "billboard": "/Game/Creative/Devices/Billboard/BP_Creative_Billboard.BP_Creative_Billboard_C",
    "trigger": "/CreativeCoreDevices/Device_Trigger_V2.Device_Trigger_V2_C",
    "button": "/CreativeCoreDevices/Device_Button_V2.Device_Button_V2_C",
    "hud": "/CreativeCoreDevices/Device_HUDMessage_V2.Device_HUDMessage_V2_C",
    "granter": "/CreativeCoreDevices/Device_ItemGranter_V2.Device_ItemGranter_V2_C",
    "classdesigner": "/CreativeCoreDevices/Device_ClassDesigner_V2.Device_ClassDesigner_V2_C",
    "classselector": "/CreativeCoreDevices/Device_ClassSelector_V2.Device_ClassSelector_V2_C",
    "timer": "/CreativeCoreDevices/Device_Timer_V2.Device_Timer_V2_C",
    "score": "/CreativeCoreDevices/Device_ScoreManager_V2.Device_ScoreManager_V2_C",
    "dummy": "/CreativeCoreDevices/Device_TargetDummy_V2.Device_TargetDummy_V2_C",
    "dummytrack": "/CreativeCoreDevices/Device_TargetDummy_Track_V2.Device_TargetDummy_Track_V2_C",
    "pad": "/CRG_Props/SetupAssets/Blueprints/TechPrimitives/CP_L_T_Primitive_Planar_Cylinder_Solid.CP_L_T_Primitive_Planar_Cylinder_Solid_C",
    "wall": "/Game/Building/ActorBlueprints/Player/Wood/L1/PBWA_W1_Solid.PBWA_W1_Solid_C",
    "floor": "/Game/Building/ActorBlueprints/Player/Wood/L1/PBWA_W1_Floor.PBWA_W1_Floor_C",
    "stair": "/Game/Building/ActorBlueprints/Player/Wood/L1/PBWA_W1_StairW.PBWA_W1_StairW_C",
    "cone": "/Game/Building/ActorBlueprints/Player/Wood/L1/PBWA_W1_RoofC.PBWA_W1_RoofC_C",
    "manager": ROOT + "/_Verse.training_hub_manager",
    "chrono": ROOT + "/_Verse.chrono_course",
}

lines = []
def log(*a):
    s = " ".join(str(x) for x in a)
    lines.append(s)
    unreal.log("[build_zones] " + s)

eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
eal = unreal.EditorAssetLibrary
mel = unreal.MaterialEditingLibrary
tools = unreal.AssetToolsHelpers.get_asset_tools()
CUBE = eal.load_asset("/Engine/BasicShapes/Cube")
CYL = eal.load_asset("/Engine/BasicShapes/Cylinder")

def V(x, y, z):
    return unreal.Vector(float(x), float(y), float(z))

def mat(name):
    return eal.load_asset(MAT_DIR + "/" + name)

def white_holo():
    """Copie blanche du materiau hologramme (cylindres RETOUR LOBBY)."""
    name = "M_Lobby_HoloWhite"
    if eal.does_asset_exist(MAT_DIR + "/" + name):
        return eal.load_asset(MAT_DIR + "/" + name)
    # reprend les fonctions materiau de build_lobby.py (sans relancer la construction du lobby)
    src = open(__file__.replace("build_zones.py", "build_lobby.py"), encoding="utf-8").read()
    part = src[src.index("def new_material"):src.index("# couleurs en lineaire")]
    ns = {"unreal": unreal, "eal": eal, "mel": mel, "tools": tools, "MAT_DIR": MAT_DIR}
    exec(part, ns)
    return ns["hologram_mat"](name, unreal.LinearColor(1.0, 1.0, 1.0, 1))

_cls_cache = {}
def load_cls(key):
    if key not in _cls_cache:
        try:
            _cls_cache[key] = unreal.load_class(None, CLS[key])
        except Exception as e:
            _cls_cache[key] = None
            log("CLASSE INTROUVABLE", key, e)
    return _cls_cache[key]

def tag(a, label, folder):
    a.set_actor_label("ZONE_" + label)
    a.set_folder_path("Zones/" + folder)

def box(label, folder, mesh, material, center, size, collision=True, yaw=0.0):
    a = eas.spawn_actor_from_class(unreal.FortStaticMeshActor, center, unreal.Rotator(roll=0, pitch=0, yaw=yaw))
    c = a.get_component_by_class(unreal.StaticMeshComponent)
    c.set_static_mesh(mesh)
    c.set_material(0, material)
    a.set_actor_scale3d(V(size.x / 100.0, size.y / 100.0, size.z / 100.0))
    if not collision:
        c.set_collision_profile_name("NoCollision")
        c.set_editor_property("cast_shadow", False)
    tag(a, label, folder)
    return a

def dev(key, label, folder, loc, yaw=0.0):
    cls = load_cls(key)
    if not cls:
        return None
    try:
        a = eas.spawn_actor_from_class(cls, loc, unreal.Rotator(roll=0, pitch=0, yaw=yaw))
        if a:
            tag(a, label, folder)
        else:
            log("spawn None", key)
        return a
    except Exception as e:
        log("spawn fail", key, e)
        return None

def fit(actor, w, d, h, bottom_center):
    """Met un acteur a la taille w x d x h (cm), pose sur bottom_center."""
    o, e = actor.get_actor_bounds(False)
    if e.x < 1 or e.y < 1 or e.z < 1:
        return
    s = actor.get_actor_scale3d()
    actor.set_actor_scale3d(V(s.x * w / (2 * e.x), s.y * d / (2 * e.y), s.z * h / (2 * e.z)))
    o, e = actor.get_actor_bounds(False)
    loc = actor.get_actor_location()
    actor.set_actor_location(V(bottom_center.x + (loc.x - o.x), bottom_center.y + (loc.y - o.y),
                               bottom_center.z + (loc.z - (o.z - e.z))), False, False)

def try_set(actor, names, value):
    if not actor:
        return False
    for n in names:
        try:
            actor.set_editor_property(n, value)
            return True
        except Exception:
            pass
    log("  propriete non trouvee", names, "sur", actor.get_actor_label())
    return False

def billboard(label, folder, loc, yaw, text, size=40):
    bb = dev("billboard", label, folder, loc, yaw + 90.0)
    try_set(bb, ["text"], text)
    try_set(bb, ["TextSize"], size)
    return bb

# ---------------------------------------------------------------------------
#  Repere local d'une zone : +x = s'eloigne du lobby, +y = a gauche
# ---------------------------------------------------------------------------
class Frame:
    def __init__(self, dx, dy):
        self.dx, self.dy = dx, dy
        self.c = V(dx * ZONE_DIST, dy * ZONE_DIST, FLOOR_Z)
        self.yaw = math.degrees(math.atan2(dy, dx))
    def p(self, x, y, z=0.0):
        # x le long de (dx,dy), y le long de la perpendiculaire (-dy,dx)
        return V(self.c.x + x * self.dx - y * self.dy, self.c.y + x * self.dy + y * self.dx, self.c.z + z)
    def size(self, sx, sy, sz):
        # taille alignee monde (zones sur les axes)
        return V(abs(sx * self.dx) + abs(sy * self.dy), abs(sx * self.dy) + abs(sy * self.dx), sz)
    def face(self, x, y):
        """yaw pour regarder du point local (x,y) vers le centre de la zone."""
        p = self.p(x, y)
        return math.degrees(math.atan2(self.c.y - p.y, self.c.x - p.x))

# ---------------------------------------------------------------------------
#  Elements communs a chaque zone
# ---------------------------------------------------------------------------
RESULT = {}   # pour le cablage du manager

def common(key, title, fr, M):
    H = ZONE_SIZE / 2.0
    box(key + "_Floor", key, CUBE, M["gloss"], fr.p(0, 0, -25), V(ZONE_SIZE, ZONE_SIZE, 50))
    # bordure LED bleue
    for (sx, sy, nm) in [(1, 0, "A"), (-1, 0, "B"), (0, 1, "C"), (0, -1, "D")]:
        if sx:
            box(key + "_Led" + nm, key, CUBE, M["blue"], fr.p(sx * (H - LED), 0, 1), fr.size(2 * LED, ZONE_SIZE, 2), False)
        else:
            box(key + "_Led" + nm, key, CUBE, M["blue"], fr.p(0, sy * (H - LED), 1), fr.size(ZONE_SIZE, 2 * LED, 2), False)

    # pad d'arrivee (creative prop) cote lobby
    arrival_xy = (-H + 600, 0)
    pad = dev("pad", key + "_Arrival", key, fr.p(*arrival_xy))
    if pad:
        fit(pad, 200, 200, 10, fr.p(*arrival_xy))
    # nom de la zone face a l'arrivee
    billboard(key + "_Title", key, fr.p(-H + 1600, 0, 450), fr.yaw + 180.0, title, 60)

    # cylindre RETOUR LOBBY (blanc) a 9 m sur le cote du pad
    rx, ry = -H + 600, 900
    box(key + "_ReturnSocle", key, CYL, M["white"], fr.p(rx, ry, 3), V(390, 390, 6), False)
    box(key + "_ReturnHolo", key, CYL, M["holo_white"], fr.p(rx, ry, 220), V(300, 300, 400), False)
    rz = dev("mutator", key + "_ReturnZone", key, fr.p(rx, ry))
    if rz:
        fit(rz, 300, 300, 400, fr.p(rx, ry, 20))
    billboard(key + "_ReturnTitle", key, fr.p(rx, ry, 540), fr.face(rx, ry) - 0.0, "RETOUR LOBBY", 40)

    # devices de bienvenue et d'equipement (a regler dans Details)
    hud = dev("hud", key + "_Welcome", key + "/Devices", fr.p(-H + 300, -900))
    granter = dev("granter", key + "_Loadout", key + "/Devices", fr.p(-H + 300, -1200))

    RESULT[key] = {"title": title, "arrival": pad, "return_zone": rz, "hud": hud, "granter": granter, "frame": fr}

# ---------------------------------------------------------------------------
#  Zones
# ---------------------------------------------------------------------------
def chrono(key, name, fr, start_xy, finish_xy, folder):
    st = dev("trigger", key + "_ChronoStart", folder, fr.p(*start_xy))
    fi = dev("trigger", key + "_ChronoFinish", folder, fr.p(*finish_xy))
    hud = dev("hud", key + "_ChronoHUD", folder, fr.p(start_xy[0], start_xy[1] - 300))
    ch = dev("chrono", key + "_Chrono", folder, fr.p(start_xy[0], start_xy[1] - 600))
    RESULT.setdefault("chronos", []).append({"device": ch, "name": name, "start": st, "finish": fi, "hud": hud})
    return st, fi

def zone_piece_control(M):
    key = "PieceControl"
    fr = Frame(1, 0)
    common(key, "PIECE CONTROL", fr, M)
    # couloir chrono (bordure LED) le long de y = -1800
    y = -1800
    box(key + "_LaneL", key, CUBE, M["blue"], fr.p(0, y - 300, 1), fr.size(4000, 2 * LED, 2), False)
    box(key + "_LaneR", key, CUBE, M["blue"], fr.p(0, y + 300, 1), fr.size(4000, 2 * LED, 2), False)
    box(key + "_StartLine", key, CUBE, M["white"], fr.p(-2000, y, 1), fr.size(2 * LED, 600, 2), False)
    box(key + "_FinishLine", key, CUBE, M["white"], fr.p(2000, y, 1), fr.size(2 * LED, 600, 2), False)
    chrono(key, "Piece Control 1", fr, (-2000, y), (2000, y), key + "/Chrono")
    billboard(key + "_ChronoTitle", key, fr.p(-2300, y, 350), fr.yaw, "PARCOURS CHRONO", 40)
    # postes d'exercice (marquage au sol + panneau)
    for i, (txt, x) in enumerate([("90s x5", -1200), ("TUNNELS", 0), ("SIDE-JUMPS", 1200), ("RETAKES", 2200)]):
        box("%s_Spot%d" % (key, i), key, CYL, M["disc"], fr.p(x, 1200, 3), V(500, 500, 6), False)
        billboard("%s_SpotTitle%d" % (key, i), key, fr.p(x, 1200, 400), fr.face(x, 1200) + 180.0, txt, 40)

def zone_edit(M):
    key = "Edit"
    fr = Frame(0, -1)
    common(key, "EDIT", fr, M)
    T = 512.0   # une case de construction
    pieces = [("wall", "MURS"), ("floor", "SOLS"), ("stair", "ESCALIERS"), ("cone", "CONES")]
    for r, (pk, txt) in enumerate(pieces):
        x0 = -1500 + r * 1100
        billboard("%s_RowTitle%d" % (key, r), key, fr.p(x0, -2200, 400), fr.face(x0, -2200) + 180.0, txt, 40)
        for i in range(6):
            dev(pk, "%s_%s_%d" % (key, pk, i), key + "/Builds", fr.p(x0, -1500 + i * (T + 100)), fr.yaw + 90.0)
    # panneaux des edits a faire
    for i, txt in enumerate(["FENETRE", "PORTE", "DEMI-MUR", "TRIANGLE", "ARCHE"]):
        x = -1500 + i * 900
        billboard("%s_EditTitle%d" % (key, i), key, fr.p(x, 2600, 300), fr.face(x, 2600) + 180.0, txt, 40)
    # parcours chrono edit : une ligne de murs a editer pour passer
    y = 1500
    for i in range(6):
        dev("wall", "%s_ChronoWall%d" % (key, i), key + "/Chrono", fr.p(-1500 + i * 600, y), fr.yaw + 90.0)
    chrono(key, "Edit 1", fr, (-2100, y), (2300, y), key + "/Chrono")
    billboard(key + "_ChronoTitle", key, fr.p(-2300, y, 350), fr.yaw, "CHRONO EDIT", 40)
    btn = dev("button", key + "_ResetButton", key + "/Devices", fr.p(-2300, -2700))
    billboard(key + "_ResetTitle", key, fr.p(-2300, -2700, 250), fr.yaw + 180.0, "RESET", 30)

def zone_aim(M):
    key = "Aim"
    fr = Frame(0, 1)
    common(key, "AIM", fr, M)
    # pas de tir
    box(key + "_ShootLine", key, CUBE, M["white"], fr.p(-1800, 0, 1), fr.size(2 * LED, 3000, 2), False)
    # cibles fixes a 15 / 25 / 35 m
    k = 0
    for dist in (1500, 2500, 3500):
        for y in (-1000, 0, 1000):
            x = -1800 + dist
            if x > ZONE_SIZE / 2 - 200:
                x = ZONE_SIZE / 2 - 200
            dev("dummy", "%s_Target%d" % (key, k), key + "/Targets", fr.p(x, y), fr.yaw + 180.0)
            k += 1
    # cibles mobiles
    dev("dummytrack", key + "_TargetTrack1", key + "/Targets", fr.p(800, -1800), fr.yaw + 180.0)
    dev("dummytrack", key + "_TargetTrack2", key + "/Targets", fr.p(1800, 1800), fr.yaw + 180.0)
    dev("timer", key + "_Timer60s", key + "/Devices", fr.p(-2200, -1800))
    dev("score", key + "_ScoreManager", key + "/Devices", fr.p(-2200, -2100))
    billboard(key + "_Challenge", key, fr.p(-2300, -1900, 300), fr.yaw, "DEFI 60 s", 40)

def zone_1v1(M):
    key = "1v1"
    fr = Frame(-1, 0)
    common(key, "1V1 BUILDFIGHT", fr, M)
    H = ZONE_SIZE / 2.0
    WH = 1500.0
    # murs de l'arene (noir + LED)
    for (sx, sy, nm) in [(1, 0, "A"), (-1, 0, "B"), (0, 1, "C"), (0, -1, "D")]:
        if sx:
            box(key + "_Wall" + nm, key + "/Arena", CUBE, M["black"], fr.p(sx * (H + 25), 0, WH / 2), fr.size(50, ZONE_SIZE + 100, WH))
            box(key + "_WallLed" + nm, key + "/Arena", CUBE, M["blue"], fr.p(sx * (H - 5), 0, WH - 20), fr.size(10, ZONE_SIZE, 20), False)
        else:
            box(key + "_Wall" + nm, key + "/Arena", CUBE, M["black"], fr.p(0, sy * (H + 25), WH / 2), fr.size(ZONE_SIZE + 100, 50, WH))
            box(key + "_WallLed" + nm, key + "/Arena", CUBE, M["blue"], fr.p(0, sy * (H - 5), WH - 20), fr.size(ZONE_SIZE, 10, 20), False)
    # ligne centrale
    box(key + "_MidLine", key, CUBE, M["white"], fr.p(0, 0, 1), fr.size(2 * LED, ZONE_SIZE, 2), False)
    # vitesse : 4 boutons + class selectors + class designers
    speeds = [("100 %", 1.0), ("75 %", 0.75), ("50 %", 0.5), ("25 %", 0.25)]
    RESULT["speed"] = []
    for i, (txt, mult) in enumerate(speeds):
        y = -1650 + i * 300
        x = -H + 250
        b = dev("button", "%s_Speed%d_Button" % (key, i), key + "/Speed", fr.p(x, y - 2000 + 3300), fr.yaw)
        billboard("%s_Speed%d_Title" % (key, i), key + "/Speed", fr.p(x, y - 2000 + 3300, 260), fr.yaw + 180.0, txt, 30)
        cd = dev("classdesigner", "%s_Speed%d_ClassDesigner" % (key, i), key + "/Speed/Devices", fr.p(-H + 100, -2800 + i * 200))
        cs = dev("classselector", "%s_Speed%d_ClassSelector" % (key, i), key + "/Speed/Devices", fr.p(-H + 300, -2800 + i * 200))
        RESULT["speed"].append({"button": b, "selector": cs, "designer": cd, "mult": mult, "slot": i + 1})

# ---------------------------------------------------------------------------
#  Manager Verse
# ---------------------------------------------------------------------------
def lobby_actor(label):
    for a in eas.get_all_level_actors():
        if a.get_actor_label() == label:
            return a
    return None

def place_manager():
    # LobbyPoint doit etre un creative prop : petit pad au centre du lobby
    lp = dev("pad", "LobbyPointProp", "Lobby", V(0, 0, FLOOR_Z))
    if lp:
        fit(lp, 150, 150, 6, V(0, 0, FLOOR_Z))
    RESULT["lobby_point"] = lp
    m = dev("manager", "TrainingHubManager", "Manager", V(0, 0, FLOOR_Z - 400))
    RESULT["manager"] = m
    log("manager", m)

# ---------------------------------------------------------------------------
try:
    n = 0
    for a in eas.get_all_level_actors():
        try:
            if a.get_actor_label().startswith("ZONE_"):
                eas.destroy_actor(a); n += 1
        except Exception:
            pass
    log("acteurs ZONE_ supprimes", n)

    M = {
        "black": mat("M_Lobby_BlackMatte"), "gloss": mat("M_Lobby_BlackGloss"),
        "blue": mat("M_Lobby_LedBlue"), "white": mat("M_Lobby_LedWhite"),
        "disc": mat("M_Lobby_DiscBlue"), "holo": mat("M_Lobby_Hologram"),
        "holo_white": white_holo(),
    }
    for f in (zone_piece_control, zone_edit, zone_aim, zone_1v1):
        try:
            f(M); log(f.__name__, "ok")
        except Exception:
            log(f.__name__, "ERREUR", traceback.format_exc())
    place_manager()

    # memoriser les labels pour le cablage
    import json
    out = {}
    for k, v in RESULT.items():
        if isinstance(v, dict) and "frame" in v:
            out[k] = {kk: (vv.get_actor_label() if hasattr(vv, "get_actor_label") else vv)
                      for kk, vv in v.items() if kk != "frame"}
    out["chronos"] = [{kk: (vv.get_actor_label() if hasattr(vv, "get_actor_label") else vv) for kk, vv in c.items()}
                      for c in RESULT.get("chronos", [])]
    out["speed"] = [{kk: (vv.get_actor_label() if hasattr(vv, "get_actor_label") else vv) for kk, vv in c.items()}
                    for c in RESULT.get("speed", [])]
    out["lobby_point"] = RESULT["lobby_point"].get_actor_label() if RESULT.get("lobby_point") else None
    out["manager"] = RESULT["manager"].get_actor_label() if RESULT.get("manager") else None
    open(LOG_FILE.replace("_log.txt", "_map.json"), "w", encoding="utf-8").write(json.dumps(out, indent=1))

    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    cnt = sum(1 for a in eas.get_all_level_actors() if a.get_actor_label().startswith("ZONE_"))
    log("TERMINE - acteurs ZONE_ :", cnt)
except Exception:
    log("ERREUR", traceback.format_exc())

open(LOG_FILE, "w", encoding="utf-8").write("\n".join(lines))
