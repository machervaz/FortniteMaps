import unreal
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
L = []
for a in eas.get_all_level_actors():
    lab = a.get_actor_label()
    if "Platform" in lab or "_Floor_" in lab:
        o, e = a.get_actor_bounds(False)
        L.append("%s | z %.0f..%.0f | y %.0f..%.0f | x %.0f..%.0f | hidden=%s | folder=%s" % (lab, o.z-e.z, o.z+e.z, o.y-e.y, o.y+e.y, o.x-e.x, o.x+e.x, a.is_hidden_ed(), a.get_folder_path()))
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\probe_plat_log.txt","w").write("\n".join(L) or "rien")
