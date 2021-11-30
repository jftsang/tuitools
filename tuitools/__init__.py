from typing import TypeVar, Dict

from prompt_toolkit import Application
from prompt_toolkit.application import get_app
from prompt_toolkit.formatted_text import AnyFormattedText
from prompt_toolkit.key_binding import merge_key_bindings, KeyBindings
from prompt_toolkit.key_binding.bindings.focus import focus_next, focus_previous
from prompt_toolkit.key_binding.defaults import load_key_bindings
from prompt_toolkit.layout import HSplit, D, VSplit, Layout
from prompt_toolkit.widgets import Button, TextArea, Dialog, Label, ValidationToolbar

Schema = TypeVar("Schema")


class NumericInput(TextArea):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ...  # TODO
        return
        # self.validator = NumericValidator
        # self.validator = NotImplemented

    @property
    def text(self) -> float:
        return float(self.buffer.text)


def make_field(field_name: str, schema: Schema) -> TextArea:
    """Create a field that's suitable to the specified schema, such as
    a TextArea. The schema is used to determine the proper type of field
    as well as the validator that applies.
    """
    # At the moment, the only supported field type is TextArea. In the
    # future, other types such as NumericInput may be supported.
    # completer = FuzzyWordCompleter(['alpha', 'beta', 'gamma', 'delta', 'omicron'])
    # validator = Validator.from_callable(lambda s: len(s) == 5)
    field_schema = schema['properties'][field_name]
    completer = None
    validator = None
    if field_schema['type'] == 'number':
        cls = NumericInput
    else:
        cls = TextArea

    return cls(
        multiline=False,
        completer=completer,
        validator=validator,
        complete_while_typing=True
    )


class SchemaForm(Application[str]):
    """An application that consists of a form from a schema"""
    def __init__(self, schema, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.schema = schema  # TODO do something with this

    def run(self, *args, **kwargs) -> Dict:
        r = super().run(*args, **kwargs)
        return dict(r) if r is not None else None


def multi_input_dialog(
        schema: Schema,
        title: AnyFormattedText = "",
        text: AnyFormattedText = "",
) -> SchemaForm:
    """
    Display a few input boxes. Creates an application that, when run,
    returns either the given information, or None when cancelled.
    """
    # def accept(buf: Buffer) -> bool:
    #     get_app().layout.focus(ok_button)
    #     return True  # Keep text.

    def ok_handler() -> None:
        # Return type of this handler is None; the dict is actually the
        # return value of Application.run()
        r = {field_name: field.text for field_name, field in fields.items()}
        get_app().exit(result=r)

    def cancel_handler() -> None:
        get_app().exit()

    ok_button = Button(text='OK', handler=ok_handler)
    cancel_button = Button(text='Cancel', handler=cancel_handler)

    fields = {
        field_name: make_field(field_name, schema)
        for field_name in schema['properties'].keys()
    }

    # noinspection PyTypeChecker
    # Pylint's type checker expects list contents to all have the same
    # type. This is inappropriate in this case.
    dialog_body = HSplit(
        [
            Label(text=text, dont_extend_height=True)
        ] + [
            VSplit([
                Label(text=field_name),
                field
            ])
            for field_name, field in fields.items()
        ] + [
            ValidationToolbar(),
        ],
        padding=D(preferred=1, max=1)
    )

    dialog = Dialog(
        title=title,
        body=dialog_body,
        buttons=[ok_button, cancel_button],
        with_background=True,
    )

    bindings = KeyBindings()
    bindings.add("down")(focus_next)
    bindings.add("up")(focus_previous)

    return SchemaForm(
        schema,
        layout=Layout(dialog),
        key_bindings=merge_key_bindings([load_key_bindings(), bindings]),
        mouse_support=True,
        style=None,
        full_screen=True,
    )


def prompt_for_dict(schema: Schema) -> Dict:
    return multi_input_dialog(schema).run()
