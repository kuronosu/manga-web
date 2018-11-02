import React from 'react'
import { Link } from 'react-router-dom'
import Form from '../containers/form'
import FormInput from './form-input'
import FormButton from './form-button'
import './login-form.css'

const LoginForm = props => {
  let errors = 0
  return (
    <form
      className='Form'
      method='post'
      action={props.signIn}
    >
      {
      props.errorFields.map(error => (
      <small key={'error_'+errors++} className='ErrorField'>
        {error.text}
      </small>
      ))
      }
      <input type="hidden" name="csrfmiddlewaretoken" value={props.csrfmiddlewaretoken}/>
      <FormInput
        type='text'
        name='username'
        id={props.isNav ? 'id_username_nav': 'id_username'}
        placeholder='Enter your Username or Email'
        autoComplete='on'
        label='Username or Email: '
        autoFocus
      />
      <FormInput
        type='password'
        name='password'
        id={props.isNav ? 'id_password_nav': 'id_password'}
        placeholder='Contraseña'
        autoComplete='off'
        label='Password: '
      />
      <FormButton/>
      <div className='NavbarGroup SpaceBetween'>
        <small className='SmallBlueText'>
          <a href={props.signUp}>Registrate</a>
        </small>
        <small className='SmallBlueText'>
          <a href={props.passwordReset}>¿Olvidaste tu contraseña?</a>
        </small>
      </div>
    </form>
  )
}

export default LoginForm
