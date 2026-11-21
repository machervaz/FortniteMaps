import unreal, traceback
L = []
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
a = None
try:
    a = eas.spawn_actor_from_class(unreal.load_class(None, "/CreativeCoreDevices/Device_ItemGranter_V2.Device_ItemGranter_V2_C"), unreal.Vector(0, 0, -5000))
    comp = [c for c in a.get_components_by_class(unreal.ActorComponent) if c.get_name() == "PickupItemList"][0]
    wid = unreal.load_asset("/Game/Athena/Items/Weapons/WID_Shotgun_Standard_Athena_SR_Ore_T03")
    L.append("wid = %s" % wid)
    for val in ([wid, wid],):
        try:
            comp.set_editor_property("ItemList", val)
            L.append("ItemList direct ok -> %s" % comp.get_editor_property("ItemList"))
        except Exception as ex:
            L.append("ItemList direct : %s" % ex)
    toy = [c for c in a.get_components_by_class(unreal.ActorComponent) if c.get_name() == "ToyOptionsComponent"][0]
    try:
        pod = toy.get_editor_property("PlayerOptionData")
        L.append("POD type %s : %s" % (type(pod), str(pod)[:300]))
        ov = pod.get_editor_property("PropertyOverrides")
        L.append("overrides n=%d first=%s" % (len(ov), ov[0] if len(ov) else None))
        if len(ov):
            L.append("override fields : %s" % [x for x in dir(ov[0]) if not x.startswith("_")][:30])
    except Exception as ex:
        L.append("POD : %s" % traceback.format_exc())
except Exception:
    L.append(traceback.format_exc())
if a: eas.destroy_actor(a)
open(r"C:\Users\marca\Documents\Fortnite Projects\testMoudon01\Tools\probe_granter2_log.txt", "w").write("\n".join(L))
