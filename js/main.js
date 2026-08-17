document.addEventListener('DOMContentLoaded', () => {
    // Mobile Menu Toggle
    const menuToggle = document.getElementById('menuToggle');
    const navLinks = document.getElementById('navLinks');

    if (menuToggle && navLinks) {
        menuToggle.addEventListener('click', () => {
            navLinks.classList.toggle('active');
        });

        navLinks.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                navLinks.classList.remove('active');
            });
        });
    }

    // Smooth scroll for internal anchors
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href === '#') return;
            const target = document.querySelector(href);
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });

    // Active section highlighting
    const sections = document.querySelectorAll('section[id]');
    const navAnchors = document.querySelectorAll('.nav-links a[href^="#"]');

    if (sections.length && navAnchors.length && 'IntersectionObserver' in window) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    navAnchors.forEach(a => a.classList.remove('active'));
                    const match = document.querySelector(`.nav-links a[href="#${entry.target.id}"]`);
                    if (match) match.classList.add('active');
                }
            });
        }, { rootMargin: '-40% 0px -55% 0px' });

        sections.forEach(s => observer.observe(s));
    }

    // Latest writing — render posts from writing/medium-posts.json
    const latestWriting = document.getElementById('latest-writing');
    if (latestWriting) {
        fetch('writing/medium-posts.json')
            .then(res => {
                if (!res.ok) throw new Error(`HTTP ${res.status}`);
                return res.json();
            })
            .then(data => {
                const posts = (data && data.posts) || [];
                const fragment = document.createDocumentFragment();
                posts.forEach((post, index) => {
                    const article = document.createElement('article');
                    article.className = 'entry';
                    article.style.animationDelay = `${index * 90}ms`;

                    const heading = document.createElement('h3');
                    const link = document.createElement('a');
                    link.href = post.url;
                    link.target = '_blank';
                    link.rel = 'noopener';
                    link.textContent = post.title;
                    heading.appendChild(link);

                    if (post.excerpt) {
                        const excerpt = document.createElement('p');
                        excerpt.textContent = post.excerpt;
                        article.appendChild(excerpt);
                    }

                    const meta = document.createElement('div');
                    meta.className = 'entry-meta';
                    const span = document.createElement('span');
                    span.textContent = `${post.dateLabel || ''} · Medium`;
                    meta.appendChild(span);

                    article.appendChild(heading);
                    article.appendChild(meta);
                    fragment.appendChild(article);
                });
                latestWriting.appendChild(fragment);
            })
            .catch(() => {
                // silent fallback — section stays empty if the JSON is missing
            });
    }
});
