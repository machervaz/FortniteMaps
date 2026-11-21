import unreal, traceback
L = []
try:
    ar = unreal.AssetRegistryHelpers.get_asset_registry()
    for ad in ar.get_assets_by_class(unreal.TopLevelAssetPath("/Script/Engine", "BlueprintGeneratedClass"), True):
        nm = str(ad.asset_name)
        if "sentry" in nm.lower() or "sentinel" in nm.lower():
            L.append("%s | %s" % (nm, ad.package_name))
    L.append("fin")
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\probe_sentry_log.txt", "w").write("\n".join(L))
