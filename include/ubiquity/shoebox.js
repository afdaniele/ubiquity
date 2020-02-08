var fs = require('fs');
let stdinBuffer = fs.readFileSync(0);
let data = JSON.parse(stdinBuffer.toString());

console.log(JSON.stringify(data, null, 2));

let shoebox = {
  id: data['__.id__'],
  objects: {}
};

if (!data.__ubiquity_object__ || data.__type__ !== '__shoebox__') {
  console.error('SyntaxError: Expected object of type __shoebox__. Exiting.');
  return;
}

for (let [object_id, object_data] of Object.entries(data['__.objects__'])) {
  if (!object_data.__ubiquity_object__ || object_data.__type__ !== '__stub__') {
    console.error('SyntaxError: Expected object of type __stub__. Exiting.');
    return;
  }
  // ---
  let object = {};
  // parse fields
  for (let [field_name, field_data] of Object.entries(object_data['__.fields__'])) {
    if (!field_data.__ubiquity_object__ || field_data.__type__ !== '__field__') {
      console.error('SyntaxError: Expected object of type __field__. Exiting.');
      return;
    }
    // ---
    Object.defineProperty(object, field_name, {
      get: _get_property_decorator(object_id, field_name)
    });
  }
  // parse methods
  for (let [method_name, method_data] of Object.entries(object_data['__.methods__'])) {
    if (!method_data.__ubiquity_object__ || method_data.__type__ !== '__method__') {
      console.error('SyntaxError: Expected object of type __method__. Exiting.');
      return;
    }
    // ---
    fcn = function(){

    }
  }






  // add object to shoebox
  console.log(Object.getOwnPropertyNames(object));
  shoebox.objects[object_id] = object;
}



function _get_property_decorator(object_id, field_name){
  return function(){
    // this is the networking part
    return 'This is the value of "' + field_name + '"';
  }
}

// console.log(JSON.stringify(shoebox, null, 2));
