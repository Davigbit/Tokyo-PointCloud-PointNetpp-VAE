import os
import shutil


def copy_data_to_master(dataset_path='dataset', master_path='master'):
    """
    Copy all contents from each 'data' subfolder within 'dataset' into 'master'.
    """
    # Ensure the master folder exists
    if not os.path.exists(master_path):
        os.makedirs(master_path)

    i = 0

    # Traverse through all folders in 'dataset'
    for folder_name in os.listdir(dataset_path):
        subfolder_path = os.path.join(dataset_path, folder_name)

        # Check if subfolder_path is actually a folder
        if os.path.isdir(subfolder_path):
            data_folder_path = os.path.join(subfolder_path, 'data')

            # If there's a 'data' folder, copy its contents
            if os.path.exists(data_folder_path) and os.path.isdir(data_folder_path):
                # List everything inside the 'data' folder
                for item_name in os.listdir(data_folder_path):
                    i += 1
                    source_item = os.path.join(data_folder_path, item_name)
                    dest_item = os.path.join(master_path, f"data{i}.b3dm")
                    print(f"{i}th file has been copied to master")

                    # If it's a directory, copy the directory tree
                    if os.path.isdir(source_item):
                        # dirs_exist_ok=True overwrites files if there's a name conflict
                        shutil.copytree(source_item, dest_item, dirs_exist_ok=True)
                    else:
                        # If it's a file, copy the file
                        shutil.copy2(source_item, dest_item)

    print("All data from 'dataset' subfolders have been copied to the 'master' folder.")


copy_data_to_master()
