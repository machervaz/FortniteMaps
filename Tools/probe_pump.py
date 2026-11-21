import unreal, traceback
L = []
try:
    ar = unreal.AssetRegistryHelpers.get_asset_registry()
    flt = unreal.ARFilter(package_paths=["/Game"], recursive_paths=True)
    n = 0
    for ad in ar.get_assets(flt):
        nm = str(ad.asset_name)
        if nm.startswith("WID_") and "Shotgun" in nm:
            L.append("%s | %s | %s" % (nm, ad.package_name, ad.asset_class_path.asset_name if hasattr(ad, "asset_class_path") else ad.asset_class))
            n += 1
    L.append("total %d" % n)
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    a = [x for x in eas.get_all_level_actors() if x.get_actor_label() == "ZONE_Aim_Loadout"][0]
    comp = [c for c in a.get_components_by_class(unreal.ActorComponent) if c.get_name() == "PickupItemList"][0]
    for pn in ("ItemList", "Items", "ItemDefinitions", "PickupItems", "ItemData", "ItemsToGrant", "Item List", "ItemEntries", "Inventory"):
        try:
            L.append("comp %s = %s" % (pn, comp.get_editor_property(pn)))
        except Exception as ex:
            pass
    for pn in ("ItemList", "Items", "ItemDefinitions", "ItemsToGrant", "ItemDefinitionList"):
        try:
            L.append("actor %s = %s" % (pn, a.get_editor_property(pn)))
        except Exception:
            pass
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\probe_pump_log.txt", "w").write("\n".join(L))
