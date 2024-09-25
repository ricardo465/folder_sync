import os
import shutil
import filecmp
import logging

# Set up logging to file
log_file = 'sync_log.txt'
logging.basicConfig(filename=log_file, level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def sync_folders(source, replica):
    # Compare the two directories
    comparison = filecmp.dircmp(source, replica)
    
    # Sync files from source to replica
    sync_files(source, replica, comparison)
    
    # Sync files from replica to source
    sync_files(replica, source, comparison)

def sync_files(src_folder, dest_folder, comparison):
    # Copy files from src_folder to dest_folder if they are not in dest_folder or different
    for file_name in comparison.left_only + comparison.diff_files:
        src_file = os.path.join(src_folder, file_name)
        dest_file = os.path.join(dest_folder, file_name)
        
        try:
            if os.path.isdir(src_file):
                shutil.copytree(src_file, dest_file)
                logging.info(f"Directory {src_file} copied to {dest_file}")
            else:
                shutil.copy2(src_file, dest_file)
                logging.info(f"File {src_file} copied to {dest_file}")
        except Exception as e:
            logging.error(f"Failed to copy {src_file} to {dest_file}: {e}")

    # Recursively sync subdirectories
    for sub_dir in comparison.common_dirs:
        sync_folders(os.path.join(src_folder, sub_dir), os.path.join(dest_folder, sub_dir))
    
    # Delete files in dest_folder that are not in src_folder
    delete_extra_files(dest_folder, comparison)

def delete_extra_files(dest_folder, comparison):
    # Files present only in the destination folder
    for file_name in comparison.right_only:
        dest_file = os.path.join(dest_folder, file_name)

        try:
            if os.path.isdir(dest_file):
                # Remove directory and its contents
                shutil.rmtree(dest_file)
                logging.info(f"Directory {dest_file} deleted from {dest_folder}")
            else:
                # Remove individual file
                os.remove(dest_file)
                logging.info(f"File {dest_file} deleted from {dest_folder}")
        except Exception as e:
            logging.error(f"Failed to delete {dest_file}: {e}")

# Example usage
source = r'C:/Users/Fábio e Ricardo/Dropbox/PC/Desktop/folder_sync/source'
replica = r'C:/Users/Fábio e Ricardo/Dropbox/PC/Desktop/folder_sync/replica'
sync_folders(source, replica)






