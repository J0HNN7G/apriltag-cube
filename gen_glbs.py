import bpy
import sys
from pathlib import Path

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
