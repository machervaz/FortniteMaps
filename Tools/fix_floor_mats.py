# Sol autour de l'arene : materiaux NON eclaires (pas de reflet miroir qui eblouit),
# couleur = couleur d'horizon du ciel assombrie. Modifie les 4 M_SkyFloor_* sur place.
import unreal, traceback
TOOLS = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools"
MAT_DIR = "/5622d7d7-d1ca-438f-8a48-1286a48e2471/Lobby/Materials"
K = 1.0    # couleur EXACTE du bas du ciel (le degrade de la voute vaut sa couleur basse au niveau du sol)
SKY_BOTTOM = {"Violet": (0.85, 0.45, 1.0), "Jour": (0.85, 0.93, 1.0), "Nuit": (0.04, 0.04, 0.12), "Rose": (1.0, 0.65, 0.4)}
FLOOR = {n: (r * K, g * K, b * K) for n, (r, g, b) in SKY_BOTTOM.items()}
mel = unreal.MaterialEditingLibrary
eal = unreal.EditorAssetLibrary
L = []
try:
    for n, (r, g, b) in FLOOR.items():
        m = eal.load_asset(MAT_DIR + "/M_SkyFloor_" + n)
        mel.delete_all_material_expressions(m)
        m.set_editor_property("shading_model", unreal.MaterialShadingModel.MSM_UNLIT)
        c = mel.create_material_expression(m, unreal.MaterialExpressionConstant3Vector, -400, 0)
        c.set_editor_property("constant", unreal.LinearColor(r, g, b, 1.0))
        mel.connect_material_property(c, "", unreal.MaterialProperty.MP_EMISSIVE_COLOR)
        mel.recompile_material(m)
        eal.save_loaded_asset(m)
        L.append("%s ok %s" % (n, (r, g, b)))
except Exception:
    L.append(traceback.format_exc())
open(TOOLS + r"\fix_floor_mats_log.txt", "w").write("\n".join(L))
