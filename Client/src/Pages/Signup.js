

import React from 'react'
import Template from '../components/Template'

export default function Signup({setIsLoggedIn}) {
  return (
    <div>
    <Template
        
         formtype= "signup"
         setIsLoggedIn={setIsLoggedIn}
    />
    </div>
  )
}
