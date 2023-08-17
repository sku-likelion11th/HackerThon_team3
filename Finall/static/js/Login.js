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