# MagentoWorkflow

**MagentoWorkflow** — is a SublimeText 3 module aimed to improve Magento 2 module
and themes development speed. It allows to work under Magento module or theme
with enabled cache. This approach results in drastically improved Magento
performance, which means faster and enjoyable development.

## Installation

> Windows is not supported

 1. Run “Package Control: Add Repository” command and add
    `https://github.com/vovayatsyuk/sublime-magento-workflow.git` link.
 2. Run “Package Control: Install Package” command, find and install
    `sublime-magento-workflow` plugin.

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

## Snippets

Previous version of this plugin had some useful snippets. Now, they've been
moved to [MagicTemplates](https://github.com/vovayatsyuk/sublime-magic-templates)
plugin.
