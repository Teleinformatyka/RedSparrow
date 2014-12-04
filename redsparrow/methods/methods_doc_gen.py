import json
import inspect

from jsonschema import validate, ValidationError
from tornado_json.utils import is_method
from tornado_json.constants import HTTP_METHODS
from tornado_json.requesthandlers import APIHandler

from redsparrow.methods.base import BaseMethod

# stolen from https://github.com/hfaran/Tornado-JSON/blob/master/tornado_json/api_doc_gen.py
def _validate_example(rh, method, example_type):
    """Validates example against schema

    :returns: Formatted example if example exists and validates, otherwise None
    :raises ValidationError: If example does not validate against the schema
    """
    if not hasattr(method, example_type + "example"):
        return None
    example = getattr(method, example_type + "_example")
    schema = getattr(method, example_type + "_schema")

    if example is None:
        return None

    try:
        validate(example, schema)
    except ValidationError as e:
        raise ValidationError(
            "{}_example for {}.{} could not be validated.\n{}".format(
                example_type, rh.__name__, method.__name__, str(e)
            )
        )

    return json.dumps(example, indent=4)


def _get_rh_methods(method):
    """Yield all HTTP methods in ``rh`` that are decorated
    with schema.validate"""
    for k, v in vars(rh).items():
        if all([
            k in HTTP_METHODS,
            is_method(v),
            hasattr(v, "input_schema")
        ]):
            yield (k, v)


def methods_doc_gen(methods):
    """
    Generates GitHub Markdown formatted API documentation using
    provided schemas in RequestHandler methods and their docstrings.

    :type  routes: [(url, RequestHandler), ...]
    :param routes: List of routes (this is ideally all possible routes of the
        app)
    """
    documentation = []
    # Iterate over routes sorted by url
    for method_dict in methods:
        method = getattr(method_dict['class'], method_dict['original_name'])
        route_doc = """
# {0}
    JSON-RPC

{1}
""".format(
            # Escape markdown literals
            method_dict['name'],
            "\n\n".join(
                [
"""**Args**
{0}


**Input Schema**
```json
{1}
```
{4}
**Output Schema**
```json
{2}
```
{5}

**Notes**

{3}

""".format(
            """
{}
            """.format("\n\n * ".join(['*'] + method_dict['args'])) if len(method_dict['args']) > 0 else "None",

            json.dumps(method.input_schema, indent=4) if hasattr(method, 'input_schema') else "",
            json.dumps(method.output_schema, indent=4) if hasattr(method, 'output_schema') else "",
            inspect.getdoc(method),
"""
**Input Example**
```json
{}
```
""".format(_validate_example(method_dict['class'], method, "input")) if _validate_example(
            method_dict['class'], method, "input") else "",
"""
**Output Example**
```json
{}
```
""".format(_validate_example(method_dict['class'], method, "output")) if _validate_example(
            method_dict['class'], method, "output") else "",
        )
                ]
            )
        )
        # END ROUTE_DOC #

        if issubclass(method_dict['class'], BaseMethod):
            documentation.append(route_doc)

    # Documentation is written to the root folder
    with open("ZMQ_Methods_Documentation.md", "w+") as f:
        f.write(
            "**This documentation is automatically generated.**\n\n" +
            "\n<br>\n<br>\n".join(documentation)
        )
