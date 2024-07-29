from PIL import Image, ImageDraw
import colorsys
import os
import argparse

def main(output_dir, side_length):
    width = side_length
    height = side_length

    # Create the output directory if it doesn't exist
    family_name = f'tagT_{side_length}'
    output_dir = os.path.join(output_dir, f'tagT{side_length}')

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Define saturation and value for printing
    saturation = 0.7  # Adjust saturation level
    value = 0.9       # Adjust brightness level

    # Create a T cross PNG for each color point
    for i in range(6):
        if i == 0:
            # Set the first cross to black
            rgb = (0, 0, 0)
        else:
            hue = (i - 1) / 5.0  # Use (i - 1) and 5.0 to spread the remaining colors evenly
            # Convert HSV color to RGB with adjusted saturation and value
            rgb = colorsys.hsv_to_rgb(hue, saturation, value)
            rgb = tuple(int(c * 255) for c in rgb)  # Convert to 0-255 range

        # Create a new image with white background
        image = Image.new('RGB', (width, height), 'white')

        # Draw the T cross in the specified color
        draw_width = side_length // 10

        draw = ImageDraw.Draw(image)
        draw.line([(-1, -1), (width, height)], fill=rgb, width=draw_width)

        if (side_length % 2) == 1:
            draw.line([(width, -1), (width // 2, height // 2)], fill=rgb, width=draw_width)
        else:
            draw.line([(width, 0), (width // 2, height // 2)], fill=rgb, width=draw_width)


        # Save the image as PNG
        filename = os.path.join(output_dir, f'{family_name}_{i}.png')
        image.save(filename, 'PNG')

if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('output_dir', help='Output directory for PNG files')
    parser.add_argument('--side-length', type=int, default=9, help='Side length of the image')
    args = parser.parse_args()

    # Call the main function with the provided output directory, width, and height
    main(args.output_dir, args.side_length)
