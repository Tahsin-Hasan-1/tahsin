/**
 * main.js — Portfolio core interactions
 * Green terminal theme | Interactive realistic shell console
 */

// ─── Resolve base path (works on localhost, GitHub Pages, Vercel, InfinityFree, custom domains) ──
// Walks up from the current script URL (assets/js/main.js) two levels to reach the site root.
const _scriptSrc = (document.currentScript && document.currentScript.src)
    || Array.from(document.querySelectorAll('script[src]')).map(s => s.src).find(s => s.includes('main.js'))
    || '';
const BASE_URL = _scriptSrc
    ? _scriptSrc.split('/').slice(0, -3).join('/') + '/'  // strip /assets/js/main.js
    : './';

Promise.all([
    fetch(BASE_URL + 'includes/header.html').then(r => r.text()),
    fetch(BASE_URL + 'includes/footer.html').then(r => r.text())
]).then(([headerHTML, footerHTML]) => {
    const headerEl = document.getElementById('site-header');
    if (headerEl) headerEl.innerHTML = headerHTML;

    const footerEl = document.getElementById('site-footer');
    if (footerEl) footerEl.innerHTML = footerHTML;

    setupNav();
    highlightActiveLink();
    startHeaderLogoAnimation();
    startRealisticTerminalSimulation();
    setupInteractiveTerminal();
}).catch(err => {
    console.warn('Includes load failed — access via http://, not file://', err);
});

// ─── Mobile hamburger toggle ─────────────────────────────────────────────────
function setupNav() {
    const menuBtn = document.getElementById('menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');
    if (!menuBtn || !mobileMenu) return;

    menuBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        const isOpen = !mobileMenu.classList.contains('hidden');
        mobileMenu.classList.toggle('hidden', isOpen);

        const bars = menuBtn.querySelectorAll('span');
        if (!isOpen) {
            bars[0].style.transform = 'translateY(8px) rotate(45deg)';
            bars[1].style.opacity = '0';
            bars[2].style.transform = 'translateY(-8px) rotate(-45deg)';
            bars[2].style.width = '24px';
        } else {
            bars[0].style.transform = '';
            bars[1].style.opacity = '';
            bars[2].style.transform = '';
            bars[2].style.width = '';
        }
    });

    document.addEventListener('click', (e) => {
        const headerEl = document.getElementById('site-header');
        if (headerEl && !headerEl.contains(e.target)) {
            mobileMenu.classList.add('hidden');
            const bars = menuBtn.querySelectorAll('span');
            bars[0].style.transform = '';
            bars[1].style.opacity = '';
            bars[2].style.transform = '';
            bars[2].style.width = '';
        }
    });
}

// ─── Active nav highlight ────────────────────────────────────────────────────
function highlightActiveLink() {
    const page = window.location.pathname.split('/').pop() || 'index.html';
    document.querySelectorAll('.nav-link, .mobile-nav-link').forEach(link => {
        if (link.getAttribute('href') === page) {
            link.classList.add('active');
        }
    });
}

// ─── Header Logo Loop (Type -> wait 10s -> Erase -> wait 5s -> Repeat) ──────
function startHeaderLogoAnimation() {
    const logoEl = document.querySelector('.logo-type');
    if (!logoEl) return;

    const FULL = 'tahsin@portfolio:~$';
    const TYPE_MS = 70;
    const ERASE_MS = 35;
    const WAIT_FULL = 10000; // 10s
    const WAIT_EMPTY = 5000;  // 5s

    let idx = 0;
    let state = 'typing'; // 'typing' | 'waiting' | 'erasing' | 'idle'

    function tick() {
        if (state === 'typing') {
            if (idx < FULL.length) {
                logoEl.textContent = FULL.slice(0, ++idx);
                setTimeout(tick, TYPE_MS + Math.random() * 20);
            } else {
                state = 'waiting';
                setTimeout(() => {
                    state = 'erasing';
                    tick();
                }, WAIT_FULL);
            }
        } else if (state === 'erasing') {
            if (idx > 0) {
                logoEl.textContent = FULL.slice(0, --idx);
                setTimeout(tick, ERASE_MS);
            } else {
                state = 'idle';
                setTimeout(() => {
                    state = 'typing';
                    tick();
                }, WAIT_EMPTY);
            }
        }
    }
    tick();
}

// Flag to stop landing simulation once user interacts
let isInteractiveTerminalActive = false;

// Hide/show the interactive prompt line
function setPromptVisible(visible) {
    const activeLine = document.getElementById('terminal-active-line');
    if (!activeLine) return;
    activeLine.style.display = visible ? 'flex' : 'none';
}

