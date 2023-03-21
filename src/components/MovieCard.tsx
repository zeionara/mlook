import { Component } from 'react'


export default class MovieCard extends Component<Readonly<{title: string}>, Readonly<{title: string}>> {
    constructor(props: {title: string}) {
        super(props)

        this.state = { title: props.title }
    }

    render() {
        return <h1>{this.state.title}</h1>
    }
}
