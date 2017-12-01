import re


def extract_ats(text):
    return set(re.findall(r"<@(.*?)>", text, re.DOTALL))
