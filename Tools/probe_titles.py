import unreal, traceback
L = []
try:
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    for a in sorted(eas.get_all_level_actors(), key=lambda a: a.get_actor_label()):
        lab = a.get_actor_label()
        if a.get_class().get_name() not in ("BP_Creative_Billboard_C", "Device_Billboard_V2_C"): continue
        if not (lab.startswith(("AIM_", "TUN_", "ZONE_Aim", "ZONE_Edit"))): continue
        p = a.get_actor_location(); r = a.get_actor_rotation()
        vals = []
        for pn in ("text", "TextSize", "TextJustification"):
            try: vals.append("%s=%r" % (pn, str(a.get_editor_property(pn))))
            except Exception: pass
        L.append("%s | %s (%.0f,%.0f,%.0f) yaw=%.0f sc=%.2f | %s" % (lab, a.get_class().get_name()[:10], p.x, p.y, p.z, r.yaw, a.get_actor_scale3d().x, " ".join(vals)))
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\probe_titles_log.txt", "w").write("\n".join(L))
