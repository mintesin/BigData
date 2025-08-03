import React from 'react' 
import Footer from './Footer'
// import { useState } from 'react'
// import General from './General'
// import PartThree from './PartThree' 
// import PartOne from './PartOne'

import './App.css'

function App() {
  

  return (
    <>
      <div className='container'>
        <div> 
           <h1 className='firstpart'> This is the efirst Part</h1>
          </div>
        <div>
          <h1 className='secondpart'> This is the second Part</h1> 
        </div>
        <div>
          <h1 className='thirdpart'> This is the third Part</h1> 
        </div>

         <Footer/>

      </div>
    </>
  )
}

export default App
