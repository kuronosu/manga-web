import React from 'react'
import './base-layout.css'

function BaseLayout(props){
    return (
        <section className="BaseLayout">
        {props.children}
        </section>
    )
}

export default BaseLayout
