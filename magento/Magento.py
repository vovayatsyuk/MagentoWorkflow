import re
import os
import json

class ClassNameDetector(object):
    def __init__(self, path):
        path = os.path.splitext(path)[0] # remove file extension

        self.pathParts = []
        self.codePoolDirectory = 'app' + os.sep + 'code' + os.sep

        if not self.codePoolDirectory in path:
            # Magento 2
            self.pathParts.append(path.split(os.sep)[-1])
            return

        self.pathParts = path.split(self.codePoolDirectory)[1].split(os.sep)
        self.pathParts.pop(0) # unset namespace part: local|core|community

        if 'controllers' in self.pathParts:
            self.pathParts.remove('controllers')

    def getClassName(self):
        return '_'.join(self.pathParts)

    def debug(self, text):
        print('[Magento ClassNameDetector] ' + text)

class NamespaceDetector(object):
    def __init__(self, path):
        self.pathParts = []
        self.vendorDirectory = 'vendor' + os.sep
        if not self.vendorDirectory in path:
            self.debug(self.vendorDirectory + ' not found in ' + path)
            return

        self.pathParts = path.split(self.vendorDirectory)[1].split(os.sep)
        del self.pathParts[:2] # remove vendor and module folders
        del self.pathParts[-1] # remove file name

        # get psr-4 settings
        modulePath = path.split(os.sep.join(self.pathParts))[0]
        with open(modulePath + 'composer.json') as composer:
            data = json.load(composer)

        currentPath = os.sep.join(self.pathParts)
        for key in data['autoload']['psr-4']:
            subfolder = data['autoload']['psr-4'][key]

            if subfolder:
                if currentPath.startswith(subfolder):
                    currentPath = currentPath[len(subfolder):]
                else:
                    continue

            currentPath = key.replace('\\', os.sep) + currentPath
            break

        self.pathParts = currentPath.split(os.sep);

    def getNamespace(self):
        return '\\'.join(self.pathParts)

    def debug(self, text):
        print('[Magento NamespaceDetector] ' + text)
