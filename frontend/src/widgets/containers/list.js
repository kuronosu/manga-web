import React, { Component } from 'react'
import ListLayout from '../components/list-layout'
import ListItem from '../components/list-item'

export default class List extends Component {
  componentWillMount = () => {
    this.setState({
      type: this.props.ordered ? 'ol': 'ul'
    })
  }
  render() {
    let c = 0
    return (
      <ListLayout
        type={this.state.type}
        className={`ListLayout ${this.props.flush ? 'ListLayoutFlush': ''}`}
      >
      {
        this.props.children.length ?

          this.props.children.map(element => (
            element &&
              <ListItem
                key={`key_${c++}_${this.props.name}`}
              >
                {element}
              </ListItem>
          )):this.props.children
        }
      </ListLayout>
    )
  }
}
