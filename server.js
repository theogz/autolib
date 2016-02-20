var express = require("express");
var app = express();
var PythonShell = require('python-shell');




app.use(express.static('public'));

app.get('/monitoring', function (req, res) {
    var longitude = req.query.long;
    var latitude = req.query.lat;

    var options = {
        args: [3, longitude, latitude, "depart"]
    };

    PythonShell.run('monitoring.py', options, function (err, results) {
        if (err) throw err;
        // results is an array consisting of messages collected during execution
        console.log('results: %j', results);
    });

    res.send("oui j'ai une voiture autour de " + req.query.long + " et " + req.query.lat);
});

app.get('*', function (req, res) {
    res.status(404).send('404');
});

app.listen(3000, function () {
  console.log('Example app listening on port 3000!');
});