# ============================================================================
#  build_aim.py - zone AIM refaite : hub avec 3 FAILLES -> 3 arenes d'exercice
#   LANCER (0,32000)  : anneau de 14 pads, le bot est propulse en cloche
#   REBOND (0,42500)  : 7 pads, le bot monte/descend sur un pad
#   CIRCUIT (0,52500) : mur a etageres, le bot suit un circuit en zigzag
#  Bots = props mannequins + Prop Manipulator (copie du modele PV eleve).
#  Device Verse aim_trainer (cablage : wire_aim.py). Relancable (prefixe AIM_).
# ============================================================================
import unreal, math, json, traceback
TOOLS = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools"
ROOT = "/5622d7d7-d1ca-438f-8a48-1286a48e2471"
MAT_DIR = ROOT + "/Lobby/Materials"
FLOOR = 1270.0
CLS = {
    "cp": "/CRG_Props/SetupAssets/Blueprints/TechPrimitives/CP_L_T_Primitive_Squared_Cube_Flat.CP_L_T_Primitive_Squared_Cube_Flat_C",
    "pad": "/CRG_Props/SetupAssets/Blueprints/TechPrimitives/CP_L_T_Primitive_Planar_Cylinder_Solid.CP_L_T_Primitive_Planar_Cylinder_Solid_C",
    "mutator": "/CRD_VolumetricRegion/Device_MutatorVolume_V2.Device_MutatorVolume_V2_C",
    "billboard": "/Game/Creative/Devices/Billboard/BP_Creative_Billboard.BP_Creative_Billboard_C",
}
NPC_SPAWNER_CLS = "/CRD_AISpawner/Device_CharacterSpawner.Device_CharacterSpawner_C"
NPC_DEF = ROOT + "/Lobby/NPC/NPC_TrainingBot"
BOUNCER_CLS = "/CRD_Bouncer/SetupAssets/Classic_Bouncer/BP_Device_ClassicBouncer.BP_Device_ClassicBouncer_C"   # matelas (device autorise)
OLD_AIM = ("ZONE_Aim_ShootLine", "ZONE_Aim_Target", "ZONE_Aim_Timer60s", "ZONE_Aim_ScoreManager",
           "ZONE_Aim_Challenge", "PROBE_", "AIM_")
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
eal = unreal.EditorAssetLibrary
mel = unreal.MaterialEditingLibrary
tools = unreal.AssetToolsHelpers.get_asset_tools()
WORLD = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
CUBE = eal.load_asset("/Engine/BasicShapes/Cube")
CYL = eal.load_asset("/Engine/BasicShapes/Cylinder")
L = []
MAP = {}

def V(x, y, z):
    return unreal.Vector(float(x), float(y), float(z))

def LC(r, g, b):
    return unreal.LinearColor(r, g, b, 1.0)

def mat(name, base, emi=None, rough=0.5):
    path = MAT_DIR + "/" + name
    if eal.does_asset_exist(path):
        return eal.load_asset(path)
    m = tools.create_asset(name, MAT_DIR, unreal.Material, unreal.MaterialFactoryNew())
    for prop, col, y in ((unreal.MaterialProperty.MP_BASE_COLOR, base, -200), (unreal.MaterialProperty.MP_EMISSIVE_COLOR, emi, 200)):
        if col is None:
            continue
        e = mel.create_material_expression(m, unreal.MaterialExpressionConstant3Vector, -400, y)
        e.set_editor_property("constant", col)
        mel.connect_material_property(e, "", prop)
    r = mel.create_material_expression(m, unreal.MaterialExpressionConstant, -400, 0)
    r.set_editor_property("r", rough)
    mel.connect_material_property(r, "", unreal.MaterialProperty.MP_ROUGHNESS)
    mel.recompile_material(m)
    eal.save_loaded_asset(m)
    return m

