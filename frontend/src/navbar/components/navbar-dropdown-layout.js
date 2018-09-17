import React from 'react'
import Icon from '../../icons/components/icon'
import './navbar-dropdown-layout.css'

const NavDropdownLayout = props => (
  <div>
    <div
      className={props.overlay}
      onClick={props.handleClick}
      />
    <div className={props.className}>
      {
        !(props.button) ?
        <span
          onClick={props.handleClick}
        >
          <Icon
            icon='fa-user'
          />
        </span>
        :
        <span
          onClick={props.handleClick}
        >
          {props.button}
        </span>
      }
      {
        !(props.content) ?
        <div
        className='DropdownContent'
        ref={props.setRef}
        >
          <div className={props.contentClass}>
            {props.children}
          </div>
        </div>
        :
        <div
          ref={props.setRef}
        >
          props.content
        </div>
      }
    </div>
  </div>
)


export default NavDropdownLayout