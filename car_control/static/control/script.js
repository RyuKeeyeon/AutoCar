document.addEventListener("DOMContentLoaded", function() {
    // 메타 태그에서 CSRF 토큰 읽기
    const csrftoken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    // 전진 버튼 클릭 이벤트
    document.getElementById("forward").addEventListener("click", function() {
        sendCommand("forward");
    });

    // 후진 버튼 클릭 이벤트
    document.getElementById("backward").addEventListener("click", function() {
        sendCommand("backward");
    });

    // 서버에 명령을 보내는 함수
    function sendCommand(command) {
        fetch("/control/" + command + "/", {  // 명령에 맞는 URL로 요청
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken,  // 메타 태그에서 읽은 CSRF 토큰 사용
            },
            body: JSON.stringify({command: command}),
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);  // 서버 응답 처리
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }
});
