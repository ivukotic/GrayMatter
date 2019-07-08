
console.log('ServiceX server starting ... ');

const fs = require('fs');

const express = require('express');
const http = require('http');
// const rRequest = require('request');

const config = require('./config.json');

let secretsPath = '/etc/';

const esConfig = JSON.parse(fs.readFileSync(`${secretsPath}elasticsearch/elasticsearch.json`));
config.ES_HOST = `http://${esConfig.ES_USER}:${esConfig.ES_PASS}@${esConfig.ES_HOST}:9200`;

console.log(config);

const app = express();
app.use(express.json());

app.get('/individual', (req, res) => {
    const individual = {

    };
    res.status_code(200).send(individual);
});


app.use((err, _req, res, _next) => {
    console.error(err.stack);
    res.status(500).send(err.message);
});

http.createServer(app).listen(80, () => {
    console.log('Your server is listening on port 80.');
});
