# Disque 1v1 : noir satine (reflet doux) au lieu du noir miroir, pour que les
# constructions posees dessus ne paraissent pas le traverser (reflet) et eviter l'eblouissement.
# Nouveau materiau M_1v1_DiscSatin (le lobby garde M_Lobby_BlackGloss).
import unreal, traceback
TOOLS = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools"
MAT_DIR = "/5622d7d7-d1ca-438f-8a48-1286a48e2471/Lobby/Materials"
NAME = "M_1v1_DiscSatin"
mel = unreal.MaterialEditingLibrary
eal = unreal.EditorAssetLibrary
L = []
try:
    path = MAT_DIR + "/" + NAME
    if eal.does_asset_exist(path):
        m = eal.load_asset(path)
        mel.delete_all_material_expressions(m)
    else:
        m = unreal.AssetToolsHelpers.get_asset_tools().create_asset(NAME, MAT_DIR, unreal.Material, unreal.MaterialFactoryNew())
    c = mel.create_material_expression(m, unreal.MaterialExpressionConstant3Vector, -400, -100)
    c.set_editor_property("constant", unreal.LinearColor(0.012, 0.012, 0.016, 1.0))
    mel.connect_material_property(c, "", unreal.MaterialProperty.MP_BASE_COLOR)
    r = mel.create_material_expression(m, unreal.MaterialExpressionConstant, -400, 100)
    r.set_editor_property("r", 0.65)
    mel.connect_material_property(r, "", unreal.MaterialProperty.MP_ROUGHNESS)
    s = mel.create_material_expression(m, unreal.MaterialExpressionConstant, -400, 200)
    s.set_editor_property("r", 0.2)
    mel.connect_material_property(s, "", unreal.MaterialProperty.MP_SPECULAR)
    mel.recompile_material(m)
    eal.save_loaded_asset(m)
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    disc = [a for a in eas.get_all_level_actors() if a.get_actor_label() == "ZONE_1v1N_Disc"][0]
    comp = disc.get_component_by_class(unreal.StaticMeshComponent)
    L.append("ancien materiau : %s" % comp.get_material(0).get_name())
    for i in range(max(1, comp.get_num_materials())):
        comp.set_material(i, m)
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE")
except Exception:
    L.append(traceback.format_exc())
open(TOOLS + r"\matte_disc_log.txt", "w").write("\n".join(L))
