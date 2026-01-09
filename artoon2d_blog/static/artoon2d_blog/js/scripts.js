document.addEventListener("DOMContentLoaded", () => {

  /* =========================
     CAROUSEL (SAFE)
  ========================= */

  const track = document.querySelector('.carousel-track');
  const nextBtn = document.querySelector('.carousel-btn.next');
  const prevBtn = document.querySelector('.carousel-btn.prev');

  if (track && nextBtn && prevBtn) {
    const slides = Array.from(track.children);
    let currentIndex = 0;

    function updateCarousel() {
      if (!slides.length) return;
      const slideWidth = slides[0].getBoundingClientRect().width;
      track.style.transform = `translateX(-${slideWidth * currentIndex}px)`;
    }

    nextBtn.addEventListener('click', () => {
      currentIndex = (currentIndex + 1) % slides.length;
      updateCarousel();
    });

    prevBtn.addEventListener('click', () => {
      currentIndex = (currentIndex - 1 + slides.length) % slides.length;
      updateCarousel();
    });

    // Optional auto-play
    setInterval(() => {
      currentIndex = (currentIndex + 1) % slides.length;
      updateCarousel();
    }, 5000);
  }


  /* =========================
     SCROLL TO TOP BUTTON (SAFE)
  ========================= */

  const scrollTopBtn = document.getElementById("scrollTopBtn");

  if (scrollTopBtn) {
    window.addEventListener("scroll", () => {
      if (document.documentElement.scrollTop > 300) {
        scrollTopBtn.style.display = "block";
      } else {
        scrollTopBtn.style.display = "none";
      }
    });

    scrollTopBtn.addEventListener("click", () => {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }

});


/* =========================
   SHARE FUNCTIONS (SAFE)
   These are fine as-is
========================= */

function MastodonShare(event) {
  const button = event.currentTarget;
  const shareText = button.getAttribute("data-src") || "Check this out!";
  const domain = "mastodon.social";
  window.open(
    `https://${domain}/share?text=${encodeURIComponent(shareText)}`,
    "_blank"
  );
}

function PixelfeldShare(event) {
  const button = event.currentTarget;
  const shareText = button.getAttribute("data-src") || "Check this out!";
  const domain = "pixelfeld.social";
  window.open(
    `https://${domain}/share?text=${encodeURIComponent(shareText)}`,
    "_blank"
  );
}

function FriendicaShare(event) {
  const button = event.currentTarget;
  const shareTitle = button.getAttribute("data-title") || "Check this out!";
  const shareURL = button.getAttribute("data-url") || window.location.href;
  const domain = "friendica.eu";
  window.open(
    `https://${domain}/share?title=${encodeURIComponent(shareTitle)}&url=${encodeURIComponent(shareURL)}`,
    "_blank"
  );
}