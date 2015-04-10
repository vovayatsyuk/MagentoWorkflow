# Magento Sublime Text
A package of Magento snippets and various helpers for Sublime Text 3

## Main Features

#### Insert if ip statement ([Sublime Ip Address plugin](https://github.com/vovayatsyuk/sublime-ip-address#installation) is required)
<kbd>Ctrl+Alt+m,Ctrl+Alt+i,Ctrl+Alt+p</kbd> or use `Tools->Command Pallette->ifip`

![If ip in action](https://cldup.com/Gwoi2aCRrb.gif)

#### Automatic class name generator
<kbd>Ctrl+Alt+m,Ctrl+Alt+c,Ctrl+Alt+n</kbd> or use `Tools->Command Pallette->class name`

![Automatic class name generator](https://cldup.com/D_3LFBbJzK.gif)

It works for classes inside `app/code` folder only.

#### Clean stack trace
Just type `deb` in php file, expand it and check browser output.

![Stack trace with subl:// links](https://cldup.com/on6mFRqU88-2000x2000.png)

To make `subl://` scheme links working, please use the following solutions:
- [Windows](https://github.com/ktunkiewicz/subl-handler)
- [MacOS](https://github.com/dhoulb/subl)

**These links are working on local server only**

### Snippets

Tab trigger | Description
------------|------------
zd | `Zend_Debug::dump(__METHOD__);`
deb | Clean stack trace with `subl://` scheme links to each file. [Windows](https://github.com/ktunkiewicz/subl-handler), [MacOS](https://github.com/dhoulb/subl)
remoteAddr | `Mage::helper('core/http')->getRemoteAddr()`
log | `Mage::log(__METHOD__, null, 'custom.log', true);`

## Installation
1. [Install Sublime Ip Address](https://github.com/vovayatsyuk/sublime-ip-address#installation) plugin.
2. Clone project from [Github](https://github.com/vovayatsyuk/magento-sublime) into the user's Packages folder.
 - On Mac
    ```
cd ~/Library/Application\ Support/Sublime\ Text\ 3/Packages/
git clone https://github.com/vovayatsyuk/magento-sublime.git Magento
```

 - On Windows
    ```
cd "%AppData%\Sublime Text 3\Packages"
git clone https://github.com/vovayatsyuk/magento-sublime.git Magento
```