def tag(a, label, folder):
    a.set_actor_label("AIM_" + label)
    a.set_folder_path("Zones/Aim/" + folder)
    a.set_editor_property("is_spatially_loaded", False)
    return a

def box(label, folder, m, c, size, collision=True, mesh=None, roll=0.0, yaw=0.0):
    a = eas.spawn_actor_from_class(unreal.FortStaticMeshActor, c, unreal.Rotator(roll=roll, pitch=0.0, yaw=yaw))
    comp = a.get_component_by_class(unreal.StaticMeshComponent)
    comp.set_static_mesh(mesh or CUBE)
    comp.set_material(0, m)
    a.set_actor_scale3d(V(size.x / 100, size.y / 100, size.z / 100))
    if not collision:
        comp.set_collision_profile_name("NoCollision")
        comp.set_editor_property("cast_shadow", False)
    return tag(a, label, folder)

def fit(a, w, d, h, bottom):
    o, e = a.get_actor_bounds(False)
    s = a.get_actor_scale3d()
    a.set_actor_scale3d(V(s.x * w / (2 * e.x), s.y * d / (2 * e.y), s.z * h / (2 * e.z)))
    o, e = a.get_actor_bounds(False)
    p = a.get_actor_location()
    a.set_actor_location(V(p.x + bottom.x - o.x, p.y + bottom.y - o.y, p.z + bottom.z - (o.z - e.z)), False, False)

def spawn(key, label, folder, loc, yaw=0.0):
    a = eas.spawn_actor_from_class(unreal.load_class(None, CLS[key]), loc, unreal.Rotator(roll=0, pitch=0, yaw=yaw))
    return tag(a, label, folder)

def marker(label, folder, loc, yaw, size=40.0):
    """petit prop repere (Verse lit sa position/rotation) - quasi invisible"""
    p = spawn("pad", label, folder, loc, yaw)
    fit(p, size, size, 2, loc)
    p.set_actor_rotation(unreal.Rotator(roll=0, pitch=0, yaw=yaw), False)
    return p

def billboard(label, folder, loc, face_yaw, text, size=44):
    # le texte regarde vers face_yaw (deg) ; yaw du billboard = face_yaw + 90
    b = spawn("billboard", label, folder, loc, face_yaw + 90.0)
    for n, v in (("text", text), ("TextSize", size), ("TextJustification", unreal.TextJustify.CENTER), ("TextColor", LC(1, 1, 1))):
        try:
            b.set_editor_property(n, v)
        except Exception as ex:
            L.append("billboard %s : %s" % (n, ex))
    for c in b.get_components_by_class(unreal.PrimitiveComponent):
        try:
            c.set_collision_profile_name("NoCollision")
        except Exception:
            pass
    return b

def face_to(src, dst):
    return math.degrees(math.atan2(dst[1] - src[1], dst[0] - src[0]))

