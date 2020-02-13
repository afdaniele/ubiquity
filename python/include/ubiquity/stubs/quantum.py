from typing import Callable, Any, Iterable
from collections import OrderedDict

from ubiquity.types import \
    Field, \
    Parameter, \
    Method, \
    QuantumID, \
    ShoeboxIF, \
    QuantumStub
from ubiquity.serialization.Method_pb2 import ParameterTypePB

from ubiquity.waves.field import \
    FieldGetRequestWave,\
    FieldGetResponseWave,\
    FieldSetRequestWave,\
    FieldSetResponseWave
from ubiquity.waves.error import ErrorWave

SIMPLE_PARAMETER_TYPES = [
    ParameterTypePB.DEFAULT,
    ParameterTypePB.POSITIONAL,
    ParameterTypePB.KEYWORD
]

DEFAULT_TIMEOUT_SECS = 20


class QuantumStubBuilder:

    def __init__(self, quantum_id: QuantumID):
        self._quantum_id = quantum_id
        self._fields = []
        self._methods = []

    def get_quantum_id(self) -> QuantumID:
        return self._quantum_id

    def add_field(self, field: Field):
        self._fields.append(field)

    def add_method(self, method: Method):
        self._methods.append(method)

    def build(self, destination: ShoeboxIF):
        # build properties
        properties = {}
        for field in self._fields:
            properties[field.name] = property(
                _get_getter_property_decorator(destination, self._quantum_id, field.name),
                _get_setter_property_decorator(destination, self._quantum_id, field.name)
            )
        # build methods
        methods = {}
        for method in self._methods:
            methods[method.name] = _get_method_decorator(
                destination, self._quantum_id, method.name, method.args
            )
        # create new class
        class_name = QuantumStub.__name__ + str(self._quantum_id)
        stub_class = type(class_name, (QuantumStub,), {**properties, **methods})
        return stub_class()


def _get_getter_property_decorator(shoebox: ShoeboxIF, quantum_id: QuantumID,
                                   field_name: str) -> Callable:
    def _callable(_):
        wave_ = FieldGetRequestWave(shoebox, quantum_id, field_name)
        shoebox.wave_out(wave_)
        try:
            _wave = shoebox.wait_on(wave_.id, timeout=DEFAULT_TIMEOUT_SECS)
        except TimeoutError:
            wave_.logger.info('The request timed out!')
            return
        # on error
        if isinstance(_wave, ErrorWave):
            _wave.logger.error('{:s}: {:s}\nTraceback:\n{:s}'.format(
                _wave.error_type, _wave.error_message, _wave.error_trace
            ))
            return
        # on success
        assert isinstance(_wave, FieldGetResponseWave)
        return _wave.field_value

    return _callable


def _get_setter_property_decorator(shoebox: ShoeboxIF, quantum_id: QuantumID,
                                   field_name: str) -> Callable:
    def _callable(_, value: Any):
        # wave_ = FieldSetRequestWave(shoebox, quantum_id, field_name)
        # shoebox.wave_out(wave_)
        # try:
        #     _wave = shoebox.wait_on(wave_.id, timeout=DEFAULT_TIMEOUT_SECS)
        # except TimeoutError:
        #     wave_.logger.info('The request timed out!')
        #     return
        # # on error
        # if isinstance(_wave, ErrorWave):
        #     _wave.logger.error('{:s}: {:s}\nTraceback:\n{:s}'.format(
        #         _wave.error_type, _wave.error_message, _wave.error_trace
        #     ))
        #     return
        # # on success
        # assert isinstance(_wave, FieldGetResponseWave)
        # return _wave.field_value
        pass

    return _callable


def _get_method_decorator(shoebox: ShoeboxIF,
                          quantum_id: QuantumID,
                          method_name: str,
                          method_args: Iterable[Parameter]) -> Callable:
    def _callable(_, *_args, **_kwargs):
        # nonlocal quantum_id, method_name, method_args
        args = OrderedDict()
        t = len(_args)
        # map simple args (either positional or keywords)
        simple_args = list(filter(lambda a: a.type in SIMPLE_PARAMETER_TYPES, method_args))
        num_simple_args = len(simple_args)
        f = min(num_simple_args, t)
        for i in range(f):
            args[simple_args[i].name] = _args[i]
        # map all the extra parameters to *args (if *args is in the prototype)
        var_positional_args = [a for a in method_args if a.type == ParameterTypePB.VAR_POSITIONAL]
        if t > f and var_positional_args:
            _star_arg = var_positional_args[0].name
            args[_star_arg] = _args[f:]
        # add kwargs
        var_keyword_args = [a for a in method_args if a.type == ParameterTypePB.VAR_KEYWORD]
        if var_keyword_args:
            args[var_keyword_args[0].name] = _kwargs
        # this is the networking part
        print('You called [Quantum:{:d}].{:s}({:s})'.format(
            quantum_id, method_name,
            ', '.join(['{:s}={:s}'.format(k, str(v)) for k, v in args.items()])
        ))

    return _callable
