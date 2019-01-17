import React, { Component } from 'react';
import FilterForm from '../../forms/containers/filter-form'
import MangaList from '../../manga-list/components/manga-list'

class MangasPage extends Component {

  render() {
    console.log('MangaList')
    return (
      <div className='MangaListLayout'>
        <FilterForm data={this.props.data}/>
        <MangaList manga_list={this.props.data.object_list}/>
      </div>
    )
  }
}

export default MangasPage
