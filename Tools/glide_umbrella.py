# GLIDE : retire la zone de chute libre et le spawner de gardes de test ; pose le parasol
# (CP_GardenParty_Umbrella_01) qui suivra le bot (faux planeur), sans collision
import unreal, traceback
L = []
try:
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    for a in eas.get_all_level_actors():
        if a.get_actor_label() in ("AIM_Glide_Skydive", "AIM_Glide_GuardTest", "AIM_Glide_Umbrella"):
            eas.destroy_actor(a); L.append("supprime " + a.get_actor_label() if False else "supprime")
    u = eas.spawn_actor_from_class(unreal.load_class(None, "/CRP_GardenPartyHG/SetupAssets/Blueprints/CP_GardenParty_Umbrella_01.CP_GardenParty_Umbrella_01_C"),
                                   unreal.Vector(3600, 71600, 1270))
    u.set_actor_label("AIM_Glide_Umbrella"); u.set_folder_path("Zones/Aim/Glide")
    u.set_editor_property("is_spatially_loaded", False)
    for c in u.get_components_by_class(unreal.PrimitiveComponent):
        try:
            c.set_collision_profile_name("NoCollision")
        except Exception:
            pass
    o, e = u.get_actor_bounds(False); p = u.get_actor_location()
    L.append("parasol : pivot z=%.0f, bas=%.0f, haut=%.0f, largeur=%.0f" % (p.z, o.z - e.z, o.z + e.z, 2 * e.x))
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE")
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\glide_umbrella_log.txt", "w").write("\n".join(L))
