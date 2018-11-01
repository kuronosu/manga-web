import React from 'react'
import NavbarToggleButton from './navbar-toggle-button'
import NavDropdown from '../containers/navbar-dropdown'
import List from '../../widgets/containers/list'

const MobileView = ({user, urls, csrftoken}) => {
  return (
    <NavDropdown
      button={<NavbarToggleButton/>}
      mobile
    >
      <List flush name='navMenuMovile'>
        {(user.isAthenticated) &&
          <a href={urls.mangaAdd}>{user.username}</a>
        }
        <a href={urls.mangaList}>Lista de mangas</a>
        {user.isAthenticated &&
          <a href={urls.mangaAdd}>Nuevo manga</a>
        }
        {(user.isAthenticated) &&
          <a href={urls.accountsLogout}>Cerrar sesión</a>
        }
        {!(user.isAthenticated) &&
          <a href={urls.accountsLogin}>Iniciar sesión</a>
        }
        {!(user.isAthenticated) &&
          <a href={urls.accountsSignup}>Regístrate</a>
        }
      </List>
    </NavDropdown>
  )
}

export default MobileView