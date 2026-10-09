import bpy

class MESH_OT_custom_box(bpy.types.Operator):
    bl_idname = "mesh.add_custom_box"
    bl_label = "Add Custom Box"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.mesh.primitive_cube_add(size=1.0)
        self.report({'INFO'}, "Size 1 Box Created! (모듈화 완료)")
        return {'FINISHED'}