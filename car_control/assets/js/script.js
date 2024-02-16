document.addEventListener("DOMContentLoaded", function() {
    const csrftoken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');


    document.getElementById("forward").addEventListener("click", function() { sendCommand("forward"); });
    document.getElementById("backward").addEventListener("click", function() { sendCommand("backward"); });

    // 좌회전 버튼 클릭 이벤트
    document.getElementById("left").addEventListener("click", function() {
        sendCommand("left");
    });

    // 우회전 버튼 클릭 이벤트
    document.getElementById("right").addEventListener("click", function() {
        sendCommand("right");
    });

    // 정지 버튼 클릭 이벤트
    document.getElementById("stop").addEventListener("click", function() {
        sendCommand("stop");
    });

    function sendCommand(command) {
        fetch("/control/" + command + "/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken,
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
