export default class Movie {
    name: string

    details: string
    magnet: string
    poster: string

    constructor ({ name, details, magnet, poster }: {name: string, details: string, magnet: string, poster: string}) {
        this.name = name
        this.details = details
        this.magnet = magnet
        this.poster = poster
    }
}
