# Tous les panneaux encore alignes a gauche -> centres ; titres longs un peu plus petits
import unreal, traceback
SIZE = {"1V1 BUILDFIGHT": 44, "PIECE CONTROL": 44, "EDIT TUNNELS": 54, "TIMED RUN": 36, "SIDE-JUMPS": 36}
L = []
try:
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    with unreal.ScopedEditorTransaction("Titres centres"):
        for a in eas.get_all_level_actors():
            if a.get_class().get_name() != "BP_Creative_Billboard_C": continue
            if a.get_editor_property("TextJustification") != unreal.TextJustify.LEFT: continue
            t = str(a.get_editor_property("text"))
            a.modify()
            a.set_editor_property("TextJustification", unreal.TextJustify.CENTER)
            if t in SIZE:
                a.set_editor_property("TextSize", SIZE[t])
            a.set_editor_property("text", t)
            L.append("%s '%s' -> centre, taille %s" % (a.get_actor_label(), t, a.get_editor_property("TextSize")))
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE")
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\fix_left_titles_log.txt", "w").write("\n".join(L))
