import React from 'react';
import logo from './logo.svg';
import './App.css';

import axios from 'axios'

import MovieCard from './components/MovieCard'

function App() {
  const url = 'https://www.justwatch.com/'

  axios.get(url, {
      method: 'GET',
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json',
      },
      withCredentials: true
    }
  ).then(
    function (response) {
      console.log(response)
    }
  )

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.tsx</code> and save to reload.
        </p>
        <MovieCard title = "foo"></MovieCard>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
