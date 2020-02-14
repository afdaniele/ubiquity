// var fs = require('fs');
// let stdinBuffer = fs.readFileSync(0);
// let data = JSON.parse(stdinBuffer.toString());

var ubiquity = require('./shoebox');

var exec = require('child_process').exec;
function execute(command, callback){
    exec(command, function(error, stdout, stderr){ callback(stdout); });
};

function load_data_from_file(){
  execute(
    'cat ./test.quark',
    function(d){
      global.data = JSON.parse(d);
      console.log('Loaded!');
    }
  );
}

function load_data_from_python(){
  execute(
    'cat ./test.quark',
    function(d){
      global.data = JSON.parse(d);
      console.log('Loaded!');
    }
  );
}

module.exports = {
    ubiquity: ubiquity,
    load_data: load_data_from_file,
    // load_data: load_data_from_python
};

