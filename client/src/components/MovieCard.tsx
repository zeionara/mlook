import { Component } from 'react'
import Movie from '../Movie'

import '../style/movie.sass'

export default class MovieCard extends Component<Readonly<Movie>> {
    render() {
        return <div className="movie">
          <img src = {this.props.poster} alt = {this.props.name} width = "300px"/>
          <a href = {this.props.details}>{this.props.name.replace(/\./g, ' ')}</a><a href = {this.props.magnet}> 🧲</a>
        </div>
    }
}
