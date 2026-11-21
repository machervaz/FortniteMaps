# Copie les reglages de TUN_Explosive0 (invisible, 0 degat joueurs, rayon 40, sans effets)
# sur TUN_Explosive1..N en les remplacant par des duplicatas.
import unreal, traceback
OUT = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\clone_explosives_log.txt"
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
L = []
try:
    ACT = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
    src = ACT["TUN_Explosive0"]
    world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
    for i in range(1, 20):
        lab = "TUN_Explosive%d" % i
        old = ACT.get(lab)
        if not old:
            break
        loc = old.get_actor_location()
        eas.destroy_actor(old)
        dup = eas.duplicate_actor(src, world, unreal.Vector(0, 0, 0))
        dup.set_actor_location(loc, False, False)
        dup.set_actor_label(lab)
        dup.set_folder_path(src.get_folder_path())
        L.append("clone " + lab)
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
except Exception:
    L.append(traceback.format_exc())
open(OUT, "w").write("\n".join(L))
