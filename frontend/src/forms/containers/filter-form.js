import React, { Component } from 'react'
import Form from './form'
import './filter-form.css'

export default class FilterForm extends Component {
  render() {
    return (
      <Form
        method='get'
        action={this.props.data.urls.mangaList}
        errorFields={[]}
        className='FilterForm'
      >
        
      </Form>
    )
  }
}
