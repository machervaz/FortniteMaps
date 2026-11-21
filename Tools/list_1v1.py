import unreal, traceback
TOOLS = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools"
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
L = []
try:
    for a in sorted(eas.get_all_level_actors(), key=lambda x: x.get_actor_label()):
        lab = a.get_actor_label()
        p = a.get_actor_location()
        if lab.startswith("ZONE_1v1") or (-38000 < p.x < -2000 and -18000 < p.y < 18000):
            o, e = a.get_actor_bounds(False)
            L.append("%-40s %-45s loc=(%.0f,%.0f,%.0f) z=[%.0f..%.0f] r=%.0f %s" % (
                lab, a.get_class().get_name(), p.x, p.y, p.z, o.z - e.z, o.z + e.z, max(e.x, e.y), a.get_folder_path()))
except Exception:
    L.append(traceback.format_exc())
open(TOOLS + r"\list_1v1_log.txt", "w").write("\n".join(L))
