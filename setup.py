from __future__ import print_function

import os
import os.path as osp
import sys
from distutils.core import setup
from setuptools.command.install import install
from distutils import log
# from IPython.utils.tempdir import TemporaryDirectory


import platform
import json
import os
import sys
import subprocess
import setuptools


def subdirs(root, file='*.*', depth=10):
    for k in range(depth):
        yield root + '*/' * k + file


# Reads the specific command line arguments

if "--help" in sys.argv:
    print('setup install|build')



def get_start_text(cmd):
    if not os.access(cmd, os.X_OK):
        return ""
    else:
        print("    command valid. Trying " + cmd)
    try:
        with subprocess.Popen(cmd,
                              bufsize=1,
                              stdout=subprocess.PIPE,
                              stdin=subprocess.PIPE) as pr:
            starttext = pr.communicate(timeout=15)[0].decode().strip()
    except Exception as e:
        print(e)
        return ""
    # only head is required, thus crop
    # strip removes leading LF or CR+LF in case of the mathics banner
    return starttext.strip()

# Mathics or nothing
wmmexec = None
if wmmexec is None:
    print("trying with Mathics")
    candidates =  [os.path.join(path, 'mathics' + ((os.path.extsep + 'exe') if os.name == 'nt' else ''))
                                                         for path in os.environ["PATH"].split(os.pathsep)]
    for candidate in candidates:
        if not osp.isfile(candidate):
            continue
        print("trying with ", candidate)
        try:
            starttext = get_start_text(candidate)
            if starttext == "":
                continue
            if starttext[:7] == "Mathics":
                print("Mathics version found at " + candidate)
                wmmexec = candidate
                break
        except Exception:
            continue

if wmmexec is None:
    print("Couldn't find a Mathics/Mathematica interpreter.")
    print("relaying in the operative system mathics installation")
    print("os.name=", os.name)
    wmmexec = "mathics" + ((os.path.extsep + 'exe') if os.name == 'nt' else '')
    #sys.exit(-1)


def _is_root():
    try:
        return os.geteuid() == 0
    except AttributeError:
        return False  # assume not an admin on non-Unix platforms


class install_with_kernelspec(install):
    def run(self):
        import os
        global wmmexec
        print("Installing kernelspec")

        user = '--user' in sys.argv or not _is_root()
        configfilestr = f"# iwolfram configuration file\nmathexec = '{wmmexec}'\n\n"
        configfilestr = configfilestr.replace('{wolfram-caller-script-path}', wmmexec)
        with open('mathics_kernel/config.py','w',encoding='utf-8') as f:
            f.write(configfilestr)

        #Run the standard intallation
        install.run(self)

        def install_kernelspec(self):

            try:
                from jupyter_client.kernelspec import install_kernel_spec
            except ImportError:
                from IPython.kernel.kernelspec import install_kernel_spec


            from ipykernel.kernelspec import write_kernel_spec
            from jupyter_client.kernelspec import KernelSpecManager
            from mathics_kernel.mathics_kernel import MathicsKernel
            kernel_json = MathicsKernel.kernel_json
            kernel_js = MathicsKernel.kernel_js
            kernel_spec_manager = KernelSpecManager()
            kernel_spec_path = write_kernel_spec(overrides=kernel_json)
            with open(kernel_spec_path+"/kernel.js","w",encoding="utf-8") as jsfile:
                 jsfile.write(kernel_js)

            log.info('Installing kernel spec')
            try:
                kernel_spec_manager.install_kernel_spec(
                    kernel_spec_path,
                    kernel_name=kernel_json['name'],
                        user=user)
            except:
                log.error('Failed to install kernel spec in ' + kernel_spec_path)
                kernel_spec_manager.install_kernel_spec(
                    kernel_spec_path,
                    kernel_name=kernel_json['name'],
                        user=not user)


        print("Installing kernel spec")
        #Build and Install the kernelspec
        install_kernelspec(self)
        log.info("Installing nbextension")
        from notebook.nbextensions import install_nbextension
        import os.path
        try:
            install_nbextension(os.path.join(os.path.dirname(__file__), 'nbmathics'),overwrite=True,)
            if os.name == 'nt':
                jup_nbex_exec = os.path.join(os.path.dirname(sys.executable), 'Scripts', 'jupyter-nbextension.exe')
            else:
                jup_nbex_exec = os.path.join(os.path.dirname(sys.executable), "jupyter-nbextension")
            os.system(jup_nbex_exec + " install --system  nbmathics")
            os.system(jup_nbex_exec + "  enable --system --py  nbmathics")
        except:
            log.info("nbextension can not be installed")

setup(name='mathics_kernel',
      version='0.0.1',
      description='A Mathics kernel for Jupyter/IPython',
      long_description='A Mathics kernel for Jupyter/IPython, based on MetaKernel',
      url=' https://github.com/aravindh-krishnamoorthy/mathics-jupyter-kernel',
      author='Juan Mauricio Matera and Aravindh Krishnamoorthy',
      author_email='aravindh.krishnamoorthy@fau.de',
      packages=['mathics_kernel','nbmathics'],
      cmdclass={'install': install_with_kernelspec},
      install_requires=['metakernel'],
      package_data={
          'mathics_kernel': ['init.m','wmath',],
          'nbmathics': ['nbmathics/static/img/*.gif',
                        'nbmathics/static/css/*.css',
                        'nbmathics/static/*.js',
                        'nbmathics/static/js/*.js',
                        'nbmathics/static/js/innerdom/*.js',
                        'nbmathics/static/js/prototype/*.js',
                        'nbmathics/static/js/scriptaculous/*.js',
                        'nbmathics/static/js/tree/Three.js',
                        'nbmathics/static/js/tree/Detector.js',
                         ] + list(subdirs('media/js/mathjax/')),
      },
      classifiers = [
          'Framework :: IPython',
          'License :: OSI Approved :: BSD License',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 2',
          'Topic :: System :: Shells',
      ]
)
