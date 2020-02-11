from typing import Callable, Dict, Any
from collections import OrderedDict

from ubiquity.types import \
    Field, \
    Parameter, \
    Method, \
    QuantumID


SIMPLE_PARAMETER_TYPES = [
  '__default__',
  '__positional__',
  '__keyword__'
]


class QuantumStub:
    pass


class QuantumStubBuilder:

    def __init__(self, shoebox: 'Shoebox', quantum_id: QuantumID):
        self._shoebox = shoebox
        self._quantum_id = quantum_id
        self._properties = {}
        self._methods = {}

    def add_field(self, field: Field):
        self._properties[field.name] = property(
            _get_getter_property_decorator(self._shoebox, self._quantum_id, field.name),
            _get_setter_property_decorator(self._shoebox, self._quantum_id, field.name)
        )

    def add_method(self, method: Method):
        self._methods[method.name] = _get_method_decorator(self._shoebox, self._quantum_id, method.name, method.args)

    def compile(self):
        # create new class
        class_name = QuantumStub.__name__ + str(self._quantum_id)
        stub_class = type(class_name, (QuantumStub,), {**self._properties, **self._methods})
        return stub_class()


def _get_getter_property_decorator(shoebox: 'Shoebox', quantum_id: QuantumID, field_name: str) -> Callable:
    def _callable():
        print('This is the value of [Quantum:{:d}].{:s}'.format(quantum_id, field_name))
    return _callable


def _get_setter_property_decorator(shoebox: 'Shoebox', quantum_id: QuantumID, field_name: str) -> Callable:
    def _callable(value: Any):
        print('You are setting [Quantum:{:d}].{:s} = [{:s}]'.format(quantum_id, field_name, str(value)))
    return _callable


def _get_method_decorator(shoebox: 'Shoebox', quantum_id: QuantumID, method_name: str, method_args: Dict[str, Parameter]) -> Callable:
    def _callable(*_args, **_kwargs):
        # nonlocal quantum_id, method_name, method_args
        args = OrderedDict()
        t = len(_args)
        # map simple args (either positional or keywords)
        simple_args = [
            a for a in method_args.values()
            if a.type in SIMPLE_PARAMETER_TYPES
        ]
        num_simple_args = len(simple_args)
        f = min(num_simple_args, t)
        for i in range(f):
            args[simple_args[i].name] = _args[i]
        # map all the extra parameters to *args (if *args is in the prototype)
        var_positional_args = [a for a in method_args.values() if a.type == '__var_positional__']
        if t > f and var_positional_args:
            _star_arg = var_positional_args[0].name
            args[_star_arg] = _args[f:]
        # add kwargs
        args.update(_kwargs)
        # this is the networking part
        print('You called [Quantum:{:d}].{:s}({:s})'.format(
            quantum_id, method_name, ', '.join(['{:s}={:s}'.format(k, str(v)) for k, v in args.items()])
        ))
    return _callable
