# Zone Aim :
#  - hub (lobby aim, sol 6000 x 6000 en (0,20000)) : 4 murs + toit + liseres LED + lumieres
#  - arene REBOND : murs/toit remontes (2200 -> 4200 de haut) pour que les bots montent plus haut
import unreal, traceback
TOOLS = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools"
MAT_DIR = "/5622d7d7-d1ca-438f-8a48-1286a48e2471/Lobby/Materials"
FLOOR = 1270.0
CX, CY, SIZE, H, T = 0.0, 20000.0, 6000.0, 1300.0, 60.0
BOUNCE_DZ = 2000.0
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
eal = unreal.EditorAssetLibrary
CUBE = eal.load_asset("/Engine/BasicShapes/Cube")
L = []
V = lambda x, y, z: unreal.Vector(float(x), float(y), float(z))

def box(label, m, c, s, collision=True):
    a = eas.spawn_actor_from_class(unreal.FortStaticMeshActor, c)
    comp = a.get_component_by_class(unreal.StaticMeshComponent)
    comp.set_static_mesh(CUBE); comp.set_material(0, m)
    a.set_actor_scale3d(V(s.x / 100, s.y / 100, s.z / 100))
    if not collision:
        comp.set_collision_profile_name("NoCollision")
        comp.set_editor_property("cast_shadow", False)
    a.set_actor_label("ZONE_AimHub_" + label)
    a.set_folder_path("Zones/Aim/Hub/Enclosure")
    a.set_editor_property("is_spatially_loaded", False)
    return a

def touch(a):
    a.modify()
    for c in a.get_components_by_class(unreal.SceneComponent):
        c.modify()

try:
    for a in eas.get_all_level_actors():
        if a.get_actor_label().startswith("ZONE_AimHub_"):
            eas.destroy_actor(a)
    wall = eal.load_asset(MAT_DIR + "/M_Aim_ArenaWall")
    led = eal.load_asset(MAT_DIR + "/M_Lobby_LedDeepBlue")
    h = SIZE / 2.0
    for nm, c, s in (("WallN", V(CX, CY + h + T / 2, FLOOR + H / 2), V(SIZE + 2 * T, T, H)),
                     ("WallS", V(CX, CY - h - T / 2, FLOOR + H / 2), V(SIZE + 2 * T, T, H)),
                     ("WallE", V(CX + h + T / 2, CY, FLOOR + H / 2), V(T, SIZE, H)),
                     ("WallW", V(CX - h - T / 2, CY, FLOOR + H / 2), V(T, SIZE, H))):
        box(nm, wall, c, s)
    box("Roof", wall, V(CX, CY, FLOOR + H + T / 2), V(SIZE + 2 * T, SIZE + 2 * T, T))
    for nm, c, s in (("LedN", V(CX, CY + h - 6, FLOOR + H - 12), V(SIZE, 12, 24)), ("LedS", V(CX, CY - h + 6, FLOOR + H - 12), V(SIZE, 12, 24)),
                     ("LedE", V(CX + h - 6, CY, FLOOR + H - 12), V(12, SIZE, 24)), ("LedW", V(CX - h + 6, CY, FLOOR + H - 12), V(12, SIZE, 24))):
        box(nm, led, c, s, False)
    k = 0
    for fx in (-0.3, 0.3):
        for fy in (-0.3, 0.3):
            pl = eas.spawn_actor_from_class(unreal.PointLight, V(CX + fx * SIZE, CY + fy * SIZE, FLOOR + H - 200))
            lc = pl.get_component_by_class(unreal.PointLightComponent)
            lc.set_light_color(unreal.LinearColor(0.85, 0.9, 1.0, 1)); lc.set_intensity(50.0); lc.set_attenuation_radius(SIZE * 0.8)
            lc.set_editor_property("cast_shadows", False)
            pl.set_actor_label("ZONE_AimHub_Light%d" % k); pl.set_folder_path("Zones/Aim/Hub/Enclosure")
            pl.set_editor_property("is_spatially_loaded", False)
            k += 1
    L.append("hub : murs + toit poses")
    # arene REBOND plus haute
    ACT = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
    with unreal.ScopedEditorTransaction("Rebond plus haut"):
        for s in "NSEW":
            a = ACT["AIM_Bounce_Wall" + s]
            touch(a)
            sc = a.get_actor_scale3d()
            hh = sc.z * 100 + BOUNCE_DZ
            p = a.get_actor_location()
            a.set_actor_location(V(p.x, p.y, FLOOR + hh / 2), False, False)
            a.set_actor_scale3d(V(sc.x, sc.y, hh / 100))
        for lab in ["AIM_Bounce_Roof"] + ["AIM_Bounce_TopLed" + s for s in "NSEW"] + ["AIM_Bounce_Light%d" % i for i in range(4)]:
            a = ACT[lab]
            touch(a)
            p = a.get_actor_location()
            a.set_actor_location(V(p.x, p.y, p.z + BOUNCE_DZ), False, False)
    L.append("rebond : murs/toit +%d" % BOUNCE_DZ)
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE")
except Exception:
    L.append(traceback.format_exc())
open(TOOLS + r"\aim_hub_walls_log.txt", "w").write("\n".join(L))
