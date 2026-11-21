# Zone Piece Control du joueur (en l'air) : quand on edite une piece, Fortnite recalcule
# la structure et tout s'effondre (rien ne touche le sol). On force le support structurel
# de toutes les pieces de la zone. Transaction -> envoye a la session.
import unreal, traceback
TOOLS = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools"
BOX = (20000, 34000, -12500, -500)
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
L = []
try:
    n = ok = 0
    with unreal.ScopedEditorTransaction("Piece Control : support force"):
        for a in eas.get_all_level_actors():
            p = a.get_actor_location()
            if not (BOX[0] < p.x < BOX[1] and BOX[2] < p.y < BOX[3]):
                continue
            if not isinstance(a, unreal.BuildingActor):
                continue
            n += 1
            a.modify()
            try:
                a.set_editor_property("forcibly_structurally_supported", True)
                ok += 1
            except Exception as ex:
                if n < 3:
                    L.append("%s : %s" % (a.get_actor_label(), ex))
    L.append("pieces : %d, support force : %d" % (n, ok))
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE")
except Exception:
    L.append(traceback.format_exc())
open(TOOLS + r"\pc_force_support_log.txt", "w").write("\n".join(L))
