import os

def join_txt_files(input_folder, output_file, encoding="utf-8", separator="\n\n"):
    """
    Joins all .txt files in a folder into a single text file.

    Parameters:
        input_folder (str): Path to the folder containing .txt files.
        output_file (str): Path of the resulting merged file.
        encoding (str): File encoding (default: UTF-8).
        separator (str): String to insert between files (default: two newlines).
    """
    txt_files = [f for f in os.listdir(input_folder) if f.lower().endswith(".txt")]
    txt_files.sort()  # ensures consistent order

    if not txt_files:
        print("⚠️ No .txt files found in the folder.")
        return

    print(f"🔍 Found {len(txt_files)} files. Joining...")

    with open(output_file, "w", encoding=encoding) as outfile:
        for i, filename in enumerate(txt_files, start=1):
            file_path = os.path.join(input_folder, filename)
            try:
                with open(file_path, "r", encoding=encoding) as infile:
                    text = infile.read().strip()
                    outfile.write(text)
                    if i < len(txt_files):
                        outfile.write(separator)
                print(f"✅ Added: {filename}")
            except Exception as e:
                print(f"❌ Error reading {filename}: {e}")

    print(f"\n🎉 Done! All files joined into: {output_file}")

# Example usage:
if __name__ == "__main__":
    join_txt_files(
        input_folder=r"kumpulan_corpora",
        output_file=r"E:\Documents\Linguistics\Javanese\Javanese NLP\combined.txt"
    )
