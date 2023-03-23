import React from 'react'
import './style/app.sass'
import { ThreeCircles } from 'react-loader-spinner'
// import { Events, scrollSpy, animateScroll } from 'react-scroll'

import axios from 'axios'

import MovieCard from './components/MovieCard'
import Movie from './Movie'

export default class App extends React.Component<{ url: string}, { movies: Movie[], loading: boolean }> {
  constructor (props: { url: string }) {
    super(props)

    this.state = { movies: [], loading: true }
    this.pullMovies()

    this.handleScroll = this.handleScroll.bind(this)
  }

  pullMovies () {
    const app = this

    this.setState({ movies: this.state.movies, loading: true })
    axios.get(this.props.url, {
        method: 'GET',
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Content-Type': 'application/json',
        }
      }
    ).then(
      function (response) {
        let movies = (response.data.items as {name: string, details: string, magnet: string, poster: string}[]).map((item) => new Movie(item))
        app.setState({ movies: [...app.state.movies, ...movies], loading: false })
      }
    )
  }

  componentDidMount () {
    // console.log('foo')
    // Events.scrollEvent.register('end', function(to, element) {
    //   console.log('end');
    // });

    // setTimeout(() => window.scrollTo({ top: 5000, behavior: "smooth" }), 1000)
    window.addEventListener('scroll', this.handleScroll)

    // scrollSpy.update()
  }

  handleScroll(e: any) {
    // console.log(window.scrollY)
    // console.log(window)
    const maxScroll = Math.max( document.body.scrollHeight, document.body.offsetHeight, 
       document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );

    if (Math.abs(maxScroll - window.scrollY - window.innerHeight) < 1 && !this.state.loading) {
      this.pullMovies()
    }
  }

  render () {
    console.log('rerender...')
    return (
      <div className="App" >
        <h1>Latest movies</h1>
        <div className = "movies">
        {
          this.state.movies.map((movie) => <MovieCard {...movie} key = {movie.name}></MovieCard>)
        }
        </div>
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
    );
  }
}
