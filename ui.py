import bpy
import rna_keymap_ui
from .ops import MESH_OT_custom_box  # 같은 폴더의 ops.py에서 클래스 가져오기

class CustomBoxPreferences(bpy.types.AddonPreferences):
    # 파일이 분리되었을 때는 __name__ 대신 __package__를 써야 
    # 애드온 이름(폴더명)을 정확히 인식하여 Preferences에 UI가 뜹니다.
    bl_idname = __package__ 

    def draw(self, context):
        layout = self.layout
        layout.label(text="$Box 단축키 설정 (모듈화 버전):")
        
        wm = context.window_manager
        kc = wm.keyconfigs.user
        km = kc.keymaps.get('3D View')
        
        if km:
            layout.context_pointer_set("keymap", km)
            for kmi in km.keymap_items:
                if kmi.idname == MESH_OT_custom_box.bl_idname:
                    rna_keymap_ui.draw_kmi([], kc, km, kmi, layout, 0)
                    break