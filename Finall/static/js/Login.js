function handleLogin(event) {
    event.preventDefault();
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/login/', true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.setRequestHeader('X-CSRFToken', document.getElementsByName('csrfmiddlewaretoken')[0].value);
    xhr.onload = function () {
        var response = JSON.parse(xhr.responseText);

        if (response.status === "success") {
            window.location.href = "/"; // 원하는 페이지 URL로 변경하세요.
        } else {
            // 아이디와 비밀번호가 일치하지 않음을 표시
            alert("아이디와 비밀번호가 일치하지 않습니다. 다시 입력해주세요.");
        }
    };

    xhr.send(new FormData(event.target));
    return false;
}

document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.querySelector("#login-form"); // 폼 요소의 ID 지정

    loginForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        const csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0].value;
        const formData = new FormData(loginForm);

        try {
            const response = await fetch(loginUrl, {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrfToken,
                },
                body: formData,
            });

            if (response.ok) {
                // 로그인 성공 시 원하는 페이지로 이동
                window.location.href = "/posts/";
            } else {
                const errorMessage = document.querySelector(".response-message");

                errorMessage.innerText = "잘못된 아이디나 패스워드입니다.";
                errorMessage.classList.add("error");
                errorMessage.classList.remove("success");
            }
        } catch (error) {
            console.error("Error while logging in:", error);
        }
    });
});