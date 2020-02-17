if(typeof process === 'object' && process + '' === '[object process]'){
  // is node
  require('./nodejs/__init__');
}
else{
  // browser
  import('./browser/Ubiquity_pb.js').then(_ => {
    window.dispatchEvent(new Event('UBIQUITY_PROTO_LOADED'));
  });
}