# ============================================================================
#  build_lobby.py - place le lobby noir + LED + hologrammes dans UEFN
#  A lancer depuis la console Python de UEFN (barre du bas) :
#     C:/Users/marca/Documents/Fortnite Projects/testMoudon01/Tools/build_lobby.py
#  Relancable : supprime d'abord tous les acteurs dont le label commence par LOBBY_
#  Toutes les tailles en cm (100 = 1 m). Voir GUIDE_MAP_ENTRAINEMENT.md
# ============================================================================
import unreal, math, traceback

LOG_FILE = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\build_lobby_log.txt"
ROOT = "/5622d7d7-d1ca-438f-8a48-1286a48e2471/Lobby"
MAT_DIR = ROOT + "/Materials"

# ---- Parametres ----
# z = 1270 : au-dessus de BuilderGridPlane135 (dalle +X/+Y, dessus a 1256)
O = unreal.Vector(0.0, 0.0, 1270.0)   # centre du lobby, niveau du sol (dessus du sol)
SIZE = 4000.0      # 40 x 40 m
HEIGHT = 1200.0    # 12 m
WALL = 50.0
LED = 10.0
WHITE_LINES = 4
GRID = 1000.0
PORTAL_DIST = 1200.0
HOLO_D = 300.0
HOLO_H = 400.0

PORTALS = [
    ("PIECE CONTROL", "PieceControl", (1.0, 0.0)),
    ("EDIT", "Edit", (0.0, -1.0)),
    ("AIM", "Aim", (0.0, 1.0)),
    ("1V1", "1v1", (-1.0, 0.0)),
]

CLS = {
    "mutator": "/CRD_VolumetricRegion/Device_MutatorVolume_V2.Device_MutatorVolume_V2_C",
    "billboard": "/Game/Creative/Devices/Billboard/BP_Creative_Billboard.BP_Creative_Billboard_C",
    "beacon": "/CreativeCoreDevices/AlwaysCook/Device_Beacon_V2_Beam_Blue.Device_Beacon_V2_Beam_Blue_C",
    "spawner": "/CRD_PlayerSpawn/BP_Creative_Player_Spawner_Prop.BP_Creative_Player_Spawner_Prop_C",
}

lines = []
def log(*a):
    s = " ".join(str(x) for x in a)
    lines.append(s)
    unreal.log("[build_lobby] " + s)

eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
eal = unreal.EditorAssetLibrary
mel = unreal.MaterialEditingLibrary
tools = unreal.AssetToolsHelpers.get_asset_tools()
CUBE = eal.load_asset("/Engine/BasicShapes/Cube")
CYL = eal.load_asset("/Engine/BasicShapes/Cylinder")

def V(x, y, z):
    return unreal.Vector(float(x), float(y), float(z))

# ---------------------------------------------------------------------------
#  Materiaux
# ---------------------------------------------------------------------------
def new_material(name):
    path = MAT_DIR + "/" + name
    if eal.does_asset_exist(path):
        eal.delete_asset(path)
    return tools.create_asset(name, MAT_DIR, unreal.Material, unreal.MaterialFactoryNew())

def const3(m, color, x=-400, y=0):
    c = mel.create_material_expression(m, unreal.MaterialExpressionConstant3Vector, x, y)
    c.set_editor_property("constant", color)
    return c

def const1(m, v, x=-400, y=0):
    c = mel.create_material_expression(m, unreal.MaterialExpressionConstant, x, y)
    c.set_editor_property("r", float(v))
    return c

def existing(name):
    path = MAT_DIR + "/" + name
    if eal.does_asset_exist(path):
        return eal.load_asset(path)
    return None

def opaque_mat(name, base, rough, emissive=None):
    if existing(name):
        return existing(name)
    m = new_material(name)
    mel.connect_material_property(const3(m, base, -400, -200), "", unreal.MaterialProperty.MP_BASE_COLOR)
    mel.connect_material_property(const1(m, rough, -400, 0), "", unreal.MaterialProperty.MP_ROUGHNESS)
    if emissive is not None:
        mel.connect_material_property(const3(m, emissive, -400, 200), "", unreal.MaterialProperty.MP_EMISSIVE_COLOR)
    mel.recompile_material(m)
    eal.save_loaded_asset(m)
    return m

