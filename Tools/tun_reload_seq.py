# Recree la sequence de rechargement du Data Layer des tunnels + son Cinematic Sequence Device
import unreal, traceback
TOOLS = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools"
TUN_DIR = "/5622d7d7-d1ca-438f-8a48-1286a48e2471/Tunnels"
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
eal = unreal.EditorAssetLibrary
tools = unreal.AssetToolsHelpers.get_asset_tools()
L = []
try:
    dl = eal.load_asset(TUN_DIR + "/DL_TunnelBuilds")
    name = "LS_TunnelReload2"
    path = TUN_DIR + "/" + name
    ls = eal.load_asset(path) if eal.does_asset_exist(path) else tools.create_asset(name, TUN_DIR, unreal.LevelSequence, unreal.LevelSequenceFactoryNew())
    if not ls.get_tracks():
        sec = ls.add_track(unreal.MovieSceneDataLayerTrack).add_section()
        sec.set_range(0, 15)
        for prop, val in (("data_layer_assets", [dl]), ("desired_state", unreal.DataLayerRuntimeState.UNLOADED),
                          ("preroll_state", unreal.DataLayerRuntimeState.UNLOADED)):
            sec.set_editor_property(prop, val)
        ls.set_playback_start(0)
        ls.set_playback_end(30)
    eal.save_loaded_asset(ls)
    ACT = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
    d = ACT.get("TUN_ReloadSequence")
    if d is None:
        d = eas.spawn_actor_from_class(unreal.load_class(None, "/CRD_CinematicSequence/Device_CinematicSequence.Device_CinematicSequence_C"),
                                       unreal.Vector(700, -22300, 870))
        d.set_actor_label("TUN_ReloadSequence")
        d.set_folder_path("Zones/Edit/Tunnels/Reset")
    d.set_editor_property("is_spatially_loaded", False)
    d.set_editor_property("Sequence", ls)
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("ok : %s" % ls)
except Exception:
    L.append(traceback.format_exc())
open(TOOLS + r"\tun_reload_seq_log.txt", "w").write("\n".join(L))
