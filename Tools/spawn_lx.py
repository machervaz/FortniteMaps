import unreal, traceback
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
L = []
try:
    o = unreal.load_object(None, "/5622d7d7-d1ca-438f-8a48-1286a48e2471/_Verse.lobby_extras")
    d = eas.spawn_actor_from_object(o, unreal.Vector(0, -600, 870))
    L.append("spawn -> %s" % d)
    if d:
        d.set_actor_label("LOBBY_Extras"); d.set_folder_path("Lobby/Extras")
        eas.set_selected_level_actors([d])
        L.append("label %s class %s" % (d.get_actor_label(), d.get_class().get_name()))
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\spawn_lx_log.txt","w").write("\n".join(L))