def rift(label, folder, x, y, face_yaw, rgb, title, M, base=FLOOR):
    """faille : ellipse neon verticale + coeur sombre colore + zone de teleportation"""
    # face_yaw = direction vers laquelle la faille regarde (+90 = +Y, -90 = -Y)
    neon = mat("M_Rift_Neon_%d_%d_%d" % tuple(int(c * 100) for c in rgb), LC(0, 0, 0), LC(rgb[0] * 12, rgb[1] * 12, rgb[2] * 12))
    core = mat("M_Rift_Core_%d_%d_%d" % tuple(int(c * 100) for c in rgb), LC(0, 0, 0), LC(rgb[0] * 1.2, rgb[1] * 1.2, rgb[2] * 1.2))
    fx, fy = math.cos(math.radians(face_yaw)), math.sin(math.radians(face_yaw))
    yaw = face_yaw - 90.0           # disque (roll 90) : epaisseur le long de la direction regardee
    zc = base + 30 + 260
    box(label + "_Edge", folder, neon, V(x, y, zc), V(300, 520, 8), False, CYL, 90.0, yaw)
    box(label + "_Core", folder, core, V(x + fx * 5, y + fy * 5, zc), V(250, 465, 8), False, CYL, 90.0, yaw)
    box(label + "_Glow", folder, neon, V(x + fx * 120, y + fy * 120, base + 1), V(320, 200, 2), False, None, 0.0, yaw)
    billboard(label + "_Title", folder, V(x + fx * 20, y + fy * 20, base + 600 - 57), face_yaw, title, 44)
    z = spawn("mutator", label + "_Zone", folder, V(x, y, base))
    z.set_actor_rotation(unreal.Rotator(0, 0, 0), False)
    o, e = z.get_actor_bounds(False)
    s = z.get_actor_scale3d()
    wx, wy = (240, 140) if abs(fx) < 0.5 else (140, 240)
    z.set_actor_scale3d(V(s.x * wx / (2 * e.x), s.y * wy / (2 * e.y), s.z * 440 / (2 * e.z)))
    o, e = z.get_actor_bounds(False)
    p = z.get_actor_location()
    z.set_actor_location(V(p.x + x - o.x, p.y + y - o.y, p.z + base + 40 - (o.z - e.z)), False, False)
    return z

def arena_floor(name, cx, cy, size, M, title, title_pos, title_z=650):
    box(name + "_Floor", name, M["gloss"], V(cx, cy, FLOOR - 25), V(size, size, 50))
    h = size / 2
    for nm, c, s in (("A", V(cx + h - 10, cy, FLOOR + 1), V(20, size, 2)), ("B", V(cx - h + 10, cy, FLOOR + 1), V(20, size, 2)),
                     ("C", V(cx, cy + h - 10, FLOOR + 1), V(size, 20, 2)), ("D", V(cx, cy - h + 10, FLOOR + 1), V(size, 20, 2))):
        box(name + "_Led" + nm, name, M["led"], c, s, False)
    billboard(name + "_Title", name, V(title_pos[0], title_pos[1], FLOOR + title_z), -90.0, title, 60)

def arrival(name, folder, x, y, yaw, base=FLOOR):
    p = spawn("pad", name, folder, V(x, y, base), yaw)
    fit(p, 200, 200, 10, V(x, y, base))
    p.set_actor_rotation(unreal.Rotator(roll=0, pitch=0, yaw=yaw), False)
    return p

def bouncer(label, folder, x, y, yaw, scale=0.45, z=FLOOR):
    """matelas rebondissant (Bouncer classique : les fleches donnent la direction)"""
    b = eas.spawn_actor_from_class(unreal.load_class(None, BOUNCER_CLS), V(x, y, z), unreal.Rotator(roll=0, pitch=0, yaw=yaw))
    b.set_actor_scale3d(V(scale, scale, scale))
    return tag(b, label, folder)

def ramp(label, folder, M, x, y, z, direction):
    """tremplin : rampe orange qui monte de 60 cm sur 200 cm et finit en x (sens direction = +1/-1 en X)"""
    ang = math.degrees(math.atan2(60, 200))
    a = eas.spawn_actor_from_class(unreal.FortStaticMeshActor, V(x - direction * 100, y, z + 30),
                                   unreal.Rotator(roll=0.0, pitch=ang * direction, yaw=0.0))
    c = a.get_component_by_class(unreal.StaticMeshComponent)
    c.set_static_mesh(CUBE); c.set_material(0, M["orange"])
    a.set_actor_scale3d(V(2.1, 1.2, 0.08))
    c.set_collision_profile_name("NoCollision")
    return tag(a, label, folder)

