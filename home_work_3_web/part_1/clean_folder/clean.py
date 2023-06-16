import shutil
import os
from pathlib import Path
import sys
import logging
import concurrent.futures


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("sort_files.log"), logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = (
    "a",
    "b",
    "v",
    "g",
    "d",
    "e",
    "e",
    "j",
    "z",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "r",
    "s",
    "t",
    "u",
    "f",
    "h",
    "ts",
    "ch",
    "sh",
    "sch",
    "",
    "y",
    "",
    "e",
    "yu",
    "ya",
    "je",
    "i",
    "ji",
    "g",
)


TRANS = {}


for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()


def normalize(file_name: str) -> str:
    result = ""
    try:
        for letter in file_name.split(".")[0]:
            if (
                letter.lower() not in CYRILLIC_SYMBOLS
                and letter.lower() not in TRANSLATION
                and letter not in "1234567890cwxWXC"
            ):
                result += "_"
            elif letter.lower() not in CYRILLIC_SYMBOLS:
                result += letter
            else:
                result += TRANS[ord(letter)]
    except:
        return name
    result += "." + file_name.split(".")[1]
    return result


# Keys - folder names. Values are the file extensions for each individual folder.
CATEGORIES = {
    "video": [
        "mp4",
        "mov",
        "avi",
        "mkv",
        "wmv",
        "3gp",
        "3g2",
        "mpg",
        "mpeg",
        "m4v",
        "h264",
        "flv",
        "rm",
        "swf",
        "vob",
    ],
    "data": [
        "sql",
        "sqlite",
        "sqlite3",
        "csv",
        "dat",
        "db",
        "log",
        "mdb",
        "sav",
        "tar",
        "xml",
    ],
    "audio": [
        "mp3",
        "wav",
        "ogg",
        "flac",
        "aif",
        "mid",
        "midi",
        "mpa",
        "wma",
        "wpl",
        "cda",
    ],
    "images": [
        "jpg",
        "png",
        "bmp",
        "ai",
        "psd",
        "ico",
        "jpeg",
        "ps",
        "svg",
        "tif",
        "tiff",
    ],
    "archives": ["zip", "rar", "7z", "z", "gz", "rpm", "arj", "pkg", "deb"],
    "docProg": ["py", "json", "md", "toml", "lock", "bin"],
    "documents": ["pdf", "txt", "doc", "docx", "rtf", "tex", "wpd", "odt"],
    "3d": ["stl", "obj", "fbx", "dae", "3ds", "iges", "step"],
    "presentation": ["pptx", "ppt", "pps", "key", "odp"],
    "spreadsheet": ["xlsx", "xls", "xlsm", "ods"],
    "font": ["otf", "ttf", "fon", "fnt"],
    "gif": ["gif"],
    "exe": ["exe"],
    "bat": ["bat"],
    "apk": ["apk"],
}


# Functions for creating folders from the list of names
def create_folders_from_list(folder_path, folder_names):
    if not Path(os.path.join(folder_path, "unknowns")).exists():
        os.mkdir(os.path.join(folder_path, "unknowns"))
    for folder in folder_names:
        if not os.path.exists(os.path.join(folder_path, folder)):
            os.mkdir(os.path.join(folder_path, folder))


# To obtain subfolder paths
def get_subfolder_paths(folder_path) -> list:
    subfolder_paths = [f.path for f in os.scandir(folder_path) if f.is_dir()]
    return subfolder_paths


# Paths of all files in a folder
def get_file_paths(folder_path) -> list:
    file_paths = [f.path for f in os.scandir(folder_path) if not f.is_dir()]
    return file_paths


def sort_files(folder_path):
    file_paths = get_file_paths(folder_path)
    file_path: os.path

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for file_path in Path(folder_path).glob("**/*"):
            if file_path.is_dir():
                continue
            futures.append(executor.submit(sort_file, folder_path, file_path))

        for future in concurrent.futures.as_completed(futures):
            if future.exception() is not None:
                logger.error(
                    f"\033[032mException occurred during sorting file: {future.exception()}\033[0m"
                )


def sort_file(folder_path, file_path):
    moved = False
    file = Path(file_path)
    extension = file.suffix.replace(".", "").lower()
    file_name = file.name

    # Unpacking archives
    if extension in CATEGORIES["archives"]:
        shutil.unpack_archive(
            file, os.path.join(folder_path, "archives", normalize(file_name))
        )
        return

    # Cycle inside
    for category, extensions in CATEGORIES.items():
        if extension in extensions:
            logger.info(f"\033[033mMoving {file_path} in {category} folder\033[0m")
            os.rename(
                file_path, os.path.join(folder_path, category, normalize(file_name))
            )
            moved = True
            break
    if not moved:
        logger.warning(f"\033[035mUnknown file type: {file_path}\033[0m")
        file_destination = os.path.join(folder_path, "unknowns")
        os.rename(file_path, os.path.join(file_destination, file_name))


# Delete empty folders
def remove_empty_folders(folder_path):
    subfolder_paths = get_subfolder_paths(folder_path)
    for p in subfolder_paths:
        if not os.listdir(p):
            logging.debug(
                f"\033[031mDeleting empty folder:\033[0m", p.split("\\")[-1], "\n"
            )
            os.rmdir(p)


def main():
    try:
        path = sys.argv[1]
    except IndexError:
        logging.debug(
            f"\033[m034You need type path to folder as param on call script\033[0m"
        )
        return None

    if not Path(path).exists():
        logging.debug(
            f"\033[035mSorry, path - {path} does not exist. Try again.\033[0m"
        )
        return None

    create_folders_from_list(path, CATEGORIES)
    get_subfolder_paths(path)
    get_file_paths(path)
    sort_files(path)
    remove_empty_folders(path)


if __name__ == "__main__":
    print(f"\033[036mSorting start!Enter the path of the folder to sort...\033[0m")
    main()
    print(f"\033[036mSorting done!\033[0m")
