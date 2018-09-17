import React from 'react'
import './list-layout.css'

const ListLayout = props => (
  <props.type
    className={props.className}
  >
    {props.children}
  </props.type>
)

export default ListLayout
