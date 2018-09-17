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
                key={element.props.id}
              >
                {element}
              </ListItem>
          )):this.props.children
        }
      </ListLayout>
    )
  }
}
