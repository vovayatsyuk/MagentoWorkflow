import subprocess


class Terminal:
    def __init__(self, app):
        self.app = app
        self.workdir = app.workdir
        self.prefix = self.app.settings.get('cmd_prefix')
        self.service = self.app.settings.get('service')

        if not self.service:
            self.service = self.app.docker.service_name('php')

        if not self.service:
            self.prefix = ''

        if self.workdir and self.prefix and self.prefix.startswith('../'):
            count = self.prefix.split('/').count('..')
            self.workdir = '/'.join(self.workdir.rstrip('/').split('/')[:-count])
            self.prefix = self.prefix.replace('../', '')

    def run(self, cmd):
        if self.workdir is None:
            return

        if not isinstance(cmd, list):
            cmd = [cmd]

        if self.prefix:
            cmd[:] = [self.prefix + ' ' + command for command in cmd]

        cmd = ' && '.join(cmd)

        return self.execute(cmd, self.workdir)

    def execute(self, cmd, workdir):
        cmd = cmd.replace(r'{service}', self.service)

        print('[MagentoWorkflow] {} [dir:{}]'.format(cmd, workdir))

        return subprocess.check_output(
            cmd,
            shell=True,
            cwd=workdir,
            stderr=subprocess.STDOUT
        )
