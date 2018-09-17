import React from "react"
import { render } from 'react-dom'

import Base from '../pages/containers/base'

const appContainer = document.getElementById('app-container')
const data = window.backendData

render(
  <Base data={data}/>, appContainer
)
