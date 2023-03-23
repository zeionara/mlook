import React from 'react';
import logo from './logo.svg';
import './App.css';

import axios from 'axios'

import MovieCard from './components/MovieCard'
import Movie from './Movie'

function App() {
  const url = 'http://localhost:8080/movies-example'

  axios.get(url, {
      method: 'GET',
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json',
      }
    }
  ).then(
    function (response) {
      let movies = (response.data.items as {name: string, details: string, magnet: string, poster: string}[]).map((item) => new Movie(item))
      console.log(movies)
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
