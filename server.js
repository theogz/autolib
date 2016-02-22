var express = require("express");
var app = express();
var PythonShell = require('python-shell');
var port = Number(process.env.PORT) || 3000;



app.use(express.static('public'));


app.get('/monitoring', function (req, res) {
    var longitude = req.query.long;
    var latitude = req.query.lat;
    var email = req.query.email;
    var options = {
        args: [3, longitude, latitude, "depart", email]
    };

    PythonShell.run('monitoring.py', options, function (err, results) {
        if (err) throw err;
        // results is an array consisting of messages collected during execution
        console.log('results: %j', results);
    });

    res.send("coordonnees : " + req.query.lat + " et " + req.query.long);
    // a terme modifier ca par sendFile pour la page de "traitement"
});

app.get('*', function (req, res) {
    res.status(404).send('404');
});

app.listen(port, function () {
  console.log('Example app listening on port 3000!');
});