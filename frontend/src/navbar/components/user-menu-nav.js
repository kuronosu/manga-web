import React, { Component } from 'react'
// import { NavLink } from 'react-router-dom'
import List from '../../widgets/containers/list'
import './user-menu-nav.css'

export default class UserMenuNav extends Component{
  render(){
    return (
      <div className='UserMenuNav'>
        <List flush name='UserMenuNav'>
          {
            this.props.loggedMenu.map(item => (
              <a href={item.url}>{item.name}</a>
            ))
          }
        </List>
      </div>
    )
  }
}
