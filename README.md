# AprilTag Cubes

This repository provides tools to generate OBJ, MTL, CSV, and GLB files for AprilTag cubes and tiles. 

![Example](https://github.com/J0HNN7G/apriltag-cube/blob/main/assets/example.png?raw=true)

## Prerequisites

- To create GLB files, you need the Blender Python API (tested with Blender version 3.4.1).
- Standard numerical packages: Numpy, Scipy.
- tqdm for monitoring progress.

## Usage

### Creating OBJ, MTL, and CSV Files for a Cube

To generate OBJ, MTL, and CSV files for 50 cubes with a side length of 0.3 meters using the AprilTag family `tag36h11`, run:

```bash
python gen_cube.py 0.3 50 data/apriltag-imgs/tag36h11/ data/
```

### Creating OBJ, MTL, and CSV Files for a One-Sided Tile

To generate files for 50 one-sided tile with a side length of 0.3 meters using the AprilTag family `tag36h11`, run:

```bash
python gen_tile.py 0.3 50 data/apriltag-imgs/tag36h11/ data/
```

### Converting OBJ and MLT Files to GLB Files (+ deleting files no longer needed)

To convert all the OBJ files in the data directory to GLB files, use the following Blender command:

```bash
blender -b -P 'gen_glbs.py' -- data/
```

Note, this will delete all the OBJ, MTL and PNG files.

## AprilTag Pose Estimation and Coordinate Frame Conversion

The default AprilTag detector pose estimation defines the coordinate system as follows:

#### Default Camera Frame
- Origin: Camera center
- Z-axis: Outward from the camera lens
- Y-axis: Downward in the camera image
- X-axis: Right in the camera image

#### Default Tag Frame
- Origin: Tag center
- Z-axis: Into the tag
- Y-axis: Downward
- X-axis: Right

For compatibility with certain simulators, we aim to use the following coordinate system:

#### Desired Camera Frame
- Z-axis: Inward to the camera lens
- Y-axis: Upward in the camera image
- X-axis: Right in the camera image

#### Desired Tag Frame
- Z-axis: Out of the tag
- Y-axis: Upward
- X-axis: Right

To convert from the default to the desired coordinate system:

1. **Camera Frame:** Rotate 180° around the X-axis
2. **Tag Orientation:** Rotate 180° around the X-axis

The CSV file provides rotations for each face ID, transforming face coordinate frames to the same orientation as the cube coordinate frame. The Face ID to Cube Coordinate Frame Basis Vector Mapping:
- 0: +X axis
- 1: -X axis
- 2: +Y axis
- 3: -Y axis
- 4: +Z axis
- 5: -Z axis

To transform from a face coordinate frame to the cube coordinate frame:

1. Translate by half the cube's side length along the negative Z-axis
2. Apply the rotation corresponding to the face ID specified in the CSV

The cube face id is the detected tag id mod 6, and for the tile, it is always the same transformation for all tags.

These steps can be combined into a single 4x4 transformation matrix.