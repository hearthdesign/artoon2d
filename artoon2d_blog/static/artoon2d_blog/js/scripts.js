const track = document.querySelector('.carousel-track');
const slides = Array.from(track.children);
const nextBtn = document.querySelector('.carousel-btn.next');
const prevBtn = document.querySelector('.carousel-btn.prev');

let currentIndex = 0;

function updateCarousel() {
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

// Optional: Auto-play
setInterval(() => {
  currentIndex = (currentIndex + 1) % slides.length;
  updateCarousel();
}, 5000);


function MastodonShare(event) {
  const button = event.currentTarget;
  // Get the share text from the button's data-src attribute
  const shareText = button.getAttribute("data-src") || "Check this out!";
  // Default Mastodon instance
  const domain = "mastodon.social";
  // Construct the share URL
  const shareURL = `https://${domain}/share?text=${encodeURIComponent(shareText)}`;
  // Open the share page in a new tab
  window.open(shareURL, '_blank');
}

function PixelfeldShare(event) {
  const button = event.currentTarget;
  // Get the share text from the button's data-src attribute
  const shareText = button.getAttribute("data-src") || "Check this out!";
  // Default Pixelfeld instance
  const domain = "pixelfeld.social";
  // Construct the share URL
  const shareURL = `https://${domain}/share?text=${encodeURIComponent(shareText)}`;
  // Open the share page in a new tab
  window.open(shareURL, '_blank');
}

function FriendicaShare(event) {
  const button = event.currentTarget;
  // Get the title and URL from the button's data attributes
  const shareTitle = button.getAttribute("data-title") || "Check this out!";
  const shareURL = button.getAttribute("data-url") || window.location.href;
  // Default Friendica instance
  const domain = "friendica.eu";
  // Construct the share URL
  const fullShareURL = `https://${domain}/share?title=${encodeURIComponent(shareTitle)}&url=${encodeURIComponent(shareURL)}`;
  // Open the share page in a new tab
  window.open(fullShareURL, '_blank');
}
