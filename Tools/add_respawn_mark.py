# Repere de retour (prop cache en jeu par le Verse) sur le disque principal,
# a l'emplacement du point d'arrivee de la zone 1v1. Liste aussi les champs Verse du panneau.
import unreal, json, traceback
TOOLS = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools"
CLS = "/CRG_Props/SetupAssets/Blueprints/TechPrimitives/CP_L_T_Primitive_Squared_Cube_Flat.CP_L_T_Primitive_Squared_Cube_Flat_C"
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
L = []
try:
    ACT = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
    if "ZONE_1v1P_RespawnMark" in ACT:
        eas.destroy_actor(ACT.pop("ZONE_1v1P_RespawnMark"))
    arr = ACT["ZONE_1v1_Arrival"]
    p = arr.get_actor_location()
    L.append("arrivee %s (%s)" % (p, arr.get_class().get_name()))
    m = eas.spawn_actor_from_class(unreal.load_class(None, CLS), unreal.Vector(p.x, p.y, 1270.0),
                                   unreal.Rotator(0, 0, 180.0))  # yaw 180 : regarde vers le centre
    m.set_actor_scale3d(unreal.Vector(0.1, 0.1, 0.1))
    for c in m.get_components_by_class(unreal.PrimitiveComponent):
        c.set_collision_profile_name("NoCollision")
    m.set_actor_label("ZONE_1v1P_RespawnMark")
    m.set_folder_path("Zones/1v1/Panel")
    m.set_editor_property("is_spatially_loaded", False)
    mp = json.load(open(TOOLS + r"\build_panel_map.json"))
    mp["respawn"] = "ZONE_1v1P_RespawnMark"
    json.dump(mp, open(TOOLS + r"\build_panel_map.json", "w"), indent=1)
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("ok")
except Exception:
    L.append(traceback.format_exc())
open(TOOLS + r"\add_respawn_mark_log.txt", "w").write("\n".join(L))
