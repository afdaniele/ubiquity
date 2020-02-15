DEFAULT_TIMEOUT_SECS = 10

class Logger
  constructor: (name) ->
    this._name = name

  info: (message) ->
    console.log("INFO:#{this._message}")

  warn: (message) ->
    console.warn(message)

  error: (message) ->
    console.error(message)

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

  register_quantum: (obj ###: any ###, quantum_id ###: null | number ### = null) ###: number ###->
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



