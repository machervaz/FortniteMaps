import unreal, traceback
TOOLS = r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools"
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
L = []
try:
    for a in eas.get_all_level_actors():
        lab = a.get_actor_label()
        if lab in ("ZONE_1v1P_TxtReset", "ZONE_1v1P_TxtDown", "ZONE_1v1P_SpeedDisplay", "ZONE_1v1P_SkinReset"):
            L.append("%s loc=%s rot=%s" % (lab, a.get_actor_location(), a.get_actor_rotation()))
            for c in a.get_components_by_class(unreal.SceneComponent):
                line = "   %s (%s)" % (c.get_name(), c.get_class().get_name())
                try:
                    o, e, r = unreal.SystemLibrary.get_component_bounds(c)
                    line += " c=(%.0f,%.0f,%.0f) e=(%.0f,%.0f,%.0f)" % (o.x, o.y, o.z, e.x, e.y, e.z)
                except Exception as ex:
                    line += " %s" % ex
                if isinstance(c, unreal.TextRenderComponent):
                    for p in ("horizontal_alignment", "vertical_alignment", "world_size", "text"):
                        try:
                            line += " %s=%s" % (p, c.get_editor_property(p))
                        except Exception:
                            pass
                L.append(line)
            for p in ("TextSize", "text", "Text"):
                try:
                    L.append("   prop %s=%s" % (p, a.get_editor_property(p)))
                except Exception:
                    pass
except Exception:
    L.append(traceback.format_exc())
open(TOOLS + r"\txt_info_log.txt", "w").write("\n".join(L))
