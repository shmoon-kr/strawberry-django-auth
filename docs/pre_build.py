"""
- get class names and docstrings as context variables into the docs
- copy [CONTRIBUTORS, CHANGES, CONTRIBUTING] files to the docs dir
"""

import os
from pathlib import Path
import shutil
import re
from pydoc_markdown.interfaces import Context
from pydoc_markdown.contrib.loaders.python import PythonLoader
from pydoc_markdown.contrib.renderers.markdown import MarkdownRenderer

if __name__ == "__main__":

    # copy mixins file from .py to .yml
    root_dir = Path(__file__).parent.parent
    source = root_dir / "src/gqlauth/user/resolvers.py"
    destination = root_dir / "docs/data/api.yml"
    dest = shutil.copyfile(source, destination)

    # get the text content
    with open(destination, "r") as file:
        text = file.read()

    # extract each class and docstring
    pattern = re.compile(
        'class\s(?P<class>\w*)Mixin[\w|\(|\)]+:\n\s*"""(?P<doc>[^*]*)"""',
        re.S | re.M,
    )
    matches = re.findall(pattern, text)

    # build the yaml string
    yaml_strings = ["# this file is auto generated by the pre_docs_script.py", ""]
    for m in matches:
        class_name, docstring = m
        yaml_strings.append(class_name + ": |" + docstring)
    yaml_string = "\n".join(yaml_strings)

    # write the file
    with open(destination, "w") as file:
        file.write(yaml_string)


    # copy files from project root to docs dir
    files = ["CONTRIBUTORS.md", "CHANGES.md", "CONTRIBUTING.md"]
    dest = ["contributors.md", "changelog.md", "contributing.md"]
    for index, file in enumerate(files):
        shutil.copyfile(root_dir / file, root_dir / "docs" / dest[index])



    context = Context(directory=root_dir / 'src')
    loader = PythonLoader(search_path=['gqlauth'], modules=['decorators'])
    renderer = MarkdownRenderer(render_module_header=False,
                                render_typehint_in_data_header=True
                                )

    loader.init(context)
    renderer.init(context)
    header = """
# Decorators

---

    """
    modules = loader.load()
    with open(root_dir / 'docs' / 'decorators.md', 'w+') as f:
        f.write(header + renderer.render_to_string(modules))