// ─── Realistic Landing Terminal Simulation ──────────────────────────────────
function startRealisticTerminalSimulation() {
    const history = document.getElementById('terminal-history');
    if (!history) return;

    // Command Sequence
    const command1 = "sudo apt update";
    const logs1 = [
        "Hit:1 http://bd.archive.ubuntu.com/ubuntu noble InRelease",
        "Get:2 http://security.ubuntu.com/ubuntu noble-security InRelease [126 kB]",
        "Fetched 126 kB in 0s (340 kB/s)",
        "Reading package lists... Done"
    ];

    const command2 = "sudo apt install -y nmap";
    const logs2 = [
        "Reading package lists... Done",
        "Building dependency tree... Done",
        "nmap is already the newest version (7.94-1ubuntu1).",
        "0 upgraded, 0 newly installed, 0 to remove."
    ];

    // Added third command (cat details/target_ips.txt)
    const command3 = "cat details/target_ips.txt";
    const logs3 = [
        "192.168.1.1   - Gateway [Active]",
        "192.168.1.45  - Linux Web Server [Ports: 80, 443 open]",
        "192.168.1.108 - Testing Host [Firewall Enabled]"
    ];

    // Hide interactive prompt during simulation
    setPromptVisible(false);

    function step1_typeCommand1() {
        if (isInteractiveTerminalActive) return;

        const cmdLine = document.createElement('div');
        cmdLine.className = 'history-item';
        cmdLine.innerHTML = `<span class="text-green-500 font-bold">tahsin@portfolio:~$</span> <span class="cmd-text text-green-400 font-bold"></span>`;
        history.appendChild(cmdLine);

        const cmdTextSpan = cmdLine.querySelector('.cmd-text');
        let charIdx = 0;

        function type() {
            if (isInteractiveTerminalActive) return;
            if (charIdx < command1.length) {
                cmdTextSpan.textContent += command1[charIdx++];
                scrollToBottom();
                setTimeout(type, 50 + Math.random() * 20);
            } else {
                let logIdx = 0;
                function printLogs() {
                    if (isInteractiveTerminalActive) return;
                    if (logIdx < logs1.length) {
                        const logDiv = document.createElement('div');
                        logDiv.className = 'text-slate-400 font-light';
                        logDiv.textContent = logs1[logIdx++];
                        history.appendChild(logDiv);
                        scrollToBottom();
                        setTimeout(printLogs, 80 + Math.random() * 50);
                    } else {
                        setTimeout(step2_typeCommand2, 1000);
                    }
                }
                setTimeout(printLogs, 250);
            }
        }
        type();
    }

    function step2_typeCommand2() {
        if (isInteractiveTerminalActive) return;

        const cmdLine = document.createElement('div');
        cmdLine.className = 'history-item';
        cmdLine.innerHTML = `<span class="text-green-500 font-bold">tahsin@portfolio:~$</span> <span class="cmd-text text-green-400 font-bold"></span>`;
        history.appendChild(cmdLine);

        const cmdTextSpan = cmdLine.querySelector('.cmd-text');
        let charIdx = 0;

        function type() {
            if (isInteractiveTerminalActive) return;
            if (charIdx < command2.length) {
                cmdTextSpan.textContent += command2[charIdx++];
                setTimeout(type, 50 + Math.random() * 20);
            } else {
                let logIdx = 0;
                function printLogs() {
                    if (isInteractiveTerminalActive) return;
                    if (logIdx < logs2.length) {
                        const logDiv = document.createElement('div');
                        logDiv.className = 'text-slate-400 font-light';
                        logDiv.textContent = logs2[logIdx++];
                        history.appendChild(logDiv);
                        scrollToBottom();
                        setTimeout(printLogs, 80 + Math.random() * 50);
                    } else {
                        setTimeout(step3_typeCommand3, 1000);
                    }
                }
                setTimeout(printLogs, 250);
            }
        }
        type();
    }

    function step3_typeCommand3() {
        if (isInteractiveTerminalActive) return;

        const cmdLine = document.createElement('div');
        cmdLine.className = 'history-item';
        cmdLine.innerHTML = `<span class="text-green-500 font-bold">tahsin@portfolio:~$</span> <span class="cmd-text text-green-400 font-bold"></span>`;
        history.appendChild(cmdLine);

        const cmdTextSpan = cmdLine.querySelector('.cmd-text');
        let charIdx = 0;

        function type() {
            if (isInteractiveTerminalActive) return;
            if (charIdx < command3.length) {
                cmdTextSpan.textContent += command3[charIdx++];
                setTimeout(type, 50 + Math.random() * 20);
            } else {
                let logIdx = 0;
                function printLogs() {
                    if (isInteractiveTerminalActive) return;
                    if (logIdx < logs3.length) {
                        const logDiv = document.createElement('div');
                        logDiv.className = 'text-slate-400 font-light';
                        logDiv.textContent = logs3[logIdx++];
                        history.appendChild(logDiv);
                        scrollToBottom();
                        setTimeout(printLogs, 80 + Math.random() * 50);
                    } else {
                        // Simulation done — reveal the interactive prompt
                        setPromptVisible(true);
                        scrollToBottom();
                    }
                }
                setTimeout(printLogs, 250);
            }
        }
        type();
    }

    function scrollToBottom() {
        const body = history.closest('.terminal-body') || history.parentElement;
        if (body) body.scrollTop = body.scrollHeight;
    }

    // Start simulation
    step1_typeCommand1();
}

// ─── Interactive Terminal Sandbox ───────────────────────────────────────────
let cmatrixIntervals = new Set();

function setupInteractiveTerminal() {
    // 1. Setup Main Page Terminal (only on index.html)
    initTerminalInstance(
        'terminal-textarea',
        'terminal-input-buffer',
        'terminal-history',
        'terminal-active-line',
        false
    );

    // 2. Create & setup Floating Terminal widget (appended to body on all pages)
    setupFloatingTerminalToggle();
}

