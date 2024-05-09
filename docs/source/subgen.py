import os
import pkgutil
import sys
# Add the path to the directory containing your source files
source_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src'))
print(source_dir)
sys.path.insert(0, source_dir)

# Add the path to the directory containing your module to the system path

package_name = 'zrcl'

def generate_submodule_rst(pkg_name, module):
    output = ""
    output+= f"{pkg_name}.{module.split(".")[-1]}\n"
    output+="------------------\n\n"
    output += f".. automodule:: {module}\n"
    output += "    :members:\n"
    output += "    :undoc-members:\n"
    output += "    :show-inheritance:\n"
    output += "    :inherited-members:\n"
    return output

def loop_pkg(mname : str, displayname : str = None):
    if not displayname:
        displayname = mname

    output = ""
    pkg = __import__(mname)
    for finder, name, ispkg in pkgutil.walk_packages(pkg.__path__, pkg.__name__ + '.'):
        if ispkg:
            continue
        
        output += generate_submodule_rst(displayname, name)
        
    with open(os.path.join(os.path.dirname(__file__), f"{mname}.rst"), "w") as f:
        f.write(output)

if __name__ == "__main__":
    loop_pkg("zrcl4")
    loop_pkg("zrcl3_utils")