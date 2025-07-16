export default function q14681(){
    const inputX = parseInt(prompt("X 값의 좌표(정수) 입력:"))
    const inputY = parseInt(prompt("Y 값의 좌표(정수) 입력:"))

    // 입력받은 좌표들의 양·음수 여부를 문자열 형식으로 저장
    const inputAll = [Math.sign(inputX), Math.sign(inputY)].join(',')
    let answer = 0

    // 문자열에서 나올 수 있는 4가지 사분면의 경우의 수에 맞는 출력
    switch(inputAll) {
        case ("1,1"): {
            answer = 1
            break
        }
        case ("-1,1"): {
            answer = 2
            break
        }
        case ("-1,-1"): {
            answer = 3
            break
        }
        case ("1,-1"): {
            answer = 4
            break
        }
    }

    alert(answer)
    console.log(answer)
}