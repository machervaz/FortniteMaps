# 3 explosifs pour le RESET (utilises a tour de role) + pad d'arrivee tourne
# vers le panneau (on arrive face aux formes).
import unreal, json, traceback
TOOLS = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools"
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
L = []
try:
    ACT = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
    src = ACT["ZONE_1v1P_ResetExplosive"]
    names = ["ZONE_1v1P_ResetExplosive"]
    for i in (2, 3):
        lab = "ZONE_1v1P_ResetExplosive%d" % i
        if lab not in ACT:
            d = eas.duplicate_actor(src, world, unreal.Vector(0, 0, 0))
            d.set_actor_location(src.get_actor_location(), False, False)
            d.set_actor_label(lab)
            d.set_folder_path(src.get_folder_path())
            d.set_editor_property("is_spatially_loaded", False)
        names.append(lab)
    m = json.load(open(TOOLS + r"\build_panel_map.json"))
    m["explosives"] = names
    json.dump(m, open(TOOLS + r"\build_panel_map.json", "w"), indent=1)
    arr = ACT["ZONE_1v1_Arrival"]
    arr.set_actor_rotation(unreal.Rotator(roll=0, pitch=0, yaw=180), False)
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("ok %s" % names)
except Exception:
    L.append(traceback.format_exc())
open(TOOLS + r"\panel_extras_log.txt", "w").write("\n".join(L))
