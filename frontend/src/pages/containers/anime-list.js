import React, { Component } from 'react';
import FilterForm from '../../forms/containers/filter-form'

class AnimeList extends Component {

  render() {
    return (
      <FilterForm data={this.props.data}/>
    )
  }
}

export default AnimeList
