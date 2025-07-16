export default function q9086(){
    let inputNum = parseInt(prompt("테스트 케이스의 개수:"))
    let answer = 0

    // 테스트 케이스의 개수만큼 문자열 입출력을 반복
    for(let i = 0; i < inputNum; i++) {
        let inputString = prompt(`${i + 1}회차 테스트 케이스의 문자열:`)

        // 입력받은 문자열의 0번째 문자와 마지막 문자를 출력
        answer = inputString.charAt(0) + inputString.charAt(inputString.length - 1)
        alert(answer)
        console.log(answer)
    }
}