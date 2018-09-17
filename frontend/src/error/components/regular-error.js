import React from 'react'

function RegularError(props) {
  const message =  props.message ? props.message: "Ha ocurrido un error."
  return (
    <h1 style={{color: 'white',textAlign: 'center',}}>{message}</h1>
  )
}

export default RegularError
