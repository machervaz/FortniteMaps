# ============================================================================
#  build_tunnels.py - 4 longs tunnels d'edit (montees, descentes, trous)
#     C:/Users/marca/Documents/Fortnite Projects/testMoudon01/Tools/build_tunnels.py
#  FACILE 16 cases | MOYEN 24 | DIFFICILE 32 | IMPOSSIBLE 44  (1 case = 5,12 m)
#  Relancable : supprime les acteurs TUN_ (sauf les devices chrono / reset,
#  que wire_tunnels.py rebranche ensuite).
#
#  Une case = jetons :
#    W  mur editable a l'entree de la case
#    S  escalier editable qui bouche la case (le plafond empeche de passer)
#    C  cone editable dans la case
#    U  MONTEE : rampe praticable, la case suivante est un etage plus haut
#    D  TROU   : le sol de la case est un sol editable, on tombe d'un etage
#                et on continue en dessous
#  Murs, plafonds et sols noirs : indestructibles.
# ============================================================================
import unreal, json, traceback

TOOLS = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools"
LOG_FILE = TOOLS + r"\build_tunnels_log.txt"
ROOT = "/5622d7d7-d1ca-438f-8a48-1286a48e2471"
MAT_DIR = ROOT + "/Lobby/Materials"

FLOOR_Z = 1152.0       # v3 : sol des tunnels sur un etage de la grille de construction (384 x 3)
ZONE_FLOOR = 1270.0   # sol de la zone Edit (ou est le pad de retour)
CELL = 512.0          # case de construction
LH = 384.0            # hauteur d'un etage
Y0 = -23296.0         # v3 : entree des tunnels sur un bord de case de la grille (256 + 512k)
EXT_LEN = 24400.0     # longueur de la plateforme des tunnels
HALF = CELL / 2

def rep(block, n):
    return block * n

TUNNELS = [   # v2 : un peu plus difficile (plus de S / C / U / D, tunnels plus longs)
    ("FACILE", -1536.0, (0.0, 1.0, 0.25),
     ["W", "", "U", "W", "", "C", "W", "D", "", "W", "U", "S", "W", "", "WD", "W", "C", "W", "", ""]),
    ("MOYEN", -512.0, (1.0, 0.75, 0.0),
     ["W", "W", "U", "WC", "WU", "W", "S", "WD", "W", "C", "WU", "W", "S", "WC", "WD", "W", "WD",
      "W", "C", "WS", "WU", "W", "WD", "C", "W", "S", "W", ""]),
    ("DIFFICILE", 512.0, (1.0, 0.25, 0.0),
     rep(["WS", "WU", "WC", "WS", "WD", "WC", "WU", "WS", "WD"], 4)),
    ("IMPOSSIBLE", 1536.0, (1.0, 0.0, 0.02),
     rep(["WS", "WU", "WC", "WU", "WS", "WD", "WC", "WD", "WC", "WU", "WD"], 4)),
]
TITLE_EN = {"FACILE": "EASY", "MOYEN": "MEDIUM", "DIFFICILE": "HARD", "IMPOSSIBLE": "IMPOSSIBLE"}

CLS = {
    "billboard": "/Game/Creative/Devices/Billboard/BP_Creative_Billboard.BP_Creative_Billboard_C",
    "trigger": "/CreativeCoreDevices/Device_Trigger_V2.Device_Trigger_V2_C",
    "hud": "/CreativeCoreDevices/Device_HUDMessage_V2.Device_HUDMessage_V2_C",
    "button": "/CreativeCoreDevices/Device_Button_V2.Device_Button_V2_C",
    "round": "/CreativeCoreDevices/Device_RoundSettings_V2.Device_RoundSettings_V2_C",
    "pad": "/CRG_Props/SetupAssets/Blueprints/TechPrimitives/CP_L_T_Primitive_Planar_Cylinder_Solid.CP_L_T_Primitive_Planar_Cylinder_Solid_C",
    "W": "/Game/Building/ActorBlueprints/Player/Wood/L1/PBWA_W1_Solid.PBWA_W1_Solid_C",
    "S": "/Game/Building/ActorBlueprints/Player/Wood/L1/PBWA_W1_StairW.PBWA_W1_StairW_C",
    "C": "/Game/Building/ActorBlueprints/Player/Wood/L1/PBWA_W1_RoofC.PBWA_W1_RoofC_C",
    "F": "/Game/Building/ActorBlueprints/Player/Wood/L1/PBWA_W1_Floor.PBWA_W1_Floor_C",
}
KEEP = ("_Chrono", "TUN_ResetDevice")   # devices Verse conserves

