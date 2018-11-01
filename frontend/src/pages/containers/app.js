import React, { Component, Fragment } from 'react'
import { Route, Switch } from 'react-router-dom';

import AnimeList from './anime-list'
import BaseLayout from '../components/base-layout'
import HandleError from "../../error/containers/handle-error"
import Header from '../components/header'

export default class App extends Component {
  render() {
    return (
      <HandleError>
        <BaseLayout>
          <Fragment>
            <Header
              data={this.props.data}
            />
            <Switch>
              <Route exact path={this.props.data.urls.mangaList} render={props => <AnimeList {...props} data={this.props.data} />} />
            </Switch>
          </Fragment>
        </BaseLayout>
      </HandleError>

    )
  }
}
