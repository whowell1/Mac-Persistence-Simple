import hashlib
import os

# Define default directories to search
default_directories = ["/Library/LaunchAgents", "/Library/LaunchDaemons"]

# Prompt the user to enter additional directories to search
user_directories = input("Enter additional directories to search (separated by spaces): ").split()

# Combine default and user-input directories into a single list
directories_to_search = default_directories + user_directories

# Define the hash algorithm (e.g., sha256)
hash_algorithm = "sha256"

# Define the output file path on the desktop
output_file = os.path.join(os.path.expanduser("~"), "Desktop", "file_hashes.txt")

# Initialize lists to store file names and hashes
file_names = []
file_hashes = []

# Function to hash a file using hashlib
def hash_file(file_path):
    hasher = hashlib.new(hash_algorithm)
    with open(file_path, "rb") as file:
        while chunk := file.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

# Function to check if a directory is empty
def is_directory_empty(directory):
    return not any(os.scandir(directory))

# Loop through the directories and hash files
for directory in directories_to_search:
    if os.path.exists(directory):
        if is_directory_empty(directory):
            with open(output_file, "a") as out_file:
                out_file.write(f"Directory '{directory}' is empty.\n")
        else:
            with open(output_file, "a") as out_file:
                out_file.write(f"Creating a hash dictionary for {directory}:\n")
            for dirpath, _, filenames in os.walk(directory):
                for filename in filenames:
                    file_path = os.path.join(dirpath, filename)
                    file_hash = hash_file(file_path)
                    if file_hash:
                        file_names.append(file_path)
                        file_hashes.append(file_hash)

# Write the hash dictionary to the output file on the desktop
with open(output_file, "a") as out_file:
    out_file.write("Writing hashes to {}\n".format(output_file))
    for file_name, file_hash in zip(file_names, file_hashes):
        out_file.write(f"File: {file_name}\n")
        out_file.write(f"Hash: {file_hash}\n")
        out_file.write("========================================\n")



print(f"Hashes and empty directories written to {output_file}")