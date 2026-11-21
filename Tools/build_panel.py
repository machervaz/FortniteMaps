# ============================================================================
#  build_panel.py - petit panneau de la zone 1v1 (a cote des rampes)
#  On TIRE sur les formes (pas de boutons) :
#    [violet] [jour] [nuit] [rose]      <- ciel de la zone 1v1
#    [RESET]           [<]  100%  [>]   <- casse les builds / vitesse
#  Chaque forme = prop (cube plat CP) + Prop Manipulator qui le surveille
#  (copie de PROBE_PM : PV des props tres hauts).
#  Garde le Skydome, l'explosif et le device Verse deja regles.
#  Relancable. Cablage : wire_panel.py
# ============================================================================
import unreal, json, traceback

TOOLS = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools"
LOG_FILE = TOOLS + r"\build_panel_log.txt"
ROOT = "/5622d7d7-d1ca-438f-8a48-1286a48e2471"
MAT_DIR = ROOT + "/Lobby/Materials"
FLOOR_Z = 1270.0
CX, CY = -20000.0, 0.0
PX = CX + 450.0               # plan du panneau, juste a cote des rampes (face vers +X, cote arrivee)
XF = PX + 11.0                # face avant
F = "Zones/1v1/Panel"
KEEP = ("ZONE_1v1P_Sky", "ZONE_1v1P_ResetExplosive", "ZONE_1v1P_PanelDevice", "ZONE_1v1P_PMTemplate")

CLS = {
    "billboard_v2": "/CreativeCoreDevices/Device_Billboard_V2.Device_Billboard_V2_C",
    "billboard": "/Game/Creative/Devices/Billboard/BP_Creative_Billboard.BP_Creative_Billboard_C",
    "shape": "/CRG_Props/SetupAssets/Blueprints/TechPrimitives/CP_L_T_Primitive_Squared_Cube_Flat.CP_L_T_Primitive_Squared_Cube_Flat_C",
    "pm": "/CRD_PropManipulationDevice/Device_PropManipulation_V2.Device_PropManipulation_V2_C",
}
SKY = [("Violet", (0.55, 0.15, 1.0)), ("Jour", (0.85, 0.92, 1.0)), ("Nuit", (0.01, 0.01, 0.03)), ("Rose", (1.0, 0.3, 0.55))]

lines = []
def log(*a):
    lines.append(" ".join(str(x) for x in a))

eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
eal = unreal.EditorAssetLibrary
mel = unreal.MaterialEditingLibrary
tools = unreal.AssetToolsHelpers.get_asset_tools()
CUBE = eal.load_asset("/Engine/BasicShapes/Cube")
WORLD = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
_src = open(TOOLS + r"\build_lobby.py", encoding="utf-8").read()
_ns = {"unreal": unreal, "eal": eal, "mel": mel, "tools": tools, "MAT_DIR": MAT_DIR}
exec(_src[_src.index("def new_material"):_src.index("# couleurs en lineaire")], _ns)

def V(x, y, z):
    return unreal.Vector(float(x), float(y), float(z))

def LC(r, g, b):
    return unreal.LinearColor(r, g, b, 1)

def fin(a, label):
    a.set_actor_label(label)
    a.set_folder_path(F)
    a.set_editor_property("is_spatially_loaded", False)
    return a

def box(label, mat, c, size, collision=True):
    a = eas.spawn_actor_from_class(unreal.FortStaticMeshActor, c)
    comp = a.get_component_by_class(unreal.StaticMeshComponent)
    comp.set_static_mesh(CUBE)
    comp.set_material(0, mat)
    a.set_actor_scale3d(V(size.x / 100, size.y / 100, size.z / 100))
    if not collision:
        comp.set_collision_profile_name("NoCollision")
    return fin(a, label)

def fit(actor, w, d, h, center):
    o, e = actor.get_actor_bounds(False)
    s = actor.get_actor_scale3d()
    actor.set_actor_scale3d(V(s.x * w / (2 * e.x), s.y * d / (2 * e.y), s.z * h / (2 * e.z)))
    o, e = actor.get_actor_bounds(False)
    loc = actor.get_actor_location()
    actor.set_actor_location(V(center.x + loc.x - o.x, center.y + loc.y - o.y, center.z + loc.z - o.z), False, False)

def text(label, y, z, txt, size, v2=False):
    b = eas.spawn_actor_from_class(unreal.load_class(None, CLS["billboard_v2" if v2 else "billboard"]),
                                   V(XF + 10, y, z), unreal.Rotator(roll=0, pitch=0, yaw=90))
    for n, v in (("text", txt), ("TextSize", size)):
        try:
            b.set_editor_property(n, v)
        except Exception:
            pass
    # un Billboard fait ~3,6 x 1,6 m : sans ca il arrete les balles avant les formes
    for c in b.get_components_by_class(unreal.PrimitiveComponent):
        try:
            c.set_collision_profile_name("NoCollision")
        except Exception:
            pass
    return fin(b, label)

