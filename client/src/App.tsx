import React from 'react'
import './style/app.sass'
import { InfinitySpin } from 'react-loader-spinner'
// import { Events, scrollSpy, animateScroll } from 'react-scroll'

import axios from 'axios'

import MovieCard from './components/MovieCard'
import Movie from './Movie'

export default class App extends React.Component<{ url: string}, { movies: Movie[], loading: boolean, offset: number }> {
  constructor (props: { url: string }) {
    super(props)

    this.state = { movies: [], loading: true, offset: 1 }
    this.pullMovies()

    this.handleScroll = this.handleScroll.bind(this)
  }

  pullMovies () {
    // console.log('pulling movies...')

    const app = this

    this.setState({ movies: this.state.movies, loading: true, offset: this.state.offset })

    const url = `${this.props.url}/${this.state.offset}/3`
    const pulled = true
    // console.log('fetching from', url)

    axios.get(url, {
        method: 'GET',
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Content-Type': 'application/json',
        }
      }
    ).then(
      function (response) {
        // console.log('got response')
        // console.log(response)
        // try {
        let movies = (response.data.items as {name: string, details: string, magnet: string, poster: string}[]).map((item) => new Movie(item))
        app.setState({ movies: [...app.state.movies, ...movies], loading: false, offset: app.state.offset + 1 })
        // } catch (err) {
        //   console.log(err)
        //   app.pullMovies()
        // }
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

    const scrollDiff = Math.abs(maxScroll - window.scrollY - window.innerHeight)

    if (scrollDiff < 2 && !this.state.loading) {
      this.pullMovies()
    }
  }

  render () {
    let header

    if (this.state.loading) {
      header = null
    } else {
      header = <img src = "logo.png" alt = "logo" width = "400px" className = "logo"/>
    }

    let footer

    if (this.state.loading) {
      footer = <InfinitySpin width="200" color="#ff3d43"/>
    } else {
      footer = null
    }

    return (
      <div className="App" >
        { header }
        <div className = "movies">
        { this.state.movies.map((movie, index) => <MovieCard {...movie} key = {index}></MovieCard>) }
        </div>
        { footer }
      </div>
    );
  }
}
