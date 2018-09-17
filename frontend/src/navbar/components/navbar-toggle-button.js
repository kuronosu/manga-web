import React from 'react'
import Icon from '../../icons/components/icon'
import './navbar-toggle-button.css'

const NavbarToggleButton = props => {
  return (
    <button className="NavbarToggleButton">
      <Icon
        icon='fa-bars'
        size='35px'
      />
    </button>
  )
}

export default NavbarToggleButton
