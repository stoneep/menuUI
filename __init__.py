bl_info = {
    "name": "Custom Box Creator (Multi-file)",
    "author": "User",
    "version": (1, 2),
    "blender": (3, 0, 0),
    "location": "View3D",
    "description": "다중 파일로 분리된 단축키 Box 애드온",
    "category": "Add Mesh",
}

# 1. 처음 켤 때는 이 블록이 무시되고 else 문으로 넘어갑니다.
# 2. F8로 리프레시 할 때는 이미 bpy가 메모리에 있으므로 아래 블록이 실행됩니다.
if "bpy" in locals():
    import importlib
    importlib.reload(operator)
    importlib.reload(ui)
    print("🔄 서브 모듈 강제 리로드 완료!")
else:
    from . import operator
    from . import ui

# 반드시 if/else 구문 아래에서 bpy를 임포트해야 합니다.
import bpy

classes = (
    operator.MESH_OT_custom_box,
    ui.CustomBoxPreferences,
)

addon_keymaps = []

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new(operator.MESH_OT_custom_box.bl_idname, 'B', 'PRESS', ctrl=True, shift=True)
        addon_keymaps.append((km, kmi))

def unregister():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)