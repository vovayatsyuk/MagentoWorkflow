# MagentoWorkflow

**MagentoWorkflow** — is a SublimeText 3 plugin that allows to work on Magento
module or theme with enabled cache and forget about cache clean and outdated
generated code. Additionally, it takes care about file sync into docker
environment. This approach results in drastically improved Magento performance,
which means faster and enjoyable development.

## Installation

> Windows is not supported. PR are welcome.

 1. Run “Package Control: Install Package” command
 2. Type `MagentoWorkflow` and press <kbd>Enter</kbd>

## How it Works

When you save some file, MagentoWorkflow plugin automatically cleanup appropriate
generated files, and triggers cache invalidation. Plugin knows when, where, and
what to clear.

You will always see when the plugin do something. It reports about its processes
in Sublime's status bar.

## Commands

Pulled a lot of changes from remote repository? We've got your back!
Press <kbd>⌘⇧P</kbd> and use MagentoWorkflow commands:

 -  Clear Cache - Cleanup selected magento cache
 -  Flush Cache - Flush cache storage
 -  Theme Clear - Cleanup theme resources (js, css)
 -  Module Clear - Cleanup module resources (js, css, php)

## Docker

Module automatically discovers if you are using docker and run
commands in appropriate container. Additionally, when docker is detected,
module will sync changes from `vendor` folder into the docker.

Tested with:

 -  [markshust/docker-magento](https://github.com/markshust/docker-magento)
 -  [mage2click/docker-magento-mutagen](https://github.com/mage2click/docker-magento-mutagen)

## Configuration

**No configuration is required.** Just install the module and it's ready!

While you don't need to change anything to work with MagentoWorkflow, sometimes
to may need to tune some option.

Option Name         | Default Value                     | Description
--------------------|-----------------------------------|-------------------------------------------
bin_magento_command | `bin/magento`                     | Command to run bin/magento.
resources           | `["css_module", "css_theme", "requirejs", "translation", "generated"]` | The list of resources to clean when needed.
service             | `EMPTY`                           | Docker service name. Autodetected.
cmd_prefix          | `docker-compose exec -T {service}`| Prefix to add to every terminal command. Service is taken from service option.
sync_command        | `docker cp {filepath} $(docker-compose ps -q {service}\|awk '{print $1}'):/var/www/html/{filepath}` | A command that copies files from the host to docker container.
sync_folders        | `["/vendor/"]`                    | Sync files from host to docker from these folders.

## Snippets

Previous version of this plugin had some useful snippets. Now, they've been
moved to [MagicTemplates](https://github.com/vovayatsyuk/sublime-magic-templates)
plugin.
