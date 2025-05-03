const express = require('express')
const app = express()
const cors = require('cors')
const mysql = require('mysql2')

app.use(express.json())
app.use(cors())

app.post('/register',async(requestAnimationFrame,res) => {
    res.send('hello from register')
})
app.post('/login',async(req,res) => {
    res.send('hello from login')
})

app.get('/check-user', async(req,res) => {
    res.send('hello from check user')
})
app.listen(8000,() => console.log('Server started'))