import React from 'react';
import logo from './logo.svg';
import './App.css';

import axios from 'axios'

import MovieCard from './components/MovieCard'
import Movie from './Movie'

export default class App extends React.Component<{ url: string}, { movies: Movie[] }> {
  constructor (props: { url: string }) {
    super(props)

    const app = this

    app.state = { movies: [] }

    axios.get(props.url, {
        method: 'GET',
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Content-Type': 'application/json',
        }
      }
    ).then(
      function (response) {
        let movies = (response.data.items as {name: string, details: string, magnet: string, poster: string}[]).map((item) => new Movie(item))
        app.setState({ movies: movies })
        console.log(app.state)
      }
    )
  }

  render () {
    console.log('rerender...')
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <p>
            Edit <code>src/App.tsx</code> and save to reload.
          </p>
          <div className = "movies">
          {
            this.state.movies.map((movie) => <MovieCard {...movie}></MovieCard>)
          }
          </div>
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
}
