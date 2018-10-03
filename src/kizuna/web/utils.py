import pathlib

content_type_map = {
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.png': 'image/png',
    '.gif': 'image/gif',
}


def image_path_to_content_type(path):
    ext = pathlib.Path(path).suffix
    if ext not in content_type_map:
        raise ValueError('image type "{}" is not recognized'.format(ext))

    return content_type_map[ext]
