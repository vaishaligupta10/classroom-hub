from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
import os
import shutil
import json
import uuid
from typing import List, Dict

app = FastAPI()

UPLOAD_DIR = "uploads"
JSON_FILE = "database.json"
ADMIN_PASSWORD = "vaishali123"  # 🔑 Aapka Secret Password! (Ise aap badal sakti hain)

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

app.mount("/static-uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# --- 🧠 DATABASE FUNCTIONS ---
def load_data_from_file() -> List[Dict]:
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r") as file:
            try:
                return json.load(file)
            except:
                return []
    return [{"id": "demo-1", "title": "Welcome Demo Note", "category": "Notes", "image_path": "", "date": "May 21, 2026"}]

def save_data_to_file():
    with open(JSON_FILE, "w") as file:
        json.dump(class_materials, file, indent=4)

class_materials = load_data_from_file()

# --- 🌐 SECURED DASHBOARD ---
@app.get("/", response_class=HTMLResponse)
def build_classroom_portal():
    cards_html = ""
    
    for item in class_materials:
        item_id = item.get("id", "")
        category = item.get("category", "Notes")
        
        badge_color = "bg-indigo-500/10 text-indigo-400 border border-indigo-500/20"
        if category == "Classwork":
            badge_color = "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20"
        elif category == "Homework":
            badge_color = "bg-rose-500/10 text-rose-400 border border-rose-500/20"
            
        image_tag = ""
        if item.get("image_path"):
            image_tag = f"""
            <div class="mt-3 border border-slate-700/50 rounded-xl overflow-hidden bg-slate-900/40">
                <img src="{item['image_path']}" class="w-full h-auto max-h-52 object-cover" alt="Notes">
            </div>
            """
            view_btn = f'<a href="{item["image_path"]}" target="_blank" class="text-xs shrink-0 bg-slate-800 border border-slate-700 text-indigo-400 hover:bg-slate-700/50 px-3 py-1.5 rounded-lg font-medium transition">View</a>'
        else:
            view_btn = '<span class="text-xs text-slate-500 italic">No Image</span>'

        cards_html += f"""
        <div class="material-card bg-slate-900/60 backdrop-blur-md p-5 rounded-2xl border border-slate-800/80 shadow-xl flex flex-col justify-between space-y-3" data-category="{category}">
            <div class="flex justify-between items-start">
                <div class="truncate pr-2">
                    <span class="inline-block text-[10px] uppercase font-bold tracking-widest px-2.5 py-0.5 rounded-full {badge_color} mb-2">{category}</span>
                    <p class="text-sm font-bold text-slate-100 truncate tracking-wide">{item.get('title', 'Untitled')}</p>
                    <span class="text-[11px] text-slate-400 block mt-1 font-mono">{item.get('date', '')}</span>
                </div>
                <div class="flex items-center gap-2">
                    {view_btn}
                    <button onclick="secureDelete('{item_id}')" class="text-xs shrink-0 bg-rose-500/10 border border-rose-500/20 hover:bg-rose-500/20 text-rose-400 p-1.5 rounded-lg transition">🗑️</button>
                </div>
            </div>
            {image_tag}
        </div>
        """

    return f"""
    <html>
        <head>
            <title>Classroom Hub Panel</title>
            <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
            <script>
                function filterCategory(category) {{
                    const cards = document.querySelectorAll('.material-card');
                    const tabs = document.querySelectorAll('.tab-btn');
                    tabs.forEach(tab => {{
                        tab.classList.remove('bg-indigo-600', 'text-white');
                        tab.classList.add('text-slate-400', 'hover:bg-slate-800/50');
                    }});
                    event.target.classList.add('bg-indigo-600', 'text-white');
                    event.target.classList.remove('text-slate-400', 'hover:bg-slate-800/50');

                    cards.forEach(card => {{
                        if (category === 'All' || card.getAttribute('data-category') === category) {{
                            card.style.display = 'flex';
                        }} else {{
                            card.style.display = 'none';
                        }}
                    }});
                }}

                // 🔐 JavaScript Prompt for Deletion Password
                function secureDelete(itemId) {{
                    const password = prompt("Admin Authorization Required.\\nEnter Secret Password to Delete:");
                    if (password === null) return; // Cancelled
                    
                    // Create dynamic standard secure form post execution
                    const form = document.createElement('form');
                    form.method = 'POST';
                    form.action = '/delete-material/' + itemId;
                    
                    const passInput = document.createElement('input');
                    passInput.type = 'hidden';
                    passInput.name = 'password';
                    passInput.value = password;
                    
                    form.appendChild(passInput);
                    document.body.appendChild(form);
                    form.submit();
                }}
            </script>
        </head>
        <body class="bg-slate-950 font-sans text-slate-200 min-h-screen p-4 md:p-12 relative overflow-x-hidden">
            
            <div class="fixed bottom-6 right-6 z-0 pointer-events-none select-none opacity-15 font-black text-3xl md:text-5xl tracking-widest text-indigo-400 font-mono font-extrabold uppercase">
                Made by Vaishali
            </div>

            <div class="max-w-5xl mx-auto space-y-8 relative z-10">
                
                <div class="bg-gradient-to-r from-indigo-950 to-slate-900 text-indigo-300 px-5 py-3 rounded-xl font-medium text-xs tracking-wider border border-indigo-900/50 flex justify-between items-center shadow-lg">
                    <span>⚡ CORE ACADEMIC REPOSITORY ENGINE</span>
                    <span class="text-emerald-400 font-mono text-[10px] bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">🔒 PASSWORD ENFORCED</span>
                </div>
                
                <div class="bg-slate-900/40 border border-slate-800/80 p-6 rounded-2xl shadow-2xl space-y-4 backdrop-blur-lg">
                    <h3 class="text-xs font-extrabold uppercase tracking-widest text-indigo-400 flex items-center gap-2">
                        <span class="w-2 h-2 rounded-full bg-indigo-500"></span>
                        Secure Upload Terminal
                    </h3>
                    <form action="/upload-note" method="POST" enctype="multipart/form-data" class="grid grid-cols-1 sm:grid-cols-5 gap-4 items-end">
                        <div class="sm:col-span-2">
                            <label class="block text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-1.5">Document Title</label>
                            <input type="text" name="title" required placeholder="e.g. Matrix Lab Proof" class="w-full text-xs p-2.5 rounded-xl border border-slate-800 bg-slate-950 text-slate-100 placeholder:text-slate-600 focus:outline-none focus:border-indigo-500 transition">
                        </div>
                        <div>
                            <label class="block text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-1.5">Stream Tag</label>
                            <select name="category" class="w-full text-xs p-2.5 rounded-xl border border-slate-800 bg-slate-950 text-slate-100 focus:outline-none focus:border-indigo-500 transition">
                                <option value="Notes">Notes</option>
                                <option value="Classwork">Classwork</option>
                                <option value="Homework">Homework</option>
                            </select>
                        </div>
                        <div>
                            <label class="block text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-1.5">Timestamp</label>
                            <input type="text" name="date" required placeholder="21 May 2026" class="w-full text-xs p-2.5 rounded-xl border border-slate-800 bg-slate-950 text-slate-100 focus:outline-none focus:border-indigo-500 transition">
                        </div>
                        <div>
                            <label class="block text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-1.5">Capture / File</label>
                            <input type="file" name="file" required class="w-full text-xs text-slate-500 file:mr-3 file:py-1.5 file:px-3 file:rounded-xl file:border-0 file:text-[11px] file:font-bold file:bg-indigo-600 file:text-white hover:file:bg-indigo-700 cursor-pointer">
                        </div>
                        
                        <div class="sm:col-span-3">
                            <label class="block text-[10px] font-bold text-amber-400 uppercase tracking-wider mb-1.5">🔑 Admin Access Token (Password)</label>
                            <input type="password" name="password" required placeholder="Enter Secret Code to Upload" class="w-full text-xs p-2.5 rounded-xl border border-amber-500/30 bg-slate-950 text-slate-100 focus:outline-none focus:border-amber-500 transition">
                        </div>
                        
                        <div class="sm:col-span-2 flex justify-end">
                            <button type="submit" class="w-full bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold px-5 py-2.5 rounded-xl transition shadow-lg shadow-indigo-600/10">🚀 Authenticate & Broadcast</button>
                        </div>
                    </form>
                </div>

                <header class="border-b border-slate-800/80 pb-3 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
                    <div>
                        <h2 class="text-xs font-extrabold uppercase tracking-widest text-slate-400">Database Feed Stream</h2>
                    </div>
                    
                    <div class="flex gap-1.5 bg-slate-900/60 p-1 rounded-xl border border-slate-800 self-start">
                        <button onclick="filterCategory('All')" class="tab-btn px-4 py-1.5 text-xs font-semibold rounded-lg bg-indigo-600 text-white transition">All</button>
                        <button onclick="filterCategory('Notes')" class="tab-btn px-4 py-1.5 text-xs font-semibold rounded-lg text-slate-400 hover:bg-slate-800/50 transition">Notes</button>
                        <button onclick="filterCategory('Classwork')" class="tab-btn px-4 py-1.5 text-xs font-semibold rounded-lg text-slate-400 hover:bg-slate-800/50 transition">Classwork</button>
                        <button onclick="filterCategory('Homework')" class="tab-btn px-4 py-1.5 text-xs font-semibold rounded-lg text-slate-400 hover:bg-slate-800/50 transition">Homework</button>
                    </div>
                </header>

                <section>
                    <div id="cards-grid" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
                        {cards_html if cards_html else '<p class="text-xs italic text-slate-500">No active uploads present.</p>'}
                    </div>
                </section>
            </div>
        </body>
    </html>
    """

# --- 🚀 SECURE UPLOAD ROUTE WITH PASSWORD LOCK ---
@app.post("/upload-note")
def upload_note_with_image(
    title: str = Form(...), 
    category: str = Form(...), 
    date: str = Form(...), 
    password: str = Form(...), # Incoming form pass token check
    file: UploadFile = File(...)
):
    if password != ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Unauthorized: Galat Password Hai!")

    item_id = str(uuid.uuid4())[:8]
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    web_accessible_path = f"/static-uploads/{file.filename}"
    
    class_materials.append({
        "id": item_id,
        "title": title,
        "category": category,
        "image_path": web_accessible_path,
        "date": date
    })
    save_data_to_file()
    return RedirectResponse(url="/", status_code=303)

# --- 🗑️ DELETE ROUTE WITH PASSWORD LOCK ---
@app.post("/delete-material/{item_id}")
def delete_material(item_id: str, password: str = Form(...)):
    global class_materials
    if password != ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Unauthorized: Galat Password Hai!")
        
    item_to_delete = next((item for item in class_materials if item.get("id") == item_id), None)
    
    if item_to_delete:
        image_path = item_to_delete.get("image_path", "")
        if image_path:
            filename = image_path.split("/")[-1]
            physical_file = os.path.join(UPLOAD_DIR, filename)
            if os.path.exists(physical_file):
                os.remove(physical_file)
        
        class_materials = [item for item in class_materials if item.get("id") != item_id]
        save_data_to_file()
        return RedirectResponse(url="/", status_code=303)
        
    raise HTTPException(status_code=404, detail="Node missing")