# Panneau 1v1 : "100%" en noir (invisible en clair sur le tableau blanc), fleches < > remontees de 15 cm
import unreal, traceback
TOOLS = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools"
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
L = []
try:
    ACT = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
    with unreal.ScopedEditorTransaction("Textes panneau 1v1 (2)"):
        for lab in ("ZONE_1v1P_TxtDown", "ZONE_1v1P_TxtUp", "ZONE_1v1P_SpeedDisplay"):
            a = ACT[lab]
            a.modify()
            for c in a.get_components_by_class(unreal.SceneComponent):
                c.modify()
        for lab in ("ZONE_1v1P_TxtDown", "ZONE_1v1P_TxtUp"):
            a = ACT[lab]
            p = a.get_actor_location()
            a.set_actor_location(unreal.Vector(p.x, p.y, p.z + 15), False, False)
        d = ACT["ZONE_1v1P_SpeedDisplay"]
        for n in ("TextColor", "Text Color", "Color"):
            try:
                L.append("%s avant = %s" % (n, d.get_editor_property(n)))
                d.set_editor_property(n, unreal.LinearColor(0.02, 0.02, 0.03, 1.0))
                L.append("%s -> noir" % n)
                break
            except Exception as ex:
                L.append("%s : %s" % (n, ex))
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE")
except Exception:
    L.append(traceback.format_exc())
open(TOOLS + r"\texts_fix2_log.txt", "w").write("\n".join(L))
