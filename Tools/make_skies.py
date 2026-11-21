# 4 Skydomes (violet, jour, nuit, rose) pour les carres du panneau 1v1.
# Copies de ZONE_1v1P_Sky (meme volume sur l'arene). Relancable.
import unreal, json, traceback
TOOLS = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools"
def C(r, g, b):
    return unreal.LinearColor(r, g, b, 1.0)
PRESETS = [  # (nom, haut, milieu, bas, brume, intensite soleil, lumiere ambiante)
    ("Violet", C(0.25, 0.05, 0.8), C(0.6, 0.25, 1.0), C(0.9, 0.6, 1.0), C(0.7, 0.45, 0.95), 100.0, 20.0),
    ("Jour", C(0.05, 0.25, 1.0), C(0.35, 0.6, 1.0), C(0.85, 0.92, 1.0), C(0.8, 0.88, 1.0), 100.0, 20.0),
    ("Nuit", C(0.0, 0.0, 0.01), C(0.01, 0.01, 0.03), C(0.03, 0.03, 0.07), C(0.02, 0.02, 0.05), 10.0, 5.0),
    ("Rose", C(0.4, 0.1, 0.6), C(1.0, 0.35, 0.6), C(1.0, 0.7, 0.5), C(1.0, 0.55, 0.65), 100.0, 20.0),
]
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
L = []
try:
    ACT = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
    base = ACT.get("ZONE_1v1P_Sky") or ACT.get("ZONE_1v1P_SkyDomeViolet")
    labels = []
    for i, (nm, top, mid, bot, fog, sun, amb) in enumerate(PRESETS):
        lab = "ZONE_1v1P_SkyDome" + nm
        a = ACT.get(lab)
        if a is None:
            a = base if i == 0 else eas.duplicate_actor(base, world, unreal.Vector(0, 0, 0))
            a.set_actor_location(base.get_actor_location(), False, False)
        for k, v in (("SkydomeTopColor", top), ("SkydomeMiddleColor", mid), ("SkydomeBottomColor", bot),
                     ("HorizonFogColor", fog), ("HorizonFogDensity", 100.0), ("LightSourceIntensity", sun),
                     ("AmbientLightIntensity_Option", amb)):
            try:
                a.set_editor_property(k, v)
            except Exception as e:
                L.append("  %s %s : %s" % (lab, k, e))
        a.set_actor_label(lab)
        a.set_folder_path("Zones/1v1/Panel")
        a.set_editor_property("is_spatially_loaded", False)
        labels.append(lab)
    m = json.load(open(TOOLS + r"\build_panel_map.json"))
    m["sky_domes"] = labels
    json.dump(m, open(TOOLS + r"\build_panel_map.json", "w"), indent=1)
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    L.append("ok %s" % labels)
except Exception:
    L.append(traceback.format_exc())
open(TOOLS + r"\make_skies_log.txt", "w").write("\n".join(L))
