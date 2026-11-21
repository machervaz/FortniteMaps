# ============================================================================
#  build_sky_vault.py - voute celeste de la zone 1v1 (changement INSTANTANE)
#  - 4 materiaux non eclaires, visibles de l'interieur, en degrade bas -> haut
#    (M_SkyVault_Violet / Jour / Nuit / Rose)
#  - une demi-sphere creuse (prop Fortnite) de 80 m de rayon au-dessus de
#    l'arene, sans collision ni ombre. Le panneau Verse lui change de
#    materiau au tir (SetMaterial = instantane). Elle cache aussi le reste
#    de la map.
#  - supprime les 4 Skydomes (transition lente).
# ============================================================================
import unreal, json, traceback

TOOLS = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools"
ROOT = "/5622d7d7-d1ca-438f-8a48-1286a48e2471"
MAT_DIR = ROOT + "/Lobby/Materials"
CX, CY, FLOOR_Z = -20000.0, 0.0, 1270.0
RADIUS = 17000.0          # 170 m : le plus grand possible sans englober le lobby (a 179 m)
MAT_PREFIX = "M_SkyVault2_"   # degrade calcule pour ce rayon (doit correspondre au Verse)
GROUND_Z = 1200.0         # sol noir : au-dessus du quadrillage (1152), sous la plateforme (1270)
DOME_CLS = "/Game/Creative/Sets/PropSets/Primitives/Rounds/Props/CP_Primitive_Sphere_Hollow_Half.CP_Primitive_Sphere_Hollow_Half_C"
def C(r, g, b):
    return unreal.LinearColor(r, g, b, 1.0)
SKIES = [  # nom, couleur en bas (horizon), couleur en haut
    ("Violet", C(0.85, 0.45, 1.0), C(0.18, 0.03, 0.55)),
    ("Jour", C(0.85, 0.93, 1.0), C(0.05, 0.3, 1.0)),
    ("Nuit", C(0.04, 0.04, 0.12), C(0.0, 0.0, 0.01)),
    ("Rose", C(1.0, 0.65, 0.4), C(0.75, 0.15, 0.45)),
]
L = []
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
eal = unreal.EditorAssetLibrary
mel = unreal.MaterialEditingLibrary
tools = unreal.AssetToolsHelpers.get_asset_tools()

def sky_mat(name, bottom, top):
    path = MAT_DIR + "/" + name
    if eal.does_asset_exist(path):
        return eal.load_asset(path)
    m = tools.create_asset(name, MAT_DIR, unreal.Material, unreal.MaterialFactoryNew())
    m.set_editor_property("shading_model", unreal.MaterialShadingModel.MSM_UNLIT)
    m.set_editor_property("two_sided", True)
    # alpha = clamp((Z - sol) / hauteur) -> degrade du bas vers le haut
    wp = mel.create_material_expression(m, unreal.MaterialExpressionWorldPosition, -1200, 0)
    mask = mel.create_material_expression(m, unreal.MaterialExpressionComponentMask, -1000, 0)
    for ch, on in (("r", False), ("g", False), ("b", True), ("a", False)):
        mask.set_editor_property(ch, on)
    mel.connect_material_expressions(wp, "", mask, "")
    sub = mel.create_material_expression(m, unreal.MaterialExpressionAdd, -850, 0)
    sub.set_editor_property("const_b", -FLOOR_Z)
    mel.connect_material_expressions(mask, "", sub, "A")
    div = mel.create_material_expression(m, unreal.MaterialExpressionMultiply, -700, 0)
    div.set_editor_property("const_b", 1.0 / (RADIUS * 0.7))
    mel.connect_material_expressions(sub, "", div, "A")
    sat = mel.create_material_expression(m, unreal.MaterialExpressionSaturate, -550, 0)
    mel.connect_material_expressions(div, "", sat, "")
    a = mel.create_material_expression(m, unreal.MaterialExpressionConstant3Vector, -550, -200)
    a.set_editor_property("constant", bottom)
    b = mel.create_material_expression(m, unreal.MaterialExpressionConstant3Vector, -550, 200)
    b.set_editor_property("constant", top)
    lerp = mel.create_material_expression(m, unreal.MaterialExpressionLinearInterpolate, -300, 0)
    mel.connect_material_expressions(a, "", lerp, "A")
    mel.connect_material_expressions(b, "", lerp, "B")
    mel.connect_material_expressions(sat, "", lerp, "Alpha")
    mel.connect_material_property(lerp, "", unreal.MaterialProperty.MP_EMISSIVE_COLOR)
    mel.recompile_material(m)
    eal.save_loaded_asset(m)
    return m

