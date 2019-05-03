import subprocess


class Terminal:
    def __init__(self, app):
        self.app = app
        self.workdir = app.workdir

    def run(self, cmd):
        if self.workdir is None:
            return

        if not isinstance(cmd, list):
            cmd = [cmd]

        prefix = self.app.settings.get('cmd_prefix')
        workdir = self.workdir
        if prefix and prefix.startswith('../'):
            count = prefix.split('/').count('..')
            workdir = '/'.join(workdir.rstrip('/').split('/')[:-count])
            prefix = prefix.replace('../', '')

        if prefix:
            cmd[:] = [prefix + ' ' + command for command in cmd]

        cmd = ' && '.join(cmd)

        print('[MagentoWorkflow] {} [dir:{}]'.format(cmd, workdir))

        return subprocess.check_output(
            cmd,
            shell=True,
            cwd=workdir,
            stderr=subprocess.STDOUT
        )
