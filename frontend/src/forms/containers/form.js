import React from 'react'
import './form.css'

const Form = props => {
  let errors = 0
  return (
    <form
      className={`Form ${props.className}`}
      method={props.method}
      action={props.action}
      >
      {
        props.errorFields.map(error => (
        <small key={'error_'+errors++} className='ErrorField'>
          {error.text}
        </small>
        ))
      }
      {props.children}
    </form>
  )
}

export default Form
