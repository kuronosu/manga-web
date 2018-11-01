import React from 'react'
import FormGroup from './form-group'
import './form-button.css'

const FormButton = props => {
  return (
    <FormGroup>
      <button
        className='FormButton'
        type='submit'
      >
        Enviar
      </button>
    </FormGroup>
  )
}

export default FormButton
