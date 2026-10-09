bl_info = {
    "name": "Custom Box Creator (Multi-file)",
    "author": "User",
    "version": (1, 2),
    "blender": (3, 0, 0),
    "location": "View3D",
    "description": "다중 파일로 분리된 단축키 Box 애드온",
    "category": "Add Mesh",
}

# ----- [핵심: 리로드(F8) 감지 및 강제 갱신 로직] -----
# 처음 켤 때는 이 블록이 무시되고, F8로 리프레시 할 때만 실행됩니다.
if "bpy" in locals():
    import importlib
    # 불러왔던 서브 모듈들을 강제로 다시 읽어들입니다.
    importlib.reload(ops)
    importlib.reload(ui)
    print("🔄 서브 모듈 강제 리로드 완료!")
else:
    # 처음 애드온을 켤 때 서브 모듈을 가져옵니다.
    from . import ops
    from . import ui
    # 반드시 if/else 구문 아래에서 bpy를 임포트해야 합니다.
    from . import bpy
# --------------------------------------------------

# 등록할 클래스들을 리스트로 묶어 관리하면 편합니다.
classes = (
    ops.MESH_OT_custom_box,
    ui.CustomBoxPreferences,
)

addon_keymaps = []

def register():
    # 클래스 일괄 등록
    for cls in classes:
        bpy.utils.register_class(cls)

    # 단축키 등록
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new(ops.MESH_OT_custom_box.bl_idname, 'B', 'PRESS', ctrl=True, shift=True)
        addon_keymaps.append((km, kmi))

def unregister():
    # 단축키 해제
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    # 클래스 일괄 해제 (등록의 역순으로 해제하는 것이 안전합니다)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)