import React from 'react'
import './navbar-group.css'

const NavbarGroup = props => {
  return (
    <div
      className={props.classNames}
    >
      {props.children}
    </div>
  )
}

export default NavbarGroup
