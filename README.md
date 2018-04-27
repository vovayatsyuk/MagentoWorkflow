# Magento Sublime

Magento 1 and Magento 2 snippets and commands for Sublime Text 3

## Contents

<!-- MarkdownTOC levels="2" autolink="true" -->

- [Commands](#commands)
- [Snippets](#snippets)
- [Installation](#installation)

<!-- /MarkdownTOC -->


## Commands

#### Generate class

`Tools > Command Pallette > Magento: Generate class` or
use <kbd>Ctrl+Alt+m,Ctrl+Alt+n,Ctrl+Alt+s</kbd> shortcut.

The following code will be inserted with detected namespace and class name
(namespace will be generated according to psr-4 rules from composer.json):

```php
namespace Vovayatsyuk\Alsoviewed\Model\Config\Source;

class Basis extends ${1}
{
    ${2}
}
```

#### Insert if ip

> [Sublime Ip Address](https://github.com/vovayatsyuk/sublime-ip-address#installation)
plugin is required.

`Tools > Command Pallette > Magento: Insert if ip` or
use <kbd>Ctrl+Alt+m,Ctrl+Alt+i,Ctrl+Alt+p</kbd> shortcut.

The following code will be inserted with dynamically detected IP address:

```php
if ('194.44.93.57' === $remoteAddress->getRemoteAddress()) {
    ${1}
}
```

#### Insert namespace

`Tools > Command Pallette > Magento: Insert namespace` or
use <kbd>Ctrl+Alt+m,Ctrl+Alt+n,Ctrl+Alt+s</kbd> shortcut.

A namespace will be generated according to psr-4 rules from composer.json:

```php
namespace Vovayatsyuk\Alsoviewed\Model\Config\Source;
```

#### Insert class name

`Tools > Command Pallette > Magento: Insert class name` or
use <kbd>Ctrl+Alt+m,Ctrl+Alt+c,Ctrl+Alt+n</kbd> shortcut.

Class name will be generated:

```php
class Basis
```

## Snippets

#### zd

```php
\Zend_Debug::dump(__METHOD__);
```

#### deb

```php
\Magento\Framework\Debug::backtrace();
```

#### log

```php
\Magento\Framework\App\ObjectManager::getInstance()
    ->get('Psr\Log\LoggerInterface')
    ->debug();

//OR

Mage::log(__METHOD__, null, 'custom.log', true);
```

## Installation

 1. Install [Sublime IpAddress][IpAddress] plugin.

    > Run “Package Control: Install Package” command, find and install IpAddress
    > plugin.

 2. Run “Package Control: Add Repository” command and add
    `https://github.com/vovayatsyuk/magento-sublime.git` link.
 3. Run “Package Control: Install Package” command, find and install
    magento-sublime plugin.

[IpAddress]: (https://github.com/vovayatsyuk/sublime-ip-address)
