/**
 * ============================================================================
 * isitreal Documentation Website — Calm Discovery & Interactive Sandbox Logic
 * ============================================================================
 */

(function () {
  'use strict';

  /* ==========================================================================
     1. Theme Management (Calm Dark / Calm Light Mode)
     ========================================================================== */

  const themeToggleBtn = document.getElementById('theme-toggle-btn');
  const savedTheme = localStorage.getItem('isitreal-theme') || 'dark';

  function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('isitreal-theme', theme);
  }

  setTheme(savedTheme);

  if (themeToggleBtn) {
    themeToggleBtn.addEventListener('click', () => {
      const currentTheme = document.documentElement.getAttribute('data-theme');
      const nextTheme = currentTheme === 'dark' ? 'light' : 'dark';
      setTheme(nextTheme);
    });
  }

  /* ==========================================================================
     2. Mobile Drawer Navigation
     ========================================================================== */

  const mobileMenuBtn = document.getElementById('mobile-menu-btn');
  const mobileDrawer = document.getElementById('mobile-drawer');

  if (mobileMenuBtn && mobileDrawer) {
    mobileMenuBtn.addEventListener('click', () => {
      const isOpen = mobileDrawer.classList.toggle('open');
      mobileMenuBtn.setAttribute('aria-expanded', isOpen);
    });

    mobileDrawer.querySelectorAll('a').forEach((link) => {
      link.addEventListener('click', () => {
        mobileDrawer.classList.remove('open');
        mobileMenuBtn.setAttribute('aria-expanded', 'false');
      });
    });
  }

  /* ==========================================================================
     3. Copy-to-Clipboard Utility
     ========================================================================== */

  document.querySelectorAll('.copy-btn').forEach((btn) => {
    btn.addEventListener('click', async () => {
      const textToCopy = btn.getAttribute('data-copy') || '';
      if (!textToCopy) return;

      try {
        await navigator.clipboard.writeText(textToCopy);
        const originalText = btn.innerHTML;
        btn.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#34D399" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg> <span style="color:#34D399;font-weight:700;">Copied</span>`;
        btn.disabled = true;

        setTimeout(() => {
          btn.innerHTML = originalText;
          btn.disabled = false;
        }, 1800);
      } catch (err) {
        console.error('Failed to copy clipboard text:', err);
      }
    });
  });

  /* ==========================================================================
     4. Interactive Sandbox — Realistic Package Reality Database
     ========================================================================== */

  const PACKAGE_DB = {
    'requests': {
      name: 'requests',
      exists: true,
      canonical_name: 'requests',
      latest_version: '2.32.3',
      summary: 'Python HTTP for Humans.',
      first_release_date: '2011-02-13T00:00:00Z',
      total_releases: 154,
      suggestions: [],
      risk: 'low',
      reasons: [
        'Package is in the top PyPI packages by download count.',
        'Package has been published for 5,640 days.',
        'Over 320,000,000 monthly downloads confirmed.'
      ],
      age_days: 5640
    },
    'react-codeshift': {
      name: 'react-codeshift',
      exists: false,
      canonical_name: null,
      latest_version: null,
      summary: null,
      first_release_date: null,
      total_releases: 0,
      suggestions: ['jscodeshift', 'react-codemod', 'codemod'],
      risk: 'high',
      reasons: [
        'Package name is in the known list of AI-hallucinated/slopsquatted packages.',
        'Name looks like an LLM conflation of well-known libraries (jscodeshift + react-codemod).',
        'High risk of malicious slopsquatting interception.'
      ],
      age_days: null
    },
    'fancylib': {
      name: 'fancylib',
      exists: false,
      canonical_name: null,
      latest_version: null,
      summary: null,
      first_release_date: null,
      total_releases: 0,
      suggestions: ['fancy-lib', 'fancier-lib', 'fancycompleter'],
      risk: null,
      reasons: [
        'Package does not exist on PyPI.',
        'No known hallucination or conflation pattern detected.'
      ],
      age_days: null
    },
    'django-postgres': {
      name: 'django-postgres',
      exists: false,
      canonical_name: null,
      latest_version: null,
      summary: null,
      first_release_date: null,
      total_releases: 0,
      suggestions: ['psycopg2-binary', 'django-postgres-extra', 'django'],
      risk: 'high',
      reasons: [
        'Package name is in the known list of AI-hallucinated/slopsquatted packages.',
        'Frequently hallucinated target for PostgreSQL Django connectors.'
      ],
      age_days: null
    },
    'pydantic': {
      name: 'pydantic',
      exists: true,
      canonical_name: 'pydantic',
      latest_version: '2.8.2',
      summary: 'Data validation and settings management using Python type hints',
      first_release_date: '2017-06-03T00:00:00Z',
      total_releases: 118,
      suggestions: [],
      risk: 'low',
      reasons: [
        'Package is in the top PyPI packages by download count.',
        'Package has been published for 2,800 days.',
        'Standard library in modern AI and backend engineering.'
      ],
      age_days: 2800
    },
    'jscodeshiftreact': {
      name: 'jscodeshiftreact',
      exists: true,
      canonical_name: 'jscodeshiftreact',
      latest_version: '0.0.1',
      summary: 'Suspicious helper library',
      first_release_date: '2026-06-01T00:00:00Z',
      total_releases: 1,
      suggestions: [],
      risk: 'high',
      reasons: [
        'Package name looks like a conflation of well-known packages (\'jscodeshift\' and \'react\').',
        'Package was first published less than 30 days ago.',
        'Zero download reputation confirmed.'
      ],
      age_days: 12
    },
    'my-fresh-pkg': {
      name: 'my-fresh-pkg',
      exists: true,
      canonical_name: 'my-fresh-pkg',
      latest_version: '0.1.0',
      summary: 'Experimental internal utility',
      first_release_date: '2026-07-15T00:00:00Z',
      total_releases: 2,
      suggestions: [],
      risk: 'high',
      reasons: [
        'Package was first published less than 30 days ago (Age: 11 days).',
        'Lacks download history or top PyPI membership.'
      ],
      age_days: 11
    }
  };

  /**
   * Smart heuristic simulator for arbitrary user-entered package names
   */
  function simulatePackageLookup(name) {
    const clean = name.trim().toLowerCase();
    if (PACKAGE_DB[clean]) {
      return PACKAGE_DB[clean];
    }

    // Heuristics for interactive realism
    if (clean.includes('react-') || clean.includes('-postgres') || clean.includes('codeshift') || clean.includes('slop')) {
      return {
        name: name.trim(),
        exists: false,
        canonical_name: null,
        latest_version: null,
        summary: null,
        first_release_date: null,
        total_releases: 0,
        suggestions: [`${clean}-lib`, 'requests', 'pydantic'],
        risk: 'high',
        reasons: [
          'Package name matches known AI hallucination syntax pattern.',
          'High risk of slopsquatting interception if installed without verification.'
        ],
        age_days: null
      };
    }

    if (['numpy', 'django', 'flask', 'httpx', 'click', 'rich', 'fastapi', 'pytest'].includes(clean)) {
      return {
        name: clean,
        exists: true,
        canonical_name: clean,
        latest_version: '3.1.0',
        summary: `Official ${clean} package on PyPI.`,
        first_release_date: '2015-01-01T00:00:00Z',
        total_releases: 85,
        suggestions: [],
        risk: 'low',
        reasons: [
          'Package is in the top PyPI packages by download count.',
          'Package has been published for over 3,500 days.'
        ],
        age_days: 3500
      };
    }

    // Default missing package
    return {
      name: name.trim(),
      exists: false,
      canonical_name: null,
      latest_version: null,
      summary: null,
      first_release_date: null,
      total_releases: 0,
      suggestions: [`${clean}-utils`, `${clean}-core`, 'requests'],
      risk: null,
      reasons: [
        'Package does not exist on PyPI.',
        'No high-risk hallucination flags detected.'
      ],
      age_days: null
    };
  }

  /* ==========================================================================
     5. Render Sandbox Single Package Results
     ========================================================================== */

  const resultContainer = document.getElementById('sandbox-result-view');
  const packageInput = document.getElementById('package-query-input');
  const checkBtn = document.getElementById('sandbox-check-btn');

  function renderPackageResult(res) {
    if (!resultContainer) return;

    let riskBadgeHtml = `<span class="risk-badge" style="background:#334155;color:#cbd5e1;">NONE</span>`;
    if (res.risk === 'high') {
      riskBadgeHtml = `<span class="risk-badge risk-high">HIGH RISK</span>`;
    } else if (res.risk === 'low') {
      riskBadgeHtml = `<span class="risk-badge risk-low">LOW RISK</span>`;
    } else if (res.risk === 'unknown') {
      riskBadgeHtml = `<span class="risk-badge risk-unknown">UNKNOWN RISK</span>`;
    }

    const existsText = res.exists
      ? `<span style="color:#34D399;font-weight:700;">Exists on PyPI</span>`
      : `<span style="color:#FB7185;font-weight:700;">Missing on PyPI</span>`;

    const suggestionsHtml = res.suggestions && res.suggestions.length > 0
      ? `<div class="suggestions-pill-group">
           <span>Did you mean?</span>
           ${res.suggestions.map((s) => `<code>${s}</code>`).join(' ')}
         </div>`
      : '';

    const isDangerBox = res.risk === 'high' ? 'box-danger' : '';

    resultContainer.innerHTML = `
      <div class="result-header">
        <div>
          <div class="result-package-name">${res.name}</div>
          <div style="font-size:0.85rem;color:#94a3b8;margin-top:0.25rem;">
            Status: ${existsText}
            ${res.canonical_name ? ` • Canonical: <code>${res.canonical_name}</code>` : ''}
          </div>
        </div>
        <div>${riskBadgeHtml}</div>
      </div>

      <div class="result-details-grid">
        <div class="detail-item">
          <span class="detail-label">Latest Version</span>
          <span class="detail-value">${res.latest_version || 'N/A'}</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">Package Age</span>
          <span class="detail-value">${res.age_days !== null ? `${res.age_days.toLocaleString()} days` : 'N/A'}</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">Total Releases</span>
          <span class="detail-value">${res.total_releases}</span>
        </div>
      </div>

      ${res.summary ? `<p style="font-size:0.9rem;color:#cbd5e1;margin-bottom:1.25rem;">${res.summary}</p>` : ''}

      ${res.reasons && res.reasons.length > 0 ? `
        <div class="reasons-box ${isDangerBox}">
          <div class="reasons-title">Explainable Safety Diagnostic</div>
          <ul class="reasons-list">
            ${res.reasons.map((r) => `<li>• ${r}</li>`).join('')}
          </ul>
        </div>
      ` : ''}

      ${suggestionsHtml}
    `;
  }

  if (checkBtn && packageInput) {
    const handleLookup = () => {
      const query = packageInput.value;
      if (!query) return;
      const res = simulatePackageLookup(query);
      renderPackageResult(res);
    };

    checkBtn.addEventListener('click', handleLookup);
    packageInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') handleLookup();
    });

    // Initial render
    renderPackageResult(simulatePackageLookup(packageInput.value));
  }

  // Example pills click
  document.querySelectorAll('.example-pill').forEach((pill) => {
    pill.addEventListener('click', () => {
      const pkgName = pill.getAttribute('data-pkg');
      if (packageInput && pkgName) {
        packageInput.value = pkgName;
        renderPackageResult(simulatePackageLookup(pkgName));
      }
    });
  });

  /* ==========================================================================
     6. Interactive Sandbox — Tabs & Batch Scanner
     ========================================================================== */

  const tabBtns = document.querySelectorAll('.sandbox-tab-btn');
  tabBtns.forEach((btn) => {
    btn.addEventListener('click', () => {
      const tabId = btn.getAttribute('data-tab');
      tabBtns.forEach((b) => b.classList.remove('active'));
      document.querySelectorAll('.sandbox-tab-content').forEach((c) => c.classList.remove('active'));

      btn.classList.add('active');
      const targetContent = document.getElementById(`tab-${tabId}`);
      if (targetContent) targetContent.classList.add('active');
    });
  });

  const runScanBtn = document.getElementById('run-scan-btn');
  const resetScannerBtn = document.getElementById('reset-scanner-btn');
  const scannerInput = document.getElementById('scanner-input-textarea');
  const scannerOutput = document.getElementById('scanner-output-view');

  function parseAndScanRequirements(text) {
    const lines = text.split('\n');
    const results = [];

    lines.forEach((line) => {
      const trimmed = line.trim();
      if (!trimmed || trimmed.startsWith('#')) return;

      // Extract raw package name before syntax ==, >=, etc.
      const match = trimmed.match(/^([a-zA-Z0-9_-]+)/);
      if (match && match[1]) {
        const pkgName = match[1];
        const result = simulatePackageLookup(pkgName);
        results.push(result);
      }
    });

    // Sort worst-risk-first: high -> unknown -> low -> null
    const orderMap = { 'high': 1, 'unknown': 2, 'low': 3 };
    results.sort((a, b) => {
      const rankA = a.risk ? orderMap[a.risk] : 4;
      const rankB = b.risk ? orderMap[b.risk] : 4;
      return rankA - rankB;
    });

    return results;
  }

  function renderScannerResults(results) {
    if (!scannerOutput) return;

    if (results.length === 0) {
      scannerOutput.innerHTML = `<p style="padding:1rem;color:#94a3b8;">No valid package dependencies found.</p>`;
      return;
    }

    let rowsHtml = results.map((res) => {
      let riskHtml = `<span style="color:#64748b;">NONE</span>`;
      if (res.risk === 'high') {
        riskHtml = `<span class="risk-badge risk-high">HIGH</span>`;
      } else if (res.risk === 'low') {
        riskHtml = `<span class="risk-badge risk-low">LOW</span>`;
      } else if (res.risk === 'unknown') {
        riskHtml = `<span class="risk-badge risk-unknown">UNKNOWN</span>`;
      }

      const existsHtml = res.exists
        ? `<span style="color:#34D399;font-weight:600;">Yes</span>`
        : `<span style="color:#FB7185;font-weight:700;">No</span>`;

      const noteText = res.reasons && res.reasons[0] ? res.reasons[0] : (res.suggestions.length ? `Suggestions: ${res.suggestions.join(', ')}` : '-');

      return `
        <tr>
          <td><code style="font-weight:700;color:#f8fafc;">${res.name}</code></td>
          <td>${existsHtml}</td>
          <td>${riskHtml}</td>
          <td><code>${res.latest_version || '-'}</code></td>
          <td>${res.age_days !== null ? `${res.age_days}d` : '-'}</td>
          <td style="color:#94a3b8;font-size:0.82rem;">${noteText}</td>
        </tr>
      `;
    }).join('');

    scannerOutput.innerHTML = `
      <table class="scan-results-table">
        <thead>
          <tr>
            <th>Package</th>
            <th>Exists</th>
            <th>Risk</th>
            <th>Version</th>
            <th>Age</th>
            <th>Safety Notes</th>
          </tr>
        </thead>
        <tbody>
          ${rowsHtml}
        </tbody>
      </table>
    `;
  }

  if (runScanBtn && scannerInput) {
    runScanBtn.addEventListener('click', () => {
      const results = parseAndScanRequirements(scannerInput.value);
      renderScannerResults(results);
    });

    // Run scan on initial load
    renderScannerResults(parseAndScanRequirements(scannerInput.value));
  }

  if (resetScannerBtn && scannerInput) {
    resetScannerBtn.addEventListener('click', () => {
      scannerInput.value = `# Genuine core libraries\nrequests==2.32.3\npydantic>=2.7.0\nhttpx==0.27.0\n\n# Hallucinated / slopsquatted AI agent targets\nreact-codeshift>=1.0.0\ndjango-postgres\nfancylib==0.1.0`;
      renderScannerResults(parseAndScanRequirements(scannerInput.value));
    });
  }

  /* ==========================================================================
     7. Scrollspy Table of Contents (Right Sidebar)
     ========================================================================== */

  const tocLinks = document.querySelectorAll('.toc-link');
  const sectionIds = ['hero', 'why-it-exists', 'sandbox', 'quickstart', 'python-api', 'cli-reference', 'mcp-server', 'risk-scoring'];

  window.addEventListener('scroll', () => {
    let currentId = 'hero';
    const scrollPos = window.scrollY + 140;

    sectionIds.forEach((id) => {
      const el = document.getElementById(id);
      if (el && el.offsetTop <= scrollPos) {
        currentId = id;
      }
    });

    tocLinks.forEach((link) => {
      const href = link.getAttribute('href');
      if (href === `#${currentId}`) {
        link.classList.add('active');
      } else {
        link.classList.remove('active');
      }
    });
  }, { passive: true });

  /* ==========================================================================
     8. Command Palette / Search Modal (`Cmd+K` / `Ctrl+K`)
     ========================================================================== */

  const SEARCH_INDEX = [
    { title: 'Why does isitreal exist?', href: '#why-it-exists', snippet: 'AI coding agents hallucinate package names and conflate libraries into slopsquat targets.' },
    { title: 'Interactive Sandbox & Simulator', href: '#sandbox', snippet: 'Test single package verification and batch scan requirements.txt live.' },
    { title: 'Quickstart & Installation', href: '#quickstart', snippet: 'pip install isitreal or clone from source for development and testing.' },
    { title: 'Python API — verify.package(name)', href: '#python-api', snippet: 'Query a single package name programmatically and inspect PackageResult.' },
    { title: 'Python API — verify.scan(target)', href: '#python-api', snippet: 'Scan a requirements.txt or pyproject.toml file worst-risk-first.' },
    { title: 'PackageResult Data Model', href: '#python-api', snippet: 'Fields: name, exists, canonical_name, latest_version, summary, suggestions, risk, reasons, age_days.' },
    { title: 'CLI — isitreal check <name>', href: '#cli-reference', snippet: 'Verify a package in your terminal with rich formatted diagnostic boxes.' },
    { title: 'CLI — isitreal scan requirements.txt', href: '#cli-reference', snippet: 'Scan dependency files and display sorted table worst-risk-first.' },
    { title: 'CI/CD Automated Gating (--fail-on high)', href: '#cli-reference', snippet: 'Exit nonzero code 1 in GitHub Actions when high risk dependencies are detected.' },
    { title: 'MCP Server for Claude Desktop', href: '#mcp-server', snippet: 'Configure "command": "isitreal-mcp" in claude_desktop_config.json.' },
    { title: 'MCP Server for Claude Code (.claude.json)', href: '#mcp-server', snippet: 'Configure "isitreal-mcp" in project root .claude.json to guard agents.' },
    { title: 'MCP Tools: verify_package & verify_dependencies', href: '#mcp-server', snippet: 'Official FastMCP tools exposed to AI coding agents.' },
    { title: 'Risk Scoring Engine Explained', href: '#risk-scoring', snippet: 'How age (<30 days), top PyPI index, slopsquatted lists, and conflation are evaluated.' }
  ];

  const searchModal = document.getElementById('search-modal');
  const searchTriggerBtn = document.getElementById('search-trigger-btn');
  const closeModalBtn = document.getElementById('close-modal-btn');
  const modalInput = document.getElementById('modal-search-input');
  const searchResultsList = document.getElementById('search-results-list');

  let selectedIndex = 0;
  let filteredResults = [...SEARCH_INDEX];

  function openSearchModal() {
    if (!searchModal) return;
    searchModal.classList.add('open');
    modalInput.value = '';
    selectedIndex = 0;
    renderSearchResults(SEARCH_INDEX);
    setTimeout(() => modalInput.focus(), 50);
  }

  function closeSearchModal() {
    if (!searchModal) return;
    searchModal.classList.remove('open');
  }

  function renderSearchResults(items) {
    if (!searchResultsList) return;
    filteredResults = items;

    if (items.length === 0) {
      searchResultsList.innerHTML = `<p style="padding:1rem;color:#94a3b8;text-align:center;">No documentation matching your query.</p>`;
      return;
    }

    searchResultsList.innerHTML = items.map((item, idx) => `
      <a href="${item.href}" class="search-result-item ${idx === selectedIndex ? 'selected' : ''}" data-idx="${idx}">
        <span class="result-title">${item.title}</span>
        <span class="result-snippet">${item.snippet}</span>
      </a>
    `).join('');

    // Add click handlers
    searchResultsList.querySelectorAll('.search-result-item').forEach((el) => {
      el.addEventListener('click', () => closeSearchModal());
      el.addEventListener('mouseenter', () => {
        selectedIndex = parseInt(el.getAttribute('data-idx'), 10);
        updateSelectedHighlight();
      });
    });
  }

  function updateSelectedHighlight() {
    if (!searchResultsList) return;
    const items = searchResultsList.querySelectorAll('.search-result-item');
    items.forEach((item, idx) => {
      if (idx === selectedIndex) {
        item.classList.add('selected');
        item.scrollIntoView({ block: 'nearest' });
      } else {
        item.classList.remove('selected');
      }
    });
  }

  if (searchTriggerBtn) {
    searchTriggerBtn.addEventListener('click', openSearchModal);
  }

  if (closeModalBtn) {
    closeModalBtn.addEventListener('click', closeSearchModal);
  }

  if (searchModal) {
    searchModal.addEventListener('click', (e) => {
      if (e.target === searchModal) closeSearchModal();
    });
  }

  window.addEventListener('keydown', (e) => {
    // Cmd+K or Ctrl+K
    if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
      e.preventDefault();
      if (searchModal.classList.contains('open')) {
        closeSearchModal();
      } else {
        openSearchModal();
      }
    }

    if (e.key === 'Escape' && searchModal && searchModal.classList.contains('open')) {
      closeSearchModal();
    }

    if (searchModal && searchModal.classList.contains('open')) {
      if (e.key === 'ArrowDown') {
        e.preventDefault();
        selectedIndex = (selectedIndex + 1) % filteredResults.length;
        updateSelectedHighlight();
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        selectedIndex = (selectedIndex - 1 + filteredResults.length) % filteredResults.length;
        updateSelectedHighlight();
      } else if (e.key === 'Enter') {
        e.preventDefault();
        const selectedItem = filteredResults[selectedIndex];
        if (selectedItem) {
          closeSearchModal();
          window.location.hash = selectedItem.href;
        }
      }
    }
  });

  if (modalInput) {
    modalInput.addEventListener('input', () => {
      const query = modalInput.value.toLowerCase().trim();
      const filtered = SEARCH_INDEX.filter((item) =>
        item.title.toLowerCase().includes(query) ||
        item.snippet.toLowerCase().includes(query)
      );
      selectedIndex = 0;
      renderSearchResults(filtered);
    });
  }

})();
