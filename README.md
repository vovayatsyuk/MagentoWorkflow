# Magento Sublime Text
A package of Magento snippets and various helpers for Sublime Text 3

## Main Features

#### Helpers

- Insert if ip statement ([Sublime Ip Address plugin](https://github.com/vovayatsyuk/sublime-ip-address#installation) is used)

 ```php
 if (Mage::helper('core/http')->getRemoteAddr() === 'DETECTED_IP_ADDRESS') {
     ...
 }
 ```

- Automatic class name generator for classes inside `app/code` folder

#### Snippets

Tab trigger | Description
------------|------------
zd | `Zend_Debug::dump(${1:__METHOD__});`
deb | Clean stack trace (debug_backtrace)
remoteAddr | `Mage::helper('core/http')->getRemoteAddr()`
log | `Mage::log(${1:__METHOD__}, null, 'custom.log', true);`

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
