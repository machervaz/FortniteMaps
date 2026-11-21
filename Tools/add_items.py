# Remplit l'Item Granter de la zone 1v1 : SCAR, pompe et SMG legendaires
import unreal, traceback
OUT = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\add_items_log.txt"
GRANTER = "ZONE_1v1_Loadout"
ITEMS = [
    "/Game/Athena/Items/Weapons/WID_Assault_AutoHigh_Athena_SR_Ore_T03.WID_Assault_AutoHigh_Athena_SR_Ore_T03",
    "/Game/Athena/Items/Weapons/WID_Shotgun_Standard_Athena_SR_Ore_T03.WID_Shotgun_Standard_Athena_SR_Ore_T03",
]   # (le pistolet automatique est refuse par UEFN : "reference illegale")
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
L = []
try:
    g = [a for a in eas.get_all_level_actors() if a.get_actor_label() == GRANTER][0]
    holders = [g] + list(g.get_components_by_class(unreal.ActorComponent))
    for h in holders:
        try:
            lst = h.get_editor_property("ItemListData")
        except Exception:
            continue
        L.append("liste trouvee sur %s (%d elements)" % (h.get_name(), len(lst)))
        template = lst[0]
        new = []
        for path in ITEMS:
            e = unreal.StructBase.cast(template) if False else type(template)()
            for prop in ("ItemDefinition", "item_definition"):
                try:
                    e.set_editor_property(prop, unreal.load_object(None, path)); break
                except Exception:
                    pass
            try:
                e.set_editor_property("Quantity", 1)
            except Exception:
                pass
            new.append(e)
        h.set_editor_property("ItemListData", new)
        L.append("ok : %d objets" % len(h.get_editor_property("ItemListData")))
        break
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
except Exception:
    L.append(traceback.format_exc())
open(OUT, "w").write("\n".join(L))
