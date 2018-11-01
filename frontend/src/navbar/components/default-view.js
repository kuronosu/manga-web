import React from 'react'
import NavDropdown from '../containers/navbar-dropdown'
// import a from './navbar-link'
import Search from '../../forms/containers/search'
import LoginFormNav from './login-form-nav'
import UserMenuNav from './user-menu-nav'

import './default-view.css'

const DefaultView = ({user, urls, csrftoken}) => {
  return (
    <div className='NavbarGroup SpaceBetween'>
      <div className="NavbarGroup">
        <a href={urls.mangaList}>Lista de mangas</a>
        {
          user.isAthenticated ?
          <a href={urls.mangaAdd}>Nuevo manga</a>:''
        }
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
              user={user}
              urls={urls}
            />
          }
        </NavDropdown>
      </div>
    </div>
  )
}

export default DefaultView