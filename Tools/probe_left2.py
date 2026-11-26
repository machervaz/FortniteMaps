import unreal
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
L = []
for a in eas.get_all_level_actors():
    if a.get_class().get_name().startswith("PBWA_") and -3500 < a.get_actor_location().x < 3500 and -48000 < a.get_actor_location().y < -22000:
        L.append("%s | %s | level=%s | pkg=%s" % (a.get_actor_label(), a.get_path_name(), a.get_level().get_path_name() if a.get_level() else None, a.get_outermost().get_name()))
        if len(L) >= 6: break
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\probe_left2_log.txt", "w").write("\n".join(L))
