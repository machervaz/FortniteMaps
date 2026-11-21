# ============================================================================
#  build_sky_floor.py - sol autour de l'arene 1v1 (sous la voute)
#  - remplace le sol noir (maillage fixe) par un PROP (disque) dont le panneau
#    Verse change le materiau en meme temps que le ciel
#  - 4 materiaux de sol assortis aux ciels (M_SkyFloor_Violet / Jour / Nuit / Rose)
#  - une Mutator Zone tres fine au ras de ce sol (sous le niveau de la
#    plateforme) : si on touche le sol, on est teleporte sur le disque principal
# ============================================================================
import unreal, json, traceback

TOOLS = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools"
ROOT = "/5622d7d7-d1ca-438f-8a48-1286a48e2471"
MAT_DIR = ROOT + "/Lobby/Materials"
CX, CY = -20000.0, 0.0
RADIUS = 17000.0
GROUND_Z = 1200.0          # dessus du sol (plateforme a 1270)
PROP_CLS = "/CRG_Props/SetupAssets/Blueprints/TechPrimitives/CP_L_T_Primitive_Planar_Cylinder_Solid.CP_L_T_Primitive_Planar_Cylinder_Solid_C"
ZONE_CLS = "/CRD_VolumetricRegion/Device_MutatorVolume_V2.Device_MutatorVolume_V2_C"
def C(r, g, b):
    return unreal.LinearColor(r, g, b, 1.0)
FLOORS = [  # nom, couleur de base, reflet emissif (version sombre du ciel)
    ("Violet", C(0.12, 0.03, 0.25), C(0.10, 0.03, 0.22)),
    ("Jour", C(0.05, 0.15, 0.35), C(0.03, 0.10, 0.28)),
    ("Nuit", C(0.005, 0.005, 0.015), C(0.0, 0.0, 0.01)),
    ("Rose", C(0.35, 0.08, 0.12), C(0.28, 0.06, 0.10)),
]
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
eal = unreal.EditorAssetLibrary
mel = unreal.MaterialEditingLibrary
tools = unreal.AssetToolsHelpers.get_asset_tools()
L = []

def floor_mat(name, base, emi):
    path = MAT_DIR + "/" + name
    if eal.does_asset_exist(path):
        return eal.load_asset(path)
    m = tools.create_asset(name, MAT_DIR, unreal.Material, unreal.MaterialFactoryNew())
    for prop, val, y in (("base", base, -200), ("emi", emi, 200)):
        c = mel.create_material_expression(m, unreal.MaterialExpressionConstant3Vector, -400, y)
        c.set_editor_property("constant", val)
        mel.connect_material_property(c, "", unreal.MaterialProperty.MP_BASE_COLOR if prop == "base" else unreal.MaterialProperty.MP_EMISSIVE_COLOR)
    r = mel.create_material_expression(m, unreal.MaterialExpressionConstant, -400, 0)
    r.set_editor_property("r", 0.15)
    mel.connect_material_property(r, "", unreal.MaterialProperty.MP_ROUGHNESS)
    mel.recompile_material(m)
    eal.save_loaded_asset(m)
    return m

def fit(actor, w, d, h, bottom):
    o, e = actor.get_actor_bounds(False)
    s = actor.get_actor_scale3d()
    actor.set_actor_scale3d(unreal.Vector(s.x * w / (2 * e.x), s.y * d / (2 * e.y), s.z * h / (2 * e.z)))
    o, e = actor.get_actor_bounds(False)
    loc = actor.get_actor_location()
    actor.set_actor_location(unreal.Vector(bottom.x + loc.x - o.x, bottom.y + loc.y - o.y, bottom.z + loc.z - (o.z - e.z)), False, False)

def fin(a, label):
    a.set_actor_label(label)
    a.set_folder_path("Zones/1v1/Panel")
    a.set_editor_property("is_spatially_loaded", False)
    return a

try:
    mats = [floor_mat("M_SkyFloor_" + n, b, e) for (n, b, e) in FLOORS]
    ACT = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
    for lab in ("ZONE_1v1P_SkyFloor", "ZONE_1v1P_FallZone"):
        if lab in ACT:
            eas.destroy_actor(ACT.pop(lab)); L.append("supprime " + lab)
    # sol = prop disque de 340 m, 30 cm d'epaisseur, dessus a GROUND_Z
    floor = eas.spawn_actor_from_class(unreal.load_class(None, PROP_CLS), unreal.Vector(CX, CY, GROUND_Z))
    fit(floor, 2 * RADIUS, 2 * RADIUS, 30, unreal.Vector(CX, CY, GROUND_Z - 30))
    for c in floor.get_components_by_class(unreal.StaticMeshComponent):
        for i in range(max(1, c.get_num_materials())):
            c.set_material(i, mats[0])
    fin(floor, "ZONE_1v1P_SkyFloor")
    o, e = floor.get_actor_bounds(False)
    L.append("sol centre=(%.0f,%.0f,%.0f) taille=(%.0f,%.0f,%.0f)" % (o.x, o.y, o.z, e.x, e.y, e.z))
    # zone de chute : de 1190 a 1255 (la plateforme est a 1270 : ses joueurs ne la touchent pas)
    zone = eas.spawn_actor_from_class(unreal.load_class(None, ZONE_CLS), unreal.Vector(CX, CY, GROUND_Z))
    fit(zone, 2 * RADIUS, 2 * RADIUS, 65, unreal.Vector(CX, CY, GROUND_Z - 10))
    fin(zone, "ZONE_1v1P_FallZone")
    o, e = zone.get_actor_bounds(False)
    L.append("zone centre=(%.0f,%.0f,%.0f) taille=(%.0f,%.0f,%.0f)" % (o.x, o.y, o.z, e.x, e.y, e.z))
    m = json.load(open(TOOLS + r"\build_panel_map.json"))
    m["sky_floor"] = "ZONE_1v1P_SkyFloor"
    m["fall_zone"] = "ZONE_1v1P_FallZone"
    m["respawn"] = "ZONE_1v1_Arrival"
    json.dump(m, open(TOOLS + r"\build_panel_map.json", "w"), indent=1)
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE")
except Exception:
    L.append(traceback.format_exc())
open(TOOLS + r"\build_sky_floor_log.txt", "w").write("\n".join(L))
