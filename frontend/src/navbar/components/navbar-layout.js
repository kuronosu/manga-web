import React from 'react'
import Container from '../../widgets/components/container'
import './navbar-layout.css'

const NavbarLayout = props => (
  <nav className='NavbarLayout'>
    <Container>
      {props.children}
    </Container>
  </nav>
)

export default NavbarLayout
