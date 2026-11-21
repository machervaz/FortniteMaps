# ============================================================================
#  build_lobby_portals.py - lobby de depart "4 portails neon en rang"
#  (AIM bleu / EDIT rouge / PIECE CONTROL blanc / 1V1 cyan), face au spawn (+X).
#  Chaque portail = cadre noir + bordure neon + voile lumineux translucide +
#  icone blanche + titre (billboard centre) + spot du plafond + lumiere coloree.
#  On TRAVERSE le portail : la Mutator Zone deja reliee au Verse (LOBBY_Zone_*)
#  est deplacee dans l'ouverture (transaction -> envoyee a la session).
#  Supprime les anciens cylindres (Socle/Holo/Billboard/Beacon/Spot). Relancable.
# ============================================================================
import unreal, math, traceback
TOOLS = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools"
MAT_DIR = "/5622d7d7-d1ca-438f-8a48-1286a48e2471/Lobby/Materials"
BB_CLS = "/Game/Creative/Devices/Billboard/BP_Creative_Billboard.BP_Creative_Billboard_C"
FLOOR = 1270.0
XP = 1500.0                 # plan des portails (mur du fond a x=2000)
OPEN_W, OPEN_H = 320.0, 580.0
NEON = 18.0                 # epaisseur de la bordure neon
CASE = 34.0                 # cadre noir autour
# vu depuis le spawn (regard +X), la gauche de l ecran est -Y
PORTALS = [  # titre, cle (LOBBY_Zone_<cle>), y, couleur lineaire, taille du texte, icone
    ("AIM", "Aim", -750.0, (0.0, 0.30, 1.0), 44, "aim"),
    ("EDIT", "Edit", -250.0, (1.0, 0.02, 0.06), 44, "edit"),
    ("PIECE CONTROL", "PieceControl", 250.0, (1.0, 1.0, 1.0), 26, "build"),
    ("1V1", "1v1", 750.0, (0.0, 0.85, 1.0), 44, "versus"),
]
OLD = ("LOBBY_Socle_", "LOBBY_Holo_", "LOBBY_Billboard_", "LOBBY_Beacon_", "LOBBY_Spot_", "LOBBY_Portal_")

eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
eal = unreal.EditorAssetLibrary
mel = unreal.MaterialEditingLibrary
tools = unreal.AssetToolsHelpers.get_asset_tools()
CUBE = eal.load_asset("/Engine/BasicShapes/Cube")
CYL = eal.load_asset("/Engine/BasicShapes/Cylinder")
L = []

def V(x, y, z):
    return unreal.Vector(float(x), float(y), float(z))

def LC(r, g, b):
    return unreal.LinearColor(r, g, b, 1.0)

def mat(name, build):
    path = MAT_DIR + "/" + name
    if eal.does_asset_exist(path):
        return eal.load_asset(path)
    m = tools.create_asset(name, MAT_DIR, unreal.Material, unreal.MaterialFactoryNew())
    build(m)
    mel.recompile_material(m)
    eal.save_loaded_asset(m)
    return m

def c3(m, col, y=0):
    e = mel.create_material_expression(m, unreal.MaterialExpressionConstant3Vector, -400, y)
    e.set_editor_property("constant", col)
    return e

def c1(m, v, y=0):
    e = mel.create_material_expression(m, unreal.MaterialExpressionConstant, -400, y)
    e.set_editor_property("r", float(v))
    return e

def neon_mat(name, rgb, k):
    def b(m):
        mel.connect_material_property(c3(m, LC(0, 0, 0), -200), "", unreal.MaterialProperty.MP_BASE_COLOR)
        mel.connect_material_property(c3(m, LC(rgb[0] * k, rgb[1] * k, rgb[2] * k), 200), "", unreal.MaterialProperty.MP_EMISSIVE_COLOR)
    return mat(name, b)

