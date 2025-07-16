// fs 모듈
const fs = require('fs');
const inputf = fs.readFileSync('input.txt').toString().trim().split(' ');

const A = parseInt(inputf[0])
const B = parseInt(inputf[1])
const C = parseInt(inputf[2])

const results = [
    (A+B)%C,
    ((A%C) + (B%C))%C,
    (A*B)%C,
    ((A%C) * (B%C))%C
];

console.log(results.join('\n'));




// readline 모듈
const readline = require('readline').createInterface({
    input: process.stdin,
    output: process.stdout,
});

let input = [];

readline.on('line', function(line) {
     input.push(line);
}).on('close', function(){

    const number = input[0].split(' ').map(Number);

    const A = number[0]
    const B = number[1]
    const C = number[2]

    const results = [
        (A+B)%C,
        ((A%C) + (B%C))%C,
        (A*B)%C,
        ((A%C) * (B%C))%C
    ];

    console.log(results.join('\n'));
});