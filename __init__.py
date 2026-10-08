bl_info = {
    "name": "Custom Box Creator",
    "author": "User",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "View3D",
    "description": "사이즈 1의 기본 Box를 단축키로 생성합니다.",
    "category": "Add Mesh",
}

import bpy
import rna_keymap_ui

class MESH_OT_custom_box(bpy.types.Operator):
    bl_idname = "mesh.add_custom_box"
    bl_label = "Add Custom Box"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.mesh.primitive_cube_add(size=1.0)
        self.report({'INFO'}, "Size 1 Box Created!")
        return {'FINISHED'}

class CustomBoxPreferences(bpy.types.AddonPreferences):
    # 설치형(폴더형) 애드온일 경우 패키지 이름을 idname으로 사용합니다.
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

def unregister():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    bpy.utils.unregister_class(CustomBoxPreferences)
    bpy.utils.unregister_class(MESH_OT_custom_box)

# __init__.py 환경에서는 직접 스크립트를 실행하는 것이 아니므로 
# if __name__ == "__main__": 부분을 생략해도 블렌더가 알아서 register()를 호출합니다.