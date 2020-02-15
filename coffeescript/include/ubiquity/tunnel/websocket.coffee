WebSocket = require('ws')


class WebSocketTunnel

  constructor: () ->

  wave_in: (wave) ->
    console.log('Message received.')
    console.log(wave)

  wave_out: (wave_pb) ->
    this._send_wave(wave_pb)
    console.log('Message sent.')
    console.log(wave_pb)


class WebSocketServerTunnel extends WebSocketTunnel

  constructor: (bind_host ###: string ### = 'localhost', bind_port ###: number ### = 5005) ->
    super()
    this._bind_host = bind_host
    this._bind_port = bind_port
    this._links = []
    this._ws = new WebSocket.Server({ port: 5005 })
    this._ws.on('connection', this._connect)

  _connect: (ws ###: WebSocket ###) ->
    this._links.push(ws)
    this._ws.on('close', this._client_disconnect)

  _client_disconnect: (ws ###: WebSocket ###) ->
    this._links = this._links.filter (w) -> w isnt ws

  _send_wave: (wave_raw ###: string ###) ->
    _send = (ws) -> ws.send(wave_raw)
    _send link for link in this._links

  __str__: ###: string ### ->
    return "WS:#{this._bind_host}:#{this._bind_port}"

  toString: ###: string ### ->
    return this.__str__()


class WebSocketClientTunnel extends WebSocketTunnel

  constructor: (server_host ###: string ###, server_port ###: number ### = 5005) ->
    super()
    this._server_host = server_host
    this._server_port = server_port
    this._ws = new WebSocket("ws://#{this._server_host}:#{this._server_port}")
    this._ws.on('open', this._connect)
    this._ws.on('close', this._client_disconnect)
    this._ws.on('message', this._receive_wave)

  _connect: ->
    console.log('Client Connected')

  _client_disconnect: (ws ###: WebSocket ###) ->
    console.log('Client Disconnected')

  _receive_wave: (message ###: string ###) ->
    console.log(message)
    super.wave_in(message)

  _send_wave: (wave_raw ###: string ###) ->
    this._ws.send(wave_raw)

  __str__: ###: string ### ->
    return "WS:#{this._server_host}:#{this._server_port}"

  toString: ###: string ### ->
    return this.__str__()


`
module.exports = {
  WebSocketClientTunnel: WebSocketClientTunnel,
  WebSocketServerTunnel: WebSocketServerTunnel
};
`

