// fs 모듈
const fs = require('fs');
const inputf = fs.readFileSync('input.txt').toString().trim().split('\n');

condinput = inputf[0].split(" ")
const N = condinput[0]
const M = condinput[1]

let count = 0;
let countn = 0;
let S = {};

for (let i = 0; i < N; i++) {
    S[i] = inputf[i+1]
    countn += 1;
}

for (let j = 0; j < M; j++) {

    let m = inputf[j+1+countn]

    for (let k = 0; k < N; k++){
        if (m == S[k]) {
            count += 1;
        }
    }
}

console.log(count)