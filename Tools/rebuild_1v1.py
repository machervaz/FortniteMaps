# ============================================================================
#  rebuild_1v1.py - nouvelle zone 1v1 (d'apres l'image de reference) :
#  plateforme ronde turquoise brillante, anneau blanc lumineux, mer turquoise
#  autour, deux rampes violettes en V au centre.
#  Supprime l'ancienne arene (sol, murs, LED). Garde et replace : pad
#  d'arrivee, cylindre RETOUR LOBBY, boutons de vitesse.
#  Relancable (supprime ZONE_1v1N_*).
# ============================================================================
import unreal, math, traceback

TOOLS = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools"
LOG_FILE = TOOLS + r"\rebuild_1v1_log.txt"
ROOT = "/5622d7d7-d1ca-438f-8a48-1286a48e2471"
MAT_DIR = ROOT + "/Lobby/Materials"
FLOOR_Z = 1270.0
CX, CY = -20000.0, 0.0        # centre de la zone 1v1
DISC_D = 4800.0               # diametre de la plateforme (48 m)
RIM = 200.0                   # largeur de l'anneau blanc
RAMP_RUN, RAMP_RISE = 512.0, 384.0   # une rampe Fortnite : 1 case, 1 etage
RAMP_ROLL = 1.0               # mettre -1 si le V est a l'envers

OLD = ["ZONE_1v1_Floor", "ZONE_1v1_LedA", "ZONE_1v1_LedB", "ZONE_1v1_LedC", "ZONE_1v1_LedD", "ZONE_1v1_MidLine"]
OLD_PREFIX = ["ZONE_1v1_Wall"]   # murs + LED des murs

lines = []
def log(*a):
    lines.append(" ".join(str(x) for x in a))

eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
eal = unreal.EditorAssetLibrary
mel = unreal.MaterialEditingLibrary
tools = unreal.AssetToolsHelpers.get_asset_tools()
CUBE = eal.load_asset("/Engine/BasicShapes/Cube")
CYL = eal.load_asset("/Engine/BasicShapes/Cylinder")
_src = open(TOOLS + r"\build_lobby.py", encoding="utf-8").read()
_ns = {"unreal": unreal, "eal": eal, "mel": mel, "tools": tools, "MAT_DIR": MAT_DIR}
exec(_src[_src.index("def new_material"):_src.index("# couleurs en lineaire")], _ns)

def V(x, y, z):
    return unreal.Vector(float(x), float(y), float(z))

def LC(r, g, b):
    return unreal.LinearColor(r, g, b, 1)

def box(label, mesh, mat, c, size, rot=None, collision=True):
    a = eas.spawn_actor_from_class(unreal.FortStaticMeshActor, c, rot or unreal.Rotator(0, 0, 0))
    comp = a.get_component_by_class(unreal.StaticMeshComponent)
    comp.set_static_mesh(mesh)
    comp.set_material(0, mat)
    a.set_actor_scale3d(V(size.x / 100, size.y / 100, size.z / 100))
    if not collision:
        comp.set_collision_profile_name("NoCollision")
        comp.set_editor_property("cast_shadow", False)
    a.set_actor_label(label)
    a.set_folder_path("Zones/1v1/Arena")
    a.set_editor_property("is_spatially_loaded", False)
    return a

