export default function q10430(){
    let inputNum = prompt("세 개의 숫자 입력(띄어쓰기로 구분):")
    let answer = 0

    // 입력받은 문자열을 띄워쓰기로 나눈 배열을 만든 다음
    // .map() 메서드로 배열의 내용물을 숫자 자료형으로 변경하고
    // 각각 a, b, c에 구조 분해 할당
    const [a, b, c] = inputNum.split(" ").map(Number)
    answer = `${(a+b)%c}\n${((a%c)+(b%c))%c}\n${(a*b)%c}\n${((a%c)*(b%c))%c}`

    alert(answer)
    console.log(answer)
}