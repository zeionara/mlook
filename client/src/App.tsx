import React from 'react'
import './style/app.sass'
import { ThreeCircles } from 'react-loader-spinner'

import axios from 'axios'

import MovieCard from './components/MovieCard'
import Movie from './Movie'

export default class App extends React.Component<{ url: string}, { movies: Movie[], loading: boolean }> {
  constructor (props: { url: string }) {
    super(props)

    const app = this

    app.state = { movies: [], loading: true }

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
        app.setState({ movies: movies, loading: false })
      }
    )
  }

  render () {
    console.log('rerender...')
    return (
      <div className="App">
        <h1>Latest movies</h1>
        <div className = "movies">
        {
          this.state.movies.map((movie) => <MovieCard {...movie} key = {movie.name}></MovieCard>)
        }
        <ThreeCircles
          height="100"
          width="100"
          color="#4fa94d"
          wrapperStyle={{}}
          wrapperClass=""
          visible={this.state.loading}
          ariaLabel="three-circles-rotating"
          outerCircleColor=""
          innerCircleColor=""
          middleCircleColor=""
        />
        </div>
      </div>
    );
  }
}
