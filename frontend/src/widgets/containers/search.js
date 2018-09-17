import React, { Component } from 'react'
import Search from '../components/search'

class SearchContainer extends Component {
  state = {
    value: ''
  }
  handleSubmit = event => {
    console.log(this.input.value, 'submit')
  }
  setInputRef = element => {
    this.input = element
  }
  handleInputChange = event => {
    this.setState({
      value: event.target.value
    })
  }
  render() {
    return (
      <Search
        setRef={this.setInputRef}
        handleSubmit={this.handleSubmit}
        handleChange={this.handleInputChange}
        value={this.state.value}
        action={this.props.action}
      />
    )
  }
}

export default SearchContainer