def hologram_mat(name, color):
    if existing(name):
        return existing(name)
    m = new_material(name)
    m.set_editor_property("blend_mode", unreal.BlendMode.BLEND_TRANSLUCENT)
    m.set_editor_property("shading_model", unreal.MaterialShadingModel.MSM_UNLIT)
    m.set_editor_property("two_sided", True)
    fres = mel.create_material_expression(m, unreal.MaterialExpressionFresnel, -900, 0)
    fres.set_editor_property("exponent", 3.0)
    fres.set_editor_property("base_reflect_fraction", 0.05)
    # Emissive = couleur * (fresnel + 0.15) * 15
    fadd = mel.create_material_expression(m, unreal.MaterialExpressionAdd, -700, -150)
    fadd.set_editor_property("const_b", 0.15)
    mel.connect_material_expressions(fres, "", fadd, "A")
    col = const3(m, color, -700, -300)
    mul1 = mel.create_material_expression(m, unreal.MaterialExpressionMultiply, -500, -200)
    mel.connect_material_expressions(col, "", mul1, "A")
    mel.connect_material_expressions(fadd, "", mul1, "B")
    mul2 = mel.create_material_expression(m, unreal.MaterialExpressionMultiply, -300, -200)
    mul2.set_editor_property("const_b", 15.0)
    mel.connect_material_expressions(mul1, "", mul2, "A")
    mel.connect_material_property(mul2, "", unreal.MaterialProperty.MP_EMISSIVE_COLOR)
    # Bandes de scan : sin(Z/12 + Time*3) -> 0..1 -> * 0.2
    wp = mel.create_material_expression(m, unreal.MaterialExpressionWorldPosition, -1300, 300)
    mask = mel.create_material_expression(m, unreal.MaterialExpressionComponentMask, -1100, 300)
    mask.set_editor_property("r", False); mask.set_editor_property("g", False)
    mask.set_editor_property("b", True); mask.set_editor_property("a", False)
    mel.connect_material_expressions(wp, "", mask, "")
    zdiv = mel.create_material_expression(m, unreal.MaterialExpressionMultiply, -950, 300)
    zdiv.set_editor_property("const_b", 1.0 / 12.0)
    mel.connect_material_expressions(mask, "", zdiv, "A")
    t = mel.create_material_expression(m, unreal.MaterialExpressionTime, -1100, 450)
    tmul = mel.create_material_expression(m, unreal.MaterialExpressionMultiply, -950, 450)
    tmul.set_editor_property("const_b", 3.0)
    mel.connect_material_expressions(t, "", tmul, "A")
    sadd = mel.create_material_expression(m, unreal.MaterialExpressionAdd, -800, 350)
    mel.connect_material_expressions(zdiv, "", sadd, "A")
    mel.connect_material_expressions(tmul, "", sadd, "B")
    sine = mel.create_material_expression(m, unreal.MaterialExpressionSine, -650, 350)
    sine.set_editor_property("period", 6.2831853)
    mel.connect_material_expressions(sadd, "", sine, "")
    smul = mel.create_material_expression(m, unreal.MaterialExpressionMultiply, -500, 350)
    smul.set_editor_property("const_b", 0.1)
    mel.connect_material_expressions(sine, "", smul, "A")
    # Opacity = fresnel*0.6 + scan*0.1 + 0.15
    fop = mel.create_material_expression(m, unreal.MaterialExpressionMultiply, -500, 150)
    fop.set_editor_property("const_b", 0.6)
    mel.connect_material_expressions(fres, "", fop, "A")
    oadd = mel.create_material_expression(m, unreal.MaterialExpressionAdd, -350, 200)
    mel.connect_material_expressions(fop, "", oadd, "A")
    mel.connect_material_expressions(smul, "", oadd, "B")
    oadd2 = mel.create_material_expression(m, unreal.MaterialExpressionAdd, -200, 200)
    oadd2.set_editor_property("const_b", 0.15)
    mel.connect_material_expressions(oadd, "", oadd2, "A")
    mel.connect_material_property(oadd2, "", unreal.MaterialProperty.MP_OPACITY)
    mel.recompile_material(m)
    eal.save_loaded_asset(m)
    return m

