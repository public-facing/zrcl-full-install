import os
import pkgutil
import sys
# Add the path to the directory containing your source files
source_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src'))
print(source_dir)
sys.path.insert(0, source_dir)

# Add the path to the directory containing your module to the system path

package_name = 'zrcl'

def extract_import_lines(module):
    importlines = []
    bracketed = False
    with open(os.path.join(source_dir, module.replace(".", os.path.sep) + ".py"), "r") as f:
        for line in f.readlines():
            oline = line
            line = line.strip()
            if bracketed and not line.endswith(")"):
                importlines.append(oline)
            elif bracketed and line.endswith(")"):
                importlines.append(oline)
                bracketed = False
            elif line.startswith("import") or line.startswith("from"):
                importlines.append(oline)
                if line.endswith("("):
                    bracketed = True
            elif not line:
                continue
            else:
                break

    return importlines


def generate_submodule_rst(pkg_name, module):
    output = ""

    output+= f"{pkg_name}.{module.split(".")[-1] if "__" not in module else pkg_name}\n"
    output+="-------------------------------------------\n\n"

    # add block for imports
    importlines = extract_import_lines(module)
    output += ".. code-block:: python\n\n"
    output += "\n".join(f"\t{line}" for line in importlines)

    output += f"\n.. automodule:: {module}\n"
    output += "    :members:\n"
    output += "    :undoc-members:\n"
    output += "    :show-inheritance:\n"
    output += "    :inherited-members:\n\n"
    return output

def loop_pkg(mname : str, displayname : str = None):
    print(f"running {mname}")

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
    loop_pkg("zrcl3_uses")