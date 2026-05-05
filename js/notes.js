(function() {
  'use strict';

  const PER_PAGE = 15;

  // ── Pagination ────────────────────────────────────────────────
  function initPagination() {
    const posts = Array.from(document.querySelectorAll('.note-preview'));
    if (!posts.length) return;

    const total = posts.length;
    const pageCount = Math.ceil(total / PER_PAGE);
    if (pageCount <= 1) return;

    let currentPage = 1;

    function showPage(page) {
      currentPage = page;
      posts.forEach((post, i) => {
        post.style.display = (i >= (page-1)*PER_PAGE && i < page*PER_PAGE) ? '' : 'none';
      });
      renderControls();
    }

    function renderControls() {
      const existing = document.querySelector('.note-pagination');
      if (existing) existing.remove();

      const nav = document.createElement('nav');
      nav.className = 'note-pagination';

      if (currentPage > 1) {
        const prev = document.createElement('a');
        prev.href = '#'; prev.textContent = '← Previous';
        prev.addEventListener('click', e => { e.preventDefault(); showPage(currentPage - 1); window.scrollTo(0,0); });
        nav.appendChild(prev);
      }

      for (let p = 1; p <= pageCount; p++) {
        const a = document.createElement('a');
        a.href = '#'; a.textContent = p;
        if (p === currentPage) a.classList.add('active');
        a.addEventListener('click', (e) => { e.preventDefault(); showPage(p); window.scrollTo(0,0); });
        nav.appendChild(a);
      }

      if (currentPage < pageCount) {
        const next = document.createElement('a');
        next.href = '#'; next.textContent = 'Next →';
        next.addEventListener('click', e => { e.preventDefault(); showPage(currentPage + 1); window.scrollTo(0,0); });
        nav.appendChild(next);
      }

      document.querySelector('.notes-list').after(nav);
    }

    showPage(1);
  }

  // ── Read more / Read less ─────────────────────────────────────
  function initReadMore() {
    document.addEventListener('click', function(e) {
      const btn = e.target.closest('.note-read-more, .note-read-less');
      if (!btn) return;
      e.preventDefault();

      const article = btn.closest('.note-preview');
      const excerpt = article.querySelector('.note-excerpt');
      const fullDiv = article.querySelector('.note-full');

      if (btn.classList.contains('note-read-more')) {
        if (fullDiv.dataset.loaded) {
          // Already fetched — just show
          excerpt.hidden = true;
          fullDiv.hidden = false;
          btn.textContent = 'Read less';
          btn.className = 'note-read-less';
          return;
        }

        btn.textContent = 'Loading…';
        btn.disabled = true;

        fetch(article.dataset.url)
          .then(r => r.text())
          .then(html => {
            const doc = new DOMParser().parseFromString(html, 'text/html');
            const content = doc.querySelector('.post-content');
            if (content) {
              // Remove nav elements (prev/next links, share buttons) before inserting
              content.querySelectorAll('.post_navi, .share-links, nav').forEach(el => el.remove());
            }
            fullDiv.innerHTML = content ? content.innerHTML : '<p>Could not load content.</p>';
            fullDiv.dataset.loaded = '1';
            excerpt.hidden = true;
            fullDiv.hidden = false;
            btn.textContent = 'Read less';
            btn.className = 'note-read-less';
            btn.disabled = false;
          })
          .catch(() => {
            btn.textContent = 'Read more';
            btn.disabled = false;
          });

      } else {
        // Read less — collapse
        fullDiv.hidden = true;
        excerpt.hidden = false;
        btn.textContent = 'Read more';
        btn.className = 'note-read-more';
      }
    });
  }

  document.addEventListener('DOMContentLoaded', function() {
    initPagination();
    initReadMore();
  });
})();