function setupFloatingTerminalToggle() {
    // Create the floating terminal and inject directly into body
    const container = document.createElement('div');
    container.id = 'floating-terminal-container';
    container.style.cssText = `
        display: none;
        position: fixed;
        bottom: 24px;
        right: 24px;
        width: 420px;
        max-width: calc(100vw - 32px);
        height: 320px;
        max-height: calc(100vh - 80px);
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid rgba(34,197,94,0.2);
        box-shadow: 0 25px 60px rgba(0,0,0,0.8), 0 0 40px rgba(34,197,94,0.05);
        flex-direction: column;
        z-index: 9999;
        background: rgba(3,7,5,0.97);
        backdrop-filter: blur(0px);
        font-family: 'JetBrains Mono', 'Fira Code', monospace;
    `;
    container.innerHTML = `
        <!-- Top invisible resize handle -->
        <div id="floating-terminal-resize-handle" style="position:absolute;top:0;left:0;right:0;height:10px;cursor:ns-resize;z-index:10"></div>
        <!-- Titlebar (Drag Handle) -->
        <div id="floating-terminal-titlebar" style="padding:8px 14px;background:rgba(34,197,94,0.05);border-bottom:1px solid rgba(34,197,94,0.1);display:flex;align-items:center;justify-content:space-between;font-family:monospace;font-size:11px;user-select:none;flex-shrink:0;cursor:move">
            <div style="display:flex;align-items:center;gap:7px;pointer-events:none">
                <span style="width:10px;height:10px;border-radius:50%;background:rgba(239,68,68,0.8);display:inline-block"></span>
                <span style="width:10px;height:10px;border-radius:50%;background:rgba(234,179,8,0.8);display:inline-block"></span>
                <span style="width:10px;height:10px;border-radius:50%;background:rgba(34,197,94,0.8);display:inline-block"></span>
                <span style="color:#22c55e;font-weight:700;margin-left:4px">shell:~</span>
                <span style="color:#475569;font-size:10px;margin-left:4px">// drag to move, pull top edge to resize</span>
            </div>
            <button id="floating-terminal-close" style="background:transparent;border:none;color:#64748b;font-size:18px;line-height:1;cursor:pointer;padding:0 2px;transition:color 0.2s" onmouseover="this.style.color='#22c55e'" onmouseout="this.style.color='#64748b'">&times;</button>
        </div>
        <!-- Terminal body -->
        <div id="floating-terminal-body" style="flex:1;padding:12px 14px;overflow-y:auto;font-family:monospace;font-size:12.5px;color:#4ade80;display:flex;flex-direction:column;min-height:0">
            <div id="floating-terminal-history" style="display:flex;flex-direction:column;gap:4px"></div>
            <div id="floating-terminal-active-line" style="display:flex;align-items:center;width:100%;margin-top:6px">
                <span style="color:#22c55e;font-weight:700;margin-right:8px;white-space:nowrap">tahsin@portfolio:~$</span>
                <div style="flex:1;display:flex;align-items:center;position:relative">
                    <span id="floating-terminal-input-buffer" style="color:#f1f5f9;white-space:pre-wrap"></span><span style="display:inline-block;width:8px;height:14px;background:#4ade80;vertical-align:middle;margin-left:2px;animation:blink 1s step-end infinite"></span>
                    <textarea id="floating-terminal-textarea" style="position:absolute;inset:0;opacity:0;cursor:default;resize:none;background:transparent;border:none;outline:none;caret-color:transparent;font-family:inherit;font-size:inherit"></textarea>
                </div>
            </div>
        </div>
    `;
    document.body.appendChild(container);

    // Wire up toggle buttons
    function closeMobileMenu() {
        const mobileMenu = document.getElementById('mobile-menu');
        const menuBtn = document.getElementById('menu-btn');
        if (mobileMenu) mobileMenu.classList.add('hidden');
        if (menuBtn) {
            const bars = menuBtn.querySelectorAll('span');
            bars[0].style.transform = '';
            bars[1].style.opacity = '';
            bars[2].style.transform = '';
            bars[2].style.width = '';
        }
    }

    function toggle() {
        const isHidden = container.style.display === 'none';
        if (isHidden) {
            closeMobileMenu();
            // Small delay lets mobile menu animate closed before terminal pops up
            setTimeout(() => {
                container.style.display = 'flex';
                const ta = container.querySelector('#floating-terminal-textarea');
                if (ta) setTimeout(() => ta.focus({ preventScroll: true }), 80);
            }, 150);
        } else {
            container.style.display = 'none';
        }
    }

    const trigger = document.getElementById('floating-terminal-trigger');
    const triggerMobile = document.getElementById('floating-terminal-trigger-mobile');
    if (trigger) trigger.addEventListener('click', toggle);
    if (triggerMobile) triggerMobile.addEventListener('click', toggle);

    const closeBtn = container.querySelector('#floating-terminal-close');
    if (closeBtn) closeBtn.addEventListener('click', () => container.style.display = 'none');

    // ─── Drag-to-Move Logic (Mouse & Touch) ──────────────────────────────────
    const titlebar = container.querySelector('#floating-terminal-titlebar');
    let isDragging = false;
    let dragStartX = 0, dragStartY = 0;
    let initialLeft = 0, initialTop = 0;

    function onDragStart(e) {
        if (e.target === closeBtn) return;
        isDragging = true;

        // Get touch or mouse coords
        const clientX = e.touches ? e.touches[0].clientX : e.clientX;
        const clientY = e.touches ? e.touches[0].clientY : e.clientY;

        dragStartX = clientX;
        dragStartY = clientY;

        // Fetch actual rendered position
        const rect = container.getBoundingClientRect();
        initialLeft = rect.left;
        initialTop = rect.top;

        // Switch from bottom/right layout to top/left layout for absolute position freedom
        container.style.bottom = 'auto';
        container.style.right = 'auto';
        container.style.left = `${initialLeft}px`;
        container.style.top = `${initialTop}px`;

        // Prevent text selection
        document.body.style.userSelect = 'none';
    }

    function onDragMove(e) {
        if (!isDragging) return;
        const clientX = e.touches ? e.touches[0].clientX : e.clientX;
        const clientY = e.touches ? e.touches[0].clientY : e.clientY;

        const deltaX = clientX - dragStartX;
        const deltaY = clientY - dragStartY;

        // Bounds validation
        const nextLeft = Math.max(0, Math.min(window.innerWidth - container.offsetWidth, initialLeft + deltaX));
        const nextTop = Math.max(0, Math.min(window.innerHeight - container.offsetHeight, initialTop + deltaY));

        container.style.left = `${nextLeft}px`;
        container.style.top = `${nextTop}px`;
    }

    function onDragEnd() {
        isDragging = false;
        document.body.style.userSelect = '';
    }

    titlebar.addEventListener('mousedown', onDragStart);
    titlebar.addEventListener('touchstart', onDragStart, { passive: true });
    window.addEventListener('mousemove', onDragMove);
    window.addEventListener('touchmove', onDragMove, { passive: false });
    window.addEventListener('mouseup', onDragEnd);
    window.addEventListener('touchend', onDragEnd);

    // ─── Drag-to-Resize Logic (Mouse & Touch on Top Edge) ────────────────────
    const resizeHandle = container.querySelector('#floating-terminal-resize-handle');
    let isResizing = false;
    let resizeStartY = 0;
    let initialHeight = 0;

    function onResizeStart(e) {
        isResizing = true;
        const clientY = e.touches ? e.touches[0].clientY : e.clientY;
        resizeStartY = clientY;
        initialHeight = container.offsetHeight;

        const rect = container.getBoundingClientRect();
        initialTop = rect.top;

        container.style.bottom = 'auto';
        container.style.right = 'auto';
        container.style.left = `${rect.left}px`;
        container.style.top = `${initialTop}px`;

        document.body.style.userSelect = 'none';
        if (e.cancelable) e.preventDefault();
    }

    function onResizeMove(e) {
        if (!isResizing) return;
        const clientY = e.touches ? e.touches[0].clientY : e.clientY;

        // Dragging top edge UP reduces mouse coordinate Y, which increases height
        const deltaY = clientY - resizeStartY;
        const newHeight = initialHeight - deltaY;
        const newTop = initialTop + deltaY;

        // Limit range (min 150px, max 80% viewport height)
        const minHeight = 160;
        const maxHeight = window.innerHeight - 80;

        if (newHeight >= minHeight && newHeight <= maxHeight && newTop >= 0) {
            container.style.height = `${newHeight}px`;
            container.style.top = `${newTop}px`;
        }
    }

    function onResizeEnd() {
        isResizing = false;
        document.body.style.userSelect = '';
    }

    resizeHandle.addEventListener('mousedown', onResizeStart);
    resizeHandle.addEventListener('touchstart', onResizeStart, { passive: false });
    window.addEventListener('mousemove', onResizeMove);
    window.addEventListener('touchmove', onResizeMove, { passive: false });
    window.addEventListener('mouseup', onResizeEnd);
    window.addEventListener('touchend', onResizeEnd);

    // Now init the terminal instance for this widget
    initTerminalInstance(
        'floating-terminal-textarea',
        'floating-terminal-input-buffer',
        'floating-terminal-history',
        'floating-terminal-active-line',
        true
    );
}

