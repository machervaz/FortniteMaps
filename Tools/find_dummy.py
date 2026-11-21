import unreal, traceback
TOOLS = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools"
L = []
try:
    ar = unreal.AssetRegistryHelpers.get_asset_registry()
    keys = ("dummy", "mannequin", "trainingdummy", "practicedummy", "targetdummy")
    seen = 0
    for path in ("/Game", "/CRG_Props", "/CreativeCoreDevices", "/VerseDevices", "/CRD_PropManipulationDevice"):
        try:
            assets = ar.get_assets_by_path(path, recursive=True)
        except Exception as ex:
            L.append("%s : %s" % (path, ex)); continue
        for a in assets:
            n = str(a.asset_name).lower()
            if any(k in n for k in keys):
                seen += 1
                if seen <= 150:
                    L.append("%s  [%s]" % (a.package_name, a.asset_class_path.asset_name if hasattr(a, "asset_class_path") else a.asset_class))
    L.append("total %d" % seen)
except Exception:
    L.append(traceback.format_exc())
open(TOOLS + r"\find_dummy_log.txt", "w").write("\n".join(L))
