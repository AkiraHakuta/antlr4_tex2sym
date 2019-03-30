# python.exe setup.py 
import cx_Freeze
import sys,os
import matplotlib


sys.argv.append('build')
# python.exe setup.py build


base = "Win32GUI"

icon = "ls_calc.ico"
SAH = "sympy.assumptions.handlers."
includes = ['PyQt4.QtCore',"matplotlib.backends.backend_qt4agg","matplotlib.figure",'numpy.core._methods', 'numpy.lib.format',
        SAH+"calculus",SAH+"matrices",SAH+"ntheory",SAH+"order",SAH+"sets"]
include_files = [(matplotlib.get_data_path(), "mpl-data"),"gen","data","images",icon]
excludes = ["wx","scipy","PIL"]
packages = ['antlr4']

executables = [cx_Freeze.Executable("ls_calc.py", base = base, icon = icon),]

cx_Freeze.setup(
    name = "ls_calc",
    options = {"build_exe": 
        {"build_exe":"ls_calc/","includes":includes, "include_files": include_files,"packages": packages}},
    version = "1.2",
    description = "LaTeX SymPy Caluculator",
    executables = executables)
