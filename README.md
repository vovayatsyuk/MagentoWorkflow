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
(new \Zend\Log\Logger())
    ->addWriter(new \Zend\Log\Writer\Stream(BP . '/var/log/custom.log'))
    ->debug(${1:__METHOD__});

//OR

Mage::log(${1:__METHOD__}, null, 'custom.log', true);
```

## Installation

 1. Run “Package Control: Add Repository” command and add
    `https://github.com/vovayatsyuk/sublime-magento.git` link.
 2. Run “Package Control: Install Package” command, find and install
    `sublime-magento` plugin.
