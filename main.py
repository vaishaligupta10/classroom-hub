from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
import os
import shutil
import json
import uuid
from typing import List, Dict, Optional

app = FastAPI()

UPLOAD_DIR = "uploads"
JSON_FILE = "database.json"
ADMIN_PASSWORD = "vaishali123"

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

app.mount("/static-uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

def load_data_from_file() -> List[Dict]:
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r") as file:
            try:
                return json.load(file)
            except:
                return []
    return [{"id": "demo-1", "title": "Welcome Demo Note", "category": "Notes", "content_type": "text", "text_or_link": "Welcome to your smart repository portal!", "image_path": "", "date": "May 21, 2026"}]

def save_data_to_file():
    with open(JSON_FILE, "w") as file:
        json.dump(class_materials, file, indent=4)

class_materials = load_data_from_file()

@app.get("/", response_class=HTMLResponse)
def build_classroom_portal():
    cards_html = ""
    
    for item in class_materials:
        item_id = item.get("id", "")
        category = item.get("category", "Notes")
        content_type = item.get("content_type", "image")
        text_or_link = item.get("text_or_link", "")
        image_path = item.get("image_path", "")
        
        badge_color = "bg-indigo-500/10 text-indigo-400 border border-indigo-500/20"
        if category == "Classwork":
            badge_color = "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20"
        elif category == "Homework":
            badge_color = "bg-rose-500/10 text-rose-400 border border-rose-500/20"
            
        # 📄 Smart Content Block Generator
        content_block = ""
        view_btn = ""
        
        if content_type == "link":
            content_block = f"""
            <div class="mt-2 p-3 bg-slate-950 rounded-xl border border-sky-500/20 text-xs flex items-center justify-between gap-2">
                <span class="text-sky-400 truncate flex-1 font-mono">{text_or_link}</span>
                <button onclick="navigator.clipboard.writeText('{text_or_link}'); alert('Link Copied!');" class="bg-sky-500/10 hover:bg-sky-500/20 border border-sky-500/30 text-sky-400 text-[10px] font-bold px-2.5 py-1 rounded-lg transition shrink-0">📋 Copy</button>
            </div>
            """
            view_btn = f'<a href="{text_or_link}" target="_blank" class="text-xs bg-slate-800 border border-slate-700 text-sky-400 hover:bg-slate-700/50 px-3 py-1.5 rounded-lg font-medium transition">Open</a>'
            
        elif content_type == "text":
            content_block = f"""
            <div class="mt-2 p-3 bg-slate-950 rounded-xl border border-slate-800 text-xs text-slate-300 break-words whitespace-pre-wrap font-sans">
                {text_or_link}
            </div>
            """
            view_btn = '<span class="text-xs text-slate-500 italic px-1">Text Note</span>'
            
        else: # Image content block
            if image_path:
                content_block = f"""
                <div class="mt-3 border border-slate-700/50 rounded-xl overflow-hidden bg-slate-900/40">
                    <img src="{image_path}" class="w-full h-auto max-h-60 object-cover" alt="Notes">
                </div>
                """
                view_btn = f'<a href="{image_path}" target="_blank" class="text-xs bg-slate-800 border border-slate-700 text-indigo-400 hover:bg-slate-700/50 px-3 py-1.5 rounded-lg font-medium transition">View</a>'
            else:
                view_btn = '<span class="text-xs text-slate-500 italic px-1">No File</span>'

        cards_html += f"""
        <div class="material-card bg-slate-900/60 backdrop-blur-md p-4 sm:p-5 rounded-2xl border border-slate-800/80 shadow-xl flex flex-col justify-between space-y-3" data-category="{category}">
            <div class="flex justify-between items-start gap-2">
                <div class="truncate flex-1">
                    <span class="inline-block text-[9px] uppercase font-bold tracking-widest px-2 py-0.5 rounded-full {badge_color} mb-1.5">{category}</span>
                    <p class="text-sm font-bold text-slate-100 truncate tracking-wide whitespace-normal break-words">{item.get('title', 'Untitled')}</p>
                    <span class="text-[11px] text-slate-400 block mt-0.5 font-mono">{item.get('date', '')}</span>
                </div>
                <div class="flex items-center gap-1.5 shrink-0">
                    {view_btn}
                    <button onclick="secureDelete('{item_id}')" class="text-xs bg-rose-500/10 border border-rose-500/20 hover:bg-rose-500/20 text-rose-400 p-1.5 rounded-lg transition">🗑️</button>
                </div>
            </div>
            {content_block}
        </div>
        """

    return f"""
    <html>
        <head>
            <title>Classroom Hub Panel</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
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

                function secureDelete(itemId) {{
                    const password = prompt("Admin Authorization Required.\\nEnter Secret Password to Delete:");
                    if (password === null) return;
                    
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

                // Toggle display form options
                function toggleInputType(type) {{
                    const fileDiv = document.getElementById('file-input-wrapper');
                    const textDiv = document.getElementById('text-input-wrapper');
                    const textInput = document.getElementById('text_or_link_input');
                    const fileInput = document.getElementById('file_input');
                    
                    if(type === 'image') {{
                        fileDiv.style.display = 'block';
                        textDiv.style.display = 'none';
                        fileInput.required = true;
                        textInput.required = false;
                    }} else {{
                        fileDiv.style.display = 'none';
                        textDiv.style.display = 'block';
                        fileInput.required = false;
                        textInput.required = true;
                        if(type === 'link') {{
                            textInput.placeholder = "Paste link here (e.g. https://drive.google.com/...)";
                        }} else {{
                            textInput.placeholder = "Write your detailed text notes here...";
                        }}
                    }}
                }}
            </script>
        </head>
        <body class="bg-slate-950 font-sans text-slate-200 min-h-screen p-3 sm:p-6 md:p-12 relative overflow-x-hidden">
            
            <div class="fixed bottom-4 right-4 z-0 pointer-events-none select-none opacity-10 font-black text-2xl sm:text-4xl tracking-widest text-indigo-400 font-mono uppercase">
                Made by Vaishali
            </div>

            <div class="max-w-5xl mx-auto space-y-6 md:space-y-8 relative z-10">
                
                <div class="bg-gradient-to-r from-indigo-950 to-slate-900 text-indigo-300 px-4 py-2.5 rounded-xl font-medium text-[10px] sm:text-xs tracking-wider border border-indigo-900/50 flex flex-col sm:flex-row justify-between items-center gap-2 shadow-lg">
                    <span>⚡ CORE ACADEMIC REPOSITORY ENGINE</span>
                    <span class="text-emerald-400 font-mono text-[9px] bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">🔒 PASSWORD ENFORCED</span>
                </div>
                
                <div class="bg-slate-900/40 border border-slate-800/80 p-4 sm:p-6 rounded-2xl shadow-2xl space-y-4 backdrop-blur-lg">
                    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800/60 pb-3">
                        <h3 class="text-xs font-extrabold uppercase tracking-widest text-indigo-400 flex items-center gap-2">
                            <span class="w-2 h-2 rounded-full bg-indigo-500"></span>
                            Secure Upload Terminal
                        </h3>
                        
                        <div class="flex gap-2 bg-slate-950 p-1 rounded-lg border border-slate-800 text-[10px] font-bold">
                            <label class="cursor-pointer px-2 py-1 rounded transition text-slate-300"><input type="radio" name="source_type" value="image" checked onclick="toggleInputType('image')" class="mr-1 accent-indigo-500">Photo / File</label>
                            <label class="cursor-pointer px-2 py-1 rounded transition text-slate-300"><input type="radio" name="source_type" value="link" onclick="toggleInputType('link')" class="mr-1 accent-indigo-500">URL Link</label>
                            <label class="cursor-pointer px-2 py-1 rounded transition text-slate-300"><input type="radio" name="source_type" value="text" onclick="toggleInputType('text')" class="mr-1 accent-indigo-500">Plain Text</label>
                        </div>
                    </div>

                    <form action="/upload-note" method="POST" enctype="multipart/form-data" class="space-y-4">
                        
                        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                            <div class="md:col-span-2">
                                <label class="block text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-1">Document Title / Topic</label>
                                <input type="text" name="title" required placeholder="e.g. Operating System Link or Diagram Name" class="w-full text-xs p-2.5 rounded-xl border border-slate-800 bg-slate-950 text-slate-100 placeholder:text-slate-600 focus:outline-none focus:border-indigo-500 transition">
                            </div>
                            <div>
                                <label class="block text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-1">Stream Tag</label>
                                <select name="category" class="w-full text-xs p-2.5 rounded-xl border border-slate-800 bg-slate-950 text-slate-100 focus:outline-none focus:border-indigo-500 transition">
                                    <option value="Notes">Notes</option>
                                    <option value="Classwork">Classwork</option>
                                    <option value="Homework">Homework</option>
                                </select>
                            </div>
                        </div>

                        <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                            <div>
                                <label class="block text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-1">Timestamp Date</label>
                                <input type="text" name="date" required placeholder="21 May 2026" class="w-full text-xs p-2.5 rounded-xl border border-slate-800 bg-slate-950 text-slate-100 focus:outline-none focus:border-indigo-500 transition">
                            </div>
                            
                            <div class="sm:col-span-2" id="file-input-wrapper">
                                <label class="block text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-1">Capture Image</label>
                                <input type="file" name="file" id="file_input" required class="w-full text-xs text-slate-500 file:mr-3 file:py-1.5 file:px-3 file:rounded-xl file:border-0 file:text-[11px] file:font-bold file:bg-indigo-600 file:text-white hover:file:bg-indigo-700 cursor-pointer">
                            </div>
                            
                            <div class="sm:col-span-2 hidden" id="text-input-wrapper">
                                <label class="block text-[10px] font-bold text-sky-400 uppercase tracking-wider mb-1">Text Data / Hyperlink String</label>
                                <input type="text" name="text_or_link" id="text_or_link_input" placeholder="Paste external links here..." class="w-full text-xs p-2.5 rounded-xl border border-slate-800 bg-slate-950 text-slate-100 focus:outline-none focus:border-indigo-500 transition">
                            </div>
                        </div>
                        
                        <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 items-end pt-2 border-t border-slate-800/50">
                            <div class="sm:col-span-2">
                                <label class="block text-[10px] font-bold text-amber-400 uppercase tracking-wider mb-1">🔑 Admin Access Token (Password)</label>
                                <input type="password" name="password" required placeholder="Enter Secret Code to Upload" class="w-full text-xs p-2.5 rounded-xl border border-amber-500/30 bg-slate-950 text-slate-100 focus:outline-none focus:border-amber-500 transition">
                            </div>
                            <div>
                                <button type="submit" class="w-full bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold px-5 py-2.5 rounded-xl transition shadow-lg shadow-indigo-600/10">🚀 Broadcast Data</button>
                            </div>
                        </div>
                    </form>
                </div>

                <header class="border-b border-slate-800/80 pb-3 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
                    <div>
                        <h2 class="text-xs font-extrabold uppercase tracking-widest text-slate-400">Database Feed Stream</h2>
                    </div>
                    
                    <div class="flex gap-1.5 bg-slate-900/60 p-1 rounded-xl border border-slate-800 overflow-x-auto max-w-full no-scrollbar self-start sm:self-auto">
                        <button onclick="filterCategory('All')" class="tab-btn shrink-0 px-4 py-1.5 text-xs font-semibold rounded-lg bg-indigo-600 text-white transition">All</button>
                        <button onclick="filterCategory('Notes')" class="tab-btn shrink-0 px-4 py-1.5 text-xs font-semibold rounded-lg text-slate-400 hover:bg-slate-800/50 transition">Notes</button>
                        <button onclick="filterCategory('Classwork')" class="tab-btn shrink-0 px-4 py-1.5 text-xs font-semibold rounded-lg text-slate-400 hover:bg-slate-800/50 transition">Classwork</button>
                        <button onclick="filterCategory('Homework')" class="tab-btn shrink-0 px-4 py-1.5 text-xs font-semibold rounded-lg text-slate-400 hover:bg-slate-800/50 transition">Homework</button>
                    </div>
                </header>

                <section>
                    <div id="cards-grid" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4 sm:gap-6">
                        {cards_html if cards_html else '<p class="text-xs italic text-slate-500">No active uploads present.</p>'}
                    </div>
                </section>
            </div>
        </body>
    </html>
    """

@app.post("/upload-note")
def upload_note_with_image(
    title: str = Form(...), 
    category: str = Form(...), 
    date: str = Form(...), 
    password: str = Form(...), 
    text_or_link: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None)
):
    if password != ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Unauthorized: Galat Password Hai!")

    item_id = str(uuid.uuid4())[:8]
    content_type = "image"
    web_accessible_path = ""
    
    # 🧠 Detect content target input type logic
    if text_or_link and text_or_link.strip():
        txt = text_or_link.strip()
        if txt.startswith("http://") or txt.startswith("https://"):
            content_type = "link"
        else:
            content_type = "text"
    elif file and file.filename:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        web_accessible_path = f"/static-uploads/{file.filename}"
        content_type = "image"
    else:
        raise HTTPException(status_code=400, detail="Kuch toh daalo! File, Text ya Link empty hai.")

    class_materials.append({
        "id": item_id,
        "title": title,
        "category": category,
        "content_type": content_type,
        "text_or_link": text_or_link if content_type in ["text", "link"] else "",
        "image_path": web_accessible_path,
        "date": date
    })
    save_data_to_file()
    return RedirectResponse(url="/", status_code=303)

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