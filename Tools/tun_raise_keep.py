# Tunnels d'edit : remonte TOUT ce qui est dans la zone des tunnels (structure TUN_ + pieces
# ajoutees par le joueur au telephone) de 118 cm (sol 1152 -> 1270, comme avant), sans rien
# reconstruire. Puis : pieces en bois -> dans le Data Layer du reset (le reset remet l'interieur
# actuel) + support force ; autres pieces de construction -> indestructibles.
import unreal, traceback, collections
TOOLS = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools"
DZ = 118.0
BOX = (-3200, 3200, -47700, -23000)
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
dls = unreal.get_editor_subsystem(unreal.DataLayerEditorSubsystem)
L = []
try:
    dl = unreal.load_asset("/5622d7d7-d1ca-438f-8a48-1286a48e2471/Tunnels/DL_TunnelBuilds")
    inst = [i for i in dls.get_all_data_layers() if i.get_asset() == dl][0]
    moved, wood, solid = 0, [], 0
    user = collections.Counter()
    with unreal.ScopedEditorTransaction("Tunnels remontes (interieur garde)"):
        for a in eas.get_all_level_actors():
            lab = a.get_actor_label()
            p = a.get_actor_location()
            if lab.startswith("ZONE_") or p.z < -10000 or not (BOX[0] < p.x < BOX[1] and BOX[2] < p.y < BOX[3]):
                continue
            if isinstance(a, unreal.WorldSettings) or a.get_class().get_name() in ("WorldDataLayers", "LevelBounds"):
                continue
            a.modify()
            for c in a.get_components_by_class(unreal.SceneComponent):
                c.modify()
            a.set_actor_location(unreal.Vector(p.x, p.y, p.z + DZ), False, False)
            try:
                a.set_editor_property("is_spatially_loaded", False)
            except Exception:
                pass
            moved += 1
            n = a.get_class().get_name()
            if not lab.startswith("TUN_"):
                user[n] += 1
            if n.startswith("PBWA_"):
                a.set_editor_property("forcibly_structurally_supported", True)
                wood.append(a)
            elif isinstance(a, unreal.BuildingActor) and "Device" not in n:
                try:
                    a.set_editor_property("bIsInvulnerable", True)
                    a.set_editor_property("bCanBeDamaged", False)
                    a.set_editor_property("forcibly_structurally_supported", True)
                    solid += 1
                except Exception:
                    pass
        L.append("ajout bois au data layer : %s" % dls.add_actors_to_data_layer(wood, inst))
    L.append("deplaces : %d, bois (reset) : %d, autres pieces indestructibles : %d" % (moved, len(wood), solid))
    L.append("pieces ajoutees par le joueur (hors TUN_) :")
    for n, c in user.most_common():
        L.append("   %4d %s" % (c, n))
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("TERMINE")
except Exception:
    L.append(traceback.format_exc())
open(TOOLS + r"\tun_raise_keep_log.txt", "w").write("\n".join(L))
