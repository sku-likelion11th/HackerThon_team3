function validateForm() {
    var password = document.getElementsByName("password")[0].value;
    var password2 = document.getElementsByName("password2")[0].value;

    if (password !== password2) {
        alert("비밀번호가 일치하지 않습니다. 다시 입력해주세요.");
        return false;
    } else {
        return true;
    }
}
