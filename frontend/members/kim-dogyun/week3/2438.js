export default function q2438(){
    const inputNum = parseInt(prompt("별의 개수 입력:"))
    let answer = ""
    let temp = ""

    for(let i = 0; i < inputNum; i++) {
        temp = "*".repeat(i + 1) + "\n"
        answer = answer + temp
    }

    alert(answer)
    console.log(answer)
}