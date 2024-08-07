import bpy
import sys
from pathlib import Path
import math

def generate_cube_with_materials(data_dir):
    obj_paths = list(data_dir.glob('*/*.obj'))

    for obj_path in obj_paths:
        obj_file = str(obj_path)
        glb_file = obj_file.replace('.obj', '.glb')

        # Convert OBJ to GLB using Blender
        try:
            bpy.ops.wm.read_factory_settings(use_empty=True)
            bpy.ops.import_scene.obj(filepath=obj_file)
            for mat in bpy.data.materials:
                # If the material has a node tree
                if mat.node_tree:
                    # Run through all nodes
                    for node in mat.node_tree.nodes:
                        # If the node type is texture 
                        if node.type == 'TEX_IMAGE':
                            # Set the interpolation -> Linear, Closest, Cubic, Smart
                            node.interpolation = 'Closest' 
                else:
                    print("No material node tree found")
            
            obj_objects = bpy.context.selected_objects[:]
            for obj in obj_objects:
                bpy.ops.object.select_all(action='DESELECT')
                obj.select_set(True)
                bpy.context.view_layer.objects.active = obj
                # go edit mode
                bpy.ops.object.mode_set(mode='EDIT')
                # select al faces
                bpy.ops.mesh.select_all(action='SELECT')
                # recalculate outside normals 
                bpy.ops.mesh.normals_make_consistent(inside=False)
                # go object mode again
                bpy.ops.object.editmode_toggle()

                # bpy.context.active_object.rotation_euler[0] = math.radians(0)
                # bpy.context.active_object.rotation_euler[1] = math.radians(0)
                # bpy.context.active_object.rotation_euler[2] = math.radians(0)


            bpy.ops.export_scene.gltf(filepath=glb_file, export_format='GLB')
            print(f"GLB file saved to {glb_file}")
        except Exception as e:
            print(f"Error during Blender operations: {e}")

if __name__ == "__main__":
    # Blender passes command-line arguments as sys.argv[5:] because sys.argv[0] is the script name
    if len(sys.argv) < 5:
        print("Usage: blender -b -P <script> -- <data_dir>")
        sys.exit(1)

    data_dir = Path(sys.argv[5])

    generate_cube_with_materials(data_dir)

    # remove obj, mtl and png files
    obj_paths = list(data_dir.glob('*/*.obj'))
    for obj_path in obj_paths:
        obj_path.unlink()
    mtl_paths = list(data_dir.glob('*/*.mtl'))
    for mtl_path in mtl_paths:
        mtl_path.unlink()
    png_paths = list(data_dir.glob('*/*.png'))
    for png_path in png_paths:
        png_path.unlink()