def platform(name, folder, M, x, y, w=900, d=900, h=320):
    """plateforme de depart lointaine (surelevee) avec liseré LED"""
    box(name, folder, M["gloss"], V(x, y, FLOOR + h / 2), V(w, d, h))
    top = FLOOR + h
    for nm, c, s in (("A", V(x + w / 2 - 8, y, top + 1), V(16, d, 4)), ("B", V(x - w / 2 + 8, y, top + 1), V(16, d, 4)),
                     ("C", V(x, y + d / 2 - 8, top + 1), V(w, 16, 4)), ("D", V(x, y - d / 2 + 8, top + 1), V(w, 16, 4))):
        box(name + "_Led" + nm, folder, M["led"], c, s, False)
    return top

def enclosure(name, M, cx, cy, size, height):
    """murs + toit + liseres LED + eclairage interieur autour d'une arene"""
    h, T = size / 2.0, 60.0
    folder = name + "/Enclosure"
    for nm, c, s in (("N", V(cx, cy + h + T / 2, FLOOR + height / 2), V(size + 2 * T, T, height)),
                     ("S", V(cx, cy - h - T / 2, FLOOR + height / 2), V(size + 2 * T, T, height)),
                     ("E", V(cx + h + T / 2, cy, FLOOR + height / 2), V(T, size, height)),
                     ("W", V(cx - h - T / 2, cy, FLOOR + height / 2), V(T, size, height))):
        box(name + "_Wall" + nm, folder, M["arenawall"], c, s)
    box(name + "_Roof", folder, M["arenawall"], V(cx, cy, FLOOR + height + T / 2), V(size + 2 * T, size + 2 * T, T))
    for nm, c, s in (("N", V(cx, cy + h - 6, FLOOR + height - 12), V(size, 12, 24)), ("S", V(cx, cy - h + 6, FLOOR + height - 12), V(size, 12, 24)),
                     ("E", V(cx + h - 6, cy, FLOOR + height - 12), V(12, size, 24)), ("W", V(cx - h + 6, cy, FLOOR + height - 12), V(12, size, 24))):
        box(name + "_TopLed" + nm, folder, M["led"], c, s, False)
    k = 0
    for fx in (-0.3, 0.3):
        for fy in (-0.3, 0.3):
            pl = eas.spawn_actor_from_class(unreal.PointLight, V(cx + fx * size, cy + fy * size, FLOOR + height - 250))
            lc = pl.get_component_by_class(unreal.PointLightComponent)
            lc.set_light_color(LC(0.85, 0.9, 1.0)); lc.set_intensity(60.0); lc.set_attenuation_radius(size * 0.9)
            lc.set_editor_property("cast_shadows", False)
            tag(pl, "%s_Light%d" % (name, k), folder)
            k += 1

def npc_spawner(name, folder, loc, definition):
    """vrai bot : NPC Spawner + definition NPC_TrainingBot (comportement vide)"""
    sp = eas.spawn_actor_from_class(unreal.load_class(None, NPC_SPAWNER_CLS), loc)
    sp.get_component_by_class(unreal.NPCCharacterDefinitionComponent).set_editor_property("NPCCharacterDefinition", definition)
    return tag(sp, name, folder)

