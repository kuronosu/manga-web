import React, { Component } from "react"
import BaseLayout from '../components/base-layout'
import HandleError from "../../error/containers/handle-error"
import Navbar from "../../navbar/containers/navbar"


class Base extends Component{

  render(){
    return (
      <HandleError>
        <BaseLayout>
          <Navbar
            data={this.props.data}
          />
          {this.props.children}
        </BaseLayout>
      </HandleError>
    )
  }
}

export default Base
