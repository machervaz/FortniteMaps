import unreal
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
L = []
for a in eas.get_all_level_actors():
    if a.get_actor_label() in ("AIM_Launch_Bot", "AIM_Bounce_Bot", "AIM_Circuit_Bot"):
        o, e = a.get_actor_bounds(False)
        L.append("%s scale=%s bounds e=%s" % (a.get_actor_label(), a.get_actor_scale3d(), e))
        for c in a.get_components_by_class(unreal.StaticMeshComponent):
            L.append("   %s mesh=%s rel_scale=%s" % (c.get_name(), c.static_mesh.get_name() if c.static_mesh else None, c.get_editor_property("relative_scale3d")))
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\bot_info_log.txt", "w").write("\n".join(L))
