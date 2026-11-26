import unreal
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
def cnt(box, dlname):
    tot = ok = 0
    for a in eas.get_all_level_actors():
        p = a.get_actor_location()
        if a.get_class().get_name().startswith("PBWA_") and box[0] < p.x < box[1] and box[2] < p.y < box[3] and p.z > -10000:
            tot += 1
            try: names = [d.get_name() for d in a.get_editor_property("data_layer_assets") if d]
            except Exception as e: names = [str(e)]
            if dlname in names: ok += 1
    return "%s : %d/%d dans le reset" % (dlname, ok, tot)
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\probe_dl_log.txt","w").write(
    cnt((-3200, 3200, -47700, -16000), "DL_TunnelBuilds") + "\n" + cnt((20000, 34000, -12500, -500), "DL_PieceControlBuilds"))
