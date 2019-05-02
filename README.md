# MagentoWorkflow

**MagentoWorkflow** — is a SublimeText 3 module aimed to improve Magento 2 module
and themes development speed. It allows to work under Magento module or theme
with enabled cache. This approach results in drastically improved Magento
performance, which means faster and enjoyable development.

## Installation

> Windows is not supported

 1. Run “Package Control: Add Repository” command and add
    `https://github.com/vovayatsyuk/MagentoWorkflow.git` link.
 2. Run “Package Control: Install Package” command, find and install
    `MagentoWorkflow` plugin.

## How it Works

When you save some file, MagentoWorkflow plugin automatically cleanup appropriate
generated files, and triggers cache invalidation. Plugin knows when, where, and
what to clear.

You will always see when the plugin do something. It reports about its processes
in Sublime's status bar.

## Commands

Pulled a lot of changes from remote repository? We've got your back!
Press <kbd>⌘⇧P</kbd> and use MagentoWorkflow commands:

 -  Clear Cache
 -  Flush Cache
 -  Clear Seleted Caches
 -  Theme: Clear Resources (js, css)
 -  Module: Clear Resources (js, css, php)

## Configuration

Module allows to customize `bin/magento` command path, and select wich resources
to cleanup when saving the file. The last is useful to disable themes resources
cleanup when using grunt tool to deploy static content files via symlinks.

## Snippets

Previous version of this plugin had some useful snippets. Now, they've been
moved to [MagicTemplates](https://github.com/vovayatsyuk/sublime-magic-templates)
plugin.
