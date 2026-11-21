# Descend les 4 textes du panneau 1v1 de 25 cm (le texte est un peu au-dessus du centre du widget)
import unreal, traceback
TOOLS = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools"
DZ = -25.0
LABELS = ("ZONE_1v1P_TxtReset", "ZONE_1v1P_TxtDown", "ZONE_1v1P_TxtUp", "ZONE_1v1P_SpeedDisplay")
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
L = []
try:
    with unreal.ScopedEditorTransaction("Textes panneau 1v1"):
        for a in eas.get_all_level_actors():
            if a.get_actor_label() in LABELS:
                a.modify()
                for c in a.get_components_by_class(unreal.SceneComponent):
                    c.modify()
                p = a.get_actor_location()
                a.set_actor_location(unreal.Vector(p.x, p.y, p.z + DZ), False, False)
                L.append("%s z=%.0f" % (a.get_actor_label(), p.z + DZ))
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE")
except Exception:
    L.append(traceback.format_exc())
open(TOOLS + r"\texts_down_log.txt", "w").write("\n".join(L))