TEMPLATE = None
def shape(name, mat, y, z, w, h):
    """Forme a tirer : prop + Prop Manipulator (copie du modele)."""
    s = eas.spawn_actor_from_class(unreal.load_class(None, CLS["shape"]), V(XF + 15, y, z))
    fit(s, 16, w, h, V(XF + 10, y, z))
    for c in s.get_components_by_class(unreal.StaticMeshComponent):
        for i in range(max(1, c.get_num_materials())):
            c.set_material(i, mat)
    fin(s, "ZONE_1v1P_Shape" + name)
    # le prop garde sa texture damier : plaque coloree SANS collision devant
    # (les balles la traversent et touchent le prop)
    box("ZONE_1v1P_Skin" + name, mat, V(XF + 21, y, z), V(4, w + 2, h + 2), collision=False)
    pm =eas.duplicate_actor(TEMPLATE, WORLD, V(0, 0, 0))
    pm.set_actor_location(V(XF - 200, y, FLOOR_Z - 300), False, False)
    pm.set_editor_property("AdditionalPropsToManipulate", [s])
    fin(pm, "ZONE_1v1P_PM" + name)
    return pm.get_actor_label()

RESULT = {}
try:
    ACT = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
    # modele de Prop Manipulator (PV des props tres hauts), regle a la main dans Details
    TEMPLATE = ACT.get("ZONE_1v1P_PMTemplate") or ACT.get("PROBE_PM")
    TEMPLATE.set_editor_property("AdditionalPropsToManipulate", [])
    TEMPLATE.set_actor_location(V(CX + 600, 600, FLOOR_Z - 500), False, False)
    fin(TEMPLATE, "ZONE_1v1P_PMTemplate")
    n = 0
    for lab, a in ACT.items():
        if lab.startswith("ZONE_1v1P_") and lab not in KEEP:
            eas.destroy_actor(a); n += 1
    log("supprimes", n)

    m_white = eal.load_asset(MAT_DIR + "/M_Panel_White2")
    m_gray = eal.load_asset(MAT_DIR + "/M_Panel_Gray")
    m_black = eal.load_asset(MAT_DIR + "/M_Lobby_BlackMatte")
    m_red = _ns["opaque_mat"]("M_Panel_Red", LC(1.0, 0.05, 0.05), 0.4, LC(0.9, 0.02, 0.02))
    m_cyan = _ns["opaque_mat"]("M_Panel_Cyan", LC(0.0, 0.7, 1.0), 0.4, LC(0.0, 0.5, 0.8))

    # panneau : 6 m x 3 m
    box("ZONE_1v1P_Frame", m_black, V(PX - 8, 0, FLOOR_Z + 280), V(14, 640, 320))
    box("ZONE_1v1P_Board", m_white, V(PX, 0, FLOOR_Z + 280), V(20, 600, 290))
    for sy in (-1, 1):
        box("ZONE_1v1P_Post%d" % sy, m_black, V(PX - 8, sy * 240, FLOOR_Z + 70), V(30, 30, 140))
    box("ZONE_1v1P_SecSpeed", m_gray, V(XF + 1, -150, FLOOR_Z + 205), V(4, 280, 110))

    # ciel (rangee du haut)
    sky = []
    for i, (nm, rgb) in enumerate(SKY):
        y = 210 - i * 140
        m = _ns["opaque_mat"]("M_Panel_Sky2_" + nm, LC(*rgb), 0.5, LC(rgb[0] * 0.6, rgb[1] * 0.6, rgb[2] * 0.6))
        box("ZONE_1v1P_SkyFrame%d" % i, m_black, V(XF + 2, y, FLOOR_Z + 345), V(4, 104, 104), False)
        sky.append(shape("Sky%d" % i, m, y, FLOOR_Z + 345, 90, 90))

    # reset (en bas a gauche pour le joueur = +Y)
    reset = shape("Reset", m_red, 165, FLOOR_Z + 205, 200, 100)
    text("ZONE_1v1P_TxtReset", 165, FLOOR_Z + 160, "RESET", 40)

    # vitesse : < 100% >
    down = shape("SpeedDown", m_cyan, -50, FLOOR_Z + 205, 60, 70)
    text("ZONE_1v1P_TxtDown", -50, FLOOR_Z + 175, "<", 60)
    disp = text("ZONE_1v1P_SpeedDisplay", -150, FLOOR_Z + 180, "100%", 40, v2=True)
    up = shape("SpeedUp", m_cyan, -250, FLOOR_Z + 205, 60, 70)
    text("ZONE_1v1P_TxtUp", -250, FLOOR_Z + 175, ">", 60)

    RESULT = {"down": down, "up": up, "display": disp.get_actor_label(), "reset": reset,
              "explosive": "ZONE_1v1P_ResetExplosive", "sky": "ZONE_1v1P_Sky", "sky_shapes": sky,
              "panel": "ZONE_1v1P_PanelDevice",
              "selectors": ["ZONE_1v1_Speed%d_ClassSelector" % i for i in range(4)]}
    open(TOOLS + r"\build_panel_map.json", "w").write(json.dumps(RESULT, indent=1))
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    log("TERMINE")
except Exception:
    log("ERREUR", traceback.format_exc())
open(LOG_FILE, "w", encoding="utf-8").write("\n".join(lines))
