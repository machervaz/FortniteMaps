# Cale les 2 rampes 1v1 (et leurs rebords LED) sur la grille de construction :
# cases de 512 cm (x -20480..-19968, y 0..+/-512) et etages de 384 cm (surface 1536 -> 1920).
# Fait dans une transaction editeur pour que le changement parte bien dans la session.
import unreal, traceback
TOOLS = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools"
DX, DZ = -224.0, -15.0
LABELS = ("ZONE_1v1N_Ramp1", "ZONE_1v1N_Ramp-1", "ZONE_1v1N_RampEdge1", "ZONE_1v1N_RampEdge-1")
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
L = []
try:
    acts = [a for a in eas.get_all_level_actors() if a.get_actor_label() in LABELS]
    with unreal.ScopedEditorTransaction("Rampes 1v1 sur la grille"):
        for a in acts:
            a.modify()
            for c in a.get_components_by_class(unreal.SceneComponent):
                c.modify()
            p = a.get_actor_location()
            if abs(p.x - (-20000.0)) > 1:
                raise Exception("%s deja deplace (x=%.0f)" % (a.get_actor_label(), p.x))
            a.set_actor_location(unreal.Vector(p.x + DX, p.y, p.z + DZ), False, False)
            o, e = a.get_actor_bounds(False)
            L.append("%s x=[%.0f..%.0f] y=[%.0f..%.0f] z=[%.0f..%.0f]" % (a.get_actor_label(),
                     o.x - e.x, o.x + e.x, o.y - e.y, o.y + e.y, o.z - e.z, o.z + e.z))
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE")
except Exception:
    L.append(traceback.format_exc())
open(TOOLS + r"\ramps_to_grid_log.txt", "w").write("\n".join(L))
