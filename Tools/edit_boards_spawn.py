# Zone Edit :
#  - tableau TOP 5 au-dessus de chaque tunnel (6 billboards V2 : titre + 5 lignes),
#    remplis par le chrono du tunnel (champ Leaderboard)
#  - arrivee depuis le lobby + cylindre RETOUR LOBBY rapproches des tunnels
import unreal, json, traceback
TOOLS = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools"
BB = "/CreativeCoreDevices/Device_Billboard_V2.Device_Billboard_V2_C"
FLOOR = 1270.0
TUN = [("FACILE", -1536.0), ("MOYEN", -512.0), ("DIFFICILE", 512.0), ("IMPOSSIBLE", 1536.0)]
ROWS = [2110.0, 2068.0, 2030.0, 1992.0, 1954.0, 1916.0]   # v3 : plus bas     # centre du texte (titre puis lignes 1..5)
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
L = []

def touch(a):
    a.modify()
    for c in a.get_components_by_class(unreal.SceneComponent):
        c.modify()

try:
    ACT = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
    for lab, a in list(ACT.items()):
        if lab.startswith("TUN_Board_"):
            eas.destroy_actor(a)
    boards = {}
    with unreal.ScopedEditorTransaction("Zone Edit : tableaux + arrivee"):
        for name, x in TUN:
            labs = []
            for i, zc in enumerate(ROWS):
                b = eas.spawn_actor_from_class(unreal.load_class(None, BB), unreal.Vector(x, -23241, zc - 57),
                                               unreal.Rotator(roll=0, pitch=0, yaw=180.0))
                for pn, v in (("text", "TOP 5" if i == 0 else "%d.  ---" % i), ("TextSize", 26 if i == 0 else 22),
                              ("TextJustification", unreal.TextJustify.CENTER),
                              ("TextColor", unreal.LinearColor(1.0, 0.85, 0.2, 1) if i == 0 else unreal.LinearColor(1, 1, 1, 1))):
                    try:
                        b.set_editor_property(pn, v)
                    except Exception as ex:
                        L.append("%s : %s" % (pn, ex))
                for c in b.get_components_by_class(unreal.PrimitiveComponent):
                    try:
                        c.set_collision_profile_name("NoCollision")
                    except Exception:
                        pass
                b.set_actor_label("TUN_Board_%s_%d" % (name, i))
                b.set_folder_path("Zones/Edit/Tunnels/Leaderboards")
                b.set_editor_property("is_spatially_loaded", False)
                labs.append(b.get_actor_label())
            boards[name] = labs
        # arrivee depuis le lobby : juste devant les tunnels, regard vers eux
        arr = ACT["ZONE_Edit_Arrival"]
        touch(arr)
        arr.set_actor_location(unreal.Vector(0, -22150, FLOOR), False, False)
        arr.set_actor_rotation(unreal.Rotator(roll=0, pitch=0, yaw=-90.0), False)
        # cylindre RETOUR LOBBY a cote
        socle = ACT["ZONE_Edit_ReturnSocle"].get_actor_location()
        d = unreal.Vector(1600 - socle.x, -21900 - socle.y, 0)
        for lab in ("ZONE_Edit_ReturnSocle", "ZONE_Edit_ReturnHolo", "ZONE_Edit_ReturnZone", "ZONE_Edit_ReturnTitle"):
            a = ACT[lab]
            touch(a)
            p = a.get_actor_location()
            a.set_actor_location(unreal.Vector(p.x + d.x, p.y + d.y, p.z), False, False)
    json.dump(boards, open(TOOLS + r"\edit_boards_map.json", "w"), indent=1)
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE : %d tableaux" % len(boards))
except Exception:
    L.append(traceback.format_exc())
open(TOOLS + r"\edit_boards_spawn_log.txt", "w").write("\n".join(L))
