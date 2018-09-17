import React from 'react'
import './form-group.css'

const FormGroup = props => {
  return (
    <div className='FormGroup'>
      {props.children}
    </div>
  )
}

export default FormGroup
