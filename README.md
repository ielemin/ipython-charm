# ipython-charm

*Charms* are invisible magics for IPython notebooks.

## Charms

A *charm* is a class implementation of AbstractCharm. It defines methods invoked by IPython cell events and magics (%). 

At the moment, you have to modify the package to write your own *charm* and have it **invoked** at import time, like the default BasicTimer *charm*. The user need not execute any special action to have the methods called by IPython events.

In the future, you will write your own *charm* in any file, and **invoke** it in a IPython cell ; all cells executed afterwards will automatically call the relevant event-triggered methods.

## Sorcerer

At package import, the current IPython InteractiveShell instance is retrieved and the *sorcerer* is instantiated.

```
In [1]: import charm
```

The *sorcerer* handles all the charms and their interactions with the InteractiveShell. This magic is invisible to the user.

A *charm* can be **invoked** or **revoked** by calling two new "regular" IPython magic commands

```
In [2] : %INVOKE (charm_name)
...
In [15]: %REVOKE (charm_name)
```

## Instance control

Instance parameters of the different *charms* can be controlled by regular IPython magic, eg for BasicTimer:

```
In [8]: %TIMER reset
        Timer Reset

In [9]: %TIMER whoami
        Timer You are: ielemin
```

There are a couple of mandatory methods for declaring such explicit magics in AbstractCharm. The *sorcerer* handles all this magic registering for you.