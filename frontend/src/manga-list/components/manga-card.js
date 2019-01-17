import React from 'react'
import './manga-card.css'

export default function MangaCard(props) {
  return (
    <li>
      <a href="#">
        <img src={`http://localhost:8000/media/${props.manga.fields.image}`} alt={props.manga.fields.title} />
      </a>
    </li>
  )
}
