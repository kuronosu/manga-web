import React from 'react'
import LoginForm from '../../widgets/components/login-form';
import './login-form-nav.css'

const LoginFormNav = props => (
  <div className='LoginFormNav'>
    <LoginForm
      signIn={props.signIn}
      signUp={props.signUp}
      passwordReset={props.passwordReset}
      csrfmiddlewaretoken={props.csrfmiddlewaretoken}
    />
  </div>
)

export default LoginFormNav
