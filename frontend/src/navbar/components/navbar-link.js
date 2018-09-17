import React from 'react'
import './navbar-link.css'

const NavLink = props => (
  <a
    className="NavbarLink"
    href={props.href}
  >
  <span>
  {props.text || props.children}
  </span>
  </a>
)

export default NavLink
