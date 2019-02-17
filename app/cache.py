import re


class Cache:
    def __init__(self, app):
        self.app = app

    def flush(self):
        return self.app.terminal.run('bin/magento cache:flush')

    def clean(self, type=None):
        if type is None:
            type = self.get_types()

        if type is 'All':
            cmd = 'bin/magento cache:clean'
        elif isinstance(type, set):
            cmd = 'bin/magento cache:clean {}'.format(' '.join(type))
        else:
            cmd = 'bin/magento cache:clean {}'.format(type)

        return self.app.terminal.run(cmd)

    def get_types(self):
        rules = {
            r'/etc/.*\.xml': ['config'],
            r'/Block/.*\.php': ['block_html'],
            r'/templates/.*\.phtml': ['block_html'],
            r'/layout/.*\.xml': ['layout', 'block_html'],
            r'/i18n/.*\.csv': ['translate', 'block_html'],
            r'.*': ['full_page'],
        }

        types = set()
        for pattern in rules:
            if re.findall(pattern, self.app.filepath):
                for cache_type in rules[pattern]:
                    types.add(cache_type)

        return types
