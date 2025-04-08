import os
import subprocess


def compress_images(input_folder, output_folder, max_height=1024):

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Loop through all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(".jpg") or filename.lower().endswith(".jpeg"):
            # Define input and output paths
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            # Use ImageMagick's convert tool to resize the image
            command = [
                "convert",
                input_path,
                "-resize",
                f"x{max_height}",
                # "-quality",
                # "90",
                output_path,
            ]

            # Execute the command
            subprocess.run(command, check=True)
            print(f"Compressed and saved: {output_path}")


# Usage
input_folder = "Historien"
output_folder = "static/assets/historien"
compress_images(input_folder, output_folder)
