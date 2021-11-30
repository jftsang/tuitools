from jsonschema import validate

from interacttools import multi_input_dialog


def _example():
    schema = {
        'properties': {
            "name": {"type": "string"},
            "price": {"type": "number"},
        }
    }

    r = multi_input_dialog(schema).run()
    print(r)
    if r is not None:
        validate(r, schema)


_example()
