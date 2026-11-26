import unreal
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
d = [a for a in eas.get_all_level_actors() if a.get_actor_label().startswith("ZONE_1v1_Arme")]
n = sum(1 for a in d if eas.destroy_actor(a))
eas.select_nothing()
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\del_spawners_log.txt","w").write("supprimes %d" % n)
