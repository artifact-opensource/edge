const express = require('express');
const basicAuth = require('express-basic-auth');
const path = require('path');
const app = express();

// Basic auth via environment (for example usage). For production, replace with OIDC proxy.
const USERS = {};
if(process.env.VIS_USER && process.env.VIS_PASS){ USERS[process.env.VIS_USER]=process.env.VIS_PASS; }

if(Object.keys(USERS).length>0){
  app.use(basicAuth({ users: USERS, challenge: true }))
}

app.use('/', express.static(path.join(__dirname, '../../')));

const port = process.env.PORT || 8080;
app.listen(port, ()=> console.log(`Visualizer server listening on ${port}`));
