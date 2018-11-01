import React from 'react'
import NavBar from '../../navbar/containers/navbar'

const Header = props => (
  <header className="Header">
    <NavBar
      data={props.data}
    />
  </header>
)

export default Header