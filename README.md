# Magento Sublime

Magento 1 and Magento 2 snippets for Sublime Text 3

## Commands

All commands moved to https://github.com/vovayatsyuk/sublime-magic-templates

## Snippets

#### zd

```php
\Zend_Debug::dump(${__METHOD__});
```

#### deb

```php
\Magento\Framework\Debug::backtrace();
```

#### log

```php
\Magento\Framework\App\ObjectManager::getInstance()
    ->get('Psr\Log\LoggerInterface')
    ->debug(${1});

//OR

Mage::log(${__METHOD__}, null, 'custom.log', true);
```

## Installation

 1. Run “Package Control: Add Repository” command and add
    `https://github.com/vovayatsyuk/magento-sublime.git` link.
 2. Run “Package Control: Install Package” command, find and install
    magento-sublime plugin.
