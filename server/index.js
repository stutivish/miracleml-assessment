const express = require('express');
const app = express();
const cors = require('cors');
const { Pool } = require('pg');

app.use(cors())

// connect to database
const pool = new Pool({
    user: 'stuti',
    host: 'localhost',
    database: 'clinical_trials',
    port: 5432,
  });

// API Calls
app.get('/us', async (req, res) => {
    try {
      const { rows } = await pool.query('SELECT * FROM us');
      res.json(rows);
    } catch (err) {
      console.error('Error executing query', err);
      res.status(500).json({ error: 'Internal server error' });
    }
  });

  app.get('/eu', async (req, res) => {
    try {
      const { rows } = await pool.query('SELECT * FROM eu');
      res.json(rows);
    } catch (err) {
      console.error('Error executing query', err);
      res.status(500).json({ error: 'Internal server error' });
    }
  });
  
  app.get('/combined', async (req, res) => {
    // utilize query to filter data in combined 
    const queryType = req.query.type || null;
    const queryTerm = req.query.term || null
    
    try {
        let query;
        if (queryType === 'conditions') {
            query = `SELECT * FROM combined WHERE LOWER(conditions) LIKE '%${queryTerm}%'`;
        } else {
            query = 'SELECT * FROM combined';
        }
      const { rows } = await pool.query(query);
      res.json(rows);
    } catch (err) {
      console.error('Error executing query', err);
      res.status(500).json({ error: 'Internal server error' });
    }
  });



app.listen(8080, () => {
    console.log('server listening on port 8080')
})