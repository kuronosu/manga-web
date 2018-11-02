import React from "react"
import { render, hydrate } from 'react-dom'
import { BrowserRouter } from 'react-router-dom'

import App from "../pages/containers/app"

const appContainer = document.getElementById('app-container')
const data = window.backendData

hydrate(
  <BrowserRouter>
    <App data={data}/>
  </BrowserRouter>, appContainer
)
