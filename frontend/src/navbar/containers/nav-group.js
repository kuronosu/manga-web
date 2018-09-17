import React from 'react'
import NavbarGroup from '../components/navbar-group'

const NavGroup = props => {
  const classNames = (
    'NavbarGroup ' +
    ((props.collapse) ? 'NavbarCollapseGroup ' : ' ') +
    ((props.between) ? 'NavbarGroupBetween ' : ' ')
    )
  return (
    <NavbarGroup
        classNames={classNames}
    >
      {props.children}
    </NavbarGroup>
  )
}

export default NavGroup