try:
    ACT = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
    n = 0
    for lab, a in list(ACT.items()):
        if lab.startswith(OLD_AIM):
            eas.destroy_actor(a); n += 1
    L.append("supprimes : %d" % n)
    M = {"gloss": eal.load_asset(MAT_DIR + "/M_Lobby_BlackGloss"),
         "led": eal.load_asset(MAT_DIR + "/M_Lobby_LedDeepBlue"),
         "padbase": mat("M_Aim_PadBase", LC(0.03, 0.03, 0.035), None, 0.6),
         "orange": mat("M_Aim_PadOrange", LC(0, 0, 0), LC(6.0, 1.6, 0.0)),
         "green": mat("M_Aim_PadGreen", LC(0, 0, 0), LC(0.5, 6.0, 1.0)),
         "wall": mat("M_Aim_WallBlue", LC(0.12, 0.25, 0.4), None, 0.7),
         "shelf": mat("M_Aim_ShelfBlue", LC(0.2, 0.4, 0.6), None, 0.6),
         "arenawall": mat("M_Aim_ArenaWall", LC(0.06, 0.09, 0.16), None, 0.5)}
    npc_def = eal.load_asset(NPC_DEF)
    with unreal.ScopedEditorTransaction("Zone Aim : failles + exercices"):
        # ---------- hub (zone Aim existante) ----------
        hub_arr = ACT["ZONE_Aim_Arrival"]
        hub_arr.modify()
        for c in hub_arr.get_components_by_class(unreal.SceneComponent):
            c.modify()
        hub_arr.set_actor_rotation(unreal.Rotator(roll=0, pitch=0, yaw=90.0), False)
        rifts, targets = [], []
        EX = [("Launch", "LANCER", (1.0, 0.35, 0.0), 1400.0), ("Bounce", "REBOND", (0.1, 1.0, 0.25), 0.0),
              ("Circuit", "CIRCUIT", (0.55, 0.1, 1.0), -1400.0)]
        for key, title, rgb, x in EX:
            rifts.append(rift("Hub_Rift" + key, "Hub", x, 20800, -90.0, rgb, title, M))
        # ---------- 1. LANCER : plateforme de depart loin de l'anneau de matelas (ecartes) ----------
        cx, cy = 0.0, 34000.0
        RC = (0.0, 35000.0)          # centre de l'anneau, ~52 m devant la plateforme
        arena_floor("Launch", cx, cy, 10000, M, "LANCER", (0, 38600))
        enclosure("Launch", M, cx, cy, 10000, 3400)
        top = platform("Launch_Platform", "Launch", M, 0, 29800)
        a1 = arrival("Launch_Arrival", "Launch", 0, 29950, 90.0, top)
        pads1 = []
        rnd = [35, -50, 20, -15, 55, -40, 10, -60, 45, -25]     # deviation fixe de chaque matelas
        for i in range(10):
            ang = 2 * math.pi * i / 10
            x, y = RC[0] + 2800 * math.cos(ang), RC[1] + 2800 * math.sin(ang)
            yaw = face_to((x, y), RC) + rnd[i]                   # pousse vers l'interieur, en biais
            bouncer("Launch_Pad%d" % i, "Launch/Pads", x, y, yaw)
            pads1.append(marker("Launch_PadMark%d" % i, "Launch/Pads", V(x, y, FLOOR + 25), yaw))
        sp1 = npc_spawner("Launch_Spawner", "Launch", V(4500, 38500, FLOOR), npc_def)
        rifts.append(rift("Launch_Return", "Launch", 0, 29500, 90.0, (0.2, 0.6, 1.0), "RETOUR AIM", M, top))
        # ---------- 2. REBOND : plateforme de depart, matelas a 25-58 m ----------
        cx, cy = 0.0, 44000.0
        arena_floor("Bounce", cx, cy, 8000, M, "REBOND", (0, 47600))
        enclosure("Bounce", M, cx, cy, 8000, 2200)
        top = platform("Bounce_Platform", "Bounce", M, 0, 40700)
        a2 = arrival("Bounce_Arrival", "Bounce", 0, 40850, 90.0, top)
        pads2 = []
        for i, (x, y) in enumerate([(-1800, 43500), (-600, 44700), (700, 43700), (1900, 45000), (-1300, 46300), (300, 46500), (1500, 46200)]):
            yaw = face_to((x, y), (0, 40850))
            bouncer("Bounce_Pad%d" % i, "Bounce/Pads", x, y, yaw)
            pads2.append(marker("Bounce_PadMark%d" % i, "Bounce/Pads", V(x, y, FLOOR + 25), yaw))
        sp2 = npc_spawner("Bounce_Spawner", "Bounce", V(3500, 47500, FLOOR), npc_def)
        rifts.append(rift("Bounce_Return", "Bounce", 0, 40400, 90.0, (0.2, 0.6, 1.0), "RETOUR AIM", M, top))
        # ---------- 3. CIRCUIT ----------
        cx, cy = 0.0, 52000.0
        arena_floor("Circuit", cx, cy, 7000, M, "CIRCUIT", (0, 53600), 1900)
        enclosure("Circuit", M, cx, cy, 7000, 2400)
        top3 = platform("Circuit_Platform", "Circuit", M, 0, 49300)
        a3 = arrival("Circuit_Arrival", "Circuit", 0, 49450, 90.0, top3)
        WY = 53800.0
        box("Circuit_Wall", "Circuit/Wall", M["wall"], V(0, WY + 30, FLOOR + 850), V(3400, 60, 1700))
        for s in (1, -1):
            box("Circuit_Post%d" % s, "Circuit/Wall", M["wall"], V(s * 1700, WY - 60, FLOOR + 850), V(60, 180, 1700))
        box("Circuit_Cap", "Circuit/Wall", M["wall"], V(0, WY - 60, FLOOR + 1700 - 30), V(3460, 180, 60))
        LV = [FLOOR + 380 * i for i in range(4)]
        # etageres decalees : L1 et L3 vont de -1500 a 1200, L2 de -1200 a 1500
        for i in (1, 2, 3):
            off = -150 if i % 2 else 150
            box("Circuit_Shelf%d" % i, "Circuit/Wall", M["shelf"], V(off, WY - 75, LV[i] - 15), V(2700, 150, 30))
        BY = WY - 110
        # circuit : le bot rebondit SANS ARRET de pad en pad le long de chaque etagere ;
        # au bout, un pad d'impulsion l'envoie sur l'etagere du dessus (sauts faits par le Verse)
        pts = []
        LEVELS = [(0, -1300, 1400), (1, 1100, -1400), (2, -1100, 1400), (3, 1100, -1300)]
        for lv, xs, xe in LEVELS:
            z = LV[lv]
            n = int(round(abs(xe - xs) / 540.0))
            for k in range(n + 1):
                x = xs + (xe - xs) * k / n
                pts.append((x, z))
                last = (k == n and lv < 3)
                bouncer("Circuit_Pad%d_%d" % (lv, k), "Circuit/Pads", x, BY, 90.0 if xe > xs else -90.0,
                        0.26 if last else 0.18, z)
        path = []
        for k, (x, z) in enumerate(pts):
            path.append(marker("Circuit_Path%02d" % k, "Circuit/Path", V(x, BY, z), -90.0, 10.0))
        sp3 = npc_spawner("Circuit_Spawner", "Circuit", V(3000, 50500, FLOOR), npc_def)
        rifts.append(rift("Circuit_Return", "Circuit", 0, 49000, 90.0, (0.2, 0.6, 1.0), "RETOUR AIM", M, top3))
        targets = [a1, a2, a3, hub_arr, hub_arr, hub_arr]
        dev = eas.spawn_actor_from_object(unreal.load_object(None, ROOT + "/_Verse.aim_trainer"), V(600, 18000, FLOOR))
        tag(dev, "Trainer", "Hub")
    MAP = {"device": dev.get_actor_label(), "rifts": [r.get_actor_label() for r in rifts],
           "targets": [t.get_actor_label() for t in targets],
           "launch": {"spawner": sp1.get_actor_label(), "pads": [p.get_actor_label() for p in pads1]},
           "bounce": {"spawner": sp2.get_actor_label(), "pads": [p.get_actor_label() for p in pads2]},
           "circuit": {"spawner": sp3.get_actor_label(), "path": [p.get_actor_label() for p in path]}}
    open(TOOLS + r"\build_aim_map.json", "w").write(json.dumps(MAP, indent=1))
    L.append("acteurs AIM_ : %d" % sum(1 for a in eas.get_all_level_actors() if a.get_actor_label().startswith("AIM_")))
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE")
except Exception:
    L.append(traceback.format_exc())
open(TOOLS + r"\build_aim_log.txt", "w").write("\n".join(L))
