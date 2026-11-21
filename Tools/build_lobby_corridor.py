# ============================================================================
#  build_lobby_corridor.py - le lobby devient un COULOIR (comme l'image) :
#  40 m de long (x -2000..2000), 24 m de large (y -1200..1200), 9 m de haut.
#  LED toutes BLEUES : arches regulieres (montants + traverse au plafond),
#  bandes au ras du sol et sous le plafond, cadre du mur des portails.
#  Spawn au fond du couloir face aux portails. Relancable (LOBBY_Cor_*).
# ============================================================================
import unreal, traceback
TOOLS = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools"
MAT_DIR = "/5622d7d7-d1ca-438f-8a48-1286a48e2471/Lobby/Materials"
FLOOR, HALF_X, HALF_Y, H, W = 1270.0, 2000.0, 1200.0, 900.0, 50.0
LED = 10.0
RIBS = [-1800.0 + 400.0 * i for i in range(8)]     # -1800 .. 1000 (pas d'arche devant les portails)
OLD = ("LOBBY_LedBlue_", "LOBBY_LedWhite_", "LOBBY_LedGrid_", "LOBBY_Light_Blue_", "LOBBY_Cor_")
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
eal = unreal.EditorAssetLibrary
CUBE = eal.load_asset("/Engine/BasicShapes/Cube")
L = []

def V(x, y, z):
    return unreal.Vector(float(x), float(y), float(z))

def touch(a):
    a.modify()
    for c in a.get_components_by_class(unreal.SceneComponent):
        c.modify()

def place(a, c, size):
    touch(a)
    a.set_actor_location(c, False, False)
    a.set_actor_scale3d(V(size.x / 100, size.y / 100, size.z / 100))

def led(label, m, c, size):
    a = eas.spawn_actor_from_class(unreal.FortStaticMeshActor, c)
    comp = a.get_component_by_class(unreal.StaticMeshComponent)
    comp.set_static_mesh(CUBE)
    comp.set_material(0, m)
    a.set_actor_scale3d(V(size.x / 100, size.y / 100, size.z / 100))
    comp.set_collision_profile_name("NoCollision")
    comp.set_editor_property("cast_shadow", False)
    a.set_actor_label("LOBBY_Cor_" + label)
    a.set_folder_path("Lobby/LED")
    a.set_editor_property("is_spatially_loaded", False)
    return a

def led_blue():
    # bleu profond comme l image (moins intense = reste bleu au lieu de virer au blanc)
    path = MAT_DIR + "/M_Lobby_LedDeepBlue"
    if eal.does_asset_exist(path):
        return eal.load_asset(path)
    mel = unreal.MaterialEditingLibrary
    m = unreal.AssetToolsHelpers.get_asset_tools().create_asset("M_Lobby_LedDeepBlue", MAT_DIR, unreal.Material, unreal.MaterialFactoryNew())
    for prop, col, y in ((unreal.MaterialProperty.MP_BASE_COLOR, unreal.LinearColor(0, 0, 0, 1), -100),
                         (unreal.MaterialProperty.MP_EMISSIVE_COLOR, unreal.LinearColor(0.04, 0.35, 4.0, 1), 100)):
        e = mel.create_material_expression(m, unreal.MaterialExpressionConstant3Vector, -400, y)
        e.set_editor_property("constant", col)
        mel.connect_material_property(e, "", prop)
    mel.recompile_material(m)
    eal.save_loaded_asset(m)
    return m

try:
    ACT = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
    n = 0
    for lab, a in list(ACT.items()):
        if lab.startswith(OLD):
            eas.destroy_actor(a); n += 1
    L.append("anciennes LED/lumieres supprimees : %d" % n)
    blue = led_blue()
    OUTX, OUTY = 2 * HALF_X + 2 * W, 2 * HALF_Y + 2 * W
    with unreal.ScopedEditorTransaction("Lobby couloir"):
        place(ACT["LOBBY_Floor"], V(0, 0, FLOOR - W / 2), V(OUTX, OUTY, W))
        place(ACT["LOBBY_Ceiling"], V(0, 0, FLOOR + H + W / 2), V(OUTX, OUTY, W))
        place(ACT["LOBBY_Wall_PX"], V(HALF_X + W / 2, 0, FLOOR + H / 2), V(W, OUTY, H))
        place(ACT["LOBBY_Wall_NX"], V(-HALF_X - W / 2, 0, FLOOR + H / 2), V(W, OUTY, H))
        place(ACT["LOBBY_Wall_PY"], V(0, HALF_Y + W / 2, FLOOR + H / 2), V(OUTX, W, H))
        place(ACT["LOBBY_Wall_NY"], V(0, -HALF_Y - W / 2, FLOOR + H / 2), V(OUTX, W, H))
        sp = ACT["LOBBY_PlayerSpawner"]
        touch(sp)
        sp.set_actor_location(V(-1500, 0, FLOOR), False, False)
        # arches
        for i, x in enumerate(RIBS):
            for s in (1, -1):
                led("Rib%d_Wall%d" % (i, s), blue, V(x, s * (HALF_Y - LED / 2), FLOOR + H / 2), V(2 * LED, LED, H))
            led("Rib%d_Ceil" % i, blue, V(x, 0, FLOOR + H - LED / 2), V(2 * LED, 2 * HALF_Y, LED))
        # bandes longitudinales (sol + haut des murs) et lignes au plafond
        for s in (1, -1):
            led("SideFloor%d" % s, blue, V(0, s * (HALF_Y - LED / 2), FLOOR + LED), V(2 * HALF_X, LED, 2 * LED))
            led("SideTop%d" % s, blue, V(0, s * (HALF_Y - LED / 2), FLOOR + H - LED), V(2 * HALF_X, LED, 2 * LED))
            led("CeilLine%d" % s, blue, V(-300, s * 450, FLOOR + H - LED / 2), V(2 * HALF_X - 600, LED, LED))
        # mur des portails (+X) et mur du fond (-X) : cadre bleu
        for nm, x in (("PX", HALF_X - LED / 2), ("NX", -HALF_X + LED / 2)):
            led(nm + "_Bot", blue, V(x, 0, FLOOR + LED), V(LED, 2 * HALF_Y, 2 * LED))
            led(nm + "_Top", blue, V(x, 0, FLOOR + H - LED), V(LED, 2 * HALF_Y, 2 * LED))
        # lumieres bleues le long du plafond
        for i, x in enumerate((-1500.0, -500.0, 500.0)):
            pl = eas.spawn_actor_from_class(unreal.PointLight, V(x, 0, FLOOR + H - 100))
            lc = pl.get_component_by_class(unreal.PointLightComponent)
            lc.set_light_color(unreal.LinearColor(0.0, 0.35, 1.0, 1))
            lc.set_intensity(35.0)
            lc.set_attenuation_radius(1600.0)
            pl.set_actor_label("LOBBY_Cor_Light%d" % i)
            pl.set_folder_path("Lobby/Lights")
            pl.set_editor_property("is_spatially_loaded", False)
    # elements du lobby restes hors du couloir ?
    for a in eas.get_all_level_actors():
        lab = a.get_actor_label()
        p = a.get_actor_location()
        if lab.startswith("LOBBY_") and (abs(p.y) > HALF_Y + 60 or p.z > FLOOR + H + 60):
            L.append("HORS COULOIR : %s %s" % (lab, p))
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE")
except Exception:
    L.append(traceback.format_exc())
open(TOOLS + r"\build_lobby_corridor_log.txt", "w").write("\n".join(L))
