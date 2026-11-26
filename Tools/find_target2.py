import unreal
ar = unreal.AssetRegistryHelpers.get_asset_registry()
L = []
for d in ar.get_assets_by_path("/Game/Creative/Devices/ShootingTargets", True):
    L.append("%s | %s" % (d.package_name, d.asset_class_path.asset_name))
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\find_target2_log.txt","w").write("\n".join(sorted(L)) or "rien")
