# Piece Control du joueur : plus de bouton RESET. Le reset se fait a l'arrivee (cylindres) :
# chaque chrono fait exploser 7 explosifs repartis sur toute la zone (rayon ~40 m chacun)
# puis joue la sequence qui recharge DL_PieceControlBuilds. Cablage : wire_pc_reset.py
import unreal, json, traceback
TOOLS = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools"
POS = [(23300, -9000, 10700), (27500, -8700, 10700), (31500, -8700, 10700),     # salle + couloirs
       (23800, -4500, 12500), (23800, -2000, 14400),                            # montees
       (21500, -8700, 8500), (21500, -8700, 6000)]                              # puits
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
WORLD = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
L = []
try:
    ACT = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
    for lab in ("PCX_ResetButton", "PCX_ResetTitle", "PCX_ResetDevice", "PCX_ResetExplosive") + tuple("PCX_ResetExplosive%d" % i for i in range(10)):
        if lab in ACT:
            eas.destroy_actor(ACT[lab]); L.append("supprime " + lab)
    names = []
    for i, (x, y, z) in enumerate(POS):
        e = eas.duplicate_actor(ACT["TUN_Explosive0"], WORLD, unreal.Vector(0, 0, 0))
        e.set_actor_location(unreal.Vector(x, y, z), False, False)
        e.set_actor_label("PCX_ResetExplosive%d" % i)
        e.set_folder_path("Zones/PieceControlX/Reset")
        e.set_editor_property("is_spatially_loaded", False)
        names.append(e.get_actor_label())
    m = json.load(open(TOOLS + r"\build_pc_map.json"))
    m["explosives"] = names
    for k in ("button", "explosive", "reset"):
        m.pop(k, None)
    json.dump(m, open(TOOLS + r"\build_pc_map.json", "w"), indent=1)
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("explosifs : %s" % names)
    L.append("TERMINE")
except Exception:
    L.append(traceback.format_exc())
open(TOOLS + r"\pc_reset_on_finish_log.txt", "w").write("\n".join(L))