function initTerminalInstance(textareaId, bufferId, historyId, activeLineId, isFloating) {
    const txtArea = document.getElementById(textareaId);
    const inputBuffer = document.getElementById(bufferId);
    const history = document.getElementById(historyId);
    if (!txtArea || !inputBuffer || !history) return;

    const parentContainer = history.closest('.terminal-container') || history.closest('#floating-terminal-container') || history.parentElement;
    if (parentContainer) {
        parentContainer.addEventListener('click', () => {
            txtArea.focus({ preventScroll: true });
        });
    }

    const helpCommands = {
        'whoami': 'Show identity details',
        'ls': 'List focus domains',
        'uname': 'System info',
        'cmatrix': 'Matrix terminal visualizer (use cmatrix -s for full-screen)',
        'help': 'Show available pages to navigate',
        'clear': 'Clear terminal screen',
        'exit': 'Close connection / leave site',
    };

    const commands = {
        'whoami': ['tahsin hasan'],
        'ls': ['network_analysis/  osint/  phishing_analysis/'],
        'uname': ['cybersecurity enthusiast'],
        'help': ['Available pages: index  about  blog  contact\nType a page name to navigate there.'],
        'man t': null,
        'sudo apt update': [
            'Hit:1 http://bd.archive.ubuntu.com/ubuntu noble InRelease',
            'Get:2 http://security.ubuntu.com/ubuntu noble-security InRelease [126 kB]',
            'Fetched 126 kB in 0s (340 kB/s)',
            'Reading package lists... Done'
        ],
        'sudo apt install -y nmap': [
            'Reading package lists... Done',
            'Building dependency tree... Done',
            'nmap is already the newest version (7.94-1ubuntu1).',
            '0 upgraded, 0 newly installed, 0 to remove.'
        ],
        'cat details/target_ips.txt': [
            '192.168.1.1   - Gateway [Active]',
            '192.168.1.45  - Linux Web Server [Ports: 80, 443 open]',
            '192.168.1.108 - Testing Host [Firewall Enabled]'
        ],
        'exit': ['exit : Closing connection...'],
    };

    let localCmatrixInterval = null;

    txtArea.addEventListener('input', () => {
        if (localCmatrixInterval) {
            clearInterval(localCmatrixInterval);
            cmatrixIntervals.delete(localCmatrixInterval);
            localCmatrixInterval = null;
            history.innerHTML = '';
        }
        if (!isFloating && !isInteractiveTerminalActive) {
            isInteractiveTerminalActive = true;
            setPromptVisible(true);
        }
        inputBuffer.textContent = txtArea.value;
        scrollToBottom();
    });

    txtArea.addEventListener('keydown', (e) => {
        if (['ArrowUp', 'ArrowDown', 'PageUp', 'PageDown'].includes(e.key)) {
            e.preventDefault();
        }
    }, { capture: true });

    txtArea.addEventListener('keydown', (e) => {
        if (e.key !== 'Enter') return;
        e.preventDefault();
        e.stopPropagation();

        const rawVal = txtArea.value;
        const cleanCmd = rawVal.trim().toLowerCase();
        txtArea.value = '';
        inputBuffer.textContent = '';

        if (!cleanCmd) return;

        const echo = document.createElement('div');
        echo.className = 'history-item';
        echo.innerHTML = `<span class="text-green-500 font-bold">tahsin@portfolio:~$</span> <span class="text-slate-100">${rawVal}</span>`;
        history.appendChild(echo);

        // ── cmatrix / cmatrix -s logic ───────────────────────────────────────
        if (cleanCmd.startsWith('cmatrix')) {
            const args = cleanCmd.split(' ').slice(1);
            if (args.includes('-s')) {
                runFullscreenCMatrix();
            } else {
                runCMatrixAnimation();
            }
            return;
        }

        if (cleanCmd === 'clear') {
            history.innerHTML = '';
            return;
        }

        if (cleanCmd === 'exit') {
            printLines(['exit: Closing connection...'], 'text-rose-400');
            setTimeout(() => {
                if (isFloating) {
                    const container = document.getElementById('floating-terminal-container');
                    if (container) container.style.display = 'none';
                } else {
                    window.close();
                    setTimeout(() => { window.location.href = 'https://www.google.com'; }, 300);
                }
            }, 800);
            return;
        }

        if (cleanCmd === 'man t') {
            const lines = ['Available Commands:', ...Object.entries(helpCommands).map(([k, v]) => `  ${k.padEnd(10)} — ${v}`)];
            printLines(lines, 'text-slate-300');
            return;
        }

        const pageNames = ['index', 'about', 'project', 'blog', 'contact'];
        if (pageNames.includes(cleanCmd)) {
            printLines([`Navigating to ${cleanCmd}...`], 'text-emerald-400');
            setTimeout(() => { window.location.href = BASE_URL + `${cleanCmd}.html`; }, 600);
            return;
        }

        if (commands[cleanCmd] !== undefined) {
            printLines(commands[cleanCmd], 'text-slate-400');
            return;
        }

        printLines([`bash: command not found: ${cleanCmd}. Try 'man t' for help.`], 'text-rose-400');
    });

    function printLines(lines, colorClass = 'text-slate-400') {
        let idx = 0;
        function next() {
            if (idx >= lines.length) return;
            const div = document.createElement('div');
            div.className = `${colorClass} mt-0.5 pl-4 whitespace-pre-wrap font-mono text-sm`;
            div.textContent = lines[idx++];
            history.appendChild(div);
            scrollToBottom();
            setTimeout(next, 60 + Math.random() * 50);
        }
        next();
    }

    function runCMatrixAnimation() {
        history.innerHTML = '';
        const matrixDiv = document.createElement('div');
        matrixDiv.className = 'text-green-500 font-mono leading-none tracking-widest text-xs h-full w-full';
        history.appendChild(matrixDiv);

        const width = isFloating ? 30 : 45;
        const columns = Array(width).fill(0);

        localCmatrixInterval = setInterval(() => {
            let row = '';
            for (let i = 0; i < width; i++) {
                if (Math.random() > 0.95) { columns[i] = Math.floor(Math.random() * 15); }
                if (columns[i] > 0) {
                    row += String.fromCharCode(33 + Math.floor(Math.random() * 93));
                    columns[i]--;
                } else {
                    row += '&nbsp;';
                }
            }
            const line = document.createElement('div');
            line.innerHTML = row;
            matrixDiv.appendChild(line);
            if (matrixDiv.children.length > 18) matrixDiv.removeChild(matrixDiv.firstChild);
            scrollToBottom();
        }, 80);
    }

    function scrollToBottom() {
        // For floating terminal: scroll its body div
        // For main terminal: scroll .terminal-body
        const floatingBody = document.getElementById('floating-terminal-body');
        const mainBody = document.querySelector('.terminal-body');
        const body = isFloating ? floatingBody : mainBody;
        if (body) body.scrollTop = body.scrollHeight;
    }
}