lines = []
def log(*a):
    lines.append(" ".join(str(x) for x in a))

eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
eal = unreal.EditorAssetLibrary
mel = unreal.MaterialEditingLibrary
tools = unreal.AssetToolsHelpers.get_asset_tools()
CUBE = eal.load_asset("/Engine/BasicShapes/Cube")

def V(x, y, z):
    return unreal.Vector(float(x), float(y), float(z))

_src = open(TOOLS + r"\build_lobby.py", encoding="utf-8").read()
_ns = {"unreal": unreal, "eal": eal, "mel": mel, "tools": tools, "MAT_DIR": MAT_DIR}
exec(_src[_src.index("def new_material"):_src.index("# couleurs en lineaire")], _ns)

def led_mat(name, rgb, k=15.0):
    return _ns["opaque_mat"](name, unreal.LinearColor(0, 0, 0, 1), 0.5,
                             unreal.LinearColor(rgb[0] * k, rgb[1] * k, rgb[2] * k, 1))

_cls = {}
def cls(key):
    if key not in _cls:
        _cls[key] = unreal.load_class(None, CLS[key])
    return _cls[key]

def tag(a, label, folder):
    a.set_actor_label("TUN_" + label)
    a.set_folder_path("Zones/Edit/Tunnels/" + folder)
    return a

def box(label, folder, mat, cx, cy, cz, sx, sy, sz, collision=True):
    a = eas.spawn_actor_from_class(unreal.FortStaticMeshActor, V(cx, cy, cz))
    c = a.get_component_by_class(unreal.StaticMeshComponent)
    c.set_static_mesh(CUBE)
    c.set_material(0, mat)
    a.set_actor_scale3d(V(sx / 100.0, sy / 100.0, sz / 100.0))
    if not collision:
        c.set_collision_profile_name("NoCollision")
        c.set_editor_property("cast_shadow", False)
    return tag(a, label, folder)

def ybox(label, folder, mat, x, y_from, y_to, z_from, z_to, w, collision=True):
    """Boite alignee en Y entre y_from et y_to (y_from > y_to), de z_from a z_to."""
    return box(label, folder, mat, x, (y_from + y_to) / 2, (z_from + z_to) / 2,
               w, abs(y_from - y_to), z_to - z_from, collision)

def dev(key, label, folder, loc, yaw=0.0):
    a = eas.spawn_actor_from_class(cls(key), loc, unreal.Rotator(roll=0, pitch=0, yaw=yaw))
    return tag(a, label, folder)

def fit(actor, w, d, h, bottom_center):
    o, e = actor.get_actor_bounds(False)
    s = actor.get_actor_scale3d()
    actor.set_actor_scale3d(V(s.x * w / (2 * e.x), s.y * d / (2 * e.y), s.z * h / (2 * e.z)))
    o, e = actor.get_actor_bounds(False)
    loc = actor.get_actor_location()
    actor.set_actor_location(V(bottom_center.x + (loc.x - o.x), bottom_center.y + (loc.y - o.y),
                               bottom_center.z + (loc.z - (o.z - e.z))), False, False)

def billboard(label, folder, loc, text, size=60):
    bb = dev("billboard", label, folder, loc, 180.0)   # tourne vers +Y (zone Edit)
    bb.set_editor_property("text", text)
    bb.set_editor_property("TextSize", size)
    return bb

def runs(specs):
    """Regroupe les cases consecutives ayant la meme valeur -> (debut, fin, valeur)."""
    out, start = [], 0
    for k in range(1, len(specs) + 1):
        if k == len(specs) or specs[k] != specs[start]:
            out.append((start, k - 1, specs[start]))
            start = k
    return out

