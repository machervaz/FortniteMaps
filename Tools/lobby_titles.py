import unreal, traceback
L = []
try:
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    NEW = {"LOBBY_Portal_PieceControl_Title": ("EDIT", 44), "LOBBY_Portal_Edit_Title": ("EDIT RACE", 34)}
    with unreal.ScopedEditorTransaction("Titres portails"):
        for a in eas.get_all_level_actors():
            lab = a.get_actor_label()
            if lab in NEW:
                a.modify()
                a.set_editor_property("text", NEW[lab][0])
                a.set_editor_property("TextSize", NEW[lab][1])
                L.append("%s -> %s" % (lab, NEW[lab][0]))
    # bilan des pieces des tunnels
    dls = unreal.get_editor_subsystem(unreal.DataLayerEditorSubsystem)
    dl = unreal.load_asset("/5622d7d7-d1ca-438f-8a48-1286a48e2471/Tunnels/DL_TunnelBuilds")
    inst = [i for i in dls.get_all_data_layers() if i.get_asset() == dl][0]
    indl = set(a.get_path_name() for a in dls.get_actors_from_data_layer(inst))
    tot = 0; out = []
    for a in eas.get_all_level_actors():
        if not a.get_class().get_name().startswith("PBWA_"): continue
        p = a.get_actor_location()
        if -3500 < p.x < 3500 and -48000 < p.y < -22000:
            tot += 1
            if a.get_path_name() not in indl:
                out.append("%s (%.0f,%.0f,%.0f)" % (a.get_actor_label(), p.x, p.y, p.z))
    L.append("pieces tunnels : %d, hors reset : %d" % (tot, len(out)))
    L += out[:40]
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE")
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\lobby_titles_log.txt", "w").write("\n".join(L))
