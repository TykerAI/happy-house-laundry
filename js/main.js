// --- Mobile Navigation ---
        const hamburger = document.getElementById('hamburger-btn');
        const mobileNav = document.getElementById('mobile-nav');

        hamburger.addEventListener('click', () => {
            const isOpen = mobileNav.classList.toggle('open');
            hamburger.classList.toggle('open', isOpen);
            hamburger.setAttribute('aria-expanded', isOpen.toString());
        });

        // Close mobile nav on link click
        mobileNav.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                mobileNav.classList.remove('open');
                hamburger.classList.remove('open');
                hamburger.setAttribute('aria-expanded', 'false');
            });
        });

        // --- Scroll Reveal ---
        const revealEls = document.querySelectorAll('.reveal, .reveal-left, .reveal-right');

        const revealObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    revealObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.12, rootMargin: '0px 0px -50px 0px' });

        revealEls.forEach(el => revealObserver.observe(el));

        // --- Animated Counter ---
        function animateCounter(el, target, duration, suffix) {
            const start = performance.now();
            const update = (now) => {
                const progress = Math.min((now - start) / duration, 1);
                const eased = 1 - Math.pow(1 - progress, 3);
                el.textContent = Math.floor(eased * target) + (progress < 1 ? '' : suffix);
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
                    // Support custom suffix via data-suffix attribute (e.g. "%" for 100%)
                    const suffix = el.dataset.suffix || '+';
                    animateCounter(el, target, 1800, suffix);
                    counterObserver.unobserve(el);
                }
            });
        }, { threshold: 0.5 });

        counterEls.forEach(el => counterObserver.observe(el));

        // --- Back to Top ---
        const backToTop = document.getElementById('back-to-top');
        window.addEventListener('scroll', () => {
            if (window.scrollY > 400) {
                backToTop.classList.add('show');
            } else {
                backToTop.classList.remove('show');
            }
        });
        backToTop.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });

        // --- Smooth scroll for anchor links (offset for sticky nav) ---
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', (e) => {
                const targetId = anchor.getAttribute('href');
                if (targetId === '#') return;
                const target = document.querySelector(targetId);
                if (target) {
                    e.preventDefault();
                    const navH = document.getElementById('main-nav').offsetHeight;
                    const top = target.getBoundingClientRect().top + window.scrollY - navH - 16;
                    // JS scroll override needed for nav offset — CSS smooth-behavior handles other cases
                    window.scrollTo({ top, behavior: 'smooth' });
                }
            });
        });