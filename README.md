# invisiblethreat

A Jekyll blog with three complete brand directions, using the original charcoal,
teal, and mint palette. Existing posts and permalinks are preserved.

- **Fieldnotes** (default): spacious editorial layout, serif headlines, identity panel.
- **Signal**: structured technical journal, sans-serif headlines, monospaced metadata.
- **Quiet**: narrow personal journal, mint headlines, serif article text.

## Preview

With Ruby 3.1+ and Bundler installed:

```sh
bundle install
bundle exec jekyll serve --host 127.0.0.1
```

Open <http://localhost:4000/designs/> to compare the options. Each option works
across the home page, archive, article pages, search, and 404. Preview links carry
`?theme=fieldnotes`, `?theme=signal`, or `?theme=quiet` through navigation, with a
small comparison bar. Without a query parameter, visitors see the configured theme.
No browser storage or remote fonts are required.

## Select a theme

Fieldnotes is the selected default. Signal and Quiet are retained as complete,
config-selectable themes. In `_config.yml`:

```yaml
theme_style: fieldnotes # fieldnotes | signal | quiet
```

Change the value and rebuild to switch the entire site. The configured theme works with
JavaScript disabled. JavaScript is used for search and the temporary previews.
The comparison page is marked `noindex, nofollow` and is not linked from the
production navigation.

## Build and verify

```sh
bundle exec jekyll build --strict_front_matter
python3 script/check_site.py
node --check assets/theme.js
```

Or, using Docker without a local Ruby installation:

```sh
docker run --rm -v "$PWD:/site" -w /site -e BUNDLE_PATH=/usr/local/bundle ruby:3.3 sh -c 'bundle install && bundle exec jekyll build --strict_front_matter'
python3 -m http.server 4000 --bind 127.0.0.1 --directory _site
```

The shared theme lives in `assets/theme.css`, `_layouts`, and `_includes`.
Search builds a JSON index of all published article text and uses native DOM APIs
to display matches. The layout uses semantic landmarks, keyboard focus styles,
a skip link, fluid type, scrollable code blocks, and reduced-motion/print styles.
No Bootstrap, jQuery, icon font, external font service, or client-side syntax
highlighting library is loaded. Jekyll/Rouge handles code highlighting at build time.

Fieldnotes is ready for deployment through the repository's normal GitHub Pages
process. Local builds do not publish the site.
