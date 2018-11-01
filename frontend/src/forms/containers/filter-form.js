import React, { Component } from 'react'
import Form from './form'

export default class FilterForm extends Component {
  render() {
    return (
      <Form
        method='get'
		action={this.props.data.urls.mangaList}
		errorFields={[]}
      >
        
      </Form>
    )
  }
}
