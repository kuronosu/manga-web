import React, { Component } from 'react'
import NavDropdownLayout from '../components/navbar-dropdown-layout'

export default class NavDropdown extends Component{
  state = {
    contentVisible: false,
  }
  componentDidMount = () => {
    this.setState({
      contentHidden: true
    })
  }
  handleClick = event => {
    this.setState({
      contentVisible: !(this.state.contentVisible),
      contentHidden: false
    })
  }
  setContent = element => {
    this.setState({
      content: element
    })
  }
  render() {
    let contentClass;
    if (this.props.mobile) {
      if(this.state.contentVisible){
        contentClass = 'reveal'
      } else {
        contentClass = 'hide'
      }
    } else {
      contentClass = !this.state.contentVisible ? 'hidden': ''
    }
    return (
      <NavDropdownLayout
        handleClick={this.handleClick}
        setRef={this.setContent}
        button={this.props.button}
        overlay={`overlay ${this.state.contentVisible ? 'overlay': ''}${!this.state.contentVisible ? 'hidden': ''}`}
        className={`NavDropdown ${this.props.mobile ? 'mobile': ''}`}
        contentClass={`Content ${this.state.contentHidden ? 'hidden': ''} ${contentClass}`}
      >
        {this.props.children}
      </NavDropdownLayout>
    )
  }
}
