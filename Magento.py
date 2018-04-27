import sublime
import sublime_plugin

from .magento.Magento import *
from IpAddress.ipaddress.IpAddress import IpAddress as IpAddress

class InsertIfIpCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        ip = IpAddress.instance().get()
        template = "if (Mage::helper('core/http')->getRemoteAddr() === '%s') {\n    $0\n}"

        for region in self.view.sel():
            if not region.empty():
                text = self.view.substr(region).replace('$', '\$')
                self.view.run_command('insert_snippet', {'contents': template % (ip)})
                self.view.run_command('insert_snippet', {'contents': text})
            else:
                self.view.run_command('insert_snippet', {'contents': template % (ip)})

class GenerateClassCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        namespaceDetector = NamespaceDetector(self.view.file_name())
        classnameDetector = ClassNameDetector(self.view.file_name())
        template = "namespace %s;\n\nclass %s extends $1\n{\n    $2\n}"
        self.view.run_command('insert_snippet', {
            'contents': template % (
                namespaceDetector.getNamespace(),
                classnameDetector.getClassName()
            )
        })

class InsertClassNameCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        detector = ClassNameDetector(self.view.file_name())
        self.view.run_command('insert_snippet', {
            'contents': "${1:%s}" % detector.getClassName()
        })

class InsertNamespaceCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        detector = NamespaceDetector(self.view.file_name())
        self.view.run_command('insert_snippet', {
            'contents': "${1:%s}" % detector.getNamespace()
        })
