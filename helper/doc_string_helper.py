from account.api.user import UserResource

import docutils.nodes
from docutils.core import publish_doctree
import re

import sys

print(UserResource.on_get.__doc__)
# print(UserResource.on_post.__doc__)
print(type(UserResource.on_post.__doc__))

user_doc = UserResource.on_post.__doc__
user_doc.expandtabs()


# for a in user_doc:
#     print(a)

# help(docutils)
# print(publish_doctree(user_doc))

# ------------------------------------------------------------------
def walk(doctree, dictionary):
    literal_block_key = None
    for doc in doctree:
        if isinstance(doc, docutils.nodes.field_list):
            for child in doc:
                if isinstance(child, docutils.nodes.field):
                    field_name = None
                    for field in child:
                        if isinstance(field, docutils.nodes.field_name):
                            field_name = field.rawsource
                        elif isinstance(field, docutils.nodes.field_body):
                            if field_name in dictionary and isinstance(dictionary[field_name], list):
                                dictionary[field_name].append(field.rawsource)
                            elif field_name in dictionary and not isinstance(dictionary[field_name], list):
                                dictionary[field_name] = [dictionary[field_name], ]
                                dictionary[field_name].append(field.rawsource)
                            else:
                                dictionary[field_name] = field.rawsource
                else:
                    continue
        # Check for literal block in docstring (i.e. :input_body:: followed by json schema)
        elif isinstance(doc, docutils.nodes.paragraph):
            if re.search(r':*::', doc.rawsource) is not None:
                literal_block_key = doc.rawsource[1:-2]
            else:
                break
        # Get the literal block value and insert it into the dictionary
        elif isinstance(doc, docutils.nodes.literal_block):
            if literal_block_key is not None:
                dictionary[literal_block_key] = doc.rawsource
                literal_block_key = None
        else:
            walk(doc, dictionary)


result={}

# doctree = publish_doctree(user_doc)
# result['resource'] = {}
# walk(doctree, result['resource'])
#
if user_doc is not None:
    doctree = publish_doctree(user_doc)
    result['resource'] = {}
    walk(doctree, result['resource'])

for member in UserResource.__dict__.keys():
    if str(UserResource.__dict__[member]).find("function") == -1 and str(UserResource.__dict__[member]).find(
            "cyfunction") == -1:
        continue

    if UserResource.__dict__[member].__doc__ is not None:
        doctree = publish_doctree(UserResource.__dict__[member].__doc__)
        result[member] = {}
        walk(doctree, result[member])

# print(result)
# -----------------------------------------------------------
#
print(user_doc.expandtabs().splitlines()[5])

# print(type(user_doc.expandtabs().splitlines()))


# def trim_doc_string(docstring):
#     if not docstring:
#         return ""
#
#     # Convert tabs to spaces (following the normal Python rules)
#     # and split into a list of lines:
#     lines = docstring.expandtabs().splitlines()
#
#     # print(list)
#
#     # Determine minimum indentation (first line doesn't count):
#     indent = sys.maxsize
#
#     for line in lines[1:]:
#         stripped = line.lstrip()
#         if stripped:
#             indent = min(indent, len(line) - len(stripped))
#     # Remove indentation (first line is special):
#     trimmed = [lines[0].strip()]
#     if indent < sys.maxsize:
#         for line in lines[1:]:
#             trimmed.append(line[indent:].rstrip())
#     # Strip off trailing and leading blank lines:
#     while trimmed and not trimmed[-1]:
#         trimmed.pop()
#     while trimmed and not trimmed[0]:
#         trimmed.pop(0)
#
#     # Current code/unittests expects a line return at
#     # end of multiline docstrings
#     # workaround expected behavior from unittests
#     if "\n" in docstring:
#         trimmed.append("")
#
#     # Return a single string:
#     return "\n".join(trimmed)
#
#
# mydoc = trim_doc_string(user_doc)
#
# print(mydoc)