# Panneaux "BACK TO LOBBY" (et autres textes longs) : texte plus petit + centre
import unreal, traceback
L = []
try:
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    with unreal.ScopedEditorTransaction("Textes retour lobby"):
        for a in eas.get_all_level_actors():
            if a.get_class().get_name() != "BP_Creative_Billboard_C": continue
            t = str(a.get_editor_property("text"))
            size = a.get_editor_property("TextSize")
            just = a.get_editor_property("TextJustification")
            L.append("vu : %s '%s' taille %s %s" % (a.get_actor_label(), t, size, just))
            if "LOBBY" in t.upper() or ("BACK" in t.upper() and size > 32):
                a.modify()
                a.set_editor_property("TextSize", 30)
                a.set_editor_property("TextJustification", unreal.TextJustify.CENTER)
                a.set_editor_property("text", t)
                L.append("   -> taille 30 centre")
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE")
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\fix_lobby_titles_log.txt", "w").write("\n".join(L))
