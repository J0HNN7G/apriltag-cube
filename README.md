# AprilTag Cubes
Generate OBJ, MTL, CSV and GLB files for AprilTag Cubes

Example for creating OBJ, MTL and CSV files for cube with 0.5 units side length and AprilTag family tag16h5:
```
python gen_cube.py 0.5 data/apriltag-imgs/tag16h5/ data/
```
Converting all the cube OBJ files in data directory to GLB files:
```
blender -b -P 'gen_glbs.py' -- data/
```