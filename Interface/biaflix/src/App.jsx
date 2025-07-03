// src/App.jsx
import { Routes, Route } from 'react-router-dom';
import ProfileSelection from './pages/ProfileSelection';
import Homepage from './pages/Homepage'; // A página que vamos criar

function App() {
  return (
    <Routes>
      <Route path="/" element={<ProfileSelection />} />
      <Route path="/browse" element={<Homepage />} />
    </Routes>
  );
}

export default App;