try:
    mats = [sky_mat(MAT_PREFIX + n, bot, top) for (n, bot, top) in SKIES]
    L.append("materiaux ok")
    ACT = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
    for lab in list(ACT):
        if lab.startswith("ZONE_1v1P_SkyDome") or lab in ("ZONE_1v1P_SkyVault", "ZONE_1v1P_SkyFloor"):
            eas.destroy_actor(ACT.pop(lab))
            L.append("supprime " + lab)
    # le mesh est une demi-sphere coupee sur l'axe Y (ouverture sur le cote) :
    # roll +90 -> ouverture vers le bas, coque vers le haut ; echelle uniforme
    dome = eas.spawn_actor_from_class(unreal.load_class(None, DOME_CLS), unreal.Vector(CX, CY, FLOOR_Z),
                                      unreal.Rotator(roll=90.0, pitch=0.0, yaw=0.0))
    o, e = dome.get_actor_bounds(False)
    k = RADIUS / e.x
    dome.set_actor_scale3d(unreal.Vector(k, k, k))
    o, e = dome.get_actor_bounds(False)
    loc = dome.get_actor_location()
    dome.set_actor_location(unreal.Vector(CX + loc.x - o.x, CY + loc.y - o.y, FLOOR_Z - 300 + loc.z - (o.z - e.z)), False, False)
    o, e = dome.get_actor_bounds(False)
    L.append("voute centre=(%.0f,%.0f,%.0f) taille=(%.0f,%.0f,%.0f)" % (o.x, o.y, o.z, e.x, e.y, e.z))
    for c in dome.get_components_by_class(unreal.PrimitiveComponent):
        try:
            c.set_collision_profile_name("NoCollision")
            c.set_editor_property("cast_shadow", False)
        except Exception as ex:
            L.append("composant %s : %s" % (c.get_name(), ex))
        if isinstance(c, unreal.StaticMeshComponent):
            for i in range(max(1, c.get_num_materials())):
                c.set_material(i, mats[0])
    # sol noir sous la voute : cache le quadrillage blanc de la map
    floor = eas.spawn_actor_from_class(unreal.FortStaticMeshActor, unreal.Vector(CX, CY, GROUND_Z - 25))
    fc = floor.get_component_by_class(unreal.StaticMeshComponent)
    fc.set_static_mesh(eal.load_asset("/Engine/BasicShapes/Cylinder"))
    fc.set_material(0, eal.load_asset(MAT_DIR + "/M_Lobby_BlackGloss"))
    floor.set_actor_scale3d(unreal.Vector(2 * RADIUS / 100, 2 * RADIUS / 100, 0.5))
    floor.set_actor_label("ZONE_1v1P_SkyFloor")
    floor.set_folder_path("Zones/1v1/Panel")
    floor.set_editor_property("is_spatially_loaded", False)
    dome.set_actor_label("ZONE_1v1P_SkyVault")
    dome.set_folder_path("Zones/1v1/Panel")
    dome.set_editor_property("is_spatially_loaded", False)
    m = json.load(open(TOOLS + r"\build_panel_map.json"))
    m["sky_vault"] = "ZONE_1v1P_SkyVault"
    m.pop("sky_domes", None)
    json.dump(m, open(TOOLS + r"\build_panel_map.json", "w"), indent=1)
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE")
except Exception:
    L.append(traceback.format_exc())
open(TOOLS + r"\build_sky_vault_log.txt", "w").write("\n".join(L))
