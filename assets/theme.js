(() => {
  const theme = new URLSearchParams(location.search).get('theme');
  const valid = ['fieldnotes', 'signal', 'quiet'].includes(theme);
  function previewLink(link) {
    if (!valid) return;
    const url = new URL(link.href, location.href);
    if (url.origin === location.origin && !/\.(xml|json|png|jpg|svg|pdf)$/.test(url.pathname) && !url.searchParams.has('theme')) {
      url.searchParams.set('theme', theme); link.href = url.href;
    }
  }
  document.querySelectorAll('a[href]').forEach(previewLink);
  if (valid) {
    const bar = document.createElement('aside'); bar.className = 'preview-bar'; bar.setAttribute('aria-label', 'Theme preview');
    const label = document.createElement('span'); label.textContent = 'Preview / ' + theme;
    const link = document.createElement('a'); link.href = document.querySelector('.brand').href.split('?')[0] + 'designs/'; link.textContent = 'Compare themes ↗';
    bar.append(label, link); document.body.append(bar); document.body.classList.add('is-preview');
  }
  const input = document.getElementById('search-input');
  if (!input) return;
  const status = document.getElementById('search-status'), results = document.getElementById('search-results');
  let posts = [];
  function search() {
    const query = input.value.trim().toLocaleLowerCase(); results.replaceChildren();
    if (!query) { status.textContent = 'Search ' + posts.length + ' articles. Start typing to find a note.'; return; }
    const words = query.split(/\s+/);
    const matches = posts.filter(post => words.every(word => (post.title + ' ' + post.tags + ' ' + post.text).toLocaleLowerCase().includes(word)));
    status.textContent = matches.length ? matches.length + (matches.length === 1 ? ' article found' : ' articles found') : 'No articles found. Try a different word or phrase.';
    matches.forEach(post => {
      const item = document.createElement('li'), link = document.createElement('a'), date = document.createElement('span');
      link.href = post.url; link.textContent = post.title; previewLink(link); date.textContent = post.date;
      item.append(date, link); results.append(item);
    });
  }
  input.disabled = true;
  fetch(input.dataset.source).then(response => { if (!response.ok) throw new Error('Search unavailable'); return response.json(); }).then(data => { posts = data; input.disabled = false; search(); input.addEventListener('input', search); }).catch(() => {
    status.textContent = 'Search couldn’t load. You can browse every article in the archive.';
    const link = document.createElement('a'); link.href = document.querySelector('.brand').href.split('?')[0] + 'posts/'; link.textContent = 'Browse archive ↗'; previewLink(link); results.append(link);
  });
})();
