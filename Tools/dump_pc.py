# Exporte les pieces de la zone Piece Control du joueur (x 20000..34000, y -12000..-1000)
import unreal, traceback
TOOLS = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools"
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
L = []
try:
    for a in eas.get_all_level_actors():
        p = a.get_actor_location()
        if 20000 < p.x < 34000 and -12500 < p.y < -500 and not a.get_actor_label().startswith(("ZONE_", "LOBBY_", "TUN_", "AIM_")):
            o, e = a.get_actor_bounds(False)
            L.append("%s;%s;%.0f;%.0f;%.0f;%.0f;%.0f;%.0f;%.0f" % (a.get_class().get_name(), a.get_actor_label(), p.x, p.y, p.z, o.z - e.z, o.z + e.z, e.x, e.y))
except Exception:
    L.append(traceback.format_exc())
open(TOOLS + r"\dump_pc.csv", "w").write("\n".join(L))
