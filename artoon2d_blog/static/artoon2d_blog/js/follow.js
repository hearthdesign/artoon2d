document.addEventListener("DOMContentLoaded", function () {
  const followButtons = document.querySelectorAll(".follow-btn");

  followButtons.forEach(function (btn) {
    btn.addEventListener("click", function () {
      const userId = this.dataset.userId;
      const spinner = this.querySelector(".spinner");
      const countSpan = this.closest(".follow-container").querySelector(".count");

      spinner.style.display = "inline-block";
      this.disabled = true;

      fetch(`/follow/${userId}/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": getCookie("csrftoken"),
          "Content-Type": "application/json"
        },
        body: JSON.stringify({})
      })
      .then(response => response.json())
      .then(data => {
        this.textContent = data.status === "followed" ? "Unfollow" : "Follow";
        this.classList.toggle("followed", data.status === "followed");
        this.classList.toggle("unfollowed", data.status === "unfollowed");

        if (data.follower_count !== undefined && countSpan) {
          countSpan.textContent = data.follower_count;
        }

        this.appendChild(spinner);
      })
      .finally(() => {
        spinner.style.display = "none";
        this.disabled = false;
      });
    });
  });

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + "=")) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
});