def fill_mat(name, rgb):
    # voile translucide : plus lumineux en bas (degrade vertical sur la hauteur du portail)
    def b(m):
        m.set_editor_property("blend_mode", unreal.BlendMode.BLEND_TRANSLUCENT)
        m.set_editor_property("shading_model", unreal.MaterialShadingModel.MSM_UNLIT)
        m.set_editor_property("two_sided", True)
        wp = mel.create_material_expression(m, unreal.MaterialExpressionWorldPosition, -1200, 0)
        mk = mel.create_material_expression(m, unreal.MaterialExpressionComponentMask, -1000, 0)
        for ch, on in (("r", False), ("g", False), ("b", True), ("a", False)):
            mk.set_editor_property(ch, on)
        mel.connect_material_expressions(wp, "", mk, "")
        sub = mel.create_material_expression(m, unreal.MaterialExpressionAdd, -850, 0)
        sub.set_editor_property("const_b", -FLOOR)
        mel.connect_material_expressions(mk, "", sub, "A")
        mul = mel.create_material_expression(m, unreal.MaterialExpressionMultiply, -700, 0)
        mul.set_editor_property("const_b", 1.0 / OPEN_H)
        mel.connect_material_expressions(sub, "", mul, "A")
        sat = mel.create_material_expression(m, unreal.MaterialExpressionSaturate, -550, 0)
        mel.connect_material_expressions(mul, "", sat, "")
        inv = mel.create_material_expression(m, unreal.MaterialExpressionOneMinus, -450, 0)
        mel.connect_material_expressions(sat, "", inv, "")
        # opacite 0.12 en haut -> 0.55 en bas
        om = mel.create_material_expression(m, unreal.MaterialExpressionMultiply, -300, 150)
        om.set_editor_property("const_b", 0.43)
        mel.connect_material_expressions(inv, "", om, "A")
        oa = mel.create_material_expression(m, unreal.MaterialExpressionAdd, -150, 150)
        oa.set_editor_property("const_b", 0.12)
        mel.connect_material_expressions(om, "", oa, "A")
        mel.connect_material_property(oa, "", unreal.MaterialProperty.MP_OPACITY)
        # emissif = couleur * (1 + 3 * bas)
        em = mel.create_material_expression(m, unreal.MaterialExpressionMultiply, -300, -150)
        em.set_editor_property("const_b", 3.0)
        mel.connect_material_expressions(inv, "", em, "A")
        ea = mel.create_material_expression(m, unreal.MaterialExpressionAdd, -200, -150)
        ea.set_editor_property("const_b", 1.0)
        mel.connect_material_expressions(em, "", ea, "A")
        ec = mel.create_material_expression(m, unreal.MaterialExpressionMultiply, -100, -150)
        mel.connect_material_expressions(ea, "", ec, "A")
        mel.connect_material_expressions(c3(m, LC(*rgb), -300), "", ec, "B")
        mel.connect_material_property(ec, "", unreal.MaterialProperty.MP_EMISSIVE_COLOR)
    return mat(name, b)

def tag(a, label):
    a.set_actor_label("LOBBY_Portal_" + label)
    a.set_folder_path("Lobby/Portals")
    a.set_editor_property("is_spatially_loaded", False)
    return a

def box(label, m, c, size, collision=False, roll=0.0, mesh=None, pitch=0.0):
    a = eas.spawn_actor_from_class(unreal.FortStaticMeshActor, c, unreal.Rotator(roll=roll, pitch=pitch, yaw=0.0))
    comp = a.get_component_by_class(unreal.StaticMeshComponent)
    comp.set_static_mesh(mesh or CUBE)
    comp.set_material(0, m)
    a.set_actor_scale3d(V(size.x / 100, size.y / 100, size.z / 100))
    if not collision:
        comp.set_collision_profile_name("NoCollision")
    comp.set_editor_property("cast_shadow", False)
    return tag(a, label)

