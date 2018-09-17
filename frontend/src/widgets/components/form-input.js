import React from 'react'
import FormGroup from './form-group'
import './form-input.css'

const FormInput = props => {
  return (
    <FormGroup>
      <label htmlFor={props.id} >{props.label}</label>
      <input
        className={'FormControl'}
        type={props.type}
        name={props.name}
        id={props.id}
        maxLength={props.maxLength}
        placeholder={props.placeholder}
        required
        autoFocus={props.autoFocus}
        autoComplete={props.autoComplete}
      />
    </FormGroup>
  )
}

export default FormInput
