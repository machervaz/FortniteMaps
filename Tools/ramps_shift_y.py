# Grille de construction : cases centrees sur les multiples de 512 (limites a 256 + 512k) en X ET en Y.
# On decale les 2 rampes 1v1 et leurs rebords de +256 en Y (V colle, bas du V a y=256).
import unreal, traceback
TOOLS = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools"
DY = 256.0
LABELS = ("ZONE_1v1N_Ramp1", "ZONE_1v1N_Ramp-1", "ZONE_1v1N_RampEdge1", "ZONE_1v1N_RampEdge-1")
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
L = []
try:
    acts = [a for a in eas.get_all_level_actors() if a.get_actor_label() in LABELS]
    with unreal.ScopedEditorTransaction("Rampes 1v1 demi-case Y"):
        for a in acts:
            a.modify()
            for c in a.get_components_by_class(unreal.SceneComponent):
                c.modify()
            p = a.get_actor_location()
            if abs(p.x - (-19968.0)) > 1:
                raise Exception("%s inattendu (x=%.0f)" % (a.get_actor_label(), p.x))
            a.set_actor_location(unreal.Vector(p.x, p.y + DY, p.z), False, False)
            o, e = a.get_actor_bounds(False)
            L.append("%s y=[%.0f..%.0f]" % (a.get_actor_label(), o.y - e.y, o.y + e.y))
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE")
except Exception:
    L.append(traceback.format_exc())
open(TOOLS + r"\ramps_shift_y_log.txt", "w").write("\n".join(L))
