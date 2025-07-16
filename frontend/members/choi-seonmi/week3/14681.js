// fs 모듈
const fs = require('fs');
const inputf = fs.readFileSync('input.txt').toString().trim().split('\n');

const x = parseInt(inputf[0]);
const y = parseInt(inputf[1]);

if (x > 0) {
    if (y > 0) {
        console.log(1);
    } else {
        console.log(4);
    }
} else {
    if (y > 0) {
        console.log(2);
    } else {
        console.log(3);
    }
}




// readline 모듈
const readline = require('readline').createInterface({
    input: process.stdin,
    output: process.stdout,
});

let input = [];

readline.on('line', function(line) {
     input.push(parseInt(line));
}).on('close', function(){

    const x = parseInt(input[0]);
    const y = parseInt(input[1]);

    if (x > 0) {
        if (y > 0) {
            console.log(1);
        } else {
            console.log(4);
        }
    } else {
        if (y > 0) {
            console.log(2);
        } else {
            console.log(3);
        }
    }

    process.exit();
});