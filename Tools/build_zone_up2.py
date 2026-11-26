# Zone BUILD : tout le niveau de jeu monte de 2 etages (2 x 384) -> sol a 1920, toujours sur la grille.
import unreal, traceback
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
L = []
DZ = 768.0
try:
    ACT = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
    with unreal.ScopedEditorTransaction("Zone BUILD +2 etages"):
        if ACT["BUILD_Floor"].get_actor_bounds(False)[0].z < 1500:
            for lab, a in ACT.items():
                if lab.startswith("BUILD_") and lab not in ("BUILD_AirBots", "BUILD_Device"):
                    a.modify()
                    p = a.get_actor_location()
                    a.set_actor_location(unreal.Vector(p.x, p.y, p.z + DZ), False, False)
            L.append("monte de %d" % DZ)
        for lab in ("BUILD_Floor", "BUILD_Arrival", "BUILD_Ramp-1", "BUILD_Ramp1", "BUILD_ReturnSocle", "BUILD_BotSpawner", "BUILD_ResetButton"):
            o, e = ACT[lab].get_actor_bounds(False)
            L.append("%s : z %.0f..%.0f" % (lab, o.z - e.z, o.z + e.z))
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("OK")
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\build_zone_up2_log.txt", "w").write("\n".join(L))
