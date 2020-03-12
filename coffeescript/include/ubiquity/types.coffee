uuid4 = require('uuid4')

DEFAULT_TIMEOUT_SECS = 10
PRIMITIVE_TYPES = [number, String, null]
ITERABLE_TYPES = [Array, Set]

class Logger
  constructor: (name) ->
    this._name = name

  _log: (type, message) ->
    console.log("#{type}:#{message}")

  info: (message) ->
    this._log('INFO', message)

  warn: (message) ->
    this._log('WARN', message)

  error: (message) ->
    this._log('ERROR', message)


class ShoeboxContent
  constructor: () ->


class QuantumStub
  constructor: () ->


class ParameterType
  # NOTE: This has to match the PB protocol
  DEFAULT = 0
  POSITIONAL = 1
  KEYWORD = 2
  VAR_POSITIONAL = 3
  VAR_KEYWORD = 4

  from_inspect_type: (itype) ->
    # TODO: Likely this is useless
    return null


class ShoeboxIF

  constructor: (name) ->
    this._name = name
    this._quanta = {}
    this._tunnels = {}
    this._objects = {}
    this._waves_in = {}
    this.__logger__ = new Logger(this.toString())
#    TODO: semaphore here
    this._waves_in_lock = null
    self._content = new ShoeboxContent()

    Object.defineProperties @prototype,
      name:
        get: -> this._name

      quanta:
        get: -> this._quanta

      objects:
        get: -> this._objects

      content:
        get: -> this._content

      logger:
        get: -> this.__logger__

  register_quantum: (
    obj ###: any ###,
    quantum_id ###: null | number ### = null
  ) ###: number ###->
    throw "NotImplementedError"

  name_quantum: (name ###: str ###, quantum_id ###: number ###) ->
    throw "NotImplementedError"

  add: (name ###: str ###, obj ###: any ###) ->
    throw "NotImplementedError"

  attach: (tunnel ###: TunnelIF ###) ->
    throw "NotImplementedError"

  detach: (tunnel ###: TunnelIF ###) ->
    throw "NotImplementedError"

  wave_in: (wave ###: WaveIF ###) ->
    throw "NotImplementedError"

  wave_out: (wave ###: WaveIF ###) ->
    throw "NotImplementedError"

  wait_on: (request_wave ###: string | WaveIF ###, timeout ###: number ### = -1) ->
    throw "NotImplementedError"

  destroy: ->
    throw "NotImplementedError"

  serialize: ###: ShoeboxPB ### ->
    throw "NotImplementedError"

  deserialize: (shoebox_pb ###: ShoeboxPB ###) ###: ShoeboxIF ### ->
    throw "NotImplementedError"

  toString: ###: string ### ->
    return "SB[#{this.name}]"

  __str__: ###: string ### ->
    return this.toString()


class TunnelIF

  constructor: () ->
    this._shoebox = null
    this._is_shutdown = false
    this.__logger__ = null

    Object.defineProperties @prototype,
      shoebox:
        get: -> this._shoebox

      is_shutdown:
        get: -> this._is_shutdown

      logger:
        get: ->
          if this.__logger__ == null
            this.__logger__ = new Logger("TN\\#{this.toString()}/")
          return this.__logger__

  start: () ->
    throw "NotImplementedError"

  shutdown: () ->
    this._is_shutdown = true

  attach: (shoebox ###: ShoeboxIF ###) ->
    throw "NotImplementedError"

  detach: () ->
    throw "NotImplementedError"

  wave_in: (wave_raw ###: string ###) -> ###: Union[WaveIF, null] ###
    throw "NotImplementedError"

  wave_out: (wave ###: WaveIF ###) ->
    throw "NotImplementedError"

  _send_wave: (wave_raw ###: string ###) ->
    throw "NotImplementedError"

  toString: ###: string ### ->
    throw "NotImplementedError"

  __str__: ###: string ### ->
    return this.toString()


class WaveIF
  _type = "**"

  constructor: (
    shoebox ###: Union[ShoeboxIF, null] ###,
    quantum_id ###: Union[QuantumID, null] ###,
    request_wave ###: Union[string, null] ###,
    wave_id ###: Union[string, null] ### = null
  ) ->
    if wave_id == null
      this._id = uuid4()
    else
      this._id = wave_id
    this._shoebox = shoebox
    this._quantum_id = quantum_id
    this._request_wave = request_wave
    this.__logger__ = new Logger(this.toString())

    Object.defineProperties @prototype,
      id:
        get: ###: Union[string, null] ### ->
          this._id

      shoebox:
        get: ###: Union[ShoeboxIF, null] ### ->
          this._shoebox

      quantum_id:
        get: ###: Union[QuantumID, null] ### ->
          this._quantum_id

      request_wave:
        get: ###: Union[string, null] ### ->
          this._request_wave

      logger:
        get: ###: Union[string, null] ### ->
          return this.__logger__

  hit: (shoebox ###: Union[ShoeboxIF, null] ###) ###: Union[WaveIF, null] ### ->
    throw "NotImplementedError"

  _serialize: () ###: Any ### ->
    throw "NotImplementedError"

  deserialize: (wave_pb ###: Any ###) ###: WaveIF ### ->
    throw "NotImplementedError"

  serialize: () ###: WavePB ### ->
    throw "NotImplementedError"

  serialize_data: () ###: Any ### ->
    throw "NotImplementedError"

  toString: ###: string ### ->
    return "WV{#{this._id[0..7]}}#{this._type}"

  __str__: ###: string ### ->
    return this.toString()


class Field

  constructor: (name ###: string ###, ftype ###: FieldType ###) ->
    this._name = name
    this._type = type

    Object.defineProperties @prototype,
      name:
        get: ###: Union[string, null] ### ->
          this._name

      type:
        get: ###: Union[ShoeboxIF, null] ### ->
          this._type

  serialize: () ###: FieldPB ### ->
    return proto.FieldPB().setName(this._name).setType(this._type.toString())


class Parameter

  constructor: (name ###: string ###,
                ptype ###: ParameterType ###,
                annotation ###: Any ###,
                default_value ###: Any ###
  ) ->
    this._name = name
    this._type = ptype
    this._annotation = annotation
    this._default_value = default_value

    Object.defineProperties @prototype,
      name:
        get: ###: string ### ->
          this._name

      type:
        get: ###: ParameterType ### ->
          this._type

      annotation:
        get: ###: Any ### ->
          this._annotation

      default:
        get: ###: Any ### ->
          this._default_value

  serialize: () ###: FieldPB ### ->
    return proto.ParameterPB()
      .setName(this._name)
      .setType(this._type)
      .setAnnotation(this._annotation)


class Method

  constructor: (name ###: string ###, args ###: Iterable[Parameter] ###) ->
    this._name = name
    this._args = args

    Object.defineProperties @prototype,
      name:
        get: ###: string ### ->
          this._name

      args:
        get: ###: Iterable[Parameter] ### ->
          this._args

  serialize: () ###: MethodPB ### ->
    _s = (p) -> p.serialize()
    return proto.MethodPB()
      .setName(this._name)
      .setArgs(_s p for p in this._args)


class Quantum

  constructor: (quantum_id ###: QuantumID ###) ->
    this._id = quantum_id
    this._fields = []
    this._methods = []
    this.__logger__ = new Logger(this.toString())

    Object.defineProperties @prototype,
      id:
        get: ###: QuantumID ### ->
          this._id

      fields:
        get: ###: Iterable[Field] ### ->
          this._fields

      methods:
        get: ###: Iterable[Method] ### ->
          this._methods

      logger:
        get: ###: Logger ### ->
          this._logger

  add_field: (field ###: Field ###) ->
    this._fields.push(field)

  add_method: (method ###: Method ###) ->
    this._methods.push(method)

  serialize: () ###: MethodPB ### ->
    _f = (f) -> f.serialize()
    _m = (m) -> m.serialize()
    return proto.QuantumPB()
      .setId(this._id)
      .setFieldsList(_f field for field in this._fields)
      .setMethodsList(_m method for method in this._methods)

  deserialize: (quantum_pb ###: QuantumPB ###) ###: Quantum ### ->
    quantum = Quantum(quantum_pb.getId())
    for field in quantum_pb.getFieldsList()
      quantum.add_field(Field(field.getName(), field.getType()))
    for method in quantum_pb.getMethodsList()
      quantum.add_method(Method(
        method.getName(),
        (
          Parameter(
            p.getName(),
            ParameterType(p.getType()),
            p.getAnnotation(),
            deserialize_any(p.getDefaultValue())
          ) for p in method.getArgsList()
        )
      ))
    return quantum

  toString: ###: string ### ->
    return "QT+{#{this._id}}"

  __str__: ###: string ### ->
    return this.toString()

  from_object: (obj ###: Any ###, quantum_id ###: QuantumID ###) ###: Tuple[QuantumID, Quantum] ### ->
    # base case: already a quantum
    if obj instanceof Quantum
      return [obj.id, obj]
    # base case: quantumStubs are for local use only, cannot turn it back into a quantum
    if obj instanceof QuantumStub
        throw 'Objects of type QuantumStub cannot be turned back into a Quantum'
    # if the ID is not given, a new one will be assigned
    # TODO: fix this as there is no id() function in JS
    if quantum_id is null
      quantum_id = 0
    # create stub for the object
    stub = Quantum(quantum_id)
    # add fields to stub
    # TODO: find something similar to gemembers()
    # add methods to stub
    # TODO: find something similar to gemembers()
    # ---
    return [quantum_id, stub]

  to_stub: (destination ###: ShoeboxIF ###) ###: QuantumStub ### ->
    # TODO: find something similar to property()
    return 0

  build_stubs: (obj ###: Any ###, shoebox ###: ShoeboxIF ###) ###: Any ### ->
    # primitives
    for type in PRIMITIVE_TYPES
      if obj instanceof type
        return obj
    # iterables
    for type in ITERABLE_TYPES
      if obj instanceof type
        return (Quantum.build_stubs(e, shoebox) for e in obj)
    # Quantum
    if obj instanceof Quantum
      return obj.to_stub(shoebox)
    # ---
    throw "Cannot build Stub for object of type {#{typeof obj}}"
