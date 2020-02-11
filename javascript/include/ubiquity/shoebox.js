var SIMPLE_PARAMETER_TYPES = [
  '__default__',
  '__positional__',
  '__keyword__'
];


class QuantumShoebox{

  constructor(name) {
    this.__name__ = name;
    this.__quanta__ = {};
    this.__objects__ = {};
    this.__content__ = {};
  }

  get name(){
    return this.__name__;
  }

  get content(){
    return this.__content__;
  }

  static from_quark(data){
    if (!data.__ubiquity_object__ || data.__type__ !== '__shoebox__') {
      console.error('SyntaxError: Expected object of type __shoebox__. Exiting.');
      return;
    }

    let shoebox =  new QuantumShoebox(data['__name__']);

    for (let [object_name, object_id] of Object.entries(data['__objects__'])) {
      let object_data = data['__quanta__'][object_id];
      if (!object_data.__ubiquity_object__ || object_data.__type__ !== '__stub__') {
        console.error('SyntaxError: Expected object of type __stub__. Exiting.');
        return;
      }
      // ---
      let object = {};
      // parse fields
      for (let [field_name, field_data] of Object.entries(object_data['__fields__'])) {
        if (!field_data.__ubiquity_object__ || field_data.__type__ !== '__field__') {
          console.error('SyntaxError: Expected object of type __field__. Exiting.');
          return;
        }
        // ---
        //TODO: add setter as well?
        Object.defineProperty(object, field_name, {
          get: _get_property_decorator(object_id, field_name)
        });
      }
      // parse methods
      for (let [method_name, method_data] of Object.entries(object_data['__methods__'])) {
        if (!method_data.__ubiquity_object__ || method_data.__type__ !== '__method__') {
          console.error('SyntaxError: Expected object of type __method__. Exiting.');
          return;
        }
        // ---
        object[method_name] = _get_method_decorator(object_id, method_name, method_data['__args__']);
      }
      // add object to shoebox
      shoebox.__quanta__[object_id] = object;
      shoebox.__objects__[object_name] = object_id;
      Object.defineProperty(shoebox.__content__, object_name, {
        get: function(){return shoebox.__quanta__[object_id];}
      });
    }
    // return freshly-built shoebox
    return shoebox;
  }

}


function _get_property_decorator(object_id, field_name){
  return function(){
    // this is the networking part
    return 'This is the value of "' + field_name + '"';
  }
}

function _get_method_decorator(object_id, method_name, method_args){
  return function(){
    let args = {};
    let t = arguments.length;
    method_args = Object.values(method_args);
    // map simple args (either positional or keywords)
    let simple_args = method_args.filter(a => SIMPLE_PARAMETER_TYPES.includes(a['__type__']));
    let num_simple_args = simple_args.length;
    let f = (t > num_simple_args)? num_simple_args : t;
    for (let i = 0; i < f; i++){
      args[simple_args[i]['__name__']] = arguments[i];
    }
    // map all the extra parameters to *args (if *args is in the prototype)
    let var_positional_args = method_args.filter(a => a['__type__'] === '__var_positional__');
    if (t > f && var_positional_args.length > 0) {
      let _star_arg = var_positional_args[0]['__name__'];
      args[_star_arg] = Object.values(arguments).slice(f);
    }
    // this is the networking part
    return 'You called: ' +
        method_name + '(' +
        JSON.stringify(args).slice(1, -1).replace(':', '=') +
        ');';
  }
}

module.exports = {
  QuantumShoebox: QuantumShoebox
};




// Compatibility matrix
// - Object.entries: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/entries
// - Object.keys: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/keys
// - Object.values: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/values
// - Array.prototype.filter: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/filter
// - Object.defineProperty: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/defineProperty
// - getter: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/get
// - arguments: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/arguments


