import unreal
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
a = [x for x in eas.get_all_level_actors() if x.get_actor_label() == "AIM_Pump_Room"][0]
o, e = a.get_actor_bounds(False)
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\check_pump_room_log.txt", "w").write("centre=(%.0f,%.0f,%.0f) ext=(%.0f,%.0f,%.0f)" % (o.x, o.y, o.z, e.x, e.y, e.z))
