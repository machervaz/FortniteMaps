import unreal
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
c = unreal.load_class(None, "/Game/Creative/Sets/PropSets/Primitives/Rounds/Props/CP_Primitive_Sphere_Hollow_Half.CP_Primitive_Sphere_Hollow_Half_C")
a = eas.spawn_actor_from_class(c, unreal.Vector(0, 0, 60000))
o, e = a.get_actor_bounds(False)
L = ["offset=(%.0f,%.0f,%.0f) ext=(%.0f,%.0f,%.0f)" % (o.x, o.y, o.z - 60000, e.x, e.y, e.z)]
v = [x for x in eas.get_all_level_actors() if x.get_actor_label() == "ZONE_1v1P_SkyVault"][0]
r = v.get_actor_rotation(); s = v.get_actor_scale3d()
L.append("voute rot=%s scale=%s" % (r, s))
eas.destroy_actor(a)
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\probe_dome_out.txt", "w").write("\n".join(L))
