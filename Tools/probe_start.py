import unreal, traceback
L = []
try:
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    ACT = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
    for n in ("FACILE", "MOYEN", "DIFFICILE", "IMPOSSIBLE"):
        s = ACT["TUN_%s_Chrono" % n].get_editor_property("Script")
        st = s.get_editor_property("__verse_0x5CFF7AE4_StartTrigger").get_editor_property("SavedActor")
        L.append("%s chrono start -> %s" % (n, st.get_actor_label() if st else None))
        z = ACT.get("TUN_%s_Start" % n)
        if z:
            o, e = z.get_actor_bounds(False)
            L.append("  zone c=(%.0f,%.0f,%.0f) ext=(%.0f,%.0f,%.0f)" % (o.x, o.y, o.z, e.x, e.y, e.z))
    L.append("--- acteurs pres des entrees")
    for a in eas.get_all_level_actors():
        p = a.get_actor_location()
        if -2000 < p.x < 2000 and -23700 < p.y < -22600 and 1000 < p.z < 2400:
            L.append("%s | %s (%.0f,%.0f,%.0f)" % (a.get_actor_label(), a.get_class().get_name(), p.x, p.y, p.z))
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\probe_start_log.txt", "w").write("\n".join(L))
