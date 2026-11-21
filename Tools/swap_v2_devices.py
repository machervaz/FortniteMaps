# Remplace les anciens boutons / triggers (BP_Creative_*) par les versions V2,
# seules acceptees par Verse (button_device / trigger_device). Garde label,
# dossier et position. Relancer ensuite wire_manager.py, wire_chrono.py, wire_tunnels.py
import unreal, traceback
OUT = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\swap_v2_log.txt"
SWAP = {
    "BP_Creative_Button_C": "/CreativeCoreDevices/Device_Button_V2.Device_Button_V2_C",
    "BP_Creative_Trigger_C": "/CreativeCoreDevices/Device_Trigger_V2.Device_Trigger_V2_C",
}
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
L = []
try:
    cls = {k: unreal.load_class(None, v) for k, v in SWAP.items()}
    for a in list(eas.get_all_level_actors()):
        cn = a.get_class().get_name()
        if cn not in SWAP:
            continue
        lab, folder = a.get_actor_label(), a.get_folder_path()
        loc, rot = a.get_actor_location(), a.get_actor_rotation()
        eas.destroy_actor(a)
        b = eas.spawn_actor_from_class(cls[cn], loc, rot)
        b.set_actor_label(lab)
        b.set_folder_path(folder)
        L.append("remplace " + lab)
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
except Exception:
    L.append(traceback.format_exc())
open(OUT, "w", encoding="utf-8").write("\n".join(L))
