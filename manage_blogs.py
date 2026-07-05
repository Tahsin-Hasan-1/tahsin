#!/usr/bin/env python3
import os
import json
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = 5000
DB_FILE = os.path.join(os.path.dirname(__file__), 'blogs.json')
HTML_FILE = os.path.join(os.path.dirname(__file__), 'blog.html')

def load_blogs():
    if not os.path.exists(DB_FILE):
        return []
    try:
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading blogs.json: {e}")
        return []

def save_blogs(blogs):
    try:
        with open(DB_FILE, 'w', encoding='utf-8') as f:
            json.dump(blogs, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving blogs.json: {e}")
        return False

def generate_blog_html(blog):
    # Determine the styling based on category
    category = blog.get('category', 'binary')
    title = blog.get('title', '')
    date = blog.get('date', '')
    bold_lead = blog.get('bold_lead', '')
    preview_content = blog.get('preview_content', '')
    blog_id = blog.get('id', '')
    
    # Format paragraph tags
    paragraphs_html = ""
    for p in blog.get('body_paragraphs', []):
        if p.strip():
            paragraphs_html += f"                            <p>{p.strip()}</p>\n"
            
    if category == 'binary':
        return f"""                <article class="cyber-card reveal-on-scroll" style="border-color:rgba(255,65,65,0.15)">
                    <!-- Header always visible -->
                    <div class="p-7 md:p-8">
                        <div class="flex flex-col sm:flex-row sm:justify-between sm:items-start gap-3 mb-5">
                            <div>
                                <span class="text-xs font-mono uppercase tracking-wider text-rose-400">/Binary Realms</span>
                                <h2 class="text-xl md:text-2xl font-bold text-slate-100 mt-1">{title}</h2>
                            </div>
                            <span class="text-xs font-mono px-2.5 py-1 rounded-lg whitespace-nowrap self-start text-rose-400"
                                style="border:1px solid rgba(255,65,65,0.2);background:rgba(255,65,65,0.05)">{date}</span>
                        </div>

                        <!-- Preview text always shown -->
                        <p class="text-slate-400 font-light leading-relaxed text-sm md:text-base">
                            <strong class="text-slate-300">{bold_lead}</strong>
                            {preview_content}
                        </p>

                        <!-- Expand button -->
                        <button class="read-more-btn mt-4 inline-flex items-center gap-1.5 text-sm font-bold transition-colors duration-200 text-rose-400"
                            onclick="toggleBlog(this, '{blog_id}-body')">
                            Read Full Article <span class="arrow text-xs">▼</span>
                        </button>
                    </div>

                    <!-- Expanded body -->
                    <div id="{blog_id}-body" class="blog-body">
                        <div class="px-7 md:px-8 pb-8 pt-2 border-t space-y-4 text-slate-400 font-light leading-relaxed text-sm md:text-base"
                            style="border-color:rgba(255,65,65,0.1)">
{paragraphs_html}
                            <!-- Read Less at BOTTOM -->
                            <button class="read-less-btn mt-4 inline-flex items-center gap-1.5 text-sm font-bold transition-colors duration-200"
                                style="color:var(--green-soft)"
                                onclick="collapseBlog('{blog_id}-body')">
                                Read Less <span class="text-xs">▲</span>
                            </button>
                        </div>
                    </div>
                </article>"""
    else: # vantage
        return f"""                <article class="cyber-card reveal-on-scroll" style="border-color:rgba(0,255,65,0.15)">
                    <!-- Header always visible -->
                    <div class="p-7 md:p-8">
                        <div class="flex flex-col sm:flex-row sm:justify-between sm:items-start gap-3 mb-5">
                            <div>
                                <span class="text-xs font-mono uppercase tracking-wider" style="color:var(--green-soft)">/The Vantage</span>
                                <h2 class="text-xl md:text-2xl font-bold text-slate-100 mt-1">{title}</h2>
                            </div>
                            <span class="text-xs font-mono px-2.5 py-1 rounded-lg whitespace-nowrap self-start"
                                style="color:var(--green-soft);border:1px solid rgba(0,255,65,0.2);background:rgba(0,255,65,0.05)">{date}</span>
                        </div>

                        <!-- Preview text always shown -->
                        <p class="text-slate-400 font-light leading-relaxed text-sm md:text-base">
                            <strong class="text-slate-300">{bold_lead}</strong>
                            {preview_content}
                        </p>

                        <!-- Expand button -->
                        <button class="read-more-btn mt-4 inline-flex items-center gap-1.5 text-sm font-bold transition-colors duration-200"
                            style="color:var(--green-soft)"
                            onclick="toggleBlog(this, '{blog_id}-body')">
                            Read Full Article <span class="arrow text-xs">▼</span>
                        </button>
                    </div>

                    <!-- Expanded body -->
                    <div id="{blog_id}-body" class="blog-body">
                        <div class="px-7 md:px-8 pb-8 pt-2 border-t space-y-4 text-slate-400 font-light leading-relaxed text-sm md:text-base"
                            style="border-color:rgba(0,255,65,0.1)">
{paragraphs_html}
                            <!-- Read Less at BOTTOM -->
                            <button class="read-less-btn mt-4 inline-flex items-center gap-1.5 text-sm font-bold transition-colors duration-200"
                                style="color:var(--green-soft)"
                                onclick="collapseBlog('{blog_id}-body')">
                                Read Less <span class="text-xs">▲</span>
                            </button>
                        </div>
                    </div>
                </article>"""

def update_blog_html_file(blogs):
    if not os.path.exists(HTML_FILE):
        print(f"Error: blog.html does not exist at {HTML_FILE}")
        return False
        
    try:
        with open(HTML_FILE, 'r', encoding='utf-8') as f:
            content = f.read()

        # Build Binary Realms posts HTML
        binary_blogs = [b for b in blogs if b.get('category') == 'binary']
        binary_html = "\n\n".join(generate_blog_html(b) for b in binary_blogs)

        # Build Vantage posts HTML
        vantage_blogs = [b for b in blogs if b.get('category') == 'vantage']
        vantage_html = "\n\n".join(generate_blog_html(b) for b in vantage_blogs)

        # Replace Binary Section
        start_tag_bin = "<!-- BLOGS_BINARY_START -->"
        end_tag_bin = "<!-- BLOGS_BINARY_END -->"
        if start_tag_bin in content and end_tag_bin in content:
            before, rest = content.split(start_tag_bin, 1)
            middle, after = rest.split(end_tag_bin, 1)
            content = before + start_tag_bin + "\n" + binary_html + "\n                " + end_tag_bin + after
        else:
            print("Warning: Binary blog placeholders not found in blog.html")

        # Replace Vantage Section
        start_tag_van = "<!-- BLOGS_VANTAGE_START -->"
        end_tag_van = "<!-- BLOGS_VANTAGE_END -->"
        if start_tag_van in content and end_tag_van in content:
            before, rest = content.split(start_tag_van, 1)
            middle, after = rest.split(end_tag_van, 1)
            content = before + start_tag_van + "\n" + vantage_html + "\n                " + end_tag_van + after
        else:
            print("Warning: Vantage blog placeholders not found in blog.html")

        with open(HTML_FILE, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"Error updating blog.html: {e}")
        return False

class BlogManagerHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Silence HTTP request logs in standard console to keep it clean
        pass

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            
            # Load current blogs to pass to UI
            blogs = load_blogs()
            blogs_json_str = json.dumps(blogs)
            
            dashboard_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cyber Blog Manager</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@300;400;500;700&family=Outfit:wght@300;400;600;800&display=swap" rel="stylesheet">
    <style>
        body {{
            font-family: 'Outfit', sans-serif;
            background-color: #020408;
            background-image: radial-gradient(circle at 50% 0%, rgba(34, 197, 94, 0.05), transparent 60%);
        }}
        .font-mono {{
            font-family: 'Fira Code', monospace;
        }}
        .cyber-card {{
            background: rgba(3, 7, 18, 0.6);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(34, 197, 94, 0.15);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        }}
        .cyber-card:hover {{
            border-color: rgba(34, 197, 94, 0.3);
        }}
        .glow-btn {{
            box-shadow: 0 0 15px rgba(34, 197, 94, 0.2);
            transition: all 0.3s ease;
        }}
        .glow-btn:hover {{
            box-shadow: 0 0 25px rgba(34, 197, 94, 0.45);
        }}
    </style>
</head>
<body class="text-slate-200 min-h-screen p-4 md:p-8">
    <div class="max-w-5xl mx-auto">
        <!-- Header -->
        <header class="flex justify-between items-center mb-8 border-b border-green-500/10 pb-6">
            <div>
                <h1 class="text-3xl font-extrabold tracking-tight text-white flex items-center gap-2">
                    <span class="text-green-400">⚡</span> Blog Manager
                </h1>
                <p class="text-slate-400 font-light mt-1">Directly modify your portfolio blog sections.</p>
            </div>
            <div class="text-right">
                <span class="text-xs font-mono text-green-400/80 bg-green-500/5 px-3 py-1.5 rounded-lg border border-green-500/15">
                    localhost:{PORT}
                </span>
            </div>
        </header>

        <!-- Main Workspace -->
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">
            <!-- Left Panel: Blog Post Editor Form -->
            <div class="lg:col-span-7">
                <div class="cyber-card rounded-2xl p-6 md:p-8">
                    <div class="flex justify-between items-center mb-6">
                        <h2 id="form-title" class="text-xl font-bold text-white flex items-center gap-2">
                            <span>✏️</span> Create New Blog Post
                        </h2>
                        <button id="btn-cancel-edit" onclick="resetForm()" class="hidden text-xs text-rose-400 hover:text-rose-300 font-mono">
                            [ Cancel Edit ]
                        </button>
                    </div>

                    <form id="blog-form" onsubmit="savePost(event)" class="space-y-5">
                        <input type="hidden" id="post-id">
                        
                        <div>
                            <label class="block text-xs uppercase tracking-wider text-slate-400 font-mono mb-2">Category Tab</label>
                            <div class="grid grid-cols-2 gap-4">
                                <label class="flex items-center justify-center p-3 rounded-lg border cursor-pointer transition-all border-slate-800 bg-slate-900/20 hover:border-slate-700" id="label-cat-binary">
                                    <input type="radio" name="category" value="binary" checked class="sr-only" onchange="updateCategorySelect('binary')">
                                    <span class="text-sm font-semibold text-rose-400 font-mono">⚡ Binary Realms</span>
                                </label>
                                <label class="flex items-center justify-center p-3 rounded-lg border cursor-pointer transition-all border-slate-800 bg-slate-900/20 hover:border-slate-700" id="label-cat-vantage">
                                    <input type="radio" name="category" value="vantage" class="sr-only" onchange="updateCategorySelect('vantage')">
                                    <span class="text-sm font-semibold text-green-400 font-mono">🌐 The Vantage</span>
                                </label>
                            </div>
                        </div>

                        <div class="grid grid-cols-1 md:grid-cols-12 gap-4">
                            <div class="md:col-span-8">
                                <label class="block text-xs uppercase tracking-wider text-slate-400 font-mono mb-2">Blog Title</label>
                                <input type="text" id="post-title" required placeholder="e.g. The Internet Thing"
                                    class="w-full bg-slate-950/80 border border-slate-800 rounded-lg px-4 py-2.5 text-white placeholder-slate-600 focus:outline-none focus:border-green-500/50">
                            </div>
                            <div class="md:col-span-4">
                                <label class="block text-xs uppercase tracking-wider text-slate-400 font-mono mb-2">Date</label>
                                <input type="text" id="post-date" required placeholder="e.g. Jan 15, 2026"
                                    class="w-full bg-slate-950/80 border border-slate-800 rounded-lg px-4 py-2.5 text-white placeholder-slate-600 focus:outline-none focus:border-green-500/50">
                            </div>
                        </div>

                        <div>
                            <label class="block text-xs uppercase tracking-wider text-slate-400 font-mono mb-2">Bold Lead Text / Accent Preview</label>
                            <input type="text" id="post-bold-lead" required placeholder="e.g. Research Challenges:"
                                class="w-full bg-slate-950/80 border border-slate-800 rounded-lg px-4 py-2.5 text-white placeholder-slate-600 focus:outline-none focus:border-green-500/50">
                        </div>

                        <div>
                            <label class="block text-xs uppercase tracking-wider text-slate-400 font-mono mb-2">Preview Description Content</label>
                            <textarea id="post-preview-content" required rows="3" placeholder="This portion is always visible in the blog card..."
                                class="w-full bg-slate-950/80 border border-slate-800 rounded-lg px-4 py-2.5 text-white placeholder-slate-600 focus:outline-none focus:border-green-500/50 resize-none"></textarea>
                        </div>

                        <div>
                            <div class="flex justify-between items-center mb-2">
                                <label class="block text-xs uppercase tracking-wider text-slate-400 font-mono">Expanded Content Paragraphs</label>
                                <button type="button" onclick="addParagraphField()" class="text-xs text-green-400 hover:text-green-300 font-mono">+ Add Paragraph</button>
                            </div>
                            <div id="paragraphs-container" class="space-y-3">
                                <!-- Paragraph inputs inserted here -->
                            </div>
                        </div>

                        <div class="pt-4">
                            <button type="submit" id="btn-submit"
                                class="w-full bg-green-600 hover:bg-green-500 text-white font-semibold py-3 px-6 rounded-lg transition-colors glow-btn">
                                Save Blog Post
                            </button>
                        </div>
                    </form>
                </div>
            </div>

            <!-- Right Panel: Existing Posts List -->
            <div class="lg:col-span-5 flex flex-col gap-6">
                <div class="cyber-card rounded-2xl p-6 md:p-8 flex-1">
                    <h2 class="text-xl font-bold text-white mb-6 flex items-center gap-2">
                        <span>📚</span> Existing Blog Posts
                    </h2>

                    <div id="posts-list" class="space-y-4 max-h-[600px] overflow-y-auto pr-2">
                        <!-- Loaded via JS -->
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Notification -->
    <div id="toast" class="fixed bottom-4 right-4 bg-slate-900 border border-green-500/30 text-green-400 px-5 py-3 rounded-lg shadow-2xl transition-all opacity-0 translate-y-2 pointer-events-none z-50 font-mono text-sm">
        Successfully Saved!
    </div>

    <script>
        const initialBlogs = {blogs_json_str};
        let currentBlogs = [...initialBlogs];

        function showToast(msg, isError = false) {{
            const toast = document.getElementById('toast');
            toast.textContent = msg;
            toast.className = isError 
                ? "fixed bottom-4 right-4 bg-slate-900 border border-rose-500/30 text-rose-400 px-5 py-3 rounded-lg shadow-2xl transition-all opacity-100 translate-y-0 z-50 font-mono text-sm"
                : "fixed bottom-4 right-4 bg-slate-900 border border-green-500/30 text-green-400 px-5 py-3 rounded-lg shadow-2xl transition-all opacity-100 translate-y-0 z-50 font-mono text-sm";
            
            setTimeout(() => {{
                toast.classList.remove('opacity-100', 'translate-y-0');
                toast.classList.add('opacity-0', 'translate-y-2');
            }}, 3000);
        }}

        function updateCategorySelect(cat) {{
            const labelBin = document.getElementById('label-cat-binary');
            const labelVan = document.getElementById('label-cat-vantage');
            
            if (cat === 'binary') {{
                labelBin.classList.add('border-rose-500/50', 'bg-rose-500/5');
                labelBin.classList.remove('border-slate-800', 'bg-slate-900/20');
                labelVan.classList.add('border-slate-800', 'bg-slate-900/20');
                labelVan.classList.remove('border-green-500/50', 'bg-green-500/5');
            }} else {{
                labelVan.classList.add('border-green-500/50', 'bg-green-500/5');
                labelVan.classList.remove('border-slate-800', 'bg-slate-900/20');
                labelBin.classList.add('border-slate-800', 'bg-slate-900/20');
                labelBin.classList.remove('border-rose-500/50', 'bg-rose-500/5');
            }}
        }}

        function addParagraphField(content = '') {{
            const container = document.getElementById('paragraphs-container');
            const idx = container.children.length + 1;
            
            const field = document.createElement('div');
            field.className = 'flex gap-2 items-start';
            field.innerHTML = `
                <span class="text-xs text-slate-500 font-mono mt-3">#${{idx}}</span>
                <textarea rows="3" required placeholder="Paragraph content... Supports HTML tags like &lt;strong&gt;"
                    class="flex-1 bg-slate-950/80 border border-slate-800 rounded-lg px-3 py-2 text-sm text-slate-300 focus:outline-none focus:border-green-500/50 resize-none">${{content}}</textarea>
                <button type="button" onclick="this.parentElement.remove(); reindexParagraphs();" class="text-rose-400 hover:text-rose-300 font-mono text-sm mt-2">&times;</button>
            `;
            container.appendChild(field);
        }}

        function reindexParagraphs() {{
            const container = document.getElementById('paragraphs-container');
            Array.from(container.children).forEach((child, i) => {{
                child.querySelector('span').textContent = '#' + (i + 1);
            }});
        }}

        function resetForm() {{
            document.getElementById('blog-form').reset();
            document.getElementById('post-id').value = '';
            document.getElementById('paragraphs-container').innerHTML = '';
            document.getElementById('form-title').innerHTML = '<span>✏️</span> Create New Blog Post';
            document.getElementById('btn-cancel-edit').classList.add('hidden');
            document.getElementById('btn-submit').textContent = 'Save Blog Post';
            updateCategorySelect('binary');
            addParagraphField();
        }}

        function editPost(id) {{
            const post = currentBlogs.find(b => b.id === id);
            if (!post) return;
            
            document.getElementById('post-id').value = post.id;
            document.getElementById('post-title').value = post.title;
            document.getElementById('post-date').value = post.date;
            document.getElementById('post-bold-lead').value = post.bold_lead;
            document.getElementById('post-preview-content').value = post.preview_content;
            
            // Set radio buttons
            const radios = document.getElementsByName('category');
            for (let r of radios) {{
                if (r.value === post.category) {{
                    r.checked = true;
                    updateCategorySelect(post.category);
                }}
            }}

            // Add paragraphs
            const container = document.getElementById('paragraphs-container');
            container.innerHTML = '';
            post.body_paragraphs.forEach(p => addParagraphField(p));
            if (post.body_paragraphs.length === 0) {{
                addParagraphField();
            }}

            document.getElementById('form-title').innerHTML = '<span>✏️</span> Edit Blog Post';
            document.getElementById('btn-cancel-edit').classList.remove('hidden');
            document.getElementById('btn-submit').textContent = 'Update Blog Post';
            window.scrollTo({{ top: 0, behavior: 'smooth' }});
        }}

        function renderPostsList() {{
            const list = document.getElementById('posts-list');
            list.innerHTML = '';
            
            if (currentBlogs.length === 0) {{
                list.innerHTML = '<div class="text-center py-8 text-slate-500 font-mono">[ No Blog Posts Found ]</div>';
                return;
            }}
            
            currentBlogs.forEach(post => {{
                const isBinary = post.category === 'binary';
                const tagColor = isBinary ? 'text-rose-400 border-rose-500/20 bg-rose-500/5' : 'text-green-400 border-green-500/20 bg-green-500/5';
                const borderGlow = isBinary ? 'border-rose-500/10' : 'border-green-500/10';
                
                const item = document.createElement('div');
                item.className = `p-4 border rounded-xl bg-slate-900/30 flex justify-between items-start gap-4 hover:bg-slate-900/50 transition-all ${{borderGlow}}`;
                item.innerHTML = `
                    <div class="space-y-1.5 flex-1 min-w-0">
                        <div class="flex items-center gap-2">
                            <span class="text-[10px] font-mono px-2 py-0.5 rounded border ${{tagColor}}">
                                ${{isBinary ? '/Binary Realms' : '/The Vantage'}}
                            </span>
                            <span class="text-xs text-slate-500 font-mono">${{post.date}}</span>
                        </div>
                        <h3 class="text-base font-bold text-white truncate">${{post.title}}</h3>
                        <p class="text-xs text-slate-400 line-clamp-2 leading-relaxed">
                            <strong>${{post.bold_lead}}</strong> ${{post.preview_content}}
                        </p>
                    </div>
                    <div class="flex flex-col gap-2 flex-shrink-0 font-mono text-xs">
                        <button onclick="editPost('${{post.id}}')" class="text-green-400 hover:text-green-300 text-right">[ Edit ]</button>
                        <button onclick="deletePost('${{post.id}}')" class="text-rose-400 hover:text-rose-300 text-right">[ Delete ]</button>
                    </div>
                `;
                list.appendChild(item);
            }});
        }}

        function savePost(event) {{
            event.preventDefault();
            
            const id = document.getElementById('post-id').value;
            const category = document.querySelector('input[name="category"]:checked').value;
            const title = document.getElementById('post-title').value;
            const date = document.getElementById('post-date').value;
            const bold_lead = document.getElementById('post-bold-lead').value;
            const preview_content = document.getElementById('post-preview-content').value;
            
            // Collect paragraphs
            const paragraphs = [];
            const textareas = document.getElementById('paragraphs-container').querySelectorAll('textarea');
            textareas.forEach(ta => {{
                if (ta.value.strip ? ta.value.strip() : ta.value.trim()) {{
                    paragraphs.push(ta.value.trim());
                }}
            }});

            const payload = {{
                id: id || 'blog_' + Date.now(),
                category,
                title,
                date,
                bold_lead,
                preview_content,
                body_paragraphs: paragraphs
            }};

            fetch('/api/save', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify(payload)
            }})
            .then(res => res.json())
            .then(data => {{
                if (data.success) {{
                    currentBlogs = data.blogs;
                    renderPostsList();
                    resetForm();
                    showToast(id ? 'Post updated successfully!' : 'Post created successfully!');
                }} else {{
                    showToast('Error saving: ' + data.error, true);
                }}
            }})
            .catch(err => {{
                showToast('Failed to save', true);
            }});
        }}

        function deletePost(id) {{
            if (!confirm('Are you sure you want to delete this blog post? This will permanently modify blog.html.')) return;
            
            fetch('/api/delete', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify({{ id }})
            }})
            .then(res => res.json())
            .then(data => {{
                if (data.success) {{
                    currentBlogs = data.blogs;
                    renderPostsList();
                    resetForm();
                    showToast('Post deleted successfully!');
                }} else {{
                    showToast('Error deleting: ' + data.error, true);
                }}
            }})
            .catch(err => {{
                showToast('Failed to delete', true);
            }});
        }}

        // Init
        updateCategorySelect('binary');
        addParagraphField();
        renderPostsList();
    </script>
