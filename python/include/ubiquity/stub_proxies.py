from typing import Union, Callable, Any

from ubiquity.types import ShoeboxIF, WaveIF, QuantumID

DEFAULT_TIMEOUT_SECS = 10


def _send_and_wait(shoebox: ShoeboxIF, leaving_wave: WaveIF,
                   timeout: int = DEFAULT_TIMEOUT_SECS) -> Union[None, WaveIF]:
    # ---
    from ubiquity.waves.error import ErrorWave
    # ---
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


def _get_getter_property_decorator(shoebox: ShoeboxIF,
                                   quantum_id: QuantumID,
                                   field_name: str) -> Callable:
    # ---
    from ubiquity.waves.field import \
        FieldGetRequestWave, \
        FieldGetResponseWave
    # ---

    def _callable(_):
        wave_ = FieldGetRequestWave(shoebox, quantum_id, field_name)
        _wave = _send_and_wait(shoebox, wave_)
        if _wave is not None:
            # on success
            assert isinstance(_wave, FieldGetResponseWave)
            return _wave.field_value

    return _callable


def _get_setter_property_decorator(shoebox: ShoeboxIF,
                                   quantum_id: QuantumID,
                                   field_name: str) -> Callable:
    # ---
    from ubiquity.waves.field import \
        FieldSetRequestWave, \
        FieldSetResponseWave
    # ---

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
    # ---
    from ubiquity.waves.method import \
        MethodCallRequestWave, \
        MethodCallResponseWave
    # ---

    def _callable(_, *_args, **_kwargs):
        wave_ = MethodCallRequestWave(shoebox, quantum_id, method_name, _args, _kwargs)
        _wave = _send_and_wait(shoebox, wave_)
        if _wave is not None:
            # on success
            assert isinstance(_wave, MethodCallResponseWave)
            return _wave.return_value

    return _callable
