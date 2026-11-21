# Salle DOUBLE PUMP : retire le portail retour ; pose un teleporteur (cible du retour par emote)
# sur l'arrivee du hall aim. Le branchement "emote -> teleporter" se fait dans les details de la zone.
import unreal, json, traceback
L = []
TOOLS = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools"
try:
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    for a in eas.get_all_level_actors():
        if a.get_actor_label().startswith(("AIM_Pump_Return", "AIM_Pump_EmoteTP")):
            eas.destroy_actor(a)
    MAP = json.load(open(TOOLS + r"\build_aim_map.json"))
    if "AIM_Pump_Return_Zone" in MAP["rifts"]:
        i = MAP["rifts"].index("AIM_Pump_Return_Zone")
        del MAP["rifts"][i]; del MAP["targets"][i]
        json.dump(MAP, open(TOOLS + r"\build_aim_map.json", "w"), indent=1)
    ar = unreal.AssetRegistryHelpers.get_asset_registry()
    cls = None
    for ad in ar.get_assets_by_class(unreal.TopLevelAssetPath("/Script/Engine", "BlueprintGeneratedClass"), True):
        nm = str(ad.asset_name)
        if nm.startswith("Device_Teleporter") and nm.endswith("_C"):
            L.append("classe : %s.%s" % (ad.package_name, nm))
            if cls is None or "V2" in nm:
                cls = "%s.%s" % (ad.package_name, nm)
    arr = [a for a in eas.get_all_level_actors() if a.get_actor_label() == "ZONE_Aim_Arrival"][0].get_actor_location()
    t = eas.spawn_actor_from_class(unreal.load_class(None, cls), unreal.Vector(arr.x, arr.y + 250, 1270), unreal.Rotator(0, 0, 90))
    t.set_actor_label("AIM_Pump_EmoteTP")
    t.set_folder_path("Zones/Aim/Pump")
    t.set_editor_property("is_spatially_loaded", False)
    L.append("teleporteur pose avec %s" % cls)
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE")
except Exception:
    L.append(traceback.format_exc())
open(TOOLS + r"\pump_emote_tp_log.txt", "w").write("\n".join(L))