def icon(kind, key, y, zc, white, black):
    x = XP - 6        # devant le voile
    n = [0]
    def bar(w, h, dy=0.0, dz=0.0, roll=0.0, m=None, dx=0.0):
        n[0] += 1
        return box("%s_Icon%d" % (key, n[0]), m or white, V(x + dx, y + dy, zc + dz), V(4, w, h), roll=roll)
    def disc(d, m, dx=0.0):
        n[0] += 1
        return box("%s_Icon%d" % (key, n[0]), m, V(x + dx, y, zc), V(d, d, 4), mesh=CYL, pitch=90.0)
    if kind == "aim":                       # viseur : anneau + croix + point
        disc(150, white)
        disc(122, black, dx=-2)
        bar(8, 190, dx=-4)
        bar(190, 8, dx=-4)
        bar(18, 18, dx=-6)
    elif kind == "edit":                    # crayon
        bar(26, 150, dy=8, dz=8, roll=45.0)
        bar(20, 20, dy=-50, dz=-50, roll=45.0)
        bar(26, 14, dy=58, dz=58, roll=45.0, dx=-2)
    elif kind == "build":                   # pyramide de blocs 3-2-1
        s, g = 44.0, 8.0
        for row, cnt in enumerate((3, 2, 1)):
            for i in range(cnt):
                dy = (i - (cnt - 1) / 2.0) * (s + g)
                bar(s, s, dy=dy, dz=(row - 1) * (s + g))
    elif kind == "versus":                  # deux epees croisees
        for sgn in (1, -1):
            bar(14, 190, roll=45.0 * sgn)
            bar(60, 12, dy=sgn * 42, dz=-42, roll=45.0 * sgn, dx=-2)

def billboard(key, title, size, y, zc):
    b = eas.spawn_actor_from_class(unreal.load_class(None, BB_CLS), V(XP - 15, y, zc - 57),
                                   unreal.Rotator(roll=0, pitch=0, yaw=-90.0))
    for n, v in (("text", title), ("TextSize", size), ("TextJustification", unreal.TextJustify.CENTER),
                 ("TextColor", LC(1, 1, 1))):
        try:
            b.set_editor_property(n, v)
        except Exception as ex:
            L.append("billboard %s %s : %s" % (key, n, ex))
    for c in b.get_components_by_class(unreal.PrimitiveComponent):
        try:
            c.set_collision_profile_name("NoCollision")
        except Exception:
            pass
    return tag(b, key + "_Title")

