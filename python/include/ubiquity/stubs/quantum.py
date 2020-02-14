from typing import Callable, Any, Iterable
from collections import OrderedDict

from ubiquity.types import \
    Field, \
    Parameter, \
    Method, \
    QuantumID, \
    ShoeboxIF, \
    WaveIF, \
    QuantumStub
from ubiquity.serialization.Method_pb2 import ParameterTypePB

from ubiquity.waves.field import \
    FieldGetRequestWave,\
    FieldGetResponseWave,\
    FieldSetRequestWave,\
    FieldSetResponseWave
from ubiquity.waves.method import \
    MethodCallRequestWave, \
    MethodCallResponseWave
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
                destination, self._quantum_id, method.name
            )
        # create new class
        class_name = QuantumStub.__name__ + str(self._quantum_id)
        stub_class = type(class_name, (QuantumStub,), {**properties, **methods})
        return stub_class()


def _send_and_wait(shoebox: ShoeboxIF, leaving_wave: WaveIF, timeout: int = DEFAULT_TIMEOUT_SECS):
    shoebox.wave_out(leaving_wave)
    try:
        _wave = shoebox.wait_on(leaving_wave.id, timeout=timeout)
    except TimeoutError:
        leaving_wave.logger.info('The request timed out!')
        return
    # on error
    if isinstance(_wave, ErrorWave):
        _wave.logger.error('\n' + _wave.error)
        return
    return _wave


def _get_getter_property_decorator(shoebox: ShoeboxIF, quantum_id: QuantumID,
                                   field_name: str) -> Callable:
    def _callable(_):
        wave_ = FieldGetRequestWave(shoebox, quantum_id, field_name)
        _wave = _send_and_wait(shoebox, wave_)
        if _wave is not None:
            # on success
            assert isinstance(_wave, FieldGetResponseWave)
            return _wave.field_value

    return _callable


def _get_setter_property_decorator(shoebox: ShoeboxIF, quantum_id: QuantumID,
                                   field_name: str) -> Callable:
    def _callable(_, value: Any):
        wave_ = FieldSetRequestWave(shoebox, quantum_id, field_name, value)
        _wave = _send_and_wait(shoebox, wave_)
        if _wave is not None:
            # on success
            assert isinstance(_wave, FieldSetResponseWave)

    return _callable


def _get_method_decorator(shoebox: ShoeboxIF,
                          quantum_id: QuantumID,
                          method_name: str) -> Callable:
    def _callable(_, *_args, **_kwargs):
        wave_ = MethodCallRequestWave(shoebox, quantum_id, method_name, _args, _kwargs)
        _wave = _send_and_wait(shoebox, wave_)
        if _wave is not None:
            # on success
            assert isinstance(_wave, MethodCallResponseWave)
            return _wave.return_value

    return _callable
