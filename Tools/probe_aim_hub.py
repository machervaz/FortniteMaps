import unreal, traceback
L = []
try:
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    for a in sorted(eas.get_all_level_actors(), key=lambda a: a.get_actor_label()):
        lab = a.get_actor_label()
        p = a.get_actor_location()
        if lab.startswith(("ZONE_Aim", "AIM_Hub", "AIM_Bounce_Wall", "AIM_Bounce_Roof", "AIM_Bounce_TopLed", "AIM_Bounce_Light", "AIM_Launch_Wall", "AIM_Launch_Roof")) or (-6000 < p.x < 6000 and 17000 < p.y < 25000 and lab and not lab.startswith("AIM_Launch")):
            o, e = a.get_actor_bounds(False)
            L.append("%s | %s | c=(%.0f,%.0f,%.0f) ext=(%.0f,%.0f,%.0f) sc=%s" % (lab, a.get_class().get_name(), o.x, o.y, o.z, e.x, e.y, e.z, a.get_actor_scale3d()))
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\probe_aim_hub_log.txt", "w").write("\n".join(L))
