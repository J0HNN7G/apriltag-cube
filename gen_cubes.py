import numpy as np
import os
import argparse
import shutil
import csv
from scipy.spatial.transform import Rotation as R
from tqdm import tqdm


def generate_cube_with_materials(args):
    output_dir = args.output_dir

    side_length = args.side_length
    num_cubes = args.count
    num_tags = num_cubes * 6

    family_dir = args.family_dir
    family_name = os.path.basename(os.path.normpath(family_dir))

    cube_dirname = f'cube_{family_name}_{side_length}'

    # Define vertices of the cube
    half_side = side_length / 2.0
    vertices = np.array([
        [half_side, half_side, -half_side],
        [half_side, -half_side, -half_side],
        [-half_side, -half_side, -half_side],
        [-half_side, half_side, -half_side],
        [half_side, half_side, half_side],
        [half_side, -half_side, half_side],
        [-half_side, -half_side, half_side],
        [-half_side, half_side, half_side]
    ])

    # Define faces of the cube (two triangles per face)
    faces = np.array([
        [0, 1, 5, 4],  # x
        [2, 3, 7, 6],  # -x
        [3, 0, 4, 7],  # y
        [1, 2, 6, 5],  # -y
        [5, 6, 7, 4],  # z
        [0, 3, 2, 1]   # -z
    ])

    triangles = []
    for face in faces:
        triangles.append([face[0], face[1], face[2]])
        triangles.append([face[2], face[3], face[0]])

    # List texture files in the specified directory
    texture_files = [f for f in os.listdir(family_dir) if f.endswith('.png') and os.path.basename(f).startswith('tag')]
    if len(texture_files) < num_tags:
        raise ValueError(f"At least {num_tags} textures are needed in the directory.")
    
    # Ensure the output directory exists
    output_dir = os.path.join(output_dir, cube_dirname)
    os.makedirs(output_dir, exist_ok=True)

    texture_filenames = [os.path.splitext(f)[0] for f in texture_files]
    texture_idx = [int(f.split('_')[-1]) for f in texture_filenames]
    sorted_texture_files = [f for _, f in sorted(zip(texture_idx, texture_files))]

    # Copy textures to the output directory
    for texture_file in sorted_texture_files[:num_tags]:
        src = os.path.join(family_dir, texture_file)
        dst = os.path.join(output_dir, texture_file)
        shutil.copy(src, dst)  # Use shutil to copy the file

    for i in tqdm(range(num_cubes)):
        cube_name = f"{cube_dirname}_{i}"
        obj_file = os.path.join(output_dir, f'{cube_name}.obj')
        mtl_file = os.path.join(output_dir, f'{cube_name}.mtl')

        # Write MTL file
        with open(mtl_file, 'w') as f:
            for i, texture_file in enumerate(sorted_texture_files[i*6:(i+1)*6]):
                f.write(f"newmtl material_{i}\n")
                f.write(f"Ka 0.8 0.8 0.8\n")  # Ambient color for paper-like material
                f.write(f"Kd 1.0 1.0 1.0\n")  # Diffuse color (white)
                f.write(f"Ks 0.0 0.0 0.0\n")  # Specular color (no specular reflection)
                f.write(f"Tr 1.0\n")  # Transparency (fully opaque)
                f.write(f"illum 2\n")  # Illumination model (basic lighting model)
                f.write(f"Ns 0.0\n")  # Shininess (none)
                f.write(f"map_Kd {texture_file}\n\n")
        # print(f"MTL file saved to {mtl_file}")

        # Write OBJ file
        with open(obj_file, 'w') as f:
            f.write("# OBJ File Generated by Python Script\n")
            f.write(f"# Vertices: {len(vertices)}\n")
            f.write(f"# Faces: {len(triangles)}\n")
            f.write(f"\nmtllib {os.path.basename(mtl_file)}\n\n")

            # Write vertices
            for vertex in vertices:
                f.write(f"v {' '.join(map(str, vertex))}\n")

            f.write("\n")

            # Write texture coordinates (covering full texture per face)
            texture_coords = np.array([
                [0.0, 0.0],
                [0.0, 1.0],
                [1.0, 1.0],
                [1.0, 0.0]
            ])

            for vt in texture_coords:
                f.write(f"vt {' '.join(map(str, vt))}\n")

            f.write("\n")

            # Write faces with materials and normals
            face_vt_map = [[4, 1, 2], [2, 3, 4]]
            for i in range(6): 
                f.write(f"usemtl material_{i}\n")
                for j in range(2):
                    triangle_idx = 2*i+j
                    triangle_face = triangles[triangle_idx]
                    face_txt = []
                    for k, v in enumerate(triangle_face):
                        face_txt.append(f"{v+1}/{face_vt_map[j][k]}")
                    f.write(f"f {' '.join(face_txt)}\n")
                f.write("\n")
        # print(f"OBJ file saved to {obj_file}")

    # just trust me on this (I found them all by hand)
    rotations = {   
        0: [-0.5, -0.5, -0.5,  0.5],
        1: [-0.5,  0.5,  0.5,  0.5], 
        2: [0, -0.70710678, -0.70710678, 0],
        3: [-0.70710678, 0, 0, 0.70710678],
        4: [0, 0, 0, 1],
        5: [-1, 0, 0, 0]
    }

    csv_file = os.path.join(output_dir, f'{cube_dirname}.csv')
    with open(csv_file, 'w', newline='') as csvfile:
        fieldnames = ['face_id', 'trans_x', 'trans_y', 'trans_z', 'rot_w', 'rot_x', 'rot_y', 'rot_z']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for idx in range(6):
            translation = [0, 0, -half_side]
            rotation = rotations[idx]
            writer.writerow({
                'face_id': idx,
                'trans_x': translation[0],
                'trans_y': translation[1],
                'trans_z': translation[2],
                'rot_w': rotation[3],
                'rot_x': rotation[0],
                'rot_y': rotation[1],
                'rot_z': rotation[2]
            })

    # print(f"CSV file saved to {csv_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a cube with textures and convert to GLB.")
    parser.add_argument("side_length", type=float, default=0.3, help="The length of the cube's side.")
    parser.add_argument("count", type=int, default=1, help="Number of cubes to generate.")
    parser.add_argument("family_dir", type=str, help="Directory containing texture files.")
    parser.add_argument("output_dir", type=str, help="Directory to save the output files.")

    args = parser.parse_args()

    generate_cube_with_materials(args)
