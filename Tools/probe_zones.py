import unreal, traceback
L = []
try:
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    for a in eas.get_all_level_actors():
        if a.get_class().get_name() != "Device_MutatorVolume_V2_C":
            continue
        lab = a.get_actor_label()
        if lab.startswith(("ZONE_", "LOBBY_", "TUN_", "AIM_", "PCX_")):
            continue
        p = a.get_actor_location()
        vals = []
        for pn in ("ZoneWidth", "ZoneDepth", "ZoneHeight", "Zone Shape"):
            try:
                vals.append("%s=%s" % (pn, a.get_editor_property(pn)))
            except Exception:
                pass
        L.append("%s loc=(%.0f,%.0f,%.0f) scale=%s rot=%s %s" % (lab, p.x, p.y, p.z, a.get_actor_scale3d(), a.get_actor_rotation(), " ".join(vals)))
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\probe_zones_log.txt", "w").write("\n".join(L))