function runFullscreenCMatrix() {
    const canvas = document.createElement('canvas');
    canvas.style.cssText = 'position:fixed;top:0;left:0;width:100vw;height:100vh;z-index:999999;background:transparent;cursor:pointer';
    document.body.appendChild(canvas);

    const ctx = canvas.getContext('2d');
    const fontSize = 14;
    let cols, ypos, trails;

    function resize() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        cols = Math.floor(canvas.width / fontSize) + 1;
        // Start drops at random heights across the entire screen so it is instantly filled
        ypos = Array(cols).fill(0).map(() => Math.random() * canvas.height);
        // Initialize an empty trail array for each column
        trails = Array(cols).fill(0).map(() => []);
        ctx.clearRect(0, 0, canvas.width, canvas.height);
    }
    resize();
    window.addEventListener('resize', resize);

    function draw() {
        // Clear canvas entirely to maintain transparency
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        ctx.font = `${fontSize}px monospace`;

        for (let i = 0; i < cols; i++) {
            const trail = trails[i];

            // 1. Age existing characters in trail
            for (let j = 0; j < trail.length; j++) {
                trail[j].alpha -= 0.06; // fade speed
            }
            // Filter out faded characters
            trails[i] = trail.filter(t => t.alpha > 0);

            // 2. Add new head character
            const char = String.fromCharCode(33 + Math.floor(Math.random() * 93));
            trails[i].push({
                y: ypos[i],
                char: char,
                alpha: 1.0
            });

            // 3. Draw all characters in this trail with alpha transparency
            for (let j = 0; j < trails[i].length; j++) {
                const drop = trails[i][j];
                if (j === trails[i].length - 1) {
                    // Lead character is bright white-green
                    ctx.fillStyle = `rgba(220, 255, 220, ${drop.alpha})`;
                } else {
                    // Tail characters are green
                    ctx.fillStyle = `rgba(0, 200, 83, ${drop.alpha})`;
                }
                ctx.fillText(drop.char, i * fontSize, drop.y);
            }

            // 4. Move lead position down
            if (ypos[i] > canvas.height + Math.random() * 300) {
                ypos[i] = 0;
                trails[i] = [];
            } else {
                ypos[i] += fontSize;
            }
        }
    }

    const interval = setInterval(draw, 40);

    function close() {
        clearInterval(interval);
        window.removeEventListener('resize', resize);
        canvas.remove();
        document.removeEventListener('keydown', close);
    }

    // Delay listener registration so the current Enter keypress bubble doesn't trigger close()
    setTimeout(() => {
        document.addEventListener('keydown', close);
        canvas.addEventListener('click', close);
    }, 100);
}

