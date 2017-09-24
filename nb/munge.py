import os
import uuid

import nb.latex


def eq_number_to_placeholder(id: int) -> str:
    return "EQUATION_PLACEHOLDER_" + str(id)


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
        eq_id = eq_number_to_placeholder(equation_count)
        content += eq_id + "\n"
        equations[equation_count] = equation_content.strip()
        equation_count += 1

    return content, equations


def replace_content_placeholders(content: str, ids_to_url: dict):
    new_content = str(content)
    for id, url in ids_to_url.items():
        placeholder_str = eq_number_to_placeholder(id)
        new_content = new_content.replace(placeholder_str, "![equation_{id}]({url})".format(id=id, url=url))
    return new_content
