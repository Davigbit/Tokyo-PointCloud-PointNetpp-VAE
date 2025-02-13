# import os
# import subprocess
#
#
# def convert_b3dm_to_glb(input_folder, output_folder):
#     """
#     Converts all .b3dm files in input_folder to .glb,
#     saving the output files in output_folder.
#     """
#     npx_path = r"C:\Program Files\nodejs\npx.cmd"
#
#     # 1. Ensure the output folder exists
#     os.makedirs(output_folder, exist_ok=True)
#
#     # 2. Loop over all files in the input folder
#     for filename in os.listdir(input_folder):
#         if filename.lower().endswith(".b3dm"):
#             # Construct full input path
#             input_path = os.path.join(input_folder, filename)
#
#             # Create output filename with .glb extension
#             base_name, _ = os.path.splitext(filename)
#             output_filename = base_name + ".glb"
#             output_path = os.path.join(output_folder, output_filename)
#
#             print(f"Converting {input_path} to {output_path}...")
#
#             # 3. Run the 3d-tiles-tools conversion via npx
#             #    Add '-f' if you want to overwrite existing .glb files
#             cmd = [
#                 npx_path, "3d-tiles-tools", "b3dmToGlb",
#                 "-i", input_path,
#                 "-o", output_path
#             ]
#             # If you want force-overwrite, uncomment the next line:
#             # cmd.insert(3, "-f")
#
#             # 4. Execute the command, wait for completion
#             subprocess.run(cmd, check=True)
#
#
# if __name__ == "__main__":
#     # Example usage:
#     input_folder = r"C:\Users\Admin\PycharmProjects\AI-Projects\Tokyo-PointCloud\master"
#     output_folder = r"C:\Users\Admin\PycharmProjects\AI-Projects\Tokyo-PointCloud\master_glb"
#
#     convert_b3dm_to_glb(input_folder, output_folder)


import os
import re
import subprocess

def numeric_key(filename):
    """
    Extracts the numeric portion after 'data' in filenames like 'data123.b3dm'.
    Returns an integer for proper numeric sorting.
    If it fails to parse a number, return 0 or some fallback.
    """
    # Example filename: "data123.b3dm"
    # 1) Strip extension -> "data123"
    # 2) Remove "data" at the start
    # 3) Convert remainder to int
    base, ext = os.path.splitext(filename)
    match = re.match(r"data(\d+)$", base, re.IGNORECASE)
    if match:
        return int(match.group(1))
    else:
        # If it doesn't match the pattern, fallback to 0 or a large number
        return 0

def convert_b3dm_to_glb(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    # List all .b3dm files
    files = [f for f in os.listdir(input_folder) if f.lower().endswith(".b3dm")]

    # Sort them by the integer after "data" using our numeric_key
    files.sort(key=numeric_key)

    for filename in files:
        input_path = os.path.join(input_folder, filename)

        base_name, _ = os.path.splitext(filename)
        output_filename = base_name + ".glb"
        output_path = os.path.join(output_folder, output_filename)

        print(f"Converting {input_path} to {output_path}...")

        # Use shell=True or specify full path to npx, etc., as needed
        cmd = f'npx 3d-tiles-tools b3dmToGlb -i "{input_path}" -o "{output_path}"'
        subprocess.run(cmd, shell=True, check=True)


if __name__ == "__main__":
    input_folder = r"C:\Users\Admin\PycharmProjects\AI-Projects\Tokyo-PointCloud\master_b3dm"
    output_folder = r"C:\Users\Admin\PycharmProjects\AI-Projects\Tokyo-PointCloud\master_glb"
    convert_b3dm_to_glb(input_folder, output_folder)
