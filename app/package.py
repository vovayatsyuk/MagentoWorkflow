import re

from .filesystem import *


class Package:
    def __init__(self, filepath):
        self.type = None
        self.area = None
        self.code = None

        if filepath is None:
            return

        if 'lib/web/css/source' in filepath:
            self.type = 'theme'
            self.area = 'base'
            self.code = '.*'
            return

        registration = closest('registration.php', filepath)
        if registration is None:
            return

        types = {
            'module': r',\s+[\'"]((\w+_\w+))[\'"]',
            'theme': r'[\'"](frontend|adminhtml)/([\w-]+/[\w-]+)[\'"]',
            'library': r'[\'"]((\w+/\w+))[\'"]',
        }

        contents = open(registration, 'r', encoding='utf-8').read()
        for package_type in types:
            match = re.search(types[package_type], contents)
            if match:
                self.type = package_type
                # this value is correct for theme only
                self.area = match.group(1)
                self.code = match.group(2)
