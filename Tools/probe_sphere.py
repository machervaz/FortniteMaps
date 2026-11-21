import unreal
reg = unreal.AssetRegistryHelpers.get_asset_registry()
flt = unreal.ARFilter(class_paths=[unreal.TopLevelAssetPath("/Script/Engine", "BlueprintGeneratedClass")])
L = []
for ad in reg.get_assets(flt):
    n = str(ad.asset_name)
    if n.startswith("CP_") and ("Sphere" in n or "Dome" in n or "Ball" in n):
        L.append(str(ad.package_name))
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\probe_sphere_out.txt", "w").write("\n".join(sorted(L)[:60]))
