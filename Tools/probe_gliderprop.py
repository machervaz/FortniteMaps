import unreal, traceback
L = []
try:
    ar = unreal.AssetRegistryHelpers.get_asset_registry()
    for ad in ar.get_assets_by_class(unreal.TopLevelAssetPath("/Script/Engine", "BlueprintGeneratedClass"), True):
        nm = str(ad.asset_name); low = nm.lower(); pk = str(ad.package_name)
        if (pk.startswith("/CRG_") or pk.startswith("/CRP_") or "Gallery" in pk or nm.startswith("CP_") or nm.startswith("PBW")) and any(k in low for k in ("glider", "umbrella", "parachute", "parasol", "kite", "hangglid", "wing")):
            L.append("%s | %s" % (nm, pk))
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\probe_gliderprop_log.txt", "w").write("\n".join(sorted(L)) or "rien")
