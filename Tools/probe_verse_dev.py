import unreal
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
L = []
for a in eas.get_all_level_actors():
    if a.get_class().get_name() == "VerseDevice_C":
        s = a.get_editor_property("Script"); p = a.get_actor_location()
        extra = ""
        try:
            extra = "label=%s" % s.get_editor_property("CourseLabel")
        except Exception:
            pass
        L.append("%s | %s | (%.0f,%.0f,%.0f) %s" % (a.get_actor_label(), s.get_class().get_name() if s else None, p.x, p.y, p.z, extra))
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\probe_verse_dev_log.txt","w").write("\n".join(sorted(L)))
