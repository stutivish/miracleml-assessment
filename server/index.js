const express = require('express');
const app = express();
const cors = require('cors');
const { Pool } = require('pg');

app.use(cors())

const pool = new Pool({
    user: 'stuti',
    host: 'localhost',
    database: 'clinical_trials',
    port: 5432,
  });
  
  app.get('/', async (req, res) => {
    try {
      const { rows } = await pool.query('SELECT * FROM combined');
      res.json(rows);
    } catch (err) {
      console.error('Error executing query', err);
      res.status(500).json({ error: 'Internal server error' });
    }
  });

// app.get('/', (req, res) => {
//     res.send('Hello from our server!')
// })

app.listen(8080, () => {
    console.log('server listening on port 8080')
})