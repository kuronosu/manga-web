import React from 'react'
import LoginForm from '../../forms/components/login-form';
import './login-form-nav.css'

const LoginFormNav = props => (
  <div className='LoginFormNav'>
    <LoginForm
      signIn={props.signIn}
      signUp={props.signUp}
      passwordReset={props.passwordReset}
      csrfmiddlewaretoken={props.csrfmiddlewaretoken}
      errorFields={[]}
      isNav
    />
  </div>
)

export default LoginFormNav