try:
    ACT = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
    n = 0
    for lab, a in list(ACT.items()):
        if lab in OLD or any(lab.startswith(p) for p in OLD_PREFIX) or lab.startswith("ZONE_1v1N_"):
            eas.destroy_actor(a); ACT.pop(lab); n += 1
    log("ancienne arene supprimee :", n)

    # materiaux
    m_water = _ns["opaque_mat"]("M_1v1_Water2", LC(0.0, 0.55, 0.75), 0.04, LC(0.0, 0.12, 0.16))
    m_sea = _ns["opaque_mat"]("M_1v1_Sea", LC(0.0, 0.35, 0.55), 0.03, LC(0.0, 0.12, 0.18))
    m_rim = _ns["opaque_mat"]("M_1v1_Rim", LC(1, 1, 1), 0.3, LC(12, 12, 14))
    m_ramp = _ns["opaque_mat"]("M_1v1_RampPurple", LC(0.25, 0.03, 0.8), 0.3, LC(0.12, 0.01, 0.35))

    # mer (plan de 300 m, sans chevaucher le lobby ni les zones Edit / Aim)
    # anneau blanc (cylindre un peu plus grand, juste sous la plateforme)
    box("ZONE_1v1N_Rim", CYL, m_rim, V(CX, CY, FLOOR_Z - 102), V(DISC_D + 2 * RIM, DISC_D + 2 * RIM, 200))
    # plateforme turquoise
    box("ZONE_1v1N_Disc", CYL, eal.load_asset(MAT_DIR + "/M_Lobby_BlackGloss"),V(CX, CY, FLOOR_Z - 100), V(DISC_D, DISC_D, 200))

    # rampes en V : bas au centre, montent vers -Y et +Y
    L = math.hypot(RAMP_RUN, RAMP_RISE)
    ang = math.degrees(math.atan2(RAMP_RISE, RAMP_RUN))
    for side in (-1, 1):
        c = V(CX, CY + side * RAMP_RUN / 2, FLOOR_Z + RAMP_RISE / 2)
        rot = unreal.Rotator(roll=RAMP_ROLL * side * -ang, pitch=0.0, yaw=0.0)
        box("ZONE_1v1N_Ramp%d" % side, CUBE, m_ramp, c, V(RAMP_RUN, L, 24), rot)
        # bord lumineux en haut de la rampe
        box("ZONE_1v1N_RampEdge%d" % side, CUBE, m_rim, V(CX, CY + side * RAMP_RUN, FLOOR_Z + RAMP_RISE + 6),
            V(RAMP_RUN, 16, 16), collision=False)

    # lumieres douces turquoise / violettes
    for i, (dx, dy, col) in enumerate([(1500, 1500, (0.3, 0.9, 1)), (-1500, -1500, (0.3, 0.9, 1)),
                                       (1500, -1500, (0.8, 0.4, 1)), (-1500, 1500, (0.8, 0.4, 1))]):
        pl = eas.spawn_actor_from_class(unreal.PointLight, V(CX + dx, CY + dy, FLOOR_Z + 600))
        lc = pl.get_component_by_class(unreal.PointLightComponent)
        lc.set_light_color(LC(*col)); lc.set_intensity(40.0); lc.set_attenuation_radius(3000.0)
        pl.set_actor_label("ZONE_1v1N_Light%d" % i); pl.set_folder_path("Zones/1v1/Arena")
        pl.set_editor_property("is_spatially_loaded", False)

    # replacer arrivee, retour lobby et boutons sur la plateforme (cote lobby = +X)
    def move(label, x, y, z=None):
        a = ACT.get(label)
        if not a:
            log("introuvable", label); return
        p = a.get_actor_location()
        a.set_actor_location(V(x, y, p.z if z is None else z), False, False)

    ax = CX + 1700
    move("ZONE_1v1_Arrival", CX + 1000, 0)      # pres du panneau et des rampes
    old = ACT["ZONE_1v1_ReturnSocle"].get_actor_location()
    dxy = (CX + 1100 - old.x, -1300 - old.y)    # bien a l'interieur de la plateforme
    for lab in ("ZONE_1v1_ReturnSocle", "ZONE_1v1_ReturnHolo", "ZONE_1v1_ReturnZone", "ZONE_1v1_ReturnTitle"):
        a = ACT.get(lab)
        if a:
            p = a.get_actor_location()
            a.set_actor_location(V(p.x + dxy[0], p.y + dxy[1], p.z), False, False)
    move("ZONE_1v1_Title", ax + 200, 0)
    for i in range(4):
        y = 800 + i * 400
        b = ACT.get("ZONE_1v1_Speed%d_Button" % i)
        if b:
            b.set_actor_location(V(ax, y, FLOOR_Z), False, False)
        t = ACT.get("ZONE_1v1_Speed%d_Title" % i)
        if t:
            t.set_actor_location(V(ax, y, FLOOR_Z + 260), False, False)
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    log("TERMINE")
except Exception:
    log("ERREUR", traceback.format_exc())
open(LOG_FILE, "w", encoding="utf-8").write("\n".join(lines))