// ─── Scroll reveal ───────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
    const obs = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('reveal-active');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

    document.querySelectorAll('.reveal-on-scroll').forEach(el => {
        el.classList.add('reveal-prep');
        obs.observe(el);
    });
});

// ─── Game Tab Switcher ──────────────────────────────────────────────────────
function switchGameTab(tab) {
    document.querySelectorAll('.game-panel').forEach(p => p.style.display = 'none');
    document.getElementById('tab-scanner').classList.remove('active-tab');
    document.getElementById('tab-ips').classList.remove('active-tab');

    if (tab === 'scanner') {
        document.getElementById('panel-scanner').style.display = 'block';
        document.getElementById('tab-scanner').classList.add('active-tab');
    } else {
        document.getElementById('panel-ips').style.display = 'block';
        document.getElementById('tab-ips').classList.add('active-tab');
    }
}

// ─── Port Scanner Game Logic ─────────────────────────────────────────────────
let targetPort = 0;
let portAttempts = 5;

function initPortGame(autoFocus = false) {
    targetPort = Math.floor(Math.random() * 1024) + 1;
    portAttempts = 5;

    const log = document.getElementById('port-log');
    if (log) log.innerHTML = '<div class="text-green-500/60 mb-2">--- SCANNER INITIALIZED ---</div>';

    updateGameStatus('port-status', `Scanner ready... [${portAttempts} attempts remaining]`, 'text-slate-400');

    const input = document.getElementById('port-guess');
    if (input) {
        input.value = '';
        input.disabled = false;
        if (autoFocus) input.focus();
    }
}

function updateGameStatus(statusId, msg, colorClass) {
    const status = document.getElementById(statusId);
    if (status) {
        status.className = `text-sm font-mono mb-4 h-6 ${colorClass}`;
        status.textContent = msg;
    }
}

function logGameAction(logId, msg, isSuccess = false) {
    const log = document.getElementById(logId);
    if (log) {
        const div = document.createElement('div');
        div.className = `mb-1 ${isSuccess ? 'text-green-400 font-bold' : 'text-slate-400'}`;
        div.innerHTML = `> ${msg}`;
        log.prepend(div);
    }
}

