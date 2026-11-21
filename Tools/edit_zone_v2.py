# ============================================================================
#  edit_zone_v2.py - (apres build_tunnels.py)
#  1. supprime l'ancienne partie Edit (rangees de pieces, ligne chrono, reset)
#  2. toit au-dessus de la zone Edit
#  3. depart / arrivee des tunnels = Mutator Zones invisibles + arrivee
#     lumineuse (hologramme couleur du tunnel, socle, panneau ARRIVEE)
#  4. idem pour le chrono Piece Control (triggers -> Mutator Zones)
#  5. explosifs + Data Layer "DL_TunnelBuilds" + sequence "LS_TunnelReload"
#     + Cinematic Sequence Device pour le reset des pieces
# ============================================================================
import unreal, json, traceback

TOOLS = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools"
LOG_FILE = TOOLS + r"\edit_zone_v2_log.txt"
ROOT = "/5622d7d7-d1ca-438f-8a48-1286a48e2471"
MAT_DIR = ROOT + "/Lobby/Materials"
TUN_DIR = ROOT + "/Tunnels"
FLOOR_Z = 1270.0
CELL, LH = 512.0, 384.0
TMAP = json.load(open(TOOLS + r"\build_tunnels_map.json", encoding="utf-8"))
COLORS = {"FACILE": (0.0, 1.0, 0.25), "MOYEN": (1.0, 0.75, 0.0), "DIFFICILE": (1.0, 0.25, 0.0), "IMPOSSIBLE": (1.0, 0.0, 0.02)}

CLS = {
    "mutator": "/CRD_VolumetricRegion/Device_MutatorVolume_V2.Device_MutatorVolume_V2_C",
    "billboard": "/Game/Creative/Devices/Billboard/BP_Creative_Billboard.BP_Creative_Billboard_C",
    "explosive": "/CreativeCoreDevices/Device_ExplosiveBarrel_V2.Device_ExplosiveBarrel_V2_C",
    "cinematic": "/CRD_CinematicSequence/Device_CinematicSequence.Device_CinematicSequence_C",
}
OLD_EDIT = ["_wall_", "_floor_", "_stair_", "_cone_", "_RowTitle", "_EditTitle", "_ChronoWall", "_ChronoStart",
            "_ChronoFinish", "_ChronoHUD", "_ChronoTitle", "_ResetButton", "_ResetTitle"]

lines = []
def log(*a):
    lines.append(" ".join(str(x) for x in a))

eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
eal = unreal.EditorAssetLibrary
mel = unreal.MaterialEditingLibrary
tools = unreal.AssetToolsHelpers.get_asset_tools()
CUBE = eal.load_asset("/Engine/BasicShapes/Cube")
CYL = eal.load_asset("/Engine/BasicShapes/Cylinder")
ACT = {a.get_actor_label(): a for a in eas.get_all_level_actors()}

_src = open(TOOLS + r"\build_lobby.py", encoding="utf-8").read()
_ns = {"unreal": unreal, "eal": eal, "mel": mel, "tools": tools, "MAT_DIR": MAT_DIR}
exec(_src[_src.index("def new_material"):_src.index("# couleurs en lineaire")], _ns)

def V(x, y, z):
    return unreal.Vector(float(x), float(y), float(z))

def mat(name):
    return eal.load_asset(MAT_DIR + "/" + name)

def tag(a, label, folder):
    a.set_actor_label(label)
    a.set_folder_path(folder)
    ACT[label] = a
    return a

def box(label, folder, mesh, material, c, size, collision=True):
    a = eas.spawn_actor_from_class(unreal.FortStaticMeshActor, c)
    comp = a.get_component_by_class(unreal.StaticMeshComponent)
    comp.set_static_mesh(mesh)
    comp.set_material(0, material)
    a.set_actor_scale3d(V(size.x / 100, size.y / 100, size.z / 100))
    if not collision:
        comp.set_collision_profile_name("NoCollision")
        comp.set_editor_property("cast_shadow", False)
    return tag(a, label, folder)

def dev(key, label, folder, loc, yaw=0.0):
    a = eas.spawn_actor_from_class(unreal.load_class(None, CLS[key]), loc, unreal.Rotator(roll=0, pitch=0, yaw=yaw))
    return tag(a, label, folder)

def fit(actor, w, d, h, bottom_center):
    o, e = actor.get_actor_bounds(False)
    s = actor.get_actor_scale3d()
    actor.set_actor_scale3d(V(s.x * w / (2 * e.x), s.y * d / (2 * e.y), s.z * h / (2 * e.z)))
    o, e = actor.get_actor_bounds(False)
    loc = actor.get_actor_location()
    actor.set_actor_location(V(bottom_center.x + (loc.x - o.x), bottom_center.y + (loc.y - o.y),
                               bottom_center.z + (loc.z - (o.z - e.z))), False, False)

def zone(label, folder, bottom_center, w, d, h):
    z = dev("mutator", label, folder, bottom_center)
    fit(z, w, d, h, bottom_center)
    return z

