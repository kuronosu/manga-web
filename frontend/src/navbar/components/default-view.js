import React from 'react'
import NavDropdown from '../containers/navbar-dropdown'
// import a from './navbar-link'
import Search from '../../forms/containers/search'
import LoginFormNav from './login-form-nav'
import UserMenuNav from './user-menu-nav'

import './default-view.css'

const DefaultView = props => {
  const {user, urls, csrftoken} = props
  return (
    <div className='NavbarGroup SpaceBetween'>
      <div className="NavbarGroup">
        {
          props.menuItems.map(item => {
            if (item.show)
              return <a href={item.url}>{item.name}</a>
          })
        }
        {/* <a href={urls.mangaList}>Lista de mangas</a>
        {
          user.isAthenticated ?
          <a href={urls.mangaAdd}>Nuevo manga</a>:''
        } */}
      </div>
      <div className='NavbarGroup'>
        <Search
          action={urls.mangaList}
        />  
        <NavDropdown>
          {
            !user.isAthenticated ?
            <LoginFormNav
              signIn={urls.accountsLogin}
              signUp={urls.accountsSignup}
              passwordReset={urls.accountsPasswordReset}
              csrfmiddlewaretoken={csrftoken}
            />
            :
            <UserMenuNav
              loggedMenu={props.loggedMenu}
            />
          }
        </NavDropdown>
      </div>
    </div>
  )
}

export default DefaultView