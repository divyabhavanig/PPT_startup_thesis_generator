import { useState } from 'react'

import './App.css'
import {BrowserRouter, Routes, Route} from 'react-router-dom'
import Register from './Components/Register'
import Login from './Components/Login'
import Home from './Components/Home'
function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route path='/register' element={<Register />} />
          <Route path='/login' element={<Login />} />
          <Route path='/home' element ={<Home />} />
        
        </Routes>
      </BrowserRouter>

    </>
  )
}

export default App
