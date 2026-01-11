import os
import json
import shutil
from PIL import Image
import git
import customtkinter as ctk
from tkinter import filedialog, messagebox
import time

# Settings
# Constants
# Constants
APP_NAME = "InkDynastyAdmin"
# Determine Base Dir for Data
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, "ink_data")
REPO_DIR = os.path.join(DATA_DIR, "repo")
REMOTE_URL = "https://github.com/XsaTi4/tattoo_web.git"

# Determine Project Root
# 1. Check Local (Development / Local Usage)
detected_root = None
if getattr(sys, 'frozen', False):
    exe_dir = os.path.dirname(sys.executable)
    # Check distinct locations relative to exe
    candidates = [exe_dir, os.path.dirname(exe_dir)] 
    for path in candidates:
        if os.path.exists(os.path.join(path, '.git')):
            detected_root = path
            break
else:
    # Script mode
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent = os.path.dirname(script_dir)
    if os.path.exists(os.path.join(parent, '.git')):
        detected_root = parent

# 2. If no local repo found, use Portable System Dir
if detected_root:
    PROJECT_ROOT = detected_root
    IS_PORTABLE = False
else:
    PROJECT_ROOT = REPO_DIR
    IS_PORTABLE = True

# Ensure paths are valid even if they don't exist yet (for cloning)
SRC_DIR = os.path.join(PROJECT_ROOT, 'src')
SRC_DATA_DIR = os.path.join(SRC_DIR, 'data')
GALLERY_JSON = os.path.join(SRC_DATA_DIR, 'gallery.json')
CONFIG_JSON = os.path.join(SRC_DATA_DIR, 'config.json')
IMAGES_DIR = os.path.join(PROJECT_ROOT, 'public', 'images')

SRC_DIR = os.path.join(PROJECT_ROOT, 'src')
SRC_DATA_DIR = os.path.join(SRC_DIR, 'data')
GALLERY_JSON = os.path.join(SRC_DATA_DIR, 'gallery.json')
CONFIG_JSON = os.path.join(SRC_DATA_DIR, 'config.json')
IMAGES_DIR = os.path.join(PROJECT_ROOT, 'public', 'images')

class InkAdminApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Ink Dynasty Admin")
        self.geometry("900x700")
        ctk.set_appearance_mode("Dark")
        
        self.repo = None
        self.ensure_repo()
        
        self.load_data()
        self.setup_ui()
        self.update_status()

    def ensure_repo(self):
        global PROJECT_ROOT, SRC_DIR, SRC_DATA_DIR, GALLERY_JSON, CONFIG_JSON, IMAGES_DIR
        
        # 1. Check if .git exists in PROJECT_ROOT (Local Dev or already setup)
        if os.path.exists(os.path.join(PROJECT_ROOT, '.git')):
            try:
                self.repo = git.Repo(PROJECT_ROOT)
                self.log(f"Repository loaded: {PROJECT_ROOT}")
                # Auto-pull for portable mode if this is indeed the portable repo
                if IS_PORTABLE:
                     self.fetch_updates()
            except Exception as e:
                self.log(f"Error loading repo: {e}")
            return

        # 2. Portal Mode Setup
        if IS_PORTABLE:
            # Check if REPO_DIR exists but is empty or broken
            if os.path.exists(REPO_DIR):
                if os.path.exists(os.path.join(REPO_DIR, '.git')):
                    # It looks like a valid repo, try to use it
                    try:
                        self.repo = git.Repo(REPO_DIR)
                        self.log(f"Repository loaded from portable storage: {REPO_DIR}")
                        # Update global PROJECT_ROOT to point here if not already
                        PROJECT_ROOT = REPO_DIR
                        SRC_DIR = os.path.join(PROJECT_ROOT, 'src')
                        SRC_DATA_DIR = os.path.join(SRC_DIR, 'data')
                        GALLERY_JSON = os.path.join(SRC_DATA_DIR, 'gallery.json')
                        CONFIG_JSON = os.path.join(SRC_DATA_DIR, 'config.json')
                        IMAGES_DIR = os.path.join(PROJECT_ROOT, 'public', 'images')
                        
                         # Auto-pull to ensure freshness
                        self.fetch_updates()
                        return
                    except:
                        pass # Valid folder but invalid repo, fall through to prompt
                
            answer = messagebox.askyesno("Setup", "Download (Clone) repository from GitHub to portable storage?")
            if answer:
                def on_rm_error(func, path, exc_info):
                    # Error handler for shutil.rmtree
                    import stat
                    os.chmod(path, stat.S_IWRITE)
                    os.unlink(path)

                try:
                    # Clean up if exists but broken
                    if os.path.exists(REPO_DIR):
                        try:
                            # Force remove directory
                            shutil.rmtree(REPO_DIR, onerror=on_rm_error)
                        except Exception as ex:
                            messagebox.showerror("Error", f"Could not clear folder {REPO_DIR}.\nPlease delete it manually or close other apps using it.")
                            return

                    # DO NOT CREATE DIR manually for git.Repo.clone_from if using that
                    # But if we rely on it, we must ensure parent exists
                    os.makedirs(os.path.dirname(REPO_DIR), exist_ok=True)
                    
                    self.log(f"Cloning to {REPO_DIR}...")
                    git.Repo.clone_from(REMOTE_URL, REPO_DIR)
                    
                    # Verify Clone
                    if not os.path.exists(os.path.join(REPO_DIR, 'src')):
                         raise Exception("Clone appeared successful but 'src' folder is missing")

                    # Update paths after clone
                    PROJECT_ROOT = REPO_DIR
                    SRC_DIR = os.path.join(PROJECT_ROOT, 'src')
                    SRC_DATA_DIR = os.path.join(SRC_DIR, 'data')
                    GALLERY_JSON = os.path.join(SRC_DATA_DIR, 'gallery.json')
                    CONFIG_JSON = os.path.join(SRC_DATA_DIR, 'config.json')
                    IMAGES_DIR = os.path.join(PROJECT_ROOT, 'public', 'images')

                    self.repo = git.Repo(PROJECT_ROOT)
                    messagebox.showinfo("Success", "Repository downloaded successfully!\nApp is ready.")
                    self.log("Clone successful.")
                except Exception as e:
                    messagebox.showerror("Clone Error", f"Failed to download: {e}")
                    self.log(f"Clone failed: {e}")
            else:
                messagebox.showwarning("Warning", "App will run in limited mode without content.")

    def load_data(self):
        # Gallery Data
        self.gallery_data = []
        try:
            if os.path.exists(GALLERY_JSON):
                with open(GALLERY_JSON, 'r') as f:
                    self.gallery_data = json.load(f)
            else:
                self.log(f"Warning: Gallery data not found at {GALLERY_JSON}")
        except Exception as e:
            self.log(f"Error loading gallery data: {e}")

        # Config Data
        self.config_data = {}
        try:
            if os.path.exists(CONFIG_JSON):
                with open(CONFIG_JSON, 'r') as f:
                    self.config_data = json.load(f)
            else:
                self.log(f"Warning: Config data not found at {CONFIG_JSON}")
        except Exception as e:
            self.log(f"Error loading config data: {e}")

    def save_data(self):
        try:
            if not os.path.exists(SRC_DATA_DIR):
                os.makedirs(SRC_DATA_DIR, exist_ok=True)
                
            with open(GALLERY_JSON, 'w') as f:
                json.dump(self.gallery_data, f, indent=2)
            with open(CONFIG_JSON, 'w') as f:
                json.dump(self.config_data, f, indent=2)
        except Exception as e:
            self.log(f"Error saving data: {e}")
            messagebox.showerror("Save Error", str(e))

    def setup_ui(self):
        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        
        ctk.CTkLabel(self.sidebar, text="INK DYNASTY", font=("Arial", 20, "bold")).pack(pady=20)
        
        self.status_label = ctk.CTkLabel(self.sidebar, text="Status: Ready", text_color="gray")
        self.status_label.pack(side="bottom", pady=20)
        
        # Git Sync Controls
        sync_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        sync_frame.pack(side="bottom", fill="x", padx=10, pady=10)
        
        ctk.CTkButton(sync_frame, text="Fetch Updates (Pull)", fg_color="#F39C12", hover_color="#D68910", command=self.fetch_updates).pack(fill="x", pady=5)
        ctk.CTkButton(sync_frame, text="Update Site (Git Push)", fg_color="#27AE60", hover_color="#2ECC71", command=self.git_sync).pack(fill="x", pady=5)

        # Tabs
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        self.tab_photos = self.tabview.add("Photos")
        self.tab_studio = self.tabview.add("Studio")
        self.tab_master = self.tabview.add("Master")
        self.tab_settings = self.tabview.add("Settings")
        self.tab_console = self.tabview.add("Console")
        
        self.setup_photos_tab()
        self.setup_studio_tab()
        self.setup_master_tab()
        self.setup_settings_tab()
        self.setup_console_tab()

    def setup_console_tab(self):
        self.log_widget = ctk.CTkTextbox(self.tab_console, state="disabled")
        self.log_widget.pack(fill="both", expand=True, padx=5, pady=5)
        self.log("Admin Console Started.")

    def log(self, message):
        timestamp = time.strftime("[%Y-%m-%d %H:%M:%S]")
        full_msg = f"{timestamp} {message}"
        
        # UI Log
        if hasattr(self, 'log_widget'):
            self.log_widget.configure(state="normal")
            self.log_widget.insert("end", f"> {full_msg}\n")
            self.log_widget.see("end")
            self.log_widget.configure(state="disabled")
            
        # File Log
        try:
            with open(os.path.join(PROJECT_ROOT, "admin_log.txt"), "a") as f:
                f.write(f"{full_msg}\n")
        except:
            pass
        
        print(message)

    def update_status(self):
        try:
            head = self.repo.head.commit
            import time
            time_str = time.strftime('%Y-%m-%d %H:%M', time.localtime(head.committed_date))
            self.status_label.configure(text=f"Last Commit ({time.tzname[0]}):\n{time_str}\n\nBranch: {self.repo.active_branch.name}")
        except Exception as e:
            self.status_label.configure(text="Status: Git Error")

    def setup_photos_tab(self):
        ctk.CTkLabel(self.tab_photos, text="Gallery Manager", font=("Arial", 16)).pack(pady=10)
        
        self.photo_frame = ctk.CTkScrollableFrame(self.tab_photos, height=300)
        self.photo_frame.pack(fill="both", expand=True, padx=10)
        self.refresh_photo_list()
        
        ctk.CTkButton(self.tab_photos, text="Add New Photo", command=self.add_photo).pack(pady=10)

    def refresh_photo_list(self):
        for widget in self.photo_frame.winfo_children():
            widget.destroy()
            
        for item in self.gallery_data:
            row = ctk.CTkFrame(self.photo_frame)
            row.pack(fill="x", pady=2)
            
            # Thumbnail
            try:
                # remove leading slash for path join
                rel_path = item['src'].lstrip('/') 
                full_path = os.path.join(PROJECT_ROOT, 'public', rel_path)
                if os.path.exists(full_path):
                    pil_img = Image.open(full_path)
                    ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(50, 50))
                    img_lbl = ctk.CTkLabel(row, image=ctk_img, text="")
                    img_lbl.pack(side="left", padx=5)
            except Exception as e:
                print(f"Error loading thumbnail: {e}")

            ctk.CTkLabel(row, text=f"{item['title']} (ID: {item['id']})").pack(side="left", padx=10)
            # Controls
            controls = ctk.CTkFrame(row, fg_color="transparent")
            controls.pack(side="right", padx=5)
            
            ctk.CTkButton(controls, text="↑", width=30, command=lambda i=item['id']: self.move_photo(i, -1, 'gallery')).pack(side="left", padx=2)
            ctk.CTkButton(controls, text="↓", width=30, command=lambda i=item['id']: self.move_photo(i, 1, 'gallery')).pack(side="left", padx=2)
            ctk.CTkButton(controls, text="Edit", width=50, fg_color="#3498DB", command=lambda i=item['id']: self.edit_photo_title(i, 'gallery')).pack(side="left", padx=5)
            ctk.CTkButton(controls, text="Delete", width=60, fg_color="red", command=lambda i=item['id']: self.delete_photo(i)).pack(side="left", padx=5)

    def add_photo(self):
        # macOS Tkinter fix: separate extensions explicitly, plus all files
        file_path = filedialog.askopenfilename(filetypes=[
            ("All Files", "*.*"),
            ("JPEG Image", "*.jpg"), 
            ("JPEG Image", "*.jpeg"),
            ("PNG Image", "*.png"),
            ("WebP Image", "*.webp"),
            ("Bitmap", "*.bmp")
        ])
        if file_path:
            title = ctk.CTkInputDialog(text="Enter Photo Title:", title="New Photo").get_input()
            if not title: return

            try:
                # Process Image
                filename = f"tattoo-{len(self.gallery_data)+100}.jpg"
                save_path = os.path.join(IMAGES_DIR, filename)
                
                with Image.open(file_path) as img:
                    # Force RGB for JPEG compatibility (handles RGBA, P, LA, etc.)
                    if img.mode != 'RGB':
                        img = img.convert('RGB')
                        
                    img.thumbnail((1200, 1200)) # Resize
                    img.save(save_path, "JPEG", quality=85)
                
                # Update Data
                new_id = max([i['id'] for i in self.gallery_data] or [0]) + 1
                self.gallery_data.append({"id": new_id, "src": f"/images/{filename}", "title": title})
                self.save_data()
                self.refresh_photo_list()
                self.log(f"Added photo: {title}")
                messagebox.showinfo("Success", "Photo added!")
            except Exception as e:
                self.log(f"Error adding photo: {e}")
                messagebox.showerror("Error", str(e))

    def delete_photo(self, photo_id):
        self.gallery_data = [i for i in self.gallery_data if i['id'] != photo_id]
        self.save_data()
        self.refresh_photo_list()
        self.log(f"Deleted photo ID: {photo_id}")

    def setup_settings_tab(self):
        ctk.CTkLabel(self.tab_settings, text="Theme Control", font=("Arial", 16)).pack(pady=10)
        
        self.theme_var = ctk.StringVar(value=self.config_data.get('theme', 'default'))
        ctk.CTkOptionMenu(self.tab_settings, variable=self.theme_var, values=["default", "halloween", "newyear"], command=self.update_theme).pack(pady=10)
        
        self.banner_var = ctk.BooleanVar(value=self.config_data.get('showBanner', False))
        ctk.CTkCheckBox(self.tab_settings, text="Show Banner", variable=self.banner_var, command=self.update_banner).pack(pady=10)

    def update_theme(self, choice):
        self.config_data['theme'] = choice
        self.save_data()
        self.log(f"Theme changed to: {choice}")

    def update_banner(self):
        self.config_data['showBanner'] = self.banner_var.get()
        self.save_data()
        self.log(f"Banner toggled: {self.banner_var.get()}")

    def setup_studio_tab(self):
        # Header
        header = ctk.CTkFrame(self.tab_studio)
        header.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkLabel(header, text="Studio Photos", font=("Arial", 18, "bold")).pack(side="left", padx=10)
        ctk.CTkButton(header, text="Add Photo", command=self.add_studio_photo).pack(side="right", padx=10)
        
        # Scrollable List
        self.studio_list_frame = ctk.CTkScrollableFrame(self.tab_studio, label_text="Current Slideshow")
        self.studio_list_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.refresh_studio_list()

    def refresh_studio_list(self):
        for widget in self.studio_list_frame.winfo_children():
            widget.destroy()
            
        # studio_data is loaded in load_data, but we can re-read it here if needed
        # For simplicity, assuming self.studio_data is up-to-date or reloaded here
        try:
            with open(os.path.join(SRC_DATA_DIR, 'studio.json'), 'r') as f:
                self.studio_data = json.load(f)
        except FileNotFoundError:
            self.studio_data = []
        except Exception as e:
            self.log(f"Error loading studio data: {e}")
            self.studio_data = []
            
        for item in self.studio_data:
            row = ctk.CTkFrame(self.studio_list_frame)
            row.pack(fill="x", pady=2)
            
            # Thumbnail
            try:
                rel_path = item['src'].lstrip('/')
                full_path = os.path.join(PROJECT_ROOT, 'public', rel_path)
                if os.path.exists(full_path):
                    pil_img = Image.open(full_path)
                    ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(50, 50))
                    ctk.CTkLabel(row, image=ctk_img, text="").pack(side="left", padx=5)
                else:
                    ctk.CTkLabel(row, text="[Missing]", width=50).pack(side="left", padx=5)
            except:
                ctk.CTkLabel(row, text="[Error]", width=50).pack(side="left", padx=5)

            ctk.CTkLabel(row, text=f"ID: {item['id']}").pack(side="left", padx=10)
            ctk.CTkLabel(row, text=item.get('title', 'Untitled')).pack(side="left", padx=10)
            
            # Controls
            controls = ctk.CTkFrame(row, fg_color="transparent")
            controls.pack(side="right", padx=5)
            
            ctk.CTkButton(controls, text="↑", width=30, command=lambda i=item['id']: self.move_photo(i, -1, 'studio')).pack(side="left", padx=2)
            ctk.CTkButton(controls, text="↓", width=30, command=lambda i=item['id']: self.move_photo(i, 1, 'studio')).pack(side="left", padx=2)
            ctk.CTkButton(controls, text="Edit", width=50, fg_color="#3498DB", command=lambda i=item['id']: self.edit_photo_title(i, 'studio')).pack(side="left", padx=5)
            ctk.CTkButton(controls, text="Delete", width=60, fg_color="red", command=lambda i=item['id']: self.delete_studio_photo(i)).pack(side="left", padx=5)

    def add_studio_photo(self):
        file_path = filedialog.askopenfilename(filetypes=[("All Files", "*.*")])
        if file_path:
            title = ctk.CTkInputDialog(text="Enter Title:", title="New Studio Photo").get_input()
            if not title: return
            
            try:
                # 1. Prepare ID and Filename
                new_id = max([i['id'] for i in self.studio_data] or [0]) + 1
                ext = ".jpg" 
                filename = f"studio-{new_id}{ext}"
                
                # Ensure directory exists
                studio_dir = os.path.join(PROJECT_ROOT, 'public', 'images', 'studio')
                os.makedirs(studio_dir, exist_ok=True)
                
                save_path = os.path.join(studio_dir, filename)
                
                # 2. Process Image
                with Image.open(file_path) as img:
                    if img.mode != 'RGB':
                        img = img.convert('RGB')
                    img.thumbnail((1200, 800)) # Standard resize
                    img.save(save_path, "JPEG", quality=85)
                
                # 3. Update JSON
                new_item = {
                    "id": new_id,
                    "src": f"/images/studio/{filename}",
                    "title": title
                }
                self.studio_data.append(new_item)
                
                with open(os.path.join(SRC_DATA_DIR, 'studio.json'), 'w') as f:
                    json.dump(self.studio_data, f, indent=2)
                
                self.log(f"Added studio photo: {title}")
                self.refresh_studio_list()
                
            except Exception as e:
                self.log(f"Error adding studio photo: {e}")
                
    def move_photo(self, photo_id, direction, section):
        data_list = self.gallery_data if section == 'gallery' else self.studio_data
        idx = next((i for i, item in enumerate(data_list) if item['id'] == photo_id), -1)
        
        if idx == -1: return
        
        new_idx = idx + direction
        if 0 <= new_idx < len(data_list):
            data_list[idx], data_list[new_idx] = data_list[new_idx], data_list[idx]
            
            if section == 'gallery':
                self.save_data()
                self.refresh_photo_list()
            else:
                with open(os.path.join(SRC_DATA_DIR, 'studio.json'), 'w') as f:
                    json.dump(self.studio_data, f, indent=2)
                self.refresh_studio_list()
            
            self.log(f"Moved photo {photo_id} {'up' if direction < 0 else 'down'} in {section}")

    def edit_photo_title(self, photo_id, section):
        data_list = self.gallery_data if section == 'gallery' else self.studio_data
        item = next((i for i in data_list if i['id'] == photo_id), None)
        
        if not item: return
        
        new_title = ctk.CTkInputDialog(text="Edit Title:", title="Edit Photo").get_input()
        if new_title:
            item['title'] = new_title
            
            if section == 'gallery':
                self.save_data()
                self.refresh_photo_list()
            else:
                with open(os.path.join(SRC_DATA_DIR, 'studio.json'), 'w') as f:
                    json.dump(self.studio_data, f, indent=2)
                self.refresh_studio_list()
                
            self.log(f"Renamed photo {photo_id} to: {new_title}")

    def delete_studio_photo(self, photo_id):
        item = next((i for i in self.studio_data if i['id'] == photo_id), None)
        if item:
            # Delete file
            try:
                rel_path = item['src'].lstrip('/')
                full_path = os.path.join(PROJECT_ROOT, 'public', rel_path)
                if os.path.exists(full_path):
                    os.remove(full_path)
            except Exception as e:
                self.log(f"Error deleting file: {e}")
                
            # Update JSON
            self.studio_data = [i for i in self.studio_data if i['id'] != photo_id]
            with open(os.path.join(SRC_DATA_DIR, 'studio.json'), 'w') as f:
                json.dump(self.studio_data, f, indent=2)
                
            self.log(f"Deleted studio photo ID: {photo_id}")
            self.refresh_studio_list()

    def setup_master_tab(self):
        self.master_frame = ctk.CTkFrame(self.tab_master)
        self.master_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(self.master_frame, text="Master Profile Photo", font=("Arial", 20, "bold")).pack(pady=10)
        
        # Display Current Photo
        self.master_img_label = ctk.CTkLabel(self.master_frame, text="")
        self.master_img_label.pack(pady=10)
        
        self.refresh_master_preview()
        
        ctk.CTkButton(self.master_frame, text="Change Photo", command=self.change_master_photo).pack(pady=20)
        ctk.CTkLabel(self.master_frame, text="Note: Uploaded photo will be auto-cropped to square.").pack()

    def refresh_master_preview(self):
        try:
            with open(os.path.join(SRC_DIR, 'data', 'config.json'), 'r') as f:
                cfg = json.load(f)
                
            rel_path = cfg.get('masterPhoto', '').lstrip('/')
            full_path = os.path.join(PROJECT_ROOT, 'public', rel_path)
            
            if os.path.exists(full_path):
                pil_img = Image.open(full_path)
                pil_img.thumbnail((300, 300))
                ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(300, 300))
                self.master_img_label.configure(image=ctk_img, text="")
            else:
                self.master_img_label.configure(image=None, text="[No Photo]")
        except Exception as e:
            self.log(f"Error loading master preview: {e}")

    def change_master_photo(self):
        file_path = filedialog.askopenfilename(filetypes=[("All Files", "*.*")])
        if file_path:
            try:
                # Load Config
                cfg_path = os.path.join(SRC_DIR, 'data', 'config.json')
                with open(cfg_path, 'r') as f:
                    cfg = json.load(f)
                
                # Generate new filename to bust cache (simple timestamp)
                timestamp = int(time.time())
                filename = f"master_{timestamp}.jpg"
                save_path = os.path.join(PROJECT_ROOT, 'public', 'images', filename)
                
                # Process Image (Square Crop)
                with Image.open(file_path) as img:
                    if img.mode != 'RGB':
                        img = img.convert('RGB')
                        
                    # Center Crop to Square
                    width, height = img.size
                    new_size = min(width, height)
                    left = (width - new_size)/2
                    top = (height - new_size)/2
                    right = (width + new_size)/2
                    bottom = (height + new_size)/2
                    
                    img = img.crop((left, top, right, bottom))
                    img.thumbnail((800, 800))
                    img.save(save_path, "JPEG", quality=90)
                    
                # Clean up old photo if exists
                old_rel = cfg.get('masterPhoto', '').lstrip('/')
                old_full = os.path.join(PROJECT_ROOT, 'public', old_rel)
                if os.path.exists(old_full) and "master_" in old_rel: # Safety check
                    try: os.remove(old_full)
                    except: pass

                # Update Config
                cfg['masterPhoto'] = f"/images/{filename}"
                with open(cfg_path, 'w') as f:
                    json.dump(cfg, f, indent=2)
                    
                self.log("Updated master photo.")
                self.refresh_master_preview()
                
            except Exception as e:
                self.log(f"Error changing master photo: {e}")

    def fetch_updates(self):
        self.log("Fetching updates from remote...")
        try:
            self.repo.git.pull()
            self.log("Successfully pulled latest changes.")
            
            # Refresh all data
            self.refresh_photo_list()
            self.refresh_studio_list()
            self.refresh_master_preview()
            self.update_status()
            messagebox.showinfo("Success", "Repository Updated!")
        except Exception as e:
            self.log(f"Fetch Error: {str(e)}")
            messagebox.showerror("Error", f"Failed to fetch updates: {str(e)}")

    def git_sync(self):
        self.log("Git Sync Started...")
        try:
            self.repo.git.add('.')
            self.repo.index.commit("Update via Ink Admin")
            self.log("Committed changes locally.")
            
            # Fix Upstream Issue
            self.repo.git.push('--set-upstream', 'origin', 'main')
            
            self.log("Pushed to origin/main successfully.")
            messagebox.showinfo("Success", "Website Updated Successfully!")
            self.update_status()
        except Exception as e:
            self.log(f"Git Error: {str(e)}")
            messagebox.showerror("Error", f"Git Error: {str(e)}")

if __name__ == "__main__":
    app = InkAdminApp()
    app.mainloop()
