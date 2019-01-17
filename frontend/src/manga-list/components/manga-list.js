import React from 'react'
import MangaCard from './manga-card'
import './manga-list.css'

export default function MangaList(props) {
  return (
    <div className='MangasList'>
      <ul>
      {
        props.manga_list.map(manga => (
          <MangaCard key={manga.pk} manga={manga} />
        ))
      }
      </ul>
    </div>
  )
}
