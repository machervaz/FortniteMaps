import unreal
ar = unreal.AssetRegistryHelpers.get_asset_registry()
L = []
for d in ar.get_all_assets():
    n = str(d.asset_name)
    if (("Beacon" in n or "MapIndicator" in n or "Map_Indicator" in n or "Waypoint" in n) and "Device" in n) and str(d.asset_class_path.asset_name) in ("Blueprint", "BlueprintGeneratedClass"):
        L.append("%s | %s" % (d.package_name, d.asset_class_path.asset_name))
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\find_beacon_log.txt","w").write("\n".join(L) or "rien")
