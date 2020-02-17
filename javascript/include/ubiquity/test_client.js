// Generated by CoffeeScript 2.5.1
(function() {
  var tunnel, wave, ws;

  require('./serialization/Ubiquity_pb');

  ws = require('./tunnel/websocket');

  tunnel = new ws.WebSocketClientTunnel('localhost');

  wave = new proto.WavePB().setHeader(new proto.WaveHeaderPB().setId('asdddd').setType(proto.WaveTypePB.SHOEBOX).setShoebox('my_shoebox')).setShoebox(new proto.ShoeboxPB());

  setTimeout(function() {
    return tunnel.wave_out(wave);
  }, 1000);

  //console.log(wave.toObject());

}).call(this);
