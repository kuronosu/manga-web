import express from 'express'
import React from 'react'
import App from '../dist/ssr/app'
import { StaticRouter } from 'react-router'
import reactDOMServer from 'react-dom/server'
import bodyParser from 'body-parser'

const app = express()

app.use(bodyParser.json())
app.use(bodyParser.urlencoded({ extended: false }))

app.post('*', (req, res) => {
  console.log(`Peticion en: '${req.path}' para renderizar '${req.body.request_url}'`)
  try {
    const html = reactDOMServer.renderToString(
      <StaticRouter
        location={req.body.request_url}
        context={req.body}
      >
        <App data={req.body}/>
      </StaticRouter>
    )
    res.write(`
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="X-UA-Compatible" content="ie=edge">
        <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.3.1/css/all.css" integrity="sha384-mzrmE5qonljUremFsqc01SB46JvROS7bZs3IO2EmfFsd15uHvIt+Y8vEf7N7fWAU" crossorigin="anonymous">
        <title>${req.body.title || 'Manga'}</title>
        <link rel="stylesheet" href="/static/css/app.css">
    </head>
    <body>
        <div id="app-container">${html}</div>
        <script>window.backendData = ${JSON.stringify(req.body)}</script>
        <script src="/static/js/app.js"></script>
    </body>
    </html>
    `)
    res.end()
  } catch (error) {
    console.log(error)
    res.status(500)
    res.end()
  }
})

app.listen(3000)
console.log('el server prendió en el puerto 3000')