# couleurs en lineaire (#00AAFF -> 0, 0.402, 1 ; #00CFFF -> 0, 0.624, 1)
BLACK = unreal.LinearColor(0.005, 0.005, 0.005, 1)
BLUE_LIN = (0.0, 0.402, 1.0)

def blue(k):
    return unreal.LinearColor(BLUE_LIN[0] * k, BLUE_LIN[1] * k, BLUE_LIN[2] * k, 1)

# ---------------------------------------------------------------------------
#  Acteurs
# ---------------------------------------------------------------------------
def tag(actor, label, folder):
    actor.set_actor_label("LOBBY_" + label)
    actor.set_folder_path("Lobby/" + folder)

def box(label, folder, mesh, mat, center, size, collision=True, rot=None):
    # FortStaticMeshActor : un StaticMeshActor standard n'apparait pas en jeu dans Fortnite
    a = eas.spawn_actor_from_class(unreal.FortStaticMeshActor, center, rot or unreal.Rotator(0, 0, 0))
    comp = a.get_component_by_class(unreal.StaticMeshComponent)
    comp.set_static_mesh(mesh)
    comp.set_material(0, mat)
    a.set_actor_scale3d(V(size.x / 100.0, size.y / 100.0, size.z / 100.0))
    if not collision:
        comp.set_collision_profile_name("NoCollision")
        comp.set_editor_property("cast_shadow", False)
    tag(a, label, folder)
    return a

def spawn_class(key, label, folder, loc, yaw=0.0):
    try:
        cls = unreal.load_class(None, CLS[key])
        if not cls:
            log("CLASSE INTROUVABLE", key)
            return None
        a = eas.spawn_actor_from_class(cls, loc, unreal.Rotator(0, 0, yaw))
        if a:
            tag(a, label, folder)
        return a
    except Exception as e:
        log("spawn fail", key, e)
        return None

def set_yaw(rot, yaw):
    return unreal.Rotator(roll=0.0, pitch=0.0, yaw=yaw)

