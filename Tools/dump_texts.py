import unreal, traceback
L = []
try:
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    for a in eas.get_all_level_actors():
        n = a.get_class().get_name()
        if "Billboard" in n or "HUDMessage" in n:
            vals = []
            for pn in ("text", "Text", "Message", "message"):
                try:
                    vals.append("%s=%r" % (pn, str(a.get_editor_property(pn))))
                    break
                except Exception:
                    pass
            L.append("%s | %s | %s" % (a.get_actor_label(), n, " ".join(vals)))
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\dump_texts_log.txt", "w", encoding="utf-8").write("\n".join(L))
