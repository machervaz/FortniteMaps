# Remonte les fleches < > du panneau 1v1 de 15 cm (alignees avec "100%" et le centre des carres)
import unreal, traceback
TOOLS = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools"
DZ = 15.0
LABELS = ("ZONE_1v1P_TxtDown", "ZONE_1v1P_TxtUp")
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
L = []
try:
    with unreal.ScopedEditorTransaction("Fleches panneau 1v1"):
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
open(TOOLS + r"\arrows_up_log.txt", "w").write("\n".join(L))
