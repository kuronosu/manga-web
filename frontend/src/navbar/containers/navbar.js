import React, { Component } from 'react'
import { withRouter } from 'react-router'

import MediaQuery from  '../../widgets/containers/media-query'
import NavbarLayout from '../../navbar/components/navbar-layout'
// import NavLink from '../../navbar/components/navbar-link'
import NavbarHeader from '../../navbar/components/navbar-header'
import DefaultView from '../../navbar/components/default-view'
import MovileView from "../../navbar/components/mobile-view"

class NavBar extends Component {
  render() {
    const {
      urls,
      user,
      csrftoken
    } = this.props.data
    return (
      <NavbarLayout>
        <NavbarHeader>
          <a href={urls.home}>Manga</a>
        </NavbarHeader>
        <MediaQuery>
          {shouldShowMobileView =>
            shouldShowMobileView ? (
              <MovileView user={user} urls={urls} csrftoken={csrftoken} />
            ) : (
              <DefaultView user={user} urls={urls} csrftoken={csrftoken} />
            )
          }
        </MediaQuery>
      </NavbarLayout>
    )
  }
}

export default withRouter(NavBar);