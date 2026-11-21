import unreal, traceback
L = []
try:
    ar = unreal.AssetRegistryHelpers.get_asset_registry()
    for ad in ar.get_assets_by_class(unreal.TopLevelAssetPath("/Script/Engine", "BlueprintGeneratedClass"), True):
        nm = str(ad.asset_name); low = nm.lower()
        if nm.startswith("Device_") and any(k in low for k in ("guard", "bot", "npc", "spawner", "ai")) and "item" not in low:
            L.append("%s | %s" % (nm, ad.package_name))
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\probe_botdev_log.txt", "w").write("\n".join(sorted(L)))
