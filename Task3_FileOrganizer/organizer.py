import os
import shutil
import sys

CATEGORY_MAPPING = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".xls", ".pptx", ".csv"],
    "Audio": [".mp3", ".wav", ".aac", ".flac"],
    "Video": [".mp4", ".mkv", ".mov", ".avi"],
    "Archives": [".zip", ".tar", ".gz", ".7z", ".rar"],
    "Code": [".py", ".js", ".html", ".css", ".cpp", ".c", ".java", ".json"]
}


def get_category(file_extension):
    ext = file_extension.lower()
    for category, extensions in CATEGORY_MAPPING.items():
        if ext in extensions:
            return category
    return "Others"


def organize_directory(target_dir):
    if not os.path.exists(target_dir):
        print(f"[!] Error: The directory '{target_dir}' does not exist.")
        return

    print(f"\n[+] Organizing directory: {target_dir}\n" + "-" * 50)

    script_name = os.path.basename(__file__)
    files_moved = 0

    for item in os.listdir(target_dir):
        item_path = os.path.join(target_dir, item)

        if os.path.isdir(item_path) or item == script_name:
            continue

        filename, file_extension = os.path.splitext(item)
        category = get_category(file_extension) if file_extension else "Others"

        category_folder = os.path.join(target_dir, category)
        os.makedirs(category_folder, exist_ok=True)

        dest_path = os.path.join(category_folder, item)

        try:
            shutil.move(item_path, dest_path)
            print(f"[✓] Moved: {item} -> {category}/")
            files_moved += 1
        except Exception as e:
            print(f"[!] Failed to move {item}: {e}")

    print("-" * 50)
    print(f"[✓] Cleanup complete! Total files organized: {files_moved}")


def main():
    print("=" * 60)
    print("📁 Automated File Organizer & Cleanup Utility")
    print("=" * 60)

    if len(sys.argv) > 1:
        target_dir = sys.argv[1]
    else:
        target_dir = input("\nEnter target folder path (or press Enter for current directory): ").strip()
        if not target_dir:
            target_dir = os.path.dirname(os.path.abspath(__file__))

    organize_directory(target_dir)


if __name__ == "__main__":
    main()