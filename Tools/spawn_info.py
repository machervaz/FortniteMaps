import unreal
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
L = []
for a in eas.get_all_level_actors():
    n = a.get_class().get_name()
    if "Spawn" in n or a.get_actor_label() in ("LOBBY_LobbyPoint", "LOBBY_PlayerSpawner"):
        L.append("%s %s loc=%s rot=%s" % (a.get_actor_label(), n, a.get_actor_location(), a.get_actor_rotation()))
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\spawn_info_log.txt", "w").write("\n".join(L))
