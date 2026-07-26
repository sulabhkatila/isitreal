# isitreal Documentation Website (`gh-pages-dev`)

This branch (`gh-pages-dev`) contains the calm, readable, introduction & discovery documentation website for **[`isitreal`](https://github.com/example/isitreal)** — the dependency reality-checker for AI coding agents.

## Branch Workflow

- **Development**: Make design and content updates on the `gh-pages-dev` branch.
- **Local Preview**: Run a simple HTTP server in the root of this branch:
  ```bash
  python3 -m http.server 8000
  ```
  Then open `http://localhost:8000` in your browser.

- **Deployment**: After dev is complete, push this branch to `gh-pages` to publish on GitHub Pages:
  ```bash
  # Push local gh-pages-dev to remote gh-pages branch
  git push origin gh-pages-dev:gh-pages
  ```

## Website Highlights

- **Calm, Readable Typography & Palette**: Built with a soothing dark/light slate theme, comfortable line length (`max-w-prose`), and harmonious spacing.
- **Interactive Discovery Sandbox**: Visitors can test live/simulated package verifications (`requests`, `react-codeshift`, `fancylib`, `django-postgres`) and scan dependency files directly in their browser.
- **Command Palette (`Cmd+K`)**: Rapid documentation search across API references, CLI commands, and MCP agent integration guides.
- **Zero Dependencies**: Pure, modern semantic HTML5, Vanilla CSS, and modular JavaScript for instant page loads and excellent SEO.
