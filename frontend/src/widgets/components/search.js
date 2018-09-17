import React from 'react';
import Icon from '../../icons/components/icon'
import './search.css';

// function Search(props) {
//   return (
//     <form action=""></form>
//   )
// }

const Search = props => (
  <form
    method='get'
    action={props.action}
    className="Search"
    onSubmit={props.handleSubmit}
    style={{display: 'flex'}}
  >
    <input
      ref={props.setRef}
      type="text"
      placeholder="Buscar mangas"
      className="Search-input"
      name="search"
      onChange={props.handleChange}
      value={props.value}
    />
    <button
      className='Search-button'
      type='submit'
    >
      <Icon
        icon='fa-search'
      />
    </button>
  </form>
)

export default Search
