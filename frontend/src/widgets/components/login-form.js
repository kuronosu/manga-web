import React from 'react'
import NavLink from '../../navbar/components/navbar-link'
import NavGroup from '../../navbar/containers/nav-group'
import Form from './form'
import FormInput from './form-input'
import FormButton from './form-button'
import './login-form.css'

const LoginForm = props => {
  return (
    <Form
      method='post'
      action={props.signIn}
    >
      <input type="hidden" name="csrfmiddlewaretoken" value={props.csrfmiddlewaretoken}/>
      <FormInput
        type='text'
        name='username'
        id='id_username'
        placeholder='E-mail ó nombre de usuario'
        autoComplete='on'
        label='Username: '
        autoFocus
      />
      <FormInput
        type='password'
        name='password'
        id='id_password'
        placeholder='Contraseña'
        autoComplete='off'
        label='Password: '
      />
      <FormButton
        type='submit'
        id='id_password'
        placeholder='Contraseña'
        autoComplete='off'
      />
      <NavGroup between>
        <small className='SmallBlueText'>
          <NavLink
            href={props.signUp}
            text='Registrate'
          />
        </small>
        <small className='SmallBlueText'>
          <NavLink
            href={props.passwordReset}
            text='¿Olvidaste tu contraseña?'
          />
        </small>
      </NavGroup>
    </Form>
  )
}

export default LoginForm
