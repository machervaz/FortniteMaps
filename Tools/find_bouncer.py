import unreal, traceback
TOOLS = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools"
L = []
try:
    ar = unreal.AssetRegistryHelpers.get_asset_registry()
    keys = ("bouncer", "bounce", "trampoline", "mattress", "launchpad", "launch_pad", "jumppad", "jump_pad", "impulse", "springboard", "boostpad", "boost_pad")
    flt = unreal.ARFilter(class_paths=[unreal.TopLevelAssetPath("/Script/Engine", "BlueprintGeneratedClass")], recursive_classes=True)
    assets = ar.get_assets(flt)
    n = 0
    for a in assets:
        p = str(a.package_name)
        if p.startswith("/Game") or p.startswith("/Engine"):
            continue
        nm = str(a.asset_name).lower()
        if any(k in nm for k in keys):
            n += 1
            if n <= 200:
                L.append(p)
    L.append("total %d (sur %d blueprints)" % (n, len(assets)))
except Exception:
    L.append(traceback.format_exc())
open(TOOLS + r"\find_bouncer_log.txt", "w").write("\n".join(L))