try:
    # 1) nettoyage
    n = 0
    for a in eas.get_all_level_actors():
        try:
            if a.get_actor_label().startswith("LOBBY_") or a.get_actor_label() == "PROBE_CUBE":
                eas.destroy_actor(a); n += 1
        except Exception:
            pass
    if eal.does_asset_exist(MAT_DIR + "/M_Probe"):
        eal.delete_asset(MAT_DIR + "/M_Probe")
    log("acteurs supprimes", n)

    # 2) materiaux
    M_BLACK = opaque_mat("M_Lobby_BlackMatte", BLACK, 0.8)
    M_FLOOR = opaque_mat("M_Lobby_BlackGloss", BLACK, 0.2)
    M_BLUE = opaque_mat("M_Lobby_LedBlue", unreal.LinearColor(0, 0, 0, 1), 0.5, blue(20))
    M_WHITE = opaque_mat("M_Lobby_LedWhite", unreal.LinearColor(0, 0, 0, 1), 0.5, unreal.LinearColor(10, 10, 10, 1))
    M_DISC = opaque_mat("M_Lobby_DiscBlue", unreal.LinearColor(0, 0, 0, 1), 0.5, blue(8))
    M_HOLO = hologram_mat("M_Lobby_Hologram", unreal.LinearColor(0.0, 0.624, 1.0, 1))
    log("materiaux ok")

    # 3) piece (sol, plafond, murs)
    H = SIZE / 2.0
    W = WALL
    OUT = SIZE + 2 * W
    box("Floor", "Structure", CUBE, M_FLOOR, O + V(0, 0, -W / 2), V(OUT, OUT, W))
    box("Ceiling", "Structure", CUBE, M_BLACK, O + V(0, 0, HEIGHT + W / 2), V(OUT, OUT, W))
    box("Wall_PX", "Structure", CUBE, M_BLACK, O + V(H + W / 2, 0, HEIGHT / 2), V(W, OUT, HEIGHT))
    box("Wall_NX", "Structure", CUBE, M_BLACK, O + V(-H - W / 2, 0, HEIGHT / 2), V(W, OUT, HEIGHT))
    box("Wall_PY", "Structure", CUBE, M_BLACK, O + V(0, H + W / 2, HEIGHT / 2), V(OUT, W, HEIGHT))
    box("Wall_NY", "Structure", CUBE, M_BLACK, O + V(0, -H - W / 2, HEIGHT / 2), V(OUT, W, HEIGHT))
    log("piece ok")

    # 4) LED
    L = LED
    for (nx, ny, tagn) in [(1, 0, "PX"), (-1, 0, "NX"), (0, 1, "PY"), (0, -1, "NY")]:
        tx, ty = -ny, nx
        inner = O + V(nx * (H - L / 2), ny * (H - L / 2), 0)
        def size(depth, length, tall):
            return V(abs(nx) * depth + abs(tx) * length, abs(ny) * depth + abs(ty) * length, tall)
        box("LedBlue_Bottom_" + tagn, "LED", CUBE, M_BLUE, inner + V(0, 0, L), size(L, SIZE, 2 * L), False)
        box("LedBlue_Top_" + tagn, "LED", CUBE, M_BLUE, inner + V(0, 0, HEIGHT - L), size(L, SIZE, 2 * L), False)
        # bande bleue sur l'arete du plafond (sous le plafond, contre le mur)
        box("LedBlue_Ceil_" + tagn, "LED", CUBE, M_BLUE,
            O + V(nx * (H - 3 * L), ny * (H - 3 * L), HEIGHT - L / 2), size(2 * L, SIZE, L), False)
        for i in range(1, WHITE_LINES + 1):
            off = -H + SIZE * i / (WHITE_LINES + 1)
            box("LedWhite_%s_%d" % (tagn, i), "LED", CUBE, M_WHITE,
                inner + V(tx * off, ty * off, HEIGHT / 2), size(L, 2 * L, HEIGHT - 4 * L), False)
    pos = -H + GRID
    k = 0
    while pos < H - 1:
        box("LedGrid_X_%d" % k, "LED", CUBE, M_BLUE, O + V(pos, 0, 1), V(L, SIZE, 2), False)
        box("LedGrid_Y_%d" % k, "LED", CUBE, M_BLUE, O + V(0, pos, 1), V(SIZE, L, 2), False)
        pos += GRID; k += 1
    log("LED ok")

    # 5) eclairage
    for i, (sx, sy) in enumerate([(1, 1), (1, -1), (-1, 1), (-1, -1)]):
        pl = eas.spawn_actor_from_class(unreal.PointLight, O + V(sx * 1000, sy * 1000, HEIGHT - 150))
        lc = pl.get_component_by_class(unreal.PointLightComponent)
        lc.set_light_color(unreal.LinearColor(0.0, 0.5, 1.0, 1))
        lc.set_intensity(40.0)
        lc.set_attenuation_radius(2500.0)
        tag(pl, "Light_Blue_%d" % i, "Lights")

    # 6) portails
    for (title, key, (dx, dy)) in PORTALS:
        P = O + V(dx * PORTAL_DIST, dy * PORTAL_DIST, 0)
        yaw_to_center = math.degrees(math.atan2(-dy, -dx))
        box("Socle_" + key, "Portals/" + key, CYL, M_DISC, P + V(0, 0, 3), V(HOLO_D * 1.3, HOLO_D * 1.3, 6), False)
        box("Holo_" + key, "Portals/" + key, CYL, M_HOLO, P + V(0, 0, 20 + HOLO_H / 2), V(HOLO_D, HOLO_D, HOLO_H), False)

        # Mutator Zone ajustee a ~3 x 3 x 4 m
        mz = spawn_class("mutator", "Zone_" + key, "Portals/" + key, P)
        if mz:
            origin, ext = mz.get_actor_bounds(False)
            log("mutator bounds", key, origin, ext)
            if ext.x > 1 and ext.y > 1 and ext.z > 1:
                s = mz.get_actor_scale3d()
                mz.set_actor_scale3d(V(s.x * HOLO_D / (2 * ext.x), s.y * HOLO_D / (2 * ext.y), s.z * HOLO_H / (2 * ext.z)))
                origin, ext = mz.get_actor_bounds(False)
                loc = mz.get_actor_location()
                mz.set_actor_location(V(P.x + (loc.x - origin.x), P.y + (loc.y - origin.y), P.z + 20 + (loc.z - (origin.z - ext.z))), False, False)
                origin, ext = mz.get_actor_bounds(False)
                log("mutator after", key, origin, ext)

        # Billboard au-dessus, tourne vers le centre
        # (+90 : le panneau du Billboard est oriente sur l'axe Y local)
        bb = spawn_class("billboard", "Billboard_" + key, "Portals/" + key, P + V(0, 0, 20 + HOLO_H + 120), yaw_to_center + 90.0)
        if bb:
            try:
                bb.set_editor_property("text", title)
                bb.set_editor_property("TextSize", 40)
            except Exception as e:
                log("billboard: texte a saisir a la main ->", title, e)

        # Beacon bleu (faisceau vertical)
        spawn_class("beacon", "Beacon_" + key, "Portals/" + key, P + V(0, 0, 0))

        # Spot blanc depuis le plafond vers le cylindre
        src = O + V(dx * (PORTAL_DIST - 500), dy * (PORTAL_DIST - 500), HEIGHT - 60)
        tgt = P + V(0, 0, 200)
        rot = unreal.MathLibrary.find_look_at_rotation(src, tgt)
        sp = eas.spawn_actor_from_class(unreal.SpotLight, src, rot)
        sc = sp.get_component_by_class(unreal.SpotLightComponent)
        sc.set_light_color(unreal.LinearColor(1, 1, 1, 1))
        sc.set_intensity(60.0)
        sc.set_attenuation_radius(1500.0)
        sc.set_outer_cone_angle(25.0)
        sc.set_inner_cone_angle(12.0)
        tag(sp, "Spot_" + key, "Portals/" + key)
    log("portails ok")

    # 7) LobbyPoint (pad d'arrivee, sans collision) + Player Spawner
    box("LobbyPoint", "Gameplay", CYL, M_WHITE, O + V(0, 0, 4), V(150, 150, 8), False)
    spawn_class("spawner", "PlayerSpawner", "Gameplay", O + V(-500, 0, 0), 0.0)

    # 8) Post process (bloom pour que les LED bavent)
    try:
        pp = eas.spawn_actor_from_class(unreal.PostProcessVolume, O + V(0, 0, HEIGHT / 2))
        pp.set_editor_property("unbound", True)
        st = pp.get_editor_property("settings")
        st.set_editor_property("override_bloom_intensity", True)
        st.set_editor_property("bloom_intensity", 1.5)
        st.set_editor_property("override_auto_exposure_bias", True)
        st.set_editor_property("auto_exposure_bias", -0.5)
        pp.set_editor_property("settings", st)
        tag(pp, "PostProcess", "Ambience")
        log("postprocess ok")
    except Exception:
        log("postprocess fail", traceback.format_exc())

    # 9) sauvegarde
    try:
        unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
        log("sauvegarde ok")
    except Exception:
        log("sauvegarde fail", traceback.format_exc())

    cnt = sum(1 for a in eas.get_all_level_actors() if a.get_actor_label().startswith("LOBBY_"))
    log("TERMINE - acteurs LOBBY_ :", cnt)
except Exception:
    log("ERREUR", traceback.format_exc())

with open(LOG_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
