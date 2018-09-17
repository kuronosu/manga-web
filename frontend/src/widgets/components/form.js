import React from 'react'
import './form.css'

const Form = props => {
  return (
    <div className='Form'>
      <form
        method={props.method}
        action={props.action}
        role='form'
      >
        {props.children}
      </form>
    </div>
  )
}

export default Form
