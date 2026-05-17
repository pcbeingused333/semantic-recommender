import { useState } from 'react';

function App() {
  const [query, setQuery] = useState('');

  return (
    <div style={{
      minHeight: '100vh',
      backgroundColor: '#111827',
      color: 'white',
      padding: '60px 20px',
      fontFamily: 'system-ui, sans-serif',
      textAlign: 'center'
    }}>
      <h1 style={{ fontSize: '3.5rem', marginBottom: '20px' }}>
        ✅ Semantic Recommender
      </h1>
      <p style={{ fontSize: '1.4rem', color: '#9ca3af', marginBottom: '40px' }}>
        Frontend funcionando correctamente
      </p>

      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Escribe algo y presiona Enter..."
        style={{
          width: '600px',
          padding: '20px',
          fontSize: '1.2rem',
          borderRadius: '9999px',
          border: '3px solid #3b82f6',
          backgroundColor: '#1f2937',
          color: 'white',
          marginBottom: '30px'
        }}
        onKeyPress={(e) => e.key === 'Enter' && alert('Buscando: ' + query)}
      />

      <p style={{ color: '#10b981', fontSize: '1.1rem' }}>
        Si ves este texto → ¡el frontend ya funciona!
      </p>
    </div>
  );
}

export default App;
