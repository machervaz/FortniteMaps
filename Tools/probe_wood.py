import unreal, traceback, collections
L = []
try:
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    dls = unreal.get_editor_subsystem(unreal.DataLayerEditorSubsystem)
    dl = unreal.load_asset("/5622d7d7-d1ca-438f-8a48-1286a48e2471/Tunnels/DL_TunnelBuilds")
    inst = [i for i in dls.get_all_data_layers() if i.get_asset() == dl][0]
    indl = set(a.get_path_name() for a in dls.get_actors_from_data_layer(inst))
    c = collections.Counter()
    zs = collections.Counter()
    for a in eas.get_all_level_actors():
        n = a.get_class().get_name()
        if not n.startswith("PBWA_"): continue
        p = a.get_actor_location()
        if -3500 < p.x < 3500 and -48000 < p.y < -21000:
            user = not a.get_actor_label().startswith("TUN_")
            c[("user" if user else "TUN", a.get_path_name() in indl)] += 1
            zs[round((p.z - 1270) / 384.0, 2)] += 1
            if p.y > -23000: L.append("hors boite (devant) : %s (%.0f,%.0f,%.0f)" % (a.get_actor_label(), p.x, p.y, p.z))
    L.append(str(c)); L.append("niveaux : " + str(sorted(zs.items())))
    L.append("dans DL total : %d" % len(indl))
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\probe_wood_log.txt", "w").write("\n".join(L))
