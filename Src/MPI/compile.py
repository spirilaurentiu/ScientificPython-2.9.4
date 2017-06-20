# Compile the mpipython executable containing
# the Scientific.MPI extension module

# Normally nothing needs to be changed below
import distutils
import distutils.sysconfig
import os, sys
from Scientific import N

cfgDict = distutils.sysconfig.get_config_vars()

# Name of the MPI compilation script.
mpicompiler = 'mpicc'
sources='mpipython.c Scientific_mpi.c'

extra_compile_args = ""
if N.package == "NumPy":
    arrayobject_h_include = os.path.join(sys.prefix,
                            "%s/numpy/core/include"
                                          % distutils.sysconfig.get_python_lib())
    extra_compile_args = "-DNUMPY=1 -I"+arrayobject_h_include

linkforshared = cfgDict['LINKFORSHARED']
if sys.platform == 'darwin':
    # Fix LINKFORSHARED for framework builds under MacOS
    items = linkforshared.split()
    frameworkdir = (sys.prefix, '')
    while frameworkdir[1] != 'Python.framework':
        frameworkdir = os.path.split(frameworkdir[0])
    for i in range(len(items)):
        if 'Python.framework' in items[i] and not os.path.exists(items[i]):
            items[i] = os.path.join(frameworkdir[0], items[i])
    linkforshared = ' '.join(items)

cmd = '%s %s -o mpipython -I%s %s %s -L%s -lpython%s %s %s' % \
    (mpicompiler, 
     linkforshared,
     cfgDict['INCLUDEPY'],
     extra_compile_args,
     sources,
     cfgDict['LIBPL'],
     cfgDict['VERSION'], 
     cfgDict['LIBS'], 
     cfgDict['LIBM'])

print 'cmd = ', cmd 
os.system(cmd)
