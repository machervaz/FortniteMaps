# Relie les tableaux TOP 5 aux chronos des tunnels (+ descend un peu les tableaux sous le liseré du toit)
import unreal, json, traceback
TOOLS = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools"
F = "__verse_0xD0A1761B_Leaderboard"
W = "/CreativeCoreDevices/_Verse.billboard_device"
DZ = -40.0
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
L = []
try:
    boards = json.load(open(TOOLS + r"\edit_boards_map.json"))
    ACT = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
    with unreal.ScopedEditorTransaction("Tableaux TOP 5"):
        for labs in boards.values():
            for l in labs:
                a = ACT[l]
                a.modify()
                p = a.get_actor_location()
                a.set_actor_location(unreal.Vector(p.x, p.y, p.z + DZ), False, False)
    for name, labs in boards.items():
        s = ACT["TUN_%s_Chrono" % name].get_editor_property("Script")
        objs = []
        for l in labs:
            o = unreal.new_object(unreal.load_class(None, W), s)
            o.set_editor_property("SavedActor", ACT[l])
            objs.append(o)
        s.set_editor_property(F, objs)
        L.append("%s : %d lignes" % (name, len(objs)))
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE")
except Exception:
    L.append(traceback.format_exc())
open(TOOLS + r"\wire_edit_boards_log.txt", "w").write("\n".join(L))
