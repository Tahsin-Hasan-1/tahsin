# Md. Tahsin Hasan — Cybersecurity Portfolio

Welcome to the source repository for my personal Cybersecurity Portfolio website. This portfolio is designed as an interactive, immersive terminal and dashboard experience representing my work, projects, writing, and skills in security research, network systems, and digital forensics.

---

## 🚀 Key Features

### 1. Interactive Terminal Emulator
The homepage features a custom interactive Linux terminal replica (`tahsin@portfolio:~`).
- **Interactive Input**: Users can click the terminal container to focus and type commands directly.
- **Commands**: Built-in simulator commands such as `man t`, `help`, and other custom diagnostics.

### 2. Live Mini Security Games
Embedded on the home page are two responsive mini-games built with vanilla JavaScript:
- **Port Scanner**: A tactical scanning simulator where users guess the open port (1-1024) under a 5-attempt firewall threshold.
- **IPS Defender**: A fast-paced, grid-based intrusion prevention system simulator featuring 3 threat levels (DDoS, Ransomware, Worms) requiring multi-click patches and handling worm propagation.

### 3. Cyber blogging Platform
The portfolio includes a writing section categorized into two primary tracks:
- **`// Binary Realms`**: Deep-dive technical write-ups and security tutorials styled with a tactical red theme.
- **`// The Vantage`**: Thought leadership articles, general technology insights, and commentary styled in a green theme.

### 4. Manager Dashboard Backends (Python)
To manage updates without manual HTML manipulation, the project contains custom Python 3 HTTP servers:
- **`manage_blogs.py`**: Runs locally on `http://localhost:5000`. Manages blog posts in `blogs.json` and updates `blog.html`.
- **`manage_skills.py`**: Runs locally on `http://localhost:5001`. Manages skill categories in `skills.json` and updates `about.html`.
- Both provide a clean, TailwindCSS-powered dashboard UI to **Create, Edit, and Delete** content.
- Both automatically compile/sync into static HTML files using designated insertion comments.
  - `<!-- BLOGS_BINARY_START -->` / `<!-- BLOGS_BINARY_END -->`
  - `<!-- BLOGS_VANTAGE_START -->` / `<!-- BLOGS_VANTAGE_END -->`

### 5. Secure Contact Form Integration
Includes structured procedures to secure the Web3Forms `access_key` from scraper bots:
- **Method 1 (Proxy)**: A server-side `submit.php` script that intercepts form submissions locally and forwards them securely to the Web3Forms API endpoint, keeping the API key hidden from the frontend code.
- **Method 2 (Domain Restricting)**: Guidance on setting up Allowed Domains inside the Web3Forms Dashboard for static hosts (GitHub Pages, Vercel).

---

## 📁 File Structure

```text
├── index.html          # Homepage with Terminal, Bio, and Mini-Games
├── about.html          # Professional background, skills, and timeline
├── project.html        # Showcase of security tools and research projects
├── blog.html           # Technical & non-technical blogs page (statically compiled)
├── contact.html        # Secure contact form page
├── blogs.json          # Database file holding blog post records
├── skills.json         # Database file holding skill points and categories
├── manage_blogs.py     # Python local Blog Manager server & compiler
├── manage_skills.py    # Python local Skill Manager server & compiler
├── submit.php          # PHP backend proxy for Web3Forms submissions
├── CNAME               # Domain configuration mapping
├── assets/
│   ├── css/
│   │   └── style.css   # Main CSS stylesheet containing animations and glassmorphism UI rules
│   └── js/
│       └── main.js     # Client-side terminal emulator logic, games, and layout animations
└── media/              # Visual assets, SVG icons, and hero background images
```

---

## 🛠️ Getting Started

### Running the Local Management Servers
To add, edit, or delete content via the browser dashboard, start the corresponding Python utility server:
```bash
# For blogs (Port 5000)
python3 manage_blogs.py

# For skills (Port 5001)
python3 manage_skills.py
```
Open [http://localhost:5000](http://localhost:5000) or [http://localhost:5001](http://localhost:5001) in your browser.

### Running the Web Server
- **PHP Support (Recommended)**: Serve the project using a local stack like XAMPP or Apache to take advantage of `submit.php` proxying.
- **Static Hosting**: Serve files using any static file hosting tool (e.g., Live Server extension in VS Code, `python3 -m http.server 8000`, Vercel, or GitHub Pages).

---

## 🛡️ Web3Forms API Key Security

Refer to the details inside [submit.php](file:///opt/lampp/htdocs/my/port/submit.php) (or your Web3Forms developer console) to secure form submissions. The private access token is stored server-side to prevent harvesting.
