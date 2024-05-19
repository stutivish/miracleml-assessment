import {BrowserRouter as Router, Routes, Route, Link} from 'react-router-dom';
import EUData from './components/EUData';
import USData from './components/USData';
import CombinedData from './components/CombinedData';

function App() {
  return (
    <div className="App">
      <header className="App-header">
      <Router>
      <div>
        <nav>
          <ul>
            <li><Link to="/">Home</Link></li>
            <li><Link to="/us">US Data</Link></li>
            <li><Link to="/eu">EU Data</Link></li>
            <li><Link to="/combined">Combined US and EU Data</Link></li>
          </ul>
        </nav>
        <Routes>
          <Route path="/" element={<div>Welcome! Click to learn more about clinical trial data.</div>} />
          <Route path="/us" element={<USData />} />
          <Route path="/eu" element={<EUData />} />
          <Route path="/combined" element={<CombinedData />} />
        </Routes>
      </div>
    </Router>
      </header>
    </div>
  );
}

export default App;