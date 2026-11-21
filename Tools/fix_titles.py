# Textes coupes : taille reduite + centres (retours des exercices aim + titres des tunnels)
import unreal, traceback
SIZES = {"AIM_Launch_Return_Title": 32, "AIM_Bounce_Return_Title": 32, "AIM_Circuit_Return_Title": 32,
         "TUN_FACILE_Title": 40, "TUN_MOYEN_Title": 40, "TUN_DIFFICILE_Title": 40, "TUN_IMPOSSIBLE_Title": 34}
L = []
try:
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    with unreal.ScopedEditorTransaction("Textes coupes"):
        for a in eas.get_all_level_actors():
            lab = a.get_actor_label()
            if lab in SIZES:
                a.modify()
                a.set_editor_property("TextSize", SIZES[lab])
                a.set_editor_property("TextJustification", unreal.TextJustify.CENTER)
                t = a.get_editor_property("text")
                a.set_editor_property("text", t)
                L.append("%s : %s -> taille %d centre" % (lab, t, SIZES[lab]))
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE")
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\fix_titles_log.txt", "w").write("\n".join(L))
