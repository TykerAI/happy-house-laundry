/* ============================================================
   MAIN.JS — Happy House Laundry
   Premium interactions: Nav, Reveal, Counter, Scroll UX, Lightbox
   ============================================================ */

// ── Utility: debounce ──
function debounce(fn, delay) {
    let timer;
    return (...args) => {
        clearTimeout(timer);
        timer = setTimeout(() => fn(...args), delay);
    };
}

// ── Mobile Navigation ──
const hamburger = document.getElementById('hamburger-btn');
const mobileNav = document.getElementById('mobile-nav');

function openMobileNav() {
    mobileNav.classList.add('open');
    hamburger.classList.add('open');
    hamburger.setAttribute('aria-expanded', 'true');
    hamburger.setAttribute('aria-label', 'Đóng menu');
}

function closeMobileNav() {
    mobileNav.classList.remove('open');
    hamburger.classList.remove('open');
    hamburger.setAttribute('aria-expanded', 'false');
    hamburger.setAttribute('aria-label', 'Mở menu');
}

if (hamburger && mobileNav) {
    hamburger.addEventListener('click', (e) => {
        e.stopPropagation();
        const isOpen = mobileNav.classList.contains('open');
        isOpen ? closeMobileNav() : openMobileNav();
    });

    mobileNav.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', closeMobileNav);
    });

    document.addEventListener('click', (e) => {
        if (
            mobileNav.classList.contains('open') &&
            !mobileNav.contains(e.target) &&
            !hamburger.contains(e.target)
        ) {
            closeMobileNav();
        }
    });

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && mobileNav.classList.contains('open')) {
            closeMobileNav();
            hamburger.focus();
        }
    });
}

// ── Scroll Reveal ──
const revealEls = document.querySelectorAll('.reveal, .reveal-left, .reveal-right');

const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            revealObserver.unobserve(entry.target);
        }
    });
}, { threshold: 0.10, rootMargin: '0px 0px -40px 0px' });

revealEls.forEach(el => revealObserver.observe(el));

// ── Animated Counter ──
function animateCounter(el, target, duration, suffix) {
    const start = performance.now();
    const update = (now) => {
        const progress = Math.min((now - start) / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3);
        const current = Math.floor(eased * target);
        el.textContent = current + (progress < 1 ? '' : suffix);
        if (progress < 1) requestAnimationFrame(update);
        else el.textContent = target + suffix;
    };
    requestAnimationFrame(update);
}

const counterEls = document.querySelectorAll('[data-count]');
const counterObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const el = entry.target;
            const target = parseInt(el.dataset.count, 10);
            const suffix = el.dataset.suffix || '+';
            animateCounter(el, target, 1800, suffix);
            counterObserver.unobserve(el);
        }
    });
}, { threshold: 0.5 });

counterEls.forEach(el => counterObserver.observe(el));

// ── Back to Top ──
const backToTop = document.getElementById('back-to-top');
if (backToTop) {
    window.addEventListener('scroll', debounce(() => {
        backToTop.classList.toggle('show', window.scrollY > 400);
    }, 50));

    backToTop.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
}

// ── Smooth scroll for anchor links ──
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', (e) => {
        const targetId = anchor.getAttribute('href');
        if (targetId === '#') return;
        const target = document.querySelector(targetId);
        if (target) {
            e.preventDefault();
            const mainNav = document.getElementById('main-nav');
            const navH = mainNav ? mainNav.offsetHeight : 0;
            const top = target.getBoundingClientRect().top + window.scrollY - navH - 16;
            window.scrollTo({ top, behavior: 'smooth' });
        }
    });
});

// ── Active Nav Link on Scroll ──
const sections = document.querySelectorAll('main section[id], main div[id]');
const navLinks = document.querySelectorAll('.nav-links a[href^="#"], .mobile-nav a[href^="#"]');

const sectionObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const id = entry.target.getAttribute('id');
            navLinks.forEach(link => {
                link.classList.remove('active');
                if (link.getAttribute('href') === `#${id}`) {
                    link.classList.add('active');
                }
            });
        }
    });
}, {
    rootMargin: '-20% 0px -70% 0px',
    threshold: 0
});

sections.forEach(section => sectionObserver.observe(section));

// ── Review gallery horizontal controls ──
const reviewScrollButtons = document.querySelectorAll('.review-scroll-btn');

reviewScrollButtons.forEach((btn) => {
    btn.addEventListener('click', () => {
        const targetId = btn.getAttribute('data-scroll-target');
        const direction = Number(btn.getAttribute('data-scroll-dir') || 1);
        const track = targetId ? document.getElementById(targetId) : null;
        if (!track) return;

        const card = track.querySelector('.review-shot');
        const baseWidth = card ? card.getBoundingClientRect().width : 180;
        const gap = 12;
        const distance = (baseWidth + gap) * 1.8 * direction;

        track.scrollBy({ left: distance, behavior: 'smooth' });
    });
});

// ── Lightbox Gallery ──
// Xóa bất kỳ lightbox overlay cũ nào còn sót lại trong DOM
['lb-overlay', 'lightbox'].forEach(id => {
    const old = document.getElementById(id);
    if (old) old.remove();
});

