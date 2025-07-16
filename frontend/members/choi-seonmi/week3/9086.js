// fs 모듈
const fs = require('fs');
const inputf = fs.readFileSync('input.txt').toString().trim().split('\n');

const T = inputf[0]

for (let i = 0; i < T; i++) {

    let str = inputf[i+1].trim();

    console.log(str[0] + str[str.length-1]);
}




// readline 모듈
const readline = require('readline').createInterface({
    input: process.stdin,
    output: process.stdout,
});

let input = [];

readline.on('line', function(line) {
     input.push(line);
}).on('close', function(){

    const T = parseInt(input[0])

    for (let i = 0; i < T; i++) {

        let str = input[i+1].trim();

        console.log(str[0] + str[str.length-1]);
    }

    process.exit();
});