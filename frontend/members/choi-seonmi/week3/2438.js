// fs 모듈
const fs = require('fs');
const input = fs.readFileSync('input.txt').toString().trim()

const N = parseInt(input)

for (let i = 0; i < N + 1; i++) {
    star = '*'
    console.log(star.repeat(i))
}