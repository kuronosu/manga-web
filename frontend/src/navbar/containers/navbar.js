import React, { Component } from 'react'
import Search from '../../widgets/containers/search'
import LoginFormNav from '../components/login-form-nav'
import NavbarLayout from '../components/navbar-layout'
import NavbarHeader from '../components/navbar-header'
import NavLink from '../components/navbar-link'
import NavbarToggleButton from '../components/navbar-toggle-button'
import UserMenuNav from '../components/user-menu-nav'
import NavGroup from './nav-group'
import NavDropdown from './navbar-dropdown'
import List from '../../widgets/containers/list'

export default class NavBar extends Component {
    render = () => {
      const {
        urls,
        user
      } = this.props.data
      return(
      <NavbarLayout>
        <NavGroup>
          <NavbarHeader>
            <NavLink
              href={urls.home}
              text='Manga'
            />
          </NavbarHeader>
          <NavDropdown
            button={<NavbarToggleButton/>}
            mobile
          >
            <List flush>
              <NavLink
                href={urls.mangaList}
                text='Lista de mangas'
                id='MangaList'
              />
              {user.isAthenticated &&
                <NavLink
                  href={urls.mangaAdd}
                  text='Nuevo manga'
                  id='MangaAdd'
                />
              }
              {(user.isAthenticated) &&
                <NavLink
                href={urls.mangaAdd}
                text={user.username}
                id='Username'
                />
              }
              {(user.isAthenticated) &&
                <NavLink
                href={urls.accountsLogout}
                text='Cerrar sesión'
                id='Logout'
              />
              }
              {!(user.isAthenticated) &&
                <NavLink
                  href={urls.accountsLogin}
                  text='Iniciar sesión'
                  id='Login'
                />
              }
              {!(user.isAthenticated) &&
                <NavLink
                  href={urls.accountsSignup}
                  text='Regístrate'
                  id='Signup'
                />
              }
            </List>
          </NavDropdown>
          <NavGroup collapse between>
            <NavGroup>
              <NavLink
                href={urls.mangaList}
                text='Lista de mangas'
              />
              {
                user.isAthenticated ?
                <NavLink
                  href={urls.mangaAdd}
                  text='Nuevo manga'
                />:''
              }
            </NavGroup>
            <NavGroup>
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
                  csrfmiddlewaretoken={this.props.data.csrfmiddlewaretoken}
                  />
                  :
                  // <List>
                  //   <NavLink
                  //     href='#'
                  //     text={user.username}
                  //   />
                  //   <NavLink
                  //     href='#'
                  //     text='Editar perfil'
                  //   />
                  //   <NavLink
                  //     href={urls.accountsLogout}
                  //     text='Cerrar sesion'
                  //   />
                  // </List> 
                  <UserMenuNav
                    user={user}
                    urls={urls}
                  />
                }
              </NavDropdown>
            </NavGroup>
          </NavGroup>
        </NavGroup>
      </NavbarLayout>
    )
  }
}
