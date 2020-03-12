// The original idea of this file was to load a browserified version
// of the pb definitions in case of browser and a more structured version
// for nodejs. It turns out that the browserified version works for both,
// so we are going to keep it like this for now.


if(typeof process === 'object' && process + '' === '[object process]'){
  // is node
  // require('./nodejs/__init__');
  require('./browser/Ubiquity_pb');
}else{
  // browser
  // import('./browser/Ubiquity_pb.js').then(_ => {
  //   window.dispatchEvent(new Event('UBIQUITY_PROTO_LOADED'));
  // });
}