function checkPortGuess() {
    if (!targetPort) initPortGame(false);

    if (portAttempts <= 0) return;

    const input = document.getElementById('port-guess');
    if (!input) return;

    const guess = parseInt(input.value.trim(), 10);

    if (isNaN(guess) || guess < 1 || guess > 1024) {
        updateGameStatus('port-status', 'Error: Invalid port. Enter a number between 1 and 1024.', 'text-rose-400');
        return;
    }

    portAttempts--;

    if (guess === targetPort) {
        updateGameStatus('port-status', 'PORT IDENTIFIED', 'text-green-400 font-bold');
        logGameAction('port-log', `[Port ${guess}] Target compromised. Access Granted!`, true);
        input.disabled = true;
    } else {
        if (portAttempts > 0) {
            updateGameStatus('port-status', `Connection refused... [${portAttempts} attempts remaining]`, 'text-amber-400');
            const hint = guess > targetPort ? "Too high" : "Too low";
            logGameAction('port-log', `[Port ${guess}] Closed. Hint: ${hint}.`);
        } else {
            updateGameStatus('port-status', 'FIREWALL BLOCKED IP', 'text-rose-500 font-bold');
            logGameAction('port-log', `[Port ${guess}] Blocked. The open port was ${targetPort}.`, false);
            input.disabled = true;
        }
    }
    input.value = '';
    input.focus();
}

// ─── IPS Defender Game Logic ─────────────────────────────────────────────────
// Attack types:
//   'ddos'       = red ☠️  → single click to patch (2.5s window)
//   'ransomware' = orange 🔒 → DOUBLE click to patch (3s window)
//   'worm'       = purple 🪱 → click fast (1.5s window), spreads to neighbor
const ATTACK_TYPES = {
    ddos: { icon: '☠️', bg: 'bg-rose-900', border: 'border-rose-500', glow: 'shadow-[0_0_15px_rgba(239,68,68,0.6)]', window: 2500, label: 'DDoS' },
    ransomware: { icon: '🔒', bg: 'bg-orange-900', border: 'border-orange-500', glow: 'shadow-[0_0_15px_rgba(249,115,22,0.6)]', window: 3000, label: 'Ransomware' },
    worm: { icon: '🪱', bg: 'bg-purple-900', border: 'border-purple-500', glow: 'shadow-[0_0_15px_rgba(168,85,247,0.6)]', window: 1500, label: 'Worm' },
};

const LEVELS = [
    { attackInterval: 2000, simultaneousAttacks: 1, types: ['ddos'], winScore: 8, label: 'Level 1 — Recon' },
    { attackInterval: 1400, simultaneousAttacks: 2, types: ['ddos', 'ransomware'], winScore: 8, label: 'Level 2 — Intrusion' },
    { attackInterval: 1000, simultaneousAttacks: 3, types: ['ddos', 'ransomware', 'worm'], winScore: 8, label: 'Level 3 — APT' },
];

let ipsLives = 3;
let ipsScore = 0;
let ipsLevel = 0;
let ipsLevelScore = 0;
let ipsCombo = 0;
let ipsInterval = null;
let ipsRunning = false;
let nodeStates = new Array(9).fill('safe');   // 'safe' | 'attacked'
let nodeTypes = new Array(9).fill(null);     // attack type key
let nodeClicks = new Array(9).fill(0);        // for ransomware double-click

const NODE_BASE_CLASS = 'ips-node w-12 h-12 md:w-16 md:h-16 rounded flex justify-center items-center cursor-pointer transition-all duration-300 text-xl select-none';
const NODE_SAFE_CLASS = `${NODE_BASE_CLASS} bg-slate-800 border border-slate-700`;

function resetAllNodes() {
    for (let i = 0; i < 9; i++) {
        const node = document.getElementById(`node-${i}`);
        if (node) { node.className = NODE_SAFE_CLASS; node.innerHTML = '💻'; }
        nodeStates[i] = 'safe';
        nodeTypes[i] = null;
        nodeClicks[i] = 0;
    }
}

function startIpsGame() {
    if (ipsRunning) return;
    ipsLives = 3; ipsScore = 0; ipsLevel = 0; ipsLevelScore = 0; ipsCombo = 0;
    ipsRunning = true;
    resetAllNodes();
    updateIpsStatus();
    scheduleAttacks();
}

function scheduleAttacks() {
    clearInterval(ipsInterval);
    if (!ipsRunning) return;
    const cfg = LEVELS[ipsLevel];
    ipsInterval = setInterval(() => {
        for (let a = 0; a < cfg.simultaneousAttacks; a++) {
            attackRandomNode();
        }
    }, cfg.attackInterval);
}

function pickAttackType() {
    const types = LEVELS[ipsLevel].types;
    return types[Math.floor(Math.random() * types.length)];
}

function attackRandomNode() {
    if (!ipsRunning) return;
    const safeNodes = nodeStates.map((s, i) => s === 'safe' ? i : -1).filter(i => i !== -1);
    if (safeNodes.length === 0) return;

    const target = safeNodes[Math.floor(Math.random() * safeNodes.length)];
    const type = pickAttackType();
    const cfg = ATTACK_TYPES[type];

    nodeStates[target] = 'attacked';
    nodeTypes[target] = type;
    nodeClicks[target] = 0;

    const node = document.getElementById(`node-${target}`);
    if (node) {
        node.className = `${NODE_BASE_CLASS} ${cfg.bg} border-2 ${cfg.border} animate-pulse ${cfg.glow}`;
        node.innerHTML = cfg.icon;
    }

    // If worm — spread to a neighbor after 700ms if still active
    if (type === 'worm') {
        setTimeout(() => {
            if (nodeStates[target] === 'attacked' && nodeTypes[target] === 'worm') {
                const neighbors = getNeighbors(target);
                const safeNeighbors = neighbors.filter(n => nodeStates[n] === 'safe');
                if (safeNeighbors.length > 0) {
                    const spread = safeNeighbors[Math.floor(Math.random() * safeNeighbors.length)];
                    infectNode(spread, 'worm');
                }
            }
        }, 700);
    }

    // Auto-breach timer
    setTimeout(() => {
        if (nodeStates[target] === 'attacked') {
            breachNode(target);
        }
    }, cfg.window);
}

