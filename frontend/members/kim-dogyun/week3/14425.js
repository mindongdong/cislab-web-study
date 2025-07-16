export default function q14425(){
    let inputNum = prompt("집합 S의 문자열의 개수 N과 집합 S에 포함되어 있는지 검사할 문자열의 개수 M 입력(띄어쓰기로 구분):")
    let inputN = []
    let inputM = []
    let answer = 0

    const [n, m] = inputNum.split(" ").map(Number)

    for(let i = 0; i < n; i++) {
        inputN.push(prompt(`집합 S에 추가할 문자열 입력(${n}개 중 ${i + 1}번째):`))
    }

    for(let i = 0; i < m; i++) {
        inputM.push(prompt(`집합 S에서 검사할 문자열 입력(${m}개 중 ${i + 1}번째):`))
    }

    // 검사할 대상인 배열 M에 들어있는 요소 각각이 배열 N에 포함되어 있는지 검사
    for(let i = 0; i < m; i++) {
        if(inputN.includes(inputM[i])) {
            answer++
        }
    }

    alert(answer)
    console.log(answer)
}