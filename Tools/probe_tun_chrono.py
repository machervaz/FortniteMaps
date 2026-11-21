import unreal, traceback
L = []
CH = {"start": "__verse_0x5CFF7AE4_StartTrigger", "finish": "__verse_0x16E5C556_FinishTrigger", "hud": "__verse_0xD5F0BE43_ResultHUD"}
try:
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    ACT = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
    for n in ("FACILE", "MOYEN", "DIFFICILE", "IMPOSSIBLE"):
        s = ACT["TUN_%s_Chrono" % n].get_editor_property("Script")
        for k, f in CH.items():
            a = s.get_editor_property(f).get_editor_property("SavedActor")
            if a:
                o, e = a.get_actor_bounds(False)
                L.append("%s %s -> %s (%s) c=(%.0f,%.0f,%.0f) e=(%.0f,%.0f,%.0f)" % (n, k, a.get_actor_label(), a.get_class().get_name(), o.x, o.y, o.z, e.x, e.y, e.z))
            else:
                L.append("%s %s -> AUCUN" % (n, k))
        h = ACT.get("TUN_%s_FinHolo" % n)
        if h:
            L.append("   holo %s" % h.get_actor_location())
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\probe_tun_chrono_log.txt", "w").write("\n".join(L))