function infectNode(index, type) {
    if (nodeStates[index] !== 'safe') return;
    const cfg = ATTACK_TYPES[type];
    nodeStates[index] = 'attacked';
    nodeTypes[index] = type;
    nodeClicks[index] = 0;
    const node = document.getElementById(`node-${index}`);
    if (node) {
        node.className = `${NODE_BASE_CLASS} ${cfg.bg} border-2 ${cfg.border} animate-pulse ${cfg.glow}`;
        node.innerHTML = cfg.icon;
    }
    setTimeout(() => {
        if (nodeStates[index] === 'attacked') breachNode(index);
    }, cfg.window);
}

function getNeighbors(index) {
    // 3×3 grid adjacency (up, down, left, right)
    const row = Math.floor(index / 3), col = index % 3, neighbors = [];
    if (row > 0) neighbors.push(index - 3);
    if (row < 2) neighbors.push(index + 3);
    if (col > 0) neighbors.push(index - 1);
    if (col < 2) neighbors.push(index + 1);
    return neighbors;
}

function breachNode(index) {
    if (!ipsRunning) return;
    nodeStates[index] = 'safe';
    nodeTypes[index] = null;
    nodeClicks[index] = 0;
    ipsLives--;
    ipsCombo = 0; // Reset combo on breach
    const node = document.getElementById(`node-${index}`);
    if (node) {
        node.className = `${NODE_BASE_CLASS} bg-red-950 border border-red-900`;
        node.innerHTML = '💥';
        setTimeout(() => {
            if (nodeStates[index] === 'safe') {
                node.className = NODE_SAFE_CLASS;
                node.innerHTML = '💻';
            }
        }, 500);
    }
    updateIpsStatus();
    if (ipsLives <= 0) endIpsGame(false);
}

function patchNode(index) {
    if (!ipsRunning || nodeStates[index] !== 'attacked') return;
    const type = nodeTypes[index];
    if (!type) return;

    if (type === 'ransomware') {
        nodeClicks[index]++;
        if (nodeClicks[index] < 2) {
            // Visual feedback — first click
            const node = document.getElementById(`node-${index}`);
            if (node) node.style.opacity = '0.6';
            setTimeout(() => { if (node) node.style.opacity = '1'; }, 150);
            return; // Need one more click
        }
    }

    // Patch successful
    nodeStates[index] = 'safe';
    nodeTypes[index] = null;
    nodeClicks[index] = 0;
    ipsCombo++;
    const pts = Math.max(1, ipsCombo); // Combo bonus
    ipsScore += pts;
    ipsLevelScore++;

    const node = document.getElementById(`node-${index}`);
    if (node) {
        node.className = `${NODE_BASE_CLASS} bg-green-900 border-2 border-green-500`;
        node.innerHTML = ipsCombo >= 3 ? `🔥` : '✅';
        setTimeout(() => {
            if (nodeStates[index] === 'safe') {
                node.className = NODE_SAFE_CLASS;
                node.innerHTML = '💻';
            }
        }, 500);
    }

    // Level up check
    if (ipsLevelScore >= LEVELS[ipsLevel].winScore) {
        ipsLevel++;
        ipsLevelScore = 0;
        if (ipsLevel >= LEVELS.length) {
            endIpsGame(true);
            return;
        }
        // Level up flash
        updateGameStatus('ips-status', `⚡ ${LEVELS[ipsLevel].label} — Escalating...`, 'text-yellow-400 font-bold');
        clearInterval(ipsInterval);
        setTimeout(() => {
            if (ipsRunning) { scheduleAttacks(); updateIpsStatus(); }
        }, 1200);
        return;
    }

    updateIpsStatus();
}

function updateIpsStatus() {
    const cfg = LEVELS[Math.min(ipsLevel, LEVELS.length - 1)];
    const lives = '❤️'.repeat(ipsLives) + '🖤'.repeat(3 - ipsLives);
    const combo = ipsCombo >= 3 ? ` 🔥×${ipsCombo}` : '';
    updateGameStatus('ips-status', `${lives}  ${cfg.label}  pts:${ipsScore}${combo}`, 'text-slate-300');
}

function endIpsGame(won) {
    ipsRunning = false;
    clearInterval(ipsInterval);
    resetAllNodes();
    if (won) {
        updateGameStatus('ips-status', `🏆 NETWORK SECURE — All 3 levels cleared! pts: ${ipsScore}`, 'text-green-400 font-bold');
    } else {
        updateGameStatus('ips-status', `🔴 BREACHED at ${LEVELS[Math.min(ipsLevel, LEVELS.length - 1)].label} — pts: ${ipsScore}`, 'text-rose-500 font-bold');
    }
}

// Add enter key support
document.addEventListener('DOMContentLoaded', () => {
    const portInput = document.getElementById('port-guess');
    if (portInput) {
        portInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                checkPortGuess();
            }
        });
        initPortGame(false); // Do not autofocus on page load
    }
});
