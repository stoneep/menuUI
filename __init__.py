bl_info = {
    "name": "Custom Box Creator",
    "author": "User",
    "version": (1, 1),
    "blender": (3, 0, 0),
    "location": "View3D",
    "description": "사이즈 1의 기본 Box 생성 및 자동 리로드 기능",
    "category": "Add Mesh",
}

import bpy
import rna_keymap_ui
import os

# ----- [변경 감지 타이머를 위한 전역 변수] -----
ADDON_PATH = __file__
last_modified_time = os.path.getmtime(ADDON_PATH)

def check_script_modified():
    global last_modified_time
    try:
        current_time = os.path.getmtime(ADDON_PATH)
        # 코드를 저장하여 파일 수정 시간이 갱신되었다면
        if current_time > last_modified_time:
            last_modified_time = current_time
            print("🔄 스크립트 변경 감지됨! 자동으로 리로드합니다...")
            # 블렌더 기본 리프레시 명령어 실행
            bpy.ops.script.reload()
    except Exception as e:
        print(f"Reload Error: {e}")
        
    return 2.0  # 2초 주기로 파일 검사 반복

# ----- [오퍼레이터 및 UI] -----
class MESH_OT_custom_box(bpy.types.Operator):
    bl_idname = "mesh.add_custom_box"
    bl_label = "Add Custom Box"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.mesh.primitive_cube_add(size=1.0)
        self.report({'INFO'}, "Size 1 Box Created!")
        return {'FINISHED'}

class CustomBoxPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__ if __package__ else __name__

    def draw(self, context):
        layout = self.layout
        layout.label(text="$Box 단축키 설정:")
        
        wm = context.window_manager
        kc = wm.keyconfigs.user
        km = kc.keymaps.get('3D View')
        
        if km:
            layout.context_pointer_set("keymap", km)
            for kmi in km.keymap_items:
                if kmi.idname == MESH_OT_custom_box.bl_idname:
                    rna_keymap_ui.draw_kmi([], kc, km, kmi, layout, 0)
                    break

# ----- [등록 / 해제] -----
addon_keymaps = []

def register():
    bpy.utils.register_class(MESH_OT_custom_box)
    bpy.utils.register_class(CustomBoxPreferences)

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new(MESH_OT_custom_box.bl_idname, 'B', 'PRESS', ctrl=True, shift=True)
        addon_keymaps.append((km, kmi))
        
    # 애드온이 켜질 때 변경 감지 타이머 시작
    if not bpy.app.timers.is_registered(check_script_modified):
        bpy.app.timers.register(check_script_modified)

def unregister():
    # 애드온이 꺼질 때 타이머 해제
    if bpy.app.timers.is_registered(check_script_modified):
        bpy.app.timers.unregister(check_script_modified)

    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    bpy.utils.unregister_class(CustomBoxPreferences)
    bpy.utils.unregister_class(MESH_OT_custom_box)