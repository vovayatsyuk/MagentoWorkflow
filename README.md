# MagentoWorkflow

Magento 2 workflow without the hassle. Do the work with enabled cache to gain
maximum performance! Forget about generated code and static content!
MagentoWorkflow plugin automatically cleanup appropriate generated files and
triggers cache invalidation.

## Installation

> Windows is not supported

 1. Run “Package Control: Add Repository” command and add
    `https://github.com/vovayatsyuk/sublime-magento-workflow.git` link.
 2. Run “Package Control: Install Package” command, find and install
    `sublime-magento-workflow` plugin.

## Configuration

Disable `show_panel_on_build` option to prevent report panel to be shown on
each save. Go to _Preferences > Settings_ and add the following option:

```json
{
    "show_panel_on_build": false
}
```

## How it Works

There is a mapping between saved filepath and commands to execute:

Filepath                | Reaction
------------------------|-------------------
`/web/css/(.*)`         | Cleans up corresponsing files in `var/view_preprocessed` and `pub/static` folders. Cleans `full_page` cache.
`*.php`                 | Cleans up corresponsing files in `generated/code` folder.
`/etc/.*\.xml`          | Cleans `full_page` cache.
`/Block/.*\.php`        | Cleans `block_html full_page` caches.
`/templates/.*\.phtml`  | Cleans `block_html full_page` caches.
`/layout/.*\.xml`       | Cleans `layout block_html full_page` caches.
`/i18n/.*\.csv`         | Cleans `translate block_html full_page` caches.

## Snippets

Previous version of this plugin had some useful snippets. Now, they've been
moved to [MagicTemplates](https://github.com/vovayatsyuk/sublime-magic-templates)
plugin.
