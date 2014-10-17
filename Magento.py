import sublime
import sublime_plugin

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
