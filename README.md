# mlook

**M**ovies look - a web app for chosing movies available at torrent trackers by looking at posters

<p align="center">
    <img src="assets/demo.jpg"/>
</p>

## Deployment

The app consists of two components that should be deployed separately. First, deploy server using the following commands:

```sh
cd server
python -m server start
```

Then deploy client:

```sh
cd client
npm run serve
```

The app will be accessible by address `http://localhost:3000`
