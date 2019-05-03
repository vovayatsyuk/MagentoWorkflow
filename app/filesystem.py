import os


def closest(name, path, directory=False, max_depth=20):
    """Search for the closest file
    """

    path = path.rstrip(os.sep)
    folders = path.split(os.sep)
    if os.path.isfile(path):
        folders.pop()
    folders.append(name)

    while max_depth > 0 and len(folders) > 2:
        max_depth -= 1
        file = os.sep.join(folders)
        if os.path.isfile(file):
            if directory is True:
                return file.replace(name, '')
            else:
                return file
        else:
            del folders[-2]
