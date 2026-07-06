#!/usr/bin/env python3
import os
import json
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = 5001
DB_FILE = os.path.join(os.path.dirname(__file__), 'skills.json')
HTML_FILE = os.path.join(os.path.dirname(__file__), 'about.html')

def load_skills():
    if not os.path.exists(DB_FILE):
        return []
    try:
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading skills.json: {e}")
        return []

def save_skills(skills):
    try:
        with open(DB_FILE, 'w', encoding='utf-8') as f:
            json.dump(skills, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving skills.json: {e}")
        return False

def generate_skill_html(skill, index):
    category = skill.get('category', '')
    color = skill.get('color', 'cyan-400')
    items = skill.get('items', [])
    
    delay = f' style="transition-delay:0.{index}s"' if index > 0 else ''
    
    items_html = ""
    for item in items:
        if item.strip():
            items_html += f"""                            <li class="flex items-center gap-2"><span
                                    class="w-1.5 h-1.5 rounded-full bg-{color} shrink-0"></span>{item.strip()}</li>\n"""
            
    return f"""                    <div class="cyber-card p-5 reveal-on-scroll"{delay}>
                        <h3 class="text-sm font-bold text-{color} mb-4 font-mono">{category}</h3>
                        <ul class="space-y-2 font-mono text-sm text-slate-300">
{items_html}                        </ul>
                    </div>"""

def update_about_html_file(skills):
    if not os.path.exists(HTML_FILE):
        print(f"Error: about.html does not exist at {HTML_FILE}")
        return False
        
    try:
        with open(HTML_FILE, 'r', encoding='utf-8') as f:
            content = f.read()

        skills_html = "\n".join(generate_skill_html(s, i) for i, s in enumerate(skills))

        start_tag = "<!-- SKILLS_START -->"
        end_tag = "<!-- SKILLS_END -->"
        if start_tag in content and end_tag in content:
            before, rest = content.split(start_tag, 1)
            middle, after = rest.split(end_tag, 1)
            content = before + start_tag + "\n" + skills_html + "\n" + end_tag + after
        else:
            print("Warning: Skills placeholders not found in about.html")
            return False

        with open(HTML_FILE, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"Error updating about.html: {e}")
        return False

class SkillManagerHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            
            skills = load_skills()
            skills_json_str = json.dumps(skills)
            
            dashboard_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cyber Skill Manager</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@300;400;500;700&family=Outfit:wght@300;400;600;800&display=swap" rel="stylesheet">
    <style>
        body {{
            font-family: 'Outfit', sans-serif;
            background-color: #020408;
            background-image: radial-gradient(circle at 50% 0%, rgba(34, 211, 238, 0.05), transparent 60%);
        }}
        .font-mono {{
            font-family: 'Fira Code', monospace;
        }}
        .cyber-card {{
            background: rgba(3, 7, 18, 0.6);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(34, 211, 238, 0.15);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        }}
        .cyber-card:hover {{
            border-color: rgba(34, 211, 238, 0.3);
        }}
        .glow-btn {{
            box-shadow: 0 0 15px rgba(34, 211, 238, 0.2);
            transition: all 0.3s ease;
        }}
        .glow-btn:hover {{
            box-shadow: 0 0 25px rgba(34, 211, 238, 0.45);
        }}
    </style>
</head>
<body class="text-slate-200 min-h-screen p-4 md:p-8">
    <div class="max-w-5xl mx-auto">
        <header class="flex justify-between items-center mb-8 border-b border-cyan-500/10 pb-6">
            <div>
                <h1 class="text-3xl font-extrabold tracking-tight text-white flex items-center gap-2">
                    <span class="text-cyan-400">⚙️</span> Skill Manager
                </h1>
                <p class="text-slate-400 font-light mt-1">Directly modify your portfolio skills section.</p>
            </div>
            <div class="text-right">
                <span class="text-xs font-mono text-cyan-400/80 bg-cyan-500/5 px-3 py-1.5 rounded-lg border border-cyan-500/15">
                    localhost:{PORT}
                </span>
            </div>
        </header>

        <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">
            <div class="lg:col-span-7">
                <div class="cyber-card rounded-2xl p-6 md:p-8">
                    <div class="flex justify-between items-center mb-6">
                        <h2 id="form-title" class="text-xl font-bold text-white flex items-center gap-2">
                            <span>✏️</span> Create New Skill Category
                        </h2>
                        <button id="btn-cancel-edit" onclick="resetForm()" class="hidden text-xs text-rose-400 hover:text-rose-300 font-mono">
                            [ Cancel Edit ]
                        </button>
                    </div>

                    <form id="skill-form" onsubmit="saveSkill(event)" class="space-y-5">
                        <input type="hidden" id="skill-id">
                        
                        <div>
                            <label class="block text-xs uppercase tracking-wider text-slate-400 font-mono mb-2">Category Name</label>
                            <input type="text" id="skill-category" required placeholder="e.g. Network analysis"
                                class="w-full bg-slate-950/80 border border-slate-800 rounded-lg px-4 py-2.5 text-white placeholder-slate-600 focus:outline-none focus:border-cyan-500/50">
                        </div>

                        <div>
                            <label class="block text-xs uppercase tracking-wider text-slate-400 font-mono mb-2">Theme Color</label>
                            <select id="skill-color" required
                                class="w-full bg-slate-950/80 border border-slate-800 rounded-lg px-4 py-2.5 text-white focus:outline-none focus:border-cyan-500/50">
                                <option value="emerald-400" class="text-emerald-400">Emerald</option>
                                <option value="cyan-400" class="text-cyan-400">Cyan</option>
                                <option value="violet-400" class="text-violet-400">Violet</option>
                                <option value="pink-400" class="text-pink-400">Pink</option>
                                <option value="rose-400" class="text-rose-400">Rose</option>
                                <option value="amber-400" class="text-amber-400">Amber</option>
                            </select>
                        </div>

                        <div>
                            <div class="flex justify-between items-center mb-2">
                                <label class="block text-xs uppercase tracking-wider text-slate-400 font-mono">Skill Points</label>
                                <button type="button" onclick="addSkillItemField()" class="text-xs text-cyan-400 hover:text-cyan-300 font-mono">+ Add Point</button>
                            </div>
                            <div id="items-container" class="space-y-3">
                            </div>
                        </div>

                        <div class="pt-4">
                            <button type="submit" id="btn-submit"
                                class="w-full bg-cyan-600 hover:bg-cyan-500 text-white font-semibold py-3 px-6 rounded-lg transition-colors glow-btn">
                                Save Skill Category
                            </button>
                        </div>
                    </form>
                </div>
            </div>

            <div class="lg:col-span-5 flex flex-col gap-6">
                <div class="cyber-card rounded-2xl p-6 md:p-8 flex-1">
                    <h2 class="text-xl font-bold text-white mb-6 flex items-center gap-2">
                        <span>📚</span> Existing Categories
                    </h2>
                    <div id="skills-list" class="space-y-4 max-h-[600px] overflow-y-auto pr-2">
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div id="toast" class="fixed bottom-4 right-4 bg-slate-900 border border-cyan-500/30 text-cyan-400 px-5 py-3 rounded-lg shadow-2xl transition-all opacity-0 translate-y-2 pointer-events-none z-50 font-mono text-sm">
        Successfully Saved!
    </div>

    <script>
        const initialSkills = {skills_json_str};
        let currentSkills = [...initialSkills];

        function showToast(msg, isError = false) {{
            const toast = document.getElementById('toast');
            toast.textContent = msg;
            toast.className = isError 
                ? "fixed bottom-4 right-4 bg-slate-900 border border-rose-500/30 text-rose-400 px-5 py-3 rounded-lg shadow-2xl transition-all opacity-100 translate-y-0 z-50 font-mono text-sm"
                : "fixed bottom-4 right-4 bg-slate-900 border border-cyan-500/30 text-cyan-400 px-5 py-3 rounded-lg shadow-2xl transition-all opacity-100 translate-y-0 z-50 font-mono text-sm";
            
            setTimeout(() => {{
                toast.classList.remove('opacity-100', 'translate-y-0');
                toast.classList.add('opacity-0', 'translate-y-2');
            }}, 3000);
        }}

        function addSkillItemField(content = '') {{
            const container = document.getElementById('items-container');
            
            const field = document.createElement('div');
            field.className = 'flex gap-2 items-center';
            field.innerHTML = `
                <input type="text" required placeholder="Skill name..." value="${{content}}"
                    class="flex-1 bg-slate-950/80 border border-slate-800 rounded-lg px-3 py-2 text-sm text-slate-300 focus:outline-none focus:border-cyan-500/50">
                <button type="button" onclick="this.parentElement.remove();" class="text-rose-400 hover:text-rose-300 font-mono text-xl leading-none">&times;</button>
            `;
            container.appendChild(field);
        }}

        function resetForm() {{
            document.getElementById('skill-form').reset();
            document.getElementById('skill-id').value = '';
            document.getElementById('items-container').innerHTML = '';
            document.getElementById('form-title').innerHTML = '<span>✏️</span> Create New Skill Category';
            document.getElementById('btn-cancel-edit').classList.add('hidden');
            document.getElementById('btn-submit').textContent = 'Save Skill Category';
            addSkillItemField();
        }}

        function editSkill(id) {{
            const skill = currentSkills.find(s => s.id === id);
            if (!skill) return;
            
            document.getElementById('skill-id').value = skill.id;
            document.getElementById('skill-category').value = skill.category;
            document.getElementById('skill-color').value = skill.color;
            
            const container = document.getElementById('items-container');
            container.innerHTML = '';
            skill.items.forEach(p => addSkillItemField(p));
            if (skill.items.length === 0) {{
                addSkillItemField();
            }}

            document.getElementById('form-title').innerHTML = '<span>✏️</span> Edit Skill Category';
            document.getElementById('btn-cancel-edit').classList.remove('hidden');
            document.getElementById('btn-submit').textContent = 'Update Skill Category';
            window.scrollTo({{ top: 0, behavior: 'smooth' }});
        }}

        function renderSkillsList() {{
            const list = document.getElementById('skills-list');
            list.innerHTML = '';
            
            if (currentSkills.length === 0) {{
                list.innerHTML = '<div class="text-center py-8 text-slate-500 font-mono">[ No Skills Found ]</div>';
                return;
            }}
            
            currentSkills.forEach(skill => {{
                const item = document.createElement('div');
                item.className = `p-4 border rounded-xl bg-slate-900/30 flex justify-between items-start gap-4 hover:bg-slate-900/50 transition-all border-cyan-500/10`;
                item.innerHTML = `
                    <div class="space-y-1.5 flex-1 min-w-0">
                        <h3 class="text-base font-bold text-${{skill.color}} truncate">${{skill.category}}</h3>
                        <p class="text-xs text-slate-400 line-clamp-2 leading-relaxed">
                            ${{skill.items.join(', ')}}
                        </p>
                    </div>
                    <div class="flex flex-col gap-2 flex-shrink-0 font-mono text-xs">
                        <button onclick="editSkill('${{skill.id}}')" class="text-cyan-400 hover:text-cyan-300 text-right">[ Edit ]</button>
                        <button onclick="deleteSkill('${{skill.id}}')" class="text-rose-400 hover:text-rose-300 text-right">[ Delete ]</button>
                    </div>
                `;
                list.appendChild(item);
            }});
        }}

        function saveSkill(event) {{
            event.preventDefault();
            
            const id = document.getElementById('skill-id').value;
            const category = document.getElementById('skill-category').value;
            const color = document.getElementById('skill-color').value;
            
            const items = [];
            const inputs = document.getElementById('items-container').querySelectorAll('input');
            inputs.forEach(inp => {{
                if (inp.value.trim()) {{
                    items.push(inp.value.trim());
                }}
            }});

            const payload = {{
                id: id || 'skill_' + Date.now(),
                category,
                color,
                items
            }};

            fetch('/api/save', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify(payload)
            }})
            .then(res => res.json())
            .then(data => {{
                if (data.success) {{
                    currentSkills = data.skills;
                    renderSkillsList();
                    resetForm();
                    showToast(id ? 'Skill updated successfully!' : 'Skill created successfully!');
                }} else {{
                    showToast('Error saving: ' + data.error, true);
                }}
            }})
            .catch(err => {{
                showToast('Failed to save', true);
            }});
        }}

        function deleteSkill(id) {{
            if (!confirm('Are you sure you want to delete this skill category?')) return;
            
            fetch('/api/delete', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify({{ id }})
            }})
            .then(res => res.json())
            .then(data => {{
                if (data.success) {{
                    currentSkills = data.skills;
                    renderSkillsList();
                    resetForm();
                    showToast('Skill deleted successfully!');
                }} else {{
                    showToast('Error deleting: ' + data.error, true);
                }}
            }})
            .catch(err => {{
                showToast('Failed to delete', true);
            }});
        }}

        // Init
        addSkillItemField();
        renderSkillsList();
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

        skills = load_skills()
        
        if self.path == '/api/save':
            skill_id = req_data.get('id')
            existing_index = next((i for i, b in enumerate(skills) if b.get('id') == skill_id), -1)
            
            if existing_index != -1:
                skills[existing_index] = req_data
            else:
                skills.append(req_data)
                
            if save_skills(skills) and update_about_html_file(skills):
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"success": True, "skills": skills}).encode('utf-8'))
            else:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": "Failed to update filesystem"}).encode('utf-8'))
                
        elif self.path == '/api/delete':
            skill_id = req_data.get('id')
            skills = [s for s in skills if s.get('id') != skill_id]
            
            if save_skills(skills) and update_about_html_file(skills):
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"success": True, "skills": skills}).encode('utf-8'))
            else:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": "Failed to update filesystem"}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

def run(server_class=HTTPServer, handler_class=SkillManagerHandler):
    server_address = ('', PORT)
    httpd = server_class(server_address, handler_class)
    print(f"Cyber Skill Manager server running on http://localhost:{PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\\nShutting down server.")
        httpd.server_close()

if __name__ == '__main__':
    run()
