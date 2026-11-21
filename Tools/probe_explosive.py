import unreal, traceback
L = []
try:
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    for a in eas.get_all_level_actors():
        if a.get_actor_label() in ("TUN_Explosive0", "PCX_ResetExplosive", "TUN_ReloadSequence", "PCX_ReloadSequence"):
            L.append("%s loc=%s" % (a.get_actor_label(), a.get_actor_location()))
            for p in ("Blast Radius", "BlastRadius", "Structure Damage", "Player Damage", "Damage", "Visible During Game", "VisibleDuringGame", "Enabled", "Sequence", "Damage Structures", "Affects Players"):
                try:
                    L.append("   %s = %s" % (p, a.get_editor_property(p)))
                except Exception:
                    pass
except Exception:
    L.append(traceback.format_exc())
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\probe_explosive_log.txt", "w").write("\n".join(L))
