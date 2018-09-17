import React from 'react'
import './list-item.css'

const ListItem = props => (
  <li className="ListItem">
    {props.children}
  </li>
)

export default ListItem