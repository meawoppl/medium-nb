import os
import uuid

import nb.latex


def load_content_file(path: str):
    """
    Read a path, replace equation tags
    with placeholders.  Return
     - The markdown with placeholders
     - A dict keying placeholders to equation contents
    """
    assert os.path.isfile(path), path

    content = ""
    equations = {}
    equation_count = 0
    with open(path) as f:
        lines = list(f.readlines())

    # NOTE(MRG) GROSSSSS
    line_number = 0
    while line_number < len(lines):
        line_content = lines[line_number]
        if line_content.strip() != "$":
            content += line_content
            line_number += 1
            continue

        # Ignore the $
        line_number += 1
        equation_content = ""
        while True:
            line_content = lines[line_number]
            if line_content.strip() == "$":
                line_number += 1
                break
            equation_content += line_content
            line_number += 1
        eq_id = "EQUATION_PLACEHOLDER_" + str(equation_count)
        content += eq_id + "\n"
        equations[equation_count] = equation_content.strip()
        equation_count += 1

    return content, equations


def replace_content_placeholders(content: str, ids_to_url: dict):
    new_content = str(content)
    for anchor, url in ids_to_url.items():
        new_content.replace(anchor, "![{anchor}]({url})".format(anchor=anchor, url=url))
    return new_content
