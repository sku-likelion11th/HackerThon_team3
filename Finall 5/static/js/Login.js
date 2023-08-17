document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.querySelector("form");
  
    loginForm.addEventListener("submit", async function (event) {
      event.preventDefault();
  
      const formData = new FormData(loginForm);
      const loginData = Object.fromEntries(formData.entries());
  
      try {
        const response = await fetch(loginUrl, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
          },
          body: JSON.stringify(loginData),
        });
  
        if (response.status === 200) {
          window.location.pathname = "posts/"; // 로그인 성공 시 이동할 페이지 경로를 설정해주세요.
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