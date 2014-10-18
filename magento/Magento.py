import re
import os

class ClassNameDetector(object):
    def __init__(self, path):
        self.pathParts = []
        self.codePoolDirectory = 'app' + os.sep + 'code' + os.sep
        if not self.codePoolDirectory in path:
            self.debug(self.codePoolDirectory + ' not found in ' + path)
            return

        path = os.path.splitext(path)[0] # remove file extension
        self.pathParts = path.split(self.codePoolDirectory)[1].split(os.sep)
        self.pathParts.pop(0) # unset namespace part: local|core|community

        if 'controllers' in self.pathParts:
            self.pathParts.remove('controllers')

    def getClassName(self):
        return '_'.join(self.pathParts)

    def debug(self, text):
        print('[Magento ClassNameDetector] ' + text)
