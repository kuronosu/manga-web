import React, { Component } from 'react'
import { NavLink } from 'react-router-dom'
import List from '../../widgets/containers/list'
import './user-menu-nav.css'

export default class UserMenuNav extends Component{
  render(){
    return (
      <div className='UserMenuNav'>
        <List flush name='UserMenuNav'>
          <a href='#'>{this.props.user.username}</a>
          <a href='#'>Editar perfil</a>
          <a href={this.props.urls.accountsLogout}>Cerrar sesion</a>
        </List>
      </div>
    )
  }
}
