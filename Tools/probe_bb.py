import unreal, traceback
L = []
try:
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    b = [a for a in eas.get_all_level_actors() if a.get_actor_label() == "TUN_Board_FACILE_1"][0]
    for c in [b.get_class()] + [x.get_class() for x in b.get_components_by_class(unreal.ActorComponent)]:
        L.append("== " + c.get_name())
    for p in sorted(set(dir(b))):
        if any(k in p.lower() for k in ("wrap", "width", "size", "text", "scale", "auto")):
            L.append(p)
    for pn in ("TextSize", "text", "WrapText", "bWrapText", "AutoWrapText", "TextWidth", "MaxWidth"):
        try:
            L.append("%s = %s" % (pn, b.get_editor_property(pn)))
        except Exception as ex:
            L.append("%s : -" % pn)
    # proprietes reflechies
    cls = b.get_class()
    import re
    L.append(str([p for p in unreal.SystemLibrary.get_class_display_name(cls).split()]))
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\probe_bb_log.txt", "w").write("\n".join(L))
