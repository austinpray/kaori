import re


def _multiple_replace(text: str, sub_dict: dict) -> str:
    """https://www.safaribooksonline.com/library/view/python-cookbook-2nd/0596007973/ch01s19.html"""

    rx = re.compile('|'.join(map(re.escape, sub_dict)))

    def sub_dict_lookup(match):
        return sub_dict[match.group(0)]

    return rx.sub(sub_dict_lookup, text)