</body>
</html>
"""
            self.wfile.write(dashboard_html.encode('utf-8'))
            
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            req_data = json.loads(post_data.decode('utf-8'))
        except Exception as e:
            self.send_response(400)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"success": False, "error": "Invalid JSON"}).encode('utf-8'))
            return

        blogs = load_blogs()
        
        if self.path == '/api/save':
            post_id = req_data.get('id')
            existing_index = next((i for i, b in enumerate(blogs) if b.get('id') == post_id), -1)
            
            if existing_index != -1:
                blogs[existing_index] = req_data
            else:
                blogs.append(req_data)
                
            if save_blogs(blogs) and update_blog_html_file(blogs):
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"success": True, "blogs": blogs}).encode('utf-8'))
            else:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": "Failed to update filesystem"}).encode('utf-8'))
                
        elif self.path == '/api/delete':
            post_id = req_data.get('id')
            blogs = [b for b in blogs if b.get('id') != post_id]
            
            if save_blogs(blogs) and update_blog_html_file(blogs):
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"success": True, "blogs": blogs}).encode('utf-8'))
            else:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": "Failed to update filesystem"}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

def run(server_class=HTTPServer, handler_class=BlogManagerHandler):
    server_address = ('', PORT)
    httpd = server_class(server_address, handler_class)
    print(f"Cyber Blog Manager server running on http://localhost:{PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server.")
        httpd.server_close()

if __name__ == '__main__':
    run()
