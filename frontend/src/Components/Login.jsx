import React from 'react'

const Login = () => {
  return (
    <div className=' w-screen h-screen bg-gray-300 flex flex-col justify-center items-center'>
    <div className=' w-fit h-fit bg-gray-400 p-8 rounded-md'>
    <div>
        <h2 className=' font-bold text-2xl flex w-full justify-center items-center mb-3'>LOGIN</h2>
    </div>
    <div className='flex flex-col gap-2 mt-2'>
      <input type='email' placeholder='Email Address' className=' p-2 outline-none bg-gray-100 rounded-md w-72'/>
      <input type='password' placeholder='Password' className=' p-2 outline-none bg-gray-100 rounded-md w-72'/>
    </div>

    <div>
      <button className=' w-72 text-green-400 mt-3 py-1 rounded-md font-semibold'>Login</button>
    </div>
  </div></div>
  )
}

export default Login