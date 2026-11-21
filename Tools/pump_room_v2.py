# Salle DOUBLE PUMP : boite 1x1 (512 x 512), arrivee au milieu + plateforme d attente du spawner
# Garde le donneur d'objets (deja regle) et le spawner ; refait le reste.
import unreal, traceback
exec(open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\aim_lib.py", encoding="utf-8").read())
CX, CY, W, D, H, T = 0.0, 60000.0, 512.0, 512.0, 1000.0, 60.0
KEEP = ("AIM_Pump_Loadout", "AIM_Pump_Spawner")
try:
    for a in eas.get_all_level_actors():
        lab = a.get_actor_label()
        if lab.startswith("AIM_Pump_") and lab not in KEEP:
            eas.destroy_actor(a)
    M = {"gloss": eal.load_asset(MAT_DIR + "/M_Lobby_BlackGloss"), "led": eal.load_asset(MAT_DIR + "/M_Lobby_LedDeepBlue"),
         "wall": eal.load_asset(MAT_DIR + "/M_Aim_ArenaWall")}
    F = "Pump"
    hx, hy = W / 2, D / 2
    box("Pump_Floor", F, M["gloss"], V(CX, CY, FLOOR - 25), V(W + 2 * T, D + 2 * T, 50))
    for nm, c, s in (("N", V(CX, CY + hy + T / 2, FLOOR + H / 2), V(W + 2 * T, T, H)), ("S", V(CX, CY - hy - T / 2, FLOOR + H / 2), V(W + 2 * T, T, H)),
                     ("E", V(CX + hx + T / 2, CY, FLOOR + H / 2), V(T, D, H)), ("W", V(CX - hx - T / 2, CY, FLOOR + H / 2), V(T, D, H))):
        box("Pump_Wall" + nm, F, M["wall"], c, s)
    box("Pump_Roof", F, M["wall"], V(CX, CY, FLOOR + H + T / 2), V(W + 2 * T, D + 2 * T, T))
    for nm, c, s in (("E", V(CX + hx - 6, CY, FLOOR + H - 12), V(12, D, 24)), ("W", V(CX - hx + 6, CY, FLOOR + H - 12), V(12, D, 24)),
                     ("FE", V(CX + hx - 10, CY, FLOOR + 1), V(20, D, 2)), ("FW", V(CX - hx + 10, CY, FLOOR + 1), V(20, D, 2))):
        box("Pump_Led" + nm, F, M["led"], c, s, False)
    for i, fy in enumerate((0.0,)):
        pl = eas.spawn_actor_from_class(unreal.PointLight, V(CX, CY + fy * D, FLOOR + H - 200))
        lc = pl.get_component_by_class(unreal.PointLightComponent)
        lc.set_light_color(LC(0.85, 0.9, 1.0)); lc.set_intensity(40.0); lc.set_attenuation_radius(1400.0)
        lc.set_editor_property("cast_shadows", False)
        tag(pl, "Pump_Light%d" % i, F)
    # textes sur le mur du fond (nord), face au joueur
    yt = CY + hy - 15
    billboard("Pump_Title", F, V(CX, yt, FLOOR + 640), -90.0, "DOUBLE PUMP", 34)
    billboard("Pump_Emote1", F, V(CX, yt, FLOOR + 480), -90.0, "DO AN EMOTE", 28)
    billboard("Pump_Emote2", F, V(CX, yt, FLOOR + 420), -90.0, "TO RETURN TO LOBBY", 22)
    # plateforme sous le spawner (le bot y apparait puis est teleporte dans la boite)
    box("Pump_Staging", F, M["gloss"], V(2100, CY, FLOOR - 25), V(400, 400, 50))
    # arrivee au milieu, regard vers le mur du fond
    arrival("Pump_Arrival", F, CX, CY, 90.0)
    # zone de la salle (emote -> lobby)
    z = spawn("mutator", "Pump_Room", F, V(CX, CY, FLOOR))
    z.set_actor_rotation(unreal.Rotator(0, 0, 0), False)
    o, e = z.get_actor_bounds(False); s = z.get_actor_scale3d()
    z.set_actor_scale3d(V(s.x * (W - 20) / (2 * e.x), s.y * (D - 20) / (2 * e.y), s.z * (H - 40) / (2 * e.z)))
    o, e = z.get_actor_bounds(False); p = z.get_actor_location()
    z.set_actor_location(V(p.x + CX - o.x, p.y + CY - o.y, p.z + FLOOR + 10 - (o.z - e.z)), False, False)
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE")
except Exception:
    L.append(traceback.format_exc())
open(TOOLS + r"\pump_room_v2_log.txt", "w").write("\n".join(L))
