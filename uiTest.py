bl_info = {
    "name": "Custom UI Preferences Example",
    "author": "Your Name",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "Edit > Preferences > Add-ons",
    "description": "UI layout examples for Add-on Preferences",
    "category": "Development",
}

import bpy
from bpy.types import AddonPreferences, Operator
from bpy.props import BoolProperty, EnumProperty, IntProperty, FloatVectorProperty

# ------------------------------------------------------------------------
# 1. 버튼 클릭 시 작동할 가짜(Dummy) 오퍼레이터 (버튼 UI를 만들기 위해 필요함)
# ------------------------------------------------------------------------
class EXAMPLE_OT_dummy_button(Operator):
    bl_idname = "example.dummy_button"
    bl_label = "Dummy Button"
    action: bpy.props.StringProperty()

    def execute(self, context):
        # 버튼을 누르면 블렌더 하단 정보창에 메시지를 띄웁니다.
        self.report({'INFO'}, f"버튼 클릭됨: {self.action}")
        return {'FINISHED'}

# ------------------------------------------------------------------------
# 2. 실제 환경설정 UI 및 속성(Properties)을 정의하는 클래스
# ------------------------------------------------------------------------
class ExampleAddonPreferences(AddonPreferences):
    # __name__을 사용하면 애드온의 폴더/파일 이름과 동일하게 맞춰집니다.
    bl_idname = __name__ 

    # --- UI 토글용 속성 (섹션을 접고 펴기 위함) ---
    show_cycles_devices: BoolProperty(default=True)
    show_graphics: BoolProperty(default=True)
    show_os: BoolProperty(default=True)

    # --- 실질적인 데이터 속성 (체크박스, 드롭다운 등에 연결됨) ---
    
    # [1] 나열형 버튼 (CUDA, OptiX 등을 가로로 나열하는 용도)
    render_device: EnumProperty(
        name="Device",
        items=[
            ('NONE', "None", ""),
            ('CUDA', "CUDA", ""),
            ('OPTIX', "OptiX", ""),
            ('HIP', "HIP", ""),
            ('ONEAPI', "oneAPI", "")
        ],
        default='CUDA'
    )

    # [2] 체크박스
    use_gpu_rtx: BoolProperty(name="NVIDIA GeForce RTX 4070 Ti", default=True)
    use_cpu_ryzen: BoolProperty(name="AMD Ryzen 9 7950X3D 16-Core Processor", default=False)

    # [3] 드롭박스(Dropdown)
    display_backend: EnumProperty(
        name="Backend",
        items=[
            ('OPENGL', "OpenGL", ""),
            ('VULKAN', "Vulkan", ""),
            ('METAL', "Metal", "")
        ],
        default='OPENGL'
    )

    # [4] 숫자 입력 슬라이더
    undo_steps: IntProperty(name="Undo Steps", default=256, min=0, max=10000)

    # [5] 색상 변경 (요청하신 색상 변경 기능 추가)
    ui_theme_color: FloatVectorProperty(
        name="Highlight Color",
        subtype='COLOR',
        default=(0.2, 0.5, 0.9), # RGB 기본값 (파란색)
        min=0.0, max=1.0,
    )

    # --- UI를 화면에 그리는(Draw) 함수 ---
    def draw(self, context):
        layout = self.layout
        
        # 블렌더 기본 설정창처럼 '라벨(왼쪽)' - '값(오른쪽)'으로 깔끔하게 나누는 옵션
        layout.use_property_split = True
        layout.use_property_decorate = False

        # ==========================================
        # 섹션 1: Cycles Render Devices (가로 버튼, 체크박스)
        # ==========================================
        box = layout.box()
        row = box.row()
        icon = 'TRIA_DOWN' if self.show_cycles_devices else 'TRIA_RIGHT'
        row.prop(self, "show_cycles_devices", icon=icon, icon_only=True, emboss=False)
        row.label(text="Cycles Render Devices")

        if self.show_cycles_devices:
            # expand=True를 주면 드롭다운이 아니라 가로 버튼(라디오 버튼) 형태로 펼쳐집니다!
            box.prop(self, "render_device", expand=True) 

            # 체크박스들을 세로로 정렬
            col = box.column()
            col.prop(self, "use_gpu_rtx")
            col.prop(self, "use_cpu_ryzen")

        # ==========================================
        # 섹션 2: Display Graphics (드롭박스)
        # ==========================================
        box = layout.box()
        row = box.row()
        icon = 'TRIA_DOWN' if self.show_graphics else 'TRIA_RIGHT'
        row.prop(self, "show_graphics", icon=icon, icon_only=True, emboss=False)
        row.label(text="Display Graphics")

        if self.show_graphics:
            # expand를 주지 않으면 기본 형태인 '드롭박스'로 나타납니다.
            box.prop(self, "display_backend")

        # ==========================================
        # 섹션 3: Operating System Settings (일반 버튼)
        # ==========================================
        box = layout.box()
        row = box.row()
        icon = 'TRIA_DOWN' if self.show_os else 'TRIA_RIGHT'
        row.prop(self, "show_os", icon=icon, icon_only=True, emboss=False)
        row.label(text="Operating System Settings")

        if self.show_os:
            box.label(text="Open blend files with this Blender version")
            row = box.row(align=True)
            
            # 오퍼레이터를 호출하여 클릭 가능한 버튼을 만듭니다.
            op1 = row.operator("example.dummy_button", text="Register")
            op1.action = "Register 실행됨"
            
            op2 = row.operator("example.dummy_button", text="Unregister")
            op2.action = "Unregister 실행됨"

        # ==========================================
        # 섹션 4: 추가 기능 (숫자 입력 & 색상 선택 박스)
        # ==========================================
        box = layout.box()
        box.label(text="Extra Settings", icon='COLOR')
        
        box.prop(self, "undo_steps")
        box.prop(self, "ui_theme_color") # 색상 선택 위젯 자동 생성


# ------------------------------------------------------------------------
# 3. 등록 및 해제 (블렌더에 애드온으로 인식시키기 위함)
# ------------------------------------------------------------------------
classes = (
    EXAMPLE_OT_dummy_button,
    ExampleAddonPreferences,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()