def build_tunnel(name, X, rgb, seq, M_BLACK):
    folder = name.capitalize()
    M_LED = led_mat("M_Tunnel_Led_" + folder, rgb)
    cells = seq + ["#"]                   # derniere case = arrivee (pas de lettre W/S/C/U/D !)
    n = len(cells)
    yf = lambda k: Y0 - k * CELL          # bord avant (cote entree) de la case k
    # niveaux
    lvl, levels = 0, []
    for tok in cells:
        levels.append(lvl)
        if "U" in tok:
            lvl += 1
        elif "D" in tok:
            lvl -= 1
        if lvl < 0:
            raise Exception("%s descend sous le sol" % name)
    if levels[-1] != 0:
        log("ATTENTION", name, "finit au niveau", levels[-1])
    Z = lambda k: FLOOR_Z + levels[k] * LH

    # enveloppe de chaque case : (z bas, z haut, z du sol noir ou None)
    env = []
    for k, tok in enumerate(cells):
        z = Z(k)
        zb = z - LH if "D" in tok else z
        zt = z + 2 * LH if "U" in tok else z + LH
        floor = None
        if "D" in tok:
            floor = z - LH if levels[k] - 1 > 0 else None
        elif levels[k] > 0:
            floor = z
        env.append((zb, zt, floor))

    # murs lateraux + LED (fusionnes par troncons identiques)
    for (a, b, (zb, zt, fl)) in runs([(e[0], e[1]) + (None,) for e in env]):
        for sx in (-1, 1):
            ybox("%s_Side%d_%d" % (name, sx, a), folder, M_BLACK, X + sx * (HALF + 25), yf(a), yf(b + 1), zb, zt, 50)
            ybox("%s_SideLed%d_%d" % (name, sx, a), folder, M_LED, X + sx * (HALF - 3), yf(a), yf(b + 1), zt - 16, zt - 8, 6, False)
    for (a, b, zt) in runs([e[1] for e in env]):
        ybox("%s_Ceil_%d" % (name, a), folder, M_BLACK, X, yf(a), yf(b + 1), zt, zt + 50, CELL + 100)
        ybox("%s_CeilLed_%d" % (name, a), folder, M_LED, X, yf(a), yf(b + 1), zt - 6, zt, 20, False)
    for (a, b, fl) in runs([e[2] for e in env]):
        if fl is not None:
            ybox("%s_Floor_%d" % (name, a), folder, M_BLACK, X, yf(a), yf(b + 1), fl - 30, fl, CELL + 100)

    # fermetures (pour ne pas sortir du tunnel)
    W = CELL + 100
    for k, tok in enumerate(cells):
        z = Z(k)
        if "U" in tok:
            # dessous de la case suivante + au-dessus du plafond de la case precedente
            box("%s_CloseU%d_a" % (name, k), folder, M_BLACK, X, yf(k + 1) + 10, z + LH / 2, W, 20, LH)
            box("%s_CloseU%d_b" % (name, k), folder, M_BLACK, X, yf(k) - 10, z + LH * 1.5, W, 20, LH)
        if "D" in tok:
            # haut : on ne peut pas continuer tout droit / bas : derriere la chute
            box("%s_CloseD%d_a" % (name, k), folder, M_BLACK, X, yf(k + 1) + 10, z + LH / 2, W, 20, LH)
            box("%s_CloseD%d_b" % (name, k), folder, M_BLACK, X, yf(k) - 10, z - LH / 2, W, 20, LH)
    zl = Z(n - 1)
    box("%s_End" % name, folder, M_BLACK, X, yf(n) - 25, zl + LH / 2, W, 50, LH)

    # pieces editables
    count = 0
    for k, tok in enumerate(cells):
        z = Z(k)
        if "W" in tok:
            dev("W", "%s_Wall%d" % (name, k), folder + "/Builds", V(X, yf(k), z)); count += 1
        if "S" in tok or "U" in tok:
            # escalier (pivot sur le bord arriere, monte vers -Y)
            dev("S", "%s_%s%d" % (name, "Ramp" if "U" in tok else "Stair", k), folder + "/Builds", V(X, yf(k + 1), z))
            if "S" in tok:
                count += 1
        if "C" in tok:
            dev("C", "%s_Cone%d" % (name, k), folder + "/Builds", V(X, yf(k + 1), z)); count += 1
        if "D" in tok:
            dev("F", "%s_Hole%d" % (name, k), folder + "/Builds", V(X, yf(k + 1), z)); count += 1

    # lumieres
    for k in range(0, n, 4):
        pl = eas.spawn_actor_from_class(unreal.PointLight, V(X, yf(k) - HALF, env[k][1] - 70))
        lc = pl.get_component_by_class(unreal.PointLightComponent)
        lc.set_light_color(unreal.LinearColor(0.6 + 0.4 * rgb[0], 0.6 + 0.4 * rgb[1], 0.6 + 0.4 * rgb[2], 1))
        lc.set_intensity(15.0)
        lc.set_attenuation_radius(1000.0)
        tag(pl, "%s_Light%d" % (name, k), folder)

    # entree
    box("%s_FrameTop" % name, folder, M_LED, X, Y0 + 30, FLOOR_Z + LH + 60, W, 10, 20, False)
    for sx in (-1, 1):
        box("%s_FrameSide%d" % (name, sx), folder, M_LED, X + sx * (HALF + 45), Y0 + 30, FLOOR_Z + LH / 2 + 30, 20, 10, LH + 60, False)
    box("%s_EntryLine" % name, folder, M_LED, X, Y0 + 400, FLOOR_Z + 1, CELL, 20, 2, False)
    billboard("%s_Title" % name, folder, V(X, Y0 + 40, FLOOR_Z + LH + 150), TITLE_EN.get(name, name), 50)

    # chrono : triggers + HUD
    st = dev("trigger", "%s_Start" % name, folder + "/Chrono", V(X, Y0 + 250, FLOOR_Z))
    fi = dev("trigger", "%s_Finish" % name, folder + "/Chrono", V(X, yf(n - 1) - HALF, Z(n - 1)))
    hud = dev("hud", "%s_HUD" % name, folder + "/Chrono", V(X, Y0 + 600, FLOOR_Z - 400))
    log(name, "cases", len(seq), "editions", count, "longueur %.0f m" % (n * CELL / 100), "niveau max", max(levels))
    return {"name": name, "start": st.get_actor_label(), "finish": fi.get_actor_label(),
            "hud": hud.get_actor_label(), "x": X, "edits": count}

