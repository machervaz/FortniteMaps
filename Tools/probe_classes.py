import unreal, traceback
L = []
try:
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    for a in eas.get_all_level_actors():
        n = a.get_class().get_name()
        if "Class" in n or "TeamSettings" in n:
            L.append("%s | %s | %s" % (a.get_actor_label(), n, a.get_actor_location()))
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\probe_classes_log.txt", "w").write("\n".join(L))
