# Deplace toute la zone 1v1 (acteurs ZONE_1v1*) de DX en X : loin du lobby et des
# autres zones -> avec la brume du ciel 1v1, on ne les voit plus depuis l'arene.
# Ne deplace qu'une fois (marqueur dans move_1v1_done.txt).
import unreal, os, traceback
TOOLS = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools"
DX = -35000.0                     # centre 1v1 : -20000 -> -55000 (550 m du lobby)
DONE = TOOLS + r"\move_1v1_done.txt"
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
L = []
try:
    if os.path.exists(DONE):
        L.append("deja deplace")
    else:
        n = 0
        for a in eas.get_all_level_actors():
            if a.get_actor_label().startswith("ZONE_1v1"):
                p = a.get_actor_location()
                a.set_actor_location(unreal.Vector(p.x + DX, p.y, p.z), False, False)
                n += 1
        open(DONE, "w").write("DX=%s" % DX)
        L.append("acteurs deplaces : %d" % n)
        unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    # test : un prop manipulator pour voir ses reglages
    reg = unreal.AssetRegistryHelpers.get_asset_registry()
    flt = unreal.ARFilter(class_paths=[unreal.TopLevelAssetPath("/Script/Engine", "BlueprintGeneratedClass")])
    for ad in reg.get_assets(flt):
        n_ = str(ad.asset_name)
        if "PropManipulator" in n_ or "Prop_Manipulator" in n_:
            L.append("classe " + str(ad.package_name))
except Exception:
    L.append(traceback.format_exc())
open(TOOLS + r"\move_1v1_log.txt", "w").write("\n".join(L))
