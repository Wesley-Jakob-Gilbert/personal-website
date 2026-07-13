// Nav: transparent over hero, opaque once user scrolls
const nav = document.getElementById('site-nav');
if (nav) {
  const onScroll = () => nav.classList.toggle('scrolled', window.scrollY > 60);
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll(); // run once on load
}

// Fade-in on scroll via IntersectionObserver.
// IntersectionObserver fires a callback when elements enter/leave the viewport —
// much cheaper than listening to the scroll event for every pixel.
const io = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        io.unobserve(entry.target); // only animate once
      }
    });
  },
  { threshold: 0.08, rootMargin: '0px 0px -48px 0px' }
);

document.querySelectorAll('.fade-in, .fade-in-group').forEach((el) => io.observe(el));

// Hero video: play the intro sequence once, then loop the glide portion.
//
// Expects the <video> element to have two data attributes:
//   data-loop-start="N"  — seconds at which the looping bird-glide section begins
//
// Example: <video data-loop-start="8" autoplay muted playsinline>
const heroVideo = document.querySelector('.hero-media video');
if (heroVideo) {
  const loopStart = parseFloat(heroVideo.dataset.loopStart ?? 0);
  if (loopStart > 0) {
    heroVideo.addEventListener('timeupdate', () => {
      // When the video is within 0.15 s of ending, jump back to the glide loop
      if (heroVideo.duration && heroVideo.currentTime >= heroVideo.duration - 0.15) {
        heroVideo.currentTime = loopStart;
      }
    });
  }
}