RESULT = {"tunnels": []}
try:
    n = 0
    for a in eas.get_all_level_actors():
        lab = a.get_actor_label()
        if (lab.startswith("TUN_") and not any(k in lab for k in KEEP)) or lab == "PROBE_STAIR":
            eas.destroy_actor(a); n += 1
    log("acteurs supprimes", n)

    M_BLACK = eal.load_asset(MAT_DIR + "/M_Lobby_BlackMatte")
    M_GLOSS = eal.load_asset(MAT_DIR + "/M_Lobby_BlackGloss")
    M_BLUE = eal.load_asset(MAT_DIR + "/M_Lobby_LedBlue")

    box("Platform", "Structure", M_GLOSS, 0, -23000 - EXT_LEN / 2, FLOOR_Z - 25, 6000, EXT_LEN, 50)
    for sx in (-1, 1):
        box("PlatformLed%d" % sx, "Structure", M_BLUE, sx * 2990, -23000 - EXT_LEN / 2, FLOOR_Z + 1, 20, EXT_LEN, 2, False)
    box("PlatformLedEnd", "Structure", M_BLUE, 0, -23000 - EXT_LEN + 10, FLOOR_Z + 1, 6000, 20, 2, False)

    pad = dev("pad", "ReturnPad", "Structure", V(0, -22600, ZONE_FLOOR))
    fit(pad, 250, 250, 8, V(0, -22600, ZONE_FLOOR))
    billboard("Title", "Structure", V(0, -23300, FLOOR_Z + 900), "EDIT TUNNELS", 70)

    # bouton RESET (relance la manche -> les murs reviennent)
    # (plus de bouton RESET : le reset se fait a l'arrivee de chaque tunnel)
    rs = dev("round", "RoundSettings", "Structure", V(-700, -22600, FLOOR_Z - 400))

    for (name, X, rgb, seq) in TUNNELS:
        try:
            RESULT["tunnels"].append(build_tunnel(name, X, rgb, seq, M_BLACK))
        except Exception:
            log(name, "ERREUR", traceback.format_exc())

    RESULT["return_pad"] = pad.get_actor_label()
    RESULT["round_settings"] = rs.get_actor_label()
    open(TOOLS + r"\build_tunnels_map.json", "w", encoding="utf-8").write(json.dumps(RESULT, indent=1))
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    log("TERMINE - acteurs TUN_ :", sum(1 for a in eas.get_all_level_actors() if a.get_actor_label().startswith("TUN_")))
except Exception:
    log("ERREUR", traceback.format_exc())

open(LOG_FILE, "w", encoding="utf-8").write("\n".join(lines))
