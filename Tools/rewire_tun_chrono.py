# Rebranche les chronos des tunnels sur les zones / HUD actuels (liens vides apres reconstruction)
import unreal, traceback
L = []
CH = {"start": "__verse_0x5CFF7AE4_StartTrigger", "finish": "__verse_0x16E5C556_FinishTrigger", "hud": "__verse_0xD5F0BE43_ResultHUD"}
try:
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    ACT = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
    for n in ("FACILE", "MOYEN", "DIFFICILE", "IMPOSSIBLE"):
        s = ACT["TUN_%s_Chrono" % n].get_editor_property("Script")
        for k, suffix in (("start", "Start"), ("finish", "Finish"), ("hud", "HUD")):
            target = ACT["TUN_%s_%s" % (n, suffix)]
            s.get_editor_property(CH[k]).set_editor_property("SavedActor", target)
            a = s.get_editor_property(CH[k]).get_editor_property("SavedActor")
            o, e = a.get_actor_bounds(False)
            L.append("%s %s -> %s c=(%.0f,%.0f,%.0f)" % (n, k, a.get_actor_label(), o.x, o.y, o.z))
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE")
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\rewire_tun_chrono_log.txt", "w").write("\n".join(L))
