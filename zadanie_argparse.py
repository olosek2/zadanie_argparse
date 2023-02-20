from argparse import ArgumentParser, Namespace
from pathlib import Path

SIZE_UNITS = ["B", "KB", "MB", "GB"]


def get_cli_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("dir_list", type=str, nargs="+", help="One or more directory paths")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-B", action="store_const", const="B", dest="size_unit", help="Choose bytes as a size unit", default="B")
    group.add_argument("-KB", action="store_const", const="KB", dest="size_unit", help="Choose kilobytes as a size unit")
    group.add_argument("-MB", action="store_const", const="MB", dest="size_unit", help="Choose megabytes as a size unit")
    group.add_argument("-GB", action="store_const", const="GB", dest="size_unit", help="Choose gigabytes as a size unit")
    parsed_args = parser.parse_args()
    return parsed_args


def get_dir_size(dir_list: list) -> int:
    dir_size = 0
    for directory in dir_list:
        directory = Path(directory)
        for item in directory.glob('**/*'):
            if item.is_file():
                dir_size += item.lstat().st_size
    return dir_size


def format_dir_size(dir_size: int, size_unit: str) -> float:
    match size_unit:
        case "B":
            return dir_size
        case "KB":
            return dir_size / 1024
        case "MB":
            return dir_size / 1024 / 1024
        case "GB":
            return dir_size / 1024 / 1024 / 1024


def main():
    args = get_cli_args()
    size_unit = args.size_unit
    dir_size = get_dir_size(args.dir_list)
    formatted_dir_size = format_dir_size(dir_size, size_unit)
    print(f"Sum of sizes of all directories: {formatted_dir_size} {size_unit}")


if __name__ == "__main__":
    main()