try:
    ACT = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
    n = 0
    for lab, a in list(ACT.items()):
        if lab.startswith(OLD):
            eas.destroy_actor(a); n += 1
    L.append("anciens elements supprimes : %d" % n)
    black = eal.load_asset(MAT_DIR + "/M_Lobby_BlackMatte")
    white = eal.load_asset(MAT_DIR + "/M_Lobby_LedWhite")
    zt = FLOOR + OPEN_H          # haut de l'ouverture
    zc = FLOOR + OPEN_H / 2
    hw = OPEN_W / 2
    with unreal.ScopedEditorTransaction("Lobby : portails neon"):
        for title, key, y, rgb, tsize, ic in PORTALS:
            k = 14.0 if rgb != (1.0, 1.0, 1.0) else 9.0
            neon = neon_mat("M_Portal_Neon_" + key, rgb, k)
            frgb = (0.07, 0.07, 0.09) if rgb == (1.0, 1.0, 1.0) else rgb
            fill = fill_mat(("M_Portal_Fill3_" if key == "PieceControl" else "M_Portal_Fill_") + key, frgb)
            # cadre noir (montants + linteau), neon a l'interieur
            for s in (1, -1):
                box(key + "_Case%d" % s, black, V(XP, y + s * (hw + NEON + CASE / 2), FLOOR + (OPEN_H + NEON + CASE) / 2),
                    V(50, CASE, OPEN_H + NEON + CASE), collision=True)
                box(key + "_Neon%d" % s, neon, V(XP - 4, y + s * (hw + NEON / 2), FLOOR + (OPEN_H + NEON) / 2),
                    V(46, NEON, OPEN_H + NEON))
            box(key + "_CaseTop", black, V(XP, y, zt + NEON + CASE / 2), V(50, OPEN_W + 2 * (NEON + CASE), CASE), collision=True)
            box(key + "_NeonTop", neon, V(XP - 4, y, zt + NEON / 2), V(46, OPEN_W + 2 * NEON, NEON))
            box(key + "_NeonSill", neon, V(XP - 4, y, FLOOR + 2), V(46, OPEN_W + 2 * NEON, 4))
            # liseré interieur fin
            for s in (1, -1):
                box(key + "_Line%d" % s, neon, V(XP - 2, y + s * (hw - 22), zc), V(3, 4, OPEN_H - 44))
            for nm, zz in (("LineTop", zt - 22), ("LineBot", FLOOR + 22)):
                box(key + "_" + nm, neon, V(XP - 2, y, zz), V(3, OPEN_W - 40, 4))
            # voile lumineux
            box(key + "_Fill", fill, V(XP, y, zc), V(2, OPEN_W - 4, OPEN_H - 4))
            # lueur au sol devant le portail
            box(key + "_FloorGlow", neon, V(XP - 160, y, FLOOR + 1), V(260, OPEN_W + 2 * NEON, 2))
            icon(ic, key, y, FLOOR + 300, white, black)
            billboard(key, title, tsize, y, zt - 95)
            # lumieres : spot du plafond + lumiere coloree devant
            src = V(XP - 500, y, FLOOR + 860)   # sous le plafond du couloir (9 m)
            sp = eas.spawn_actor_from_class(unreal.SpotLight, src, unreal.MathLibrary.find_look_at_rotation(src, V(XP, y, FLOOR + 250)))
            sc = sp.get_component_by_class(unreal.SpotLightComponent)
            sc.set_light_color(LC(1, 1, 1)); sc.set_intensity(70.0); sc.set_attenuation_radius(1800.0)
            sc.set_outer_cone_angle(18.0); sc.set_inner_cone_angle(8.0)
            tag(sp, key + "_Spot")
            pl = eas.spawn_actor_from_class(unreal.PointLight, V(XP - 180, y, FLOOR + 160))
            lc = pl.get_component_by_class(unreal.PointLightComponent)
            lc.set_light_color(LC(*[max(v, 0.05) for v in rgb])); lc.set_intensity(25.0); lc.set_attenuation_radius(700.0)
            tag(pl, key + "_Glow")
            # Mutator Zone existante (reliee au Verse) -> dans l'ouverture
            z = ACT["LOBBY_Zone_" + key]
            z.modify()
            for c in z.get_components_by_class(unreal.SceneComponent):
                c.modify()
            z.set_actor_rotation(unreal.Rotator(0, 0, 0), False)
            o, e = z.get_actor_bounds(False)
            s3 = z.get_actor_scale3d()
            z.set_actor_scale3d(V(s3.x * 120 / (2 * e.x), s3.y * (OPEN_W - 40) / (2 * e.y), s3.z * (OPEN_H - 40) / (2 * e.z)))
            o, e = z.get_actor_bounds(False)
            p = z.get_actor_location()
            z.set_actor_location(V(p.x + XP - o.x, p.y + y - o.y, p.z + (FLOOR + 20) - (o.z - e.z)), False, False)
            o, e = z.get_actor_bounds(False)
            L.append("%s : zone x=[%.0f..%.0f] y=[%.0f..%.0f] z=[%.0f..%.0f]" % (key, o.x - e.x, o.x + e.x, o.y - e.y, o.y + e.y, o.z - e.z, o.z + e.z))
    L.append("acteurs LOBBY_Portal_ : %d" % sum(1 for a in eas.get_all_level_actors() if a.get_actor_label().startswith("LOBBY_Portal_")))
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE")
except Exception:
    L.append(traceback.format_exc())
open(TOOLS + r"\build_lobby_portals_log.txt", "w").write("\n".join(L))
