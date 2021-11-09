def is_cmd_file(filename: str) -> bool:
    return filename.endswith(".py") and filename.startswith("cmd")


def cmd_name_from_file(filename: str) -> str:
    return filename[4:-3]
