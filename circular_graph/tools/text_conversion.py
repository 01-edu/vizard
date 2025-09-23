import re as re2


def to_slug(text: str, project_path_dict: dict) -> str:
    """
    Convert a string into a slug:
      - lowercase everything
      - replace any sequence of non-alphanumeric characters with a single hyphen
      - strip leading/trailing hyphens
    """

    try:
        txt = project_path_dict[text]
    except:
        # 1) lowercase
        txt = text.lower()
        # 2) replace any group of characters that are NOT a-z or 0-9 with a hyphen
        txt = re2.sub(r"[^a-z0-9]+", "-", txt)
        # 3) strip leading/trailing hyphens
    return txt.strip("-")


def replace_keys(input_dict, project_path_dict: dict) -> str:
    new_dict = {}
    for key, value in input_dict.items():
        if isinstance(key, str):
            new_key = to_slug(key, project_path_dict)
        else:
            new_key = key
        new_dict[new_key] = value
    return new_dict
