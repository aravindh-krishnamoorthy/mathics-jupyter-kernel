# IMathics

Jupyter Interface for Mathics Notebooks based on the [IWolfram Kernel](https://github.com/Mathics3/iwolfram) by [Juan Mauricio Matera](https://github.com/mmatera).
This version is maintained by me, [Aravindh Krishnamoorthy](https://github.com/aravindh-krishnamoorthy).

Installing
----------

```
$ pip install -e .
...
Installing collected packages: mathics_kernel
Attempting uninstall: mathics_kernel
Successfully installed mathics_kernel-X.Y.Z
```

Running
-------

To launch the Jupyter file explorer in a browser window, use:
```
$ jupyter notebook --kernel=mathics_kernel
```

Alternatively, to start the [Jupyter Desktop](https://github.com/jupyterlab/jupyterlab-desktop) application and select the 'Mathics' kernel afterwards, use:
```
$ jlab .
```

Contributing
------------

Please feel encouraged to contribute to this project! Create your
own fork, make the desired changes, commit, and make a pull request.

License
-------

IMathics is released under the GNU General Public License (GPL).

Interactive 3D Graphics
-----------------------

Basic support for interactive 3D graphics is implemented. The implementation
is based on [Three.js](https://threejs.org) and on the interface developed by
Angus Griffith for [the Mathics Project](https://github.com/mathics/Mathics).

Current Support (V0.0.1)
------------------------

- Text output from Mathics
- 2D graphics via SVG
