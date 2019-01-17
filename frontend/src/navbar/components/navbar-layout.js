import React from 'react'
import './navbar-layout.css'

const NavbarLayout = props => (
  <nav className='NavbarLayout'>
    <div className='Container'>
      {props.children}
    </div>
  </nav>
)

export default NavbarLayout
