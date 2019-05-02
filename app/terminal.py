import subprocess


class Terminal:
    def __init__(self, workdir):
        self.workdir = workdir

    def run(self, cmd):
        if self.workdir is None:
            return

        workdir = self.workdir

        if cmd.startswith('../'):
            count = cmd.split('../').count('')
            workdir = '/'.join(workdir.rstrip('/').split('/')[:-count])
            cmd = cmd.replace('../', '')

        print('[MagentoWorkflow] {} [dir:{}]'.format(cmd, workdir))

        return subprocess.check_output(
            cmd,
            shell=True,
            cwd=workdir,
            stderr=subprocess.STDOUT
        )
