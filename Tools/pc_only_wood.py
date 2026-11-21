# Reset Piece Control : seul le BOIS doit casser. Briques, dalles de sol et escaliers Pueblo :
# invulnerables + retires du Data Layer (sinon ils disparaissent un instant au rechargement).
import unreal, traceback
TOOLS = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools"
BOX = (20000, 34000, -12500, -500)
SOLID = ("BrickSimple", "SM_FORT_Floors", "Pueblo")
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
dls = unreal.get_editor_subsystem(unreal.DataLayerEditorSubsystem)
L = []
try:
    dl = unreal.load_asset("/5622d7d7-d1ca-438f-8a48-1286a48e2471/Lobby/PieceControl/DL_PieceControlBuilds")
    inst = [i for i in dls.get_all_data_layers() if i.get_asset() == dl][0]
    solid, wood = [], 0
    with unreal.ScopedEditorTransaction("Piece Control : seul le bois casse"):
        for a in eas.get_all_level_actors():
            p = a.get_actor_location()
            if not (BOX[0] < p.x < BOX[1] and BOX[2] < p.y < BOX[3]):
                continue
            n = a.get_class().get_name()
            if n.startswith(SOLID):
                a.modify()
                a.set_editor_property("bIsInvulnerable", True)
                solid.append(a)
            elif n.startswith("PBWA_"):
                wood += 1
        L.append("retires du data layer : %s" % dls.remove_actors_from_data_layer(solid, inst))
    L.append("pieces solides invulnerables : %d, pieces en bois (restent dans le reset) : %d" % (len(solid), wood))
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE")
except Exception:
    L.append(traceback.format_exc())
open(TOOLS + r"\pc_only_wood_log.txt", "w").write("\n".join(L))
