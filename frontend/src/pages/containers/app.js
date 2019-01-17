import React, { Component, Fragment } from 'react'
import { Route, Switch } from 'react-router-dom';

import MangasPage from './mangas'
import BaseLayout from '../components/base-layout'
import HandleError from "../../error/containers/handle-error"
import Header from '../components/header'
import NotFound from '../components/not-found'
import Home from '../components/home'
import './app.css'


export default class App extends Component {
  render() {
    let dev = null
    if (this.props.data.DEBUG){
      // Route for webpack-dev-server
      <Route exact path={this.props.data.urls.home} render={props => <Home {...props} data={this.props.data} />} />
    }
    return (
      <HandleError>
        <BaseLayout>
          <Fragment>
            <Header
              data={this.props.data}
            />
            <Switch>
              {/* ----------- Ruta para pruebas en desarrollo ----------- */}
              {dev}
              {/* ----------------------O---------------------- */}
              <Route exact path={this.props.data.urls.home} render={props => <Home {...props} data={this.props.data} />} />
              <Route exact path={this.props.data.urls.mangaList} render={props => <MangasPage {...props} data={this.props.data} />} />
              {/* <Route render={NotFound} /> */}
            </Switch>
          </Fragment>
        </BaseLayout>
      </HandleError>
    )
  }
}
