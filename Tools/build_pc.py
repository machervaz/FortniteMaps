# ============================================================================
#  build_pc.py - equipe la zone PIECE CONTROL construite par le joueur (en l'air,
#  salle centrale x 22000..24600, y -11300..-7400, sol z 10376) :
#   - le portail PIECE CONTROL du lobby y amene (on deplace le pad d'arrivee)
#   - cylindre RETOUR LOBBY dans la salle (on deplace celui de l'ancienne zone)
#   - 9 parcours : zone de depart + zone d'arrivee avec cylindre lumineux ARRIVEE,
#     chrono (chrono_course, nom via CourseLabel 1..9) et HUD ; a l'arrivee le
#     temps s'affiche et on est renvoye dans la salle centrale
#   - bouton RESET : explosif (copie de TUN_Explosive0) + Data Layer
#     DL_PieceControlBuilds rechargee par une sequence (device tunnel_reset)
#  Relancable (prefixe PCX_). Cablage : wire_pc.py
# ============================================================================
import unreal, json, traceback
TOOLS = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools"
ROOT = "/5622d7d7-d1ca-438f-8a48-1286a48e2471"
MAT_DIR = ROOT + "/Lobby/Materials"
PC_DIR = ROOT + "/Lobby/PieceControl"
HUBZ = 10376.0
CLS = {
    "mutator": "/CRD_VolumetricRegion/Device_MutatorVolume_V2.Device_MutatorVolume_V2_C",
    "hud": "/CreativeCoreDevices/Device_HUDMessage_V2.Device_HUDMessage_V2_C",
    "button": "/CreativeCoreDevices/Device_Button_V2.Device_Button_V2_C",
    "billboard": "/Game/Creative/Devices/Billboard/BP_Creative_Billboard.BP_Creative_Billboard_C",
    "cinematic": "/CRD_CinematicSequence/Device_CinematicSequence.Device_CinematicSequence_C",
}
# (nom, depart (x,y,z,largeur x, largeur y, hauteur), arrivee (x,y,z), couleur)
CY = [-7680.0, -8704.0, -9728.0]
COURSES = []
for i, y in enumerate(CY):
    COURSES.append(("Couloir%d" % (i + 1), (25600, y, HUBZ, 500, 900, 760), (32700, y, HUBZ), (0.0, 0.8, 1.0)))
for i, x in enumerate([22784.0, 23808.0, 24832.0]):
    COURSES.append(("Montee%d" % (i + 1), (x, -6400, HUBZ, 900, 500, 900), (x, -1536, 14216), (0.2, 1.0, 0.3)))
for i, y in enumerate(CY):
    COURSES.append(("Descente%d" % (i + 1), (21504, y, 9984, 480, 480, 380), (21504, y, 4992), (1.0, 0.45, 0.0)))
ARRIVAL = (23552.0, -9984.0)
RETURN = (24576.0, -10496.0)
BUTTON = (22272.0, -10752.0)
USER_BOX = (20000, 34000, -12500, -500)        # zone des pieces du joueur (x, x, y, y)
USER_CLASSES = ("BrickSimple", "Floors_Generic", "PBWA_", "Pueblo_")

eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
eal = unreal.EditorAssetLibrary
tools = unreal.AssetToolsHelpers.get_asset_tools()
WORLD = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
CYL = eal.load_asset("/Engine/BasicShapes/Cylinder")
L = []

def V(x, y, z):
    return unreal.Vector(float(x), float(y), float(z))

def tag(a, label, folder):
    a.set_actor_label("PCX_" + label)
    a.set_folder_path("Zones/PieceControlX/" + folder)
    a.set_editor_property("is_spatially_loaded", False)
    return a

def spawn(key, label, folder, loc, yaw=0.0):
    return tag(eas.spawn_actor_from_class(unreal.load_class(None, CLS[key]), loc, unreal.Rotator(roll=0, pitch=0, yaw=yaw)), label, folder)

def zone(label, folder, x, y, z, wx, wy, h):
    a = spawn("mutator", label, folder, V(x, y, z))
    o, e = a.get_actor_bounds(False)
    s = a.get_actor_scale3d()
    a.set_actor_scale3d(V(s.x * wx / (2 * e.x), s.y * wy / (2 * e.y), s.z * h / (2 * e.z)))
    o, e = a.get_actor_bounds(False)
    p = a.get_actor_location()
    a.set_actor_location(V(p.x + x - o.x, p.y + y - o.y, p.z + z - (o.z - e.z)), False, False)
    return a

def cyl(label, folder, m, c, size):
    a = eas.spawn_actor_from_class(unreal.FortStaticMeshActor, c)
    comp = a.get_component_by_class(unreal.StaticMeshComponent)
    comp.set_static_mesh(CYL); comp.set_material(0, m)
    a.set_actor_scale3d(V(size.x / 100, size.y / 100, size.z / 100))
    comp.set_collision_profile_name("NoCollision")
    comp.set_editor_property("cast_shadow", False)
    return tag(a, label, folder)

def billboard(label, folder, loc, text, size=30):
    b = spawn("billboard", label, folder, loc, 0.0)
    for n, v in (("text", text), ("TextSize", size), ("TextJustification", unreal.TextJustify.CENTER), ("TextColor", unreal.LinearColor(1, 1, 1, 1))):
        try:
            b.set_editor_property(n, v)
        except Exception:
            pass
    for c in b.get_components_by_class(unreal.PrimitiveComponent):
        try:
            c.set_collision_profile_name("NoCollision")
        except Exception:
            pass
    return b

def holo_mat(name, rgb):
    path = MAT_DIR + "/" + name
    if eal.does_asset_exist(path):
        return eal.load_asset(path)
    src = open(TOOLS + r"\build_lobby.py", encoding="utf-8").read()
    ns = {"unreal": unreal, "eal": eal, "mel": unreal.MaterialEditingLibrary, "tools": tools, "MAT_DIR": MAT_DIR}
    exec(src[src.index("def new_material"):src.index("# couleurs en lineaire")], ns)
    return ns["hologram_mat"](name, unreal.LinearColor(rgb[0], rgb[1], rgb[2], 1))

def touch(a):
    a.modify()
    for c in a.get_components_by_class(unreal.SceneComponent):
        c.modify()

try:
    ACT = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
    n = 0
    for lab, a in list(ACT.items()):
        if lab.startswith("PCX_"):
            eas.destroy_actor(a); n += 1
    L.append("anciens PCX_ supprimes : %d" % n)
    white = eal.load_asset(MAT_DIR + "/M_Lobby_LedWhite")
    MAP = {"courses": []}
    with unreal.ScopedEditorTransaction("Piece Control du joueur"):
        # --- arrivee depuis le lobby + retour lobby (objets deja relies au Verse) ---
        arr = ACT["ZONE_PieceControl_Arrival"]
        touch(arr)
        arr.set_actor_location(V(ARRIVAL[0], ARRIVAL[1], HUBZ), False, False)
        arr.set_actor_rotation(unreal.Rotator(roll=0, pitch=0, yaw=0.0), False)
        socle = ACT["ZONE_PieceControl_ReturnSocle"].get_actor_location()
        d = V(RETURN[0] - socle.x, RETURN[1] - socle.y, HUBZ + 3 - socle.z)
        for lab in ("ZONE_PieceControl_ReturnSocle", "ZONE_PieceControl_ReturnHolo", "ZONE_PieceControl_ReturnZone", "ZONE_PieceControl_ReturnTitle"):
            a = ACT[lab]
            touch(a)
            p = a.get_actor_location()
            a.set_actor_location(V(p.x + d.x, p.y + d.y, p.z + d.z), False, False)
            a.set_editor_property("is_spatially_loaded", False)
        MAP["arrival"] = arr.get_actor_label()
        # --- 9 parcours ---
        for idx, (name, st, fi, rgb) in enumerate(COURSES):
            f = "Courses/" + name
            sz = zone(name + "_Start", f, st[0], st[1], st[2], st[3], st[4], st[5])
            fz = zone(name + "_Finish", f, fi[0], fi[1], fi[2], 440, 440, 700)
            holo = holo_mat("M_PC_Holo_%d_%d_%d" % tuple(int(c * 100) for c in rgb), rgb)
            led = eal.load_asset(MAT_DIR + "/M_Lobby_DiscBlue")
            cyl(name + "_FinSocle", f, led, V(fi[0], fi[1], fi[2] + 3), V(420, 420, 6))
            cyl(name + "_FinRing", f, white, V(fi[0], fi[1], fi[2] + 2), V(470, 470, 3))
            cyl(name + "_FinHolo", f, holo, V(fi[0], fi[1], fi[2] + 15 + 170), V(330, 330, 340))
            billboard(name + "_FinTitle", f, V(fi[0], fi[1], fi[2] + 300), "ARRIVEE", 30)
            pl = eas.spawn_actor_from_class(unreal.PointLight, V(fi[0], fi[1], fi[2] + 250))
            lc = pl.get_component_by_class(unreal.PointLightComponent)
            lc.set_light_color(unreal.LinearColor(rgb[0], rgb[1], rgb[2], 1)); lc.set_intensity(40.0); lc.set_attenuation_radius(700.0)
            tag(pl, name + "_FinLight", f)
            hud = spawn("hud", name + "_HUD", f, V(23000, -10000 + idx * 150, HUBZ - 600))
            ch = eas.spawn_actor_from_object(unreal.load_object(None, ROOT + "/_Verse.chrono_course"), V(23300, -10000 + idx * 150, HUBZ - 600))
            tag(ch, name + "_Chrono", f)
            MAP["courses"].append({"name": name, "label": idx + 1, "chrono": ch.get_actor_label(), "start": sz.get_actor_label(),
                                   "finish": fz.get_actor_label(), "hud": hud.get_actor_label()})
        # --- RESET ---
        btn = spawn("button", "ResetButton", "Reset", V(BUTTON[0], BUTTON[1], HUBZ), 0.0)
        billboard("ResetTitle", "Reset", V(BUTTON[0], BUTTON[1], HUBZ + 220), "RESET", 30)
        exp = eas.duplicate_actor(ACT["TUN_Explosive0"], WORLD, V(0, 0, 0))
        exp.set_actor_location(V(26500, -7500, HUBZ + 300), False, False)
        tag(exp, "ResetExplosive", "Reset")
        seqdev = spawn("cinematic", "ReloadSequence", "Reset", V(23600, -10000, HUBZ - 900))
        rdev = eas.spawn_actor_from_object(unreal.load_object(None, ROOT + "/_Verse.tunnel_reset"), V(23900, -10000, HUBZ - 900))
        tag(rdev, "ResetDevice", "Reset")
        MAP.update({"button": btn.get_actor_label(), "explosive": exp.get_actor_label(), "seq": seqdev.get_actor_label(), "reset": rdev.get_actor_label()})
        # --- pieces du joueur : jamais dechargees (teleport) ---
        pieces = []
        for a in eas.get_all_level_actors():
            p = a.get_actor_location()
            if USER_BOX[0] < p.x < USER_BOX[1] and USER_BOX[2] < p.y < USER_BOX[3] and a.get_class().get_name().startswith(USER_CLASSES):
                touch(a)
                a.set_editor_property("is_spatially_loaded", False)
                pieces.append(a)
        L.append("pieces du joueur : %d" % len(pieces))
    # --- Data Layer + sequence de rechargement (comme les tunnels) ---
    dls = unreal.get_editor_subsystem(unreal.DataLayerEditorSubsystem)
    path = PC_DIR + "/DL_PieceControlBuilds"
    dl = eal.load_asset(path) if eal.does_asset_exist(path) else tools.create_asset("DL_PieceControlBuilds", PC_DIR, unreal.DataLayerAsset, unreal.DataLayerFactory())
    dl.set_editor_property("data_layer_type", unreal.DataLayerType.RUNTIME)
    eal.save_loaded_asset(dl)
    inst = None
    for i in dls.get_all_data_layers():
        try:
            if i.get_asset() == dl:
                inst = i
        except Exception:
            pass
    if inst is None:
        prm = unreal.DataLayerCreationParameters()
        prm.set_editor_property("data_layer_asset", dl)
        inst = dls.create_data_layer_instance(prm)
    try:
        inst.set_editor_property("initial_runtime_state", unreal.DataLayerRuntimeState.ACTIVATED)
    except Exception as ex:
        L.append("etat initial : %s" % ex)
    L.append("ajout au data layer : %s" % dls.add_actors_to_data_layer(pieces, inst))
    lpath = PC_DIR + "/LS_PieceControlReload"
    if eal.does_asset_exist(lpath):
        eal.delete_asset(lpath)
    ls = tools.create_asset("LS_PieceControlReload", PC_DIR, unreal.LevelSequence, unreal.LevelSequenceFactoryNew())
    sec = ls.add_track(unreal.MovieSceneDataLayerTrack).add_section()
    sec.set_range(0, 15)
    for prop, val in (("data_layer_assets", [dl]), ("desired_state", unreal.DataLayerRuntimeState.UNLOADED),
                      ("preroll_state", unreal.DataLayerRuntimeState.UNLOADED)):
        try:
            sec.set_editor_property(prop, val)
        except Exception as ex:
            L.append("section %s : %s" % (prop, ex))
    ls.set_playback_start(0)
    ls.set_playback_end(30)
    eal.save_loaded_asset(ls)
    ok = False
    for pn in ("Sequence", "sequence", "LevelSequence"):
        try:
            seqdev.set_editor_property(pn, ls); ok = pn; break
        except Exception:
            pass
    L.append("sequence posee via : %s" % ok)
    open(TOOLS + r"\build_pc_map.json", "w").write(json.dumps(MAP, indent=1))
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE")
except Exception:
    L.append(traceback.format_exc())
open(TOOLS + r"\build_pc_log.txt", "w").write("\n".join(L))
