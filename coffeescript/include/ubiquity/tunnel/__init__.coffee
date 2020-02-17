#websocket = require('./websocket')
protobuf = require("../serialization/google-protobuf");
field_pb = require('../serialization/Field_pb')

#ws = new websocket.WebSocketClientTunnel('localhost')

#send = () ->
#  ws.wave_out('ASD')
#
#setTimeout(send, 1000)

console.log('ASD')
console.log(field_pb)
