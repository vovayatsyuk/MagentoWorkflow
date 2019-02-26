import os


def closest(name, path, directory=False):
    """Search for the closest file
    """

    folders = path.split(os.sep)
    if os.path.isfile(path):
        folders.pop()
    folders.append(name)

    while len(folders) > 2:
        file = os.sep.join(folders)
        if os.path.isfile(file):
            if directory is True:
                return file.replace(name, '')
            else:
                return file
        else:
            del folders[-2]
