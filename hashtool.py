import hashlib
import os
import datetime

def hash_file(filename):
    if not os.path.exists(filename):
        raise FileNotFoundError("File not found for hash operation: {}".format(filename))

    if os.path.isfile(filename):
        # Make a SHA256 hash object
        h_sha256 = hashlib.sha256()

        # Open file for reading in binary mode
        with open(filename, 'rb') as file:
            # Define the chunk size in bytes
            chunk_size = 1024

            # Read the first chunk
            chunk = file.read(chunk_size)

            # Keep reading and updating the hash until the end of the file
            while chunk:
                h_sha256.update(chunk)
                chunk = file.read(chunk_size)

        # Return the hex digest
        return h_sha256.hexdigest()
    elif os.path.isdir(filename):
        # Hash all files within the directory
        hashes = []
        for root, _, files in os.walk(filename):
            for file in files:
                file_path = os.path.join(root, file)
                hash_value = hash_file(file_path)
                hashes.append((file_path, hash_value))

        return hashes
    else:
        raise ValueError("Invalid file or directory")

def save_hashes_to_file(file_hashes, output_file):
    with open(output_file, 'a') as file:
        for file_path, hash_value in file_hashes:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"{timestamp} | {file_path} | {hash_value}\n")

def compare_hashes(file1, hash1, file2, hash2):
    if hash1 == hash2:
        return f"The hashes match: {hash1}"
    else:
        return f"The hashes do not match:\n{file1}: {hash1}\n{file2}: {hash2}"

def main():
    while True:
        choice = input("Enter '1' to compute and save hashes, '2' to compare hashes, or 'q' to quit: ")
        if choice == 'q':
            break

        if choice == '1':
            path = input("Enter the file or directory path to hash: ")
            try:
                hash_values = hash_file(path)
                if isinstance(hash_values, list):
                    output_file = "hashes.txt"  # File to save hashes
                    save_hashes_to_file(hash_values, output_file)
                    print("Hashes successfully computed and saved to {}".format(output_file))
                else:
                    print("Hash value: ", hash_values)
                    output_file = "hashes.txt"  # File to save hashes
                    save_hashes_to_file([(path, hash_values)], output_file)
                    print("Hash successfully saved to {}".format(output_file))
            except (FileNotFoundError, ValueError) as e:
                print("Error: ", str(e))

        elif choice == '2':
            file1 = input("Enter the first file path: ")
            file2 = input("Enter the second file path: ")

            try:
                hash1 = hash_file(file1)
                hash2 = hash_file(file2)
                result = compare_hashes(file1, hash1, file2, hash2)
                print(result)
            except FileNotFoundError as e:
                print("Error: ", str(e))

        else:
            print("Invalid choice. Please try again.")

main()