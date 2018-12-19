import sublime_plugin

class CleanupOnFileSave(sublime_plugin.EventListener):
    def on_post_save(self, view):
        filename = view.file_name() # full path to the file: /Users/username/...

        # Mapping
        #   module .less            => pub/static(name.css), var/view_preprocessed(name.less), cache (fpc)
        #   theme .less             => pub/static(styles.css), var/view_preprocessed(styles?), cache (fpc)
        #   etc/*.xml               => cache (config, fpc)
        #   Block.*.php, *.phtml    => cache (block, fpc)
        #   layout/*.xml            => cache (layout, fpc)
        #   i18n/*.csv              => cache (translate, fpc)

        # view.window().run_command('build')
