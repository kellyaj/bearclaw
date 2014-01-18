var connect = require('connect');
var port = 8090;

process.stdout.write("Running server on port " + port + "...\r\n");

 connect.createServer(
     connect.static(__dirname)
).listen(port);