(function () {
    let images = [];
    let currentIndex = 0;
    let touchStartX = 0;

    // Tạo overlay DOM — chỉ 1 lần duy nhất
    const overlay = document.createElement('div');
    overlay.className = 'lb-overlay';
    overlay.id = 'lb-overlay';
    overlay.setAttribute('role', 'dialog');
    overlay.setAttribute('aria-modal', 'true');
    overlay.setAttribute('aria-label', 'Image viewer');
    overlay.innerHTML = `
        <button class="lb-close-btn" id="lb-close" aria-label="Close">&#10005;</button>
        <button class="lb-nav-btn lb-prev" id="lb-prev" aria-label="Previous">&#8249;</button>
        <button class="lb-nav-btn lb-next" id="lb-next" aria-label="Next">&#8250;</button>
        <div class="lb-img-wrap">
            <img class="lb-main-img" id="lb-img" src="" alt="">
        </div>
        <div class="lb-footer">
            <div class="lb-counter" id="lb-counter" aria-live="polite"></div>
            <div class="lb-dots" id="lb-dots" role="tablist"></div>
        </div>
    `;
    document.body.appendChild(overlay);

    const lbImg = document.getElementById('lb-img');
    const lbCounter = document.getElementById('lb-counter');
    const lbDots = document.getElementById('lb-dots');

    function openLB(trackId, index) {
        const track = document.getElementById(trackId);
        if (!track) return;

        images = Array.from(track.querySelectorAll('.review-shot img')).map(img => ({
            src: img.src,
            alt: img.alt || ''
        }));

        if (!images.length) return;

        currentIndex = index;
        buildDots();
        render(false);

        overlay.classList.add('open');
        document.body.style.overflow = 'hidden';
        document.getElementById('lb-close').focus();
    }

    function closeLB() {
        overlay.classList.remove('open');
        document.body.style.overflow = '';
    }

    function navigate(dir) {
        currentIndex = (currentIndex + dir + images.length) % images.length;
        render(true);
    }

    function goTo(i) {
        currentIndex = i;
        render(true);
    }

    function render(animate) {
        if (animate) {
            lbImg.classList.add('fading');
            setTimeout(() => {
                setImage();
                lbImg.classList.remove('fading');
            }, 200);
        } else {
            setImage();
        }
        lbCounter.textContent = `${currentIndex + 1} / ${images.length}`;
        lbDots.querySelectorAll('.lb-dot').forEach((dot, i) => {
            dot.classList.toggle('active', i === currentIndex);
            dot.setAttribute('aria-selected', i === currentIndex ? 'true' : 'false');
        });
    }

    function setImage() {
        const item = images[currentIndex];
        lbImg.src = item.src;
        lbImg.alt = item.alt;
    }

    function buildDots() {
        lbDots.innerHTML = images.map((_, i) => `
            <button class="lb-dot${i === 0 ? ' active' : ''}"
                role="tab"
                aria-selected="${i === 0}"
                aria-label="Image ${i + 1}"
                data-index="${i}">
            </button>
        `).join('');
        lbDots.querySelectorAll('.lb-dot').forEach(dot => {
            dot.addEventListener('click', () => goTo(parseInt(dot.dataset.index)));
        });
    }

    // Buttons
    document.getElementById('lb-close').addEventListener('click', closeLB);
    document.getElementById('lb-prev').addEventListener('click', () => navigate(-1));
    document.getElementById('lb-next').addEventListener('click', () => navigate(1));

    // Backdrop click
    overlay.addEventListener('click', e => {
        if (e.target === overlay) closeLB();
    });

    // Keyboard
    document.addEventListener('keydown', e => {
        if (!overlay.classList.contains('open')) return;
        if (e.key === 'Escape') closeLB();
        if (e.key === 'ArrowLeft') navigate(-1);
        if (e.key === 'ArrowRight') navigate(1);
    });

    // Swipe (mobile)
    overlay.addEventListener('touchstart', e => {
        touchStartX = e.changedTouches[0].screenX;
    }, { passive: true });

    overlay.addEventListener('touchend', e => {
        const diff = touchStartX - e.changedTouches[0].screenX;
        if (Math.abs(diff) > 50) navigate(diff > 0 ? 1 : -1);
    }, { passive: true });

    // Init tracks
    function initTrack(trackId) {
        const track = document.getElementById(trackId);
        if (!track) return;

        track.querySelectorAll('.review-shot').forEach((figure, index) => {
            // Thêm zoom hint icon nếu chưa có
            if (!figure.querySelector('.lb-zoom-hint')) {
                const hint = document.createElement('div');
                hint.className = 'lb-zoom-hint';
                hint.setAttribute('aria-hidden', 'true');
                hint.innerHTML = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="11" cy="11" r="8"/>
                    <line x1="21" y1="21" x2="16.65" y2="16.65"/>
                    <line x1="11" y1="8" x2="11" y2="14"/>
                    <line x1="8" y1="11" x2="14" y2="11"/>
                </svg>`;
                figure.appendChild(hint);
            }

            figure.style.cursor = 'zoom-in';
            figure.addEventListener('click', () => openLB(trackId, index));

            // Accessibility
            figure.setAttribute('role', 'button');
            figure.setAttribute('tabindex', '0');
            const img = figure.querySelector('img');
            figure.setAttribute('aria-label', `Xem ảnh phóng to: ${img ? img.alt : ''}`);
            figure.addEventListener('keydown', e => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    openLB(trackId, index);
                }
            });
        });
    }

    // Init cả 2 ngôn ngữ
    initTrack('reviews-track-vi');
    initTrack('reviews-track-en');

})();