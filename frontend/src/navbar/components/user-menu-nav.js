import React, { Component } from 'react'
import NavLink from '../components/navbar-link'
import List from '../../widgets/containers/list'
import './user-menu-nav.css'

export default class UserMenuNav extends Component{
  render(){
    return (
      <div className='UserMenuNav'>
        <List flush>
          <NavLink
            href='#'
            text={this.props.user.username}
            id='Username'
          />
          <NavLink
            href='#'
            text='Editar perfil'
            id='EditProfile'
          />
          <NavLink
            href={this.props.urls.accountsLogout}
            text='Cerrar sesion'
            id='Logout'
          />
        </List>
      </div>
    )
  }
}