def destroy(label):
    a = ACT.pop(label, None)
    if a:
        loc = a.get_actor_location()
        eas.destroy_actor(a)
        return loc
    return None

def step(name, fn):
    try:
        fn(); log(name, "ok")
    except Exception:
        log(name, "ERREUR", traceback.format_exc())

# ---------------------------------------------------------------------------
def remove_old_edit():
    n = 0
    for lab in list(ACT):
        if lab.startswith("ZONE_Edit") and (any(k in lab for k in OLD_EDIT) or lab == "ZONE_Edit_Chrono"):
            destroy(lab); n += 1
    log("  ancienne partie Edit supprimee :", n, "acteurs")

def roof():
    for lab in [l for l in ACT if l.startswith("ZONE_EditRoof")]:
        destroy(lab)
    F = "Zones/Edit/Roof"
    cx, cy, z = 0.0, -20400.0, FLOOR_Z + 1000
    W, D = 6200.0, 6800.0
    box("ZONE_EditRoof", F, CUBE, mat("M_Lobby_BlackMatte"), V(cx, cy, z + 25), V(W, D, 50))
    blue, white = mat("M_Lobby_LedBlue"), mat("M_Lobby_LedWhite")
    for sx in (-1, 1):
        box("ZONE_EditRoofLedX%d" % sx, F, CUBE, blue, V(cx + sx * (W / 2 - 20), cy, z - 5), V(20, D, 10), False)
        box("ZONE_EditRoofLedY%d" % sx, F, CUBE, blue, V(cx, cy + sx * (D / 2 - 20), z - 5), V(W, 20, 10), False)
        for sy in (-1, 1):
            box("ZONE_EditRoofPillar%d%d" % (sx, sy), F, CUBE, mat("M_Lobby_BlackMatte"),
                V(cx + sx * (W / 2 - 60), cy + sy * (D / 2 - 60), FLOOR_Z + 500), V(120, 120, 1000))
            box("ZONE_EditRoofPillarLed%d%d" % (sx, sy), F, CUBE, white,
                V(cx + sx * (W / 2 - 60) - sx * 62, cy + sy * (D / 2 - 60), FLOOR_Z + 500), V(6, 30, 980), False)
    for i in range(-2, 3):
        box("ZONE_EditRoofLine%d" % i, F, CUBE, white, V(cx + i * 1200, cy, z - 4), V(14, D - 400, 8), False)
    for sx in (-1, 1):
        for sy in (-1, 0, 1):
            pl = eas.spawn_actor_from_class(unreal.PointLight, V(cx + sx * 1500, cy + sy * 2200, z - 150))
            lc = pl.get_component_by_class(unreal.PointLightComponent)
            lc.set_light_color(unreal.LinearColor(0.75, 0.88, 1.0, 1))
            lc.set_intensity(60.0)
            lc.set_attenuation_radius(3000.0)
            tag(pl, "ZONE_EditRoofLight%d%d" % (sx, sy), F)

def tunnel_zones():
    for t in TMAP["tunnels"]:
        name, X = t["name"], t["x"]
        folder = "Zones/Edit/Tunnels/%s/Chrono" % name.capitalize()
        rgb = COLORS[name]
        # depart : zone invisible juste devant l'entree
        sloc = destroy(t["start"]) or ACT.get(t["start"])
        zone(t["start"], folder, V(X, -23296 + 250, 1152.0), CELL - 40, 300, 500)   # v3 : tunnels sur la grille (sol 1152)
        # arrivee : zone qui remplit la derniere case + visuel
        floc = destroy(t["finish"])
        if floc is None:
            log("  pas d'arrivee pour", name); continue
        fz = floc.z
        zone(t["finish"], folder, V(X, floc.y, fz), CELL - 60, CELL - 60, LH - 20)
        vf = "Zones/Edit/Tunnels/%s/Finish" % name.capitalize()
        for lab in [l for l in ACT if l.startswith("TUN_%s_Fin" % name) and l != t["finish"]]:
            destroy(lab)
        holo = _ns["hologram_mat"]("M_Tunnel_Holo_" + name.capitalize(), unreal.LinearColor(rgb[0], rgb[1], rgb[2], 1)) \
            if not eal.does_asset_exist(MAT_DIR + "/M_Tunnel_Holo_" + name.capitalize()) else mat("M_Tunnel_Holo_" + name.capitalize())
        led = mat("M_Tunnel_Led_" + name.capitalize())
        box("TUN_%s_FinSocle" % name, vf, CYL, led, V(X, floc.y, fz + 3), V(420, 420, 6), False)
        box("TUN_%s_FinRing" % name, vf, CYL, mat("M_Lobby_LedWhite"), V(X, floc.y, fz + 2), V(470, 470, 3), False)
        box("TUN_%s_FinHolo" % name, vf, CYL, holo, V(X, floc.y, fz + 15 + 170), V(330, 330, 340), False)
        bb = eas.spawn_actor_from_class(unreal.load_class(None, CLS["billboard"]), V(X, floc.y + 250, fz + 300), unreal.Rotator(roll=0, pitch=0, yaw=180))
        bb.set_editor_property("text", "FINISH")
        bb.set_editor_property("TextSize", 30)
        tag(bb, "TUN_%s_FinTitle" % name, vf)
        pl = eas.spawn_actor_from_class(unreal.PointLight, V(X, floc.y, fz + 250))
        lc = pl.get_component_by_class(unreal.PointLightComponent)
        lc.set_light_color(unreal.LinearColor(rgb[0], rgb[1], rgb[2], 1))
        lc.set_intensity(40.0)
        lc.set_attenuation_radius(700.0)
        tag(pl, "TUN_%s_FinLight" % name, vf)

def piece_control_zones():
    for lab in ("ZONE_PieceControl_ChronoStart", "ZONE_PieceControl_ChronoFinish"):
        loc = destroy(lab)
        if loc:
            zone(lab, "Zones/PieceControl/Chrono", V(loc.x, loc.y, loc.z), 600, 600, 400)

def explosives():
    for lab in [l for l in ACT if l.startswith("TUN_Explosive")]:
        destroy(lab)
    names = []
    for i, y in enumerate(range(-24500, -47001, -4500)):
        e = dev("explosive", "TUN_Explosive%d" % i, "Zones/Edit/Tunnels/Reset", V(0, y, FLOOR_Z + 600))
        names.append(e.get_actor_label())
    TMAP["explosives"] = names

def data_layer_and_sequence():
    dls = unreal.get_editor_subsystem(unreal.DataLayerEditorSubsystem)
    path = TUN_DIR + "/DL_TunnelBuilds"
    if eal.does_asset_exist(path):
        dl = eal.load_asset(path)
    else:
        dl = tools.create_asset("DL_TunnelBuilds", TUN_DIR, unreal.DataLayerAsset, unreal.DataLayerFactory())
    try:
        dl.set_editor_property("data_layer_type", unreal.DataLayerType.RUNTIME)
    except Exception as e:
        log("  type runtime:", e)
    eal.save_loaded_asset(dl)
    inst = None
    for i in dls.get_all_data_layers():
        try:
            if i.get_asset() == dl:
                inst = i
        except Exception:
            pass
    if inst is None:
        p = unreal.DataLayerCreationParameters()
        p.set_editor_property("data_layer_asset", dl)
        inst = dls.create_data_layer_instance(p)
    log("  data layer instance", inst)
    for prop, val in (("initial_runtime_state", unreal.DataLayerRuntimeState.ACTIVATED),):
        try:
            inst.set_editor_property(prop, val)
        except Exception as e:
            log("  initial state:", e)
    pieces = [a for l, a in ACT.items() if l.startswith("TUN_") and any(k in l for k in ("_Wall", "_Stair", "_Ramp", "_Cone", "_Hole"))]
    ok = dls.add_actors_to_data_layer(pieces, inst)
    log("  pieces ajoutees au data layer :", len(pieces), ok)

    lpath = TUN_DIR + "/LS_TunnelReload"
    if eal.does_asset_exist(lpath):
        eal.delete_asset(lpath)
    ls = tools.create_asset("LS_TunnelReload", TUN_DIR, unreal.LevelSequence, unreal.LevelSequenceFactoryNew())
    track = ls.add_track(unreal.MovieSceneDataLayerTrack)
    sec = track.add_section()
    sec.set_range(0, 15)
    for prop, val in (("data_layer_assets", [dl]), ("desired_state", unreal.DataLayerRuntimeState.UNLOADED),
                      ("preroll_state", unreal.DataLayerRuntimeState.UNLOADED)):
        try:
            sec.set_editor_property(prop, val)
        except Exception as e:
            log("  section", prop, e)
    ls.set_playback_start(0)
    ls.set_playback_end(30)
    eal.save_loaded_asset(ls)
    log("  sequence", ls)
    if "TUN_ReloadSequence" not in ACT:
        dev("cinematic", "TUN_ReloadSequence", "Zones/Edit/Tunnels/Reset", V(700, -22300, FLOOR_Z - 400))
    for p in ("Sequence", "sequence", "LevelSequence"):
        try:
            ACT["TUN_ReloadSequence"].set_editor_property(p, ls); log("  sequence posee via", p); break
        except Exception:
            pass

step("ancienne partie Edit", remove_old_edit)
step("toit", roof)
step("zones des tunnels", tunnel_zones)
step("zones Piece Control", piece_control_zones)
step("explosifs", explosives)
step("data layer + sequence", data_layer_and_sequence)
open(TOOLS + r"\build_tunnels_map.json", "w", encoding="utf-8").write(json.dumps(TMAP, indent=1))
try:
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
except Exception:
    log("sauvegarde", traceback.format_exc())
open(LOG_FILE, "w", encoding="utf-8").write("\n".join(lines))
