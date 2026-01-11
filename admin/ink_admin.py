import os
import json
import shutil
from PIL import Image
import git
import customtkinter as ctk
from tkinter import filedialog, messagebox

# Settings
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
GALLERY_JSON = os.path.join(PROJECT_ROOT, 'src', 'data', 'gallery.json')
CONFIG_JSON = os.path.join(PROJECT_ROOT, 'src', 'data', 'config.json')
IMAGES_DIR = os.path.join(PROJECT_ROOT, 'public', 'images')

class InkAdminApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Ink Dynasty Admin")
        self.geometry("800x600")
        ctk.set_appearance_mode("Dark")
        
        self.repo = git.Repo(PROJECT_ROOT)
        self.load_data()
        self.setup_ui()

    def load_data(self):
        with open(GALLERY_JSON, 'r') as f:
            self.gallery_data = json.load(f)
        with open(CONFIG_JSON, 'r') as f:
            self.config_data = json.load(f)

    def save_data(self):
        with open(GALLERY_JSON, 'w') as f:
            json.dump(self.gallery_data, f, indent=2)
        with open(CONFIG_JSON, 'w') as f:
            json.dump(self.config_data, f, indent=2)

    def setup_ui(self):
        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        
        ctk.CTkLabel(self.sidebar, text="INK DYNASTY", font=("Arial", 20, "bold")).pack(pady=20)
        
        ctk.CTkButton(self.sidebar, text="Update Site (Git Push)", command=self.git_sync, fg_color="green").pack(pady=10, padx=10)
        
        # Tabs
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        self.tab_photos = self.tabview.add("Photos")
        self.tab_settings = self.tabview.add("Settings")
        
        self.setup_photos_tab()
        self.setup_settings_tab()

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
            ctk.CTkLabel(row, text=f"ID: {item['id']} - {item['title']}").pack(side="left", padx=10)
            ctk.CTkButton(row, text="Delete", width=60, fg_color="red", command=lambda i=item['id']: self.delete_photo(i)).pack(side="right", padx=5)

    def add_photo(self):
        # macOS Tkinter fix: separate extensions explicitly
        file_path = filedialog.askopenfilename(filetypes=[("PNG Image", "*.png"), ("JPEG Image", "*.jpg"), ("JPEG Image", "*.jpeg")])
        if file_path:
            title = ctk.CTkInputDialog(text="Enter Photo Title:", title="New Photo").get_input()
            if not title: return

            # Process Image
            filename = f"tattoo-{len(self.gallery_data)+100}.jpg"
            save_path = os.path.join(IMAGES_DIR, filename)
            
            with Image.open(file_path) as img:
                img.thumbnail((1200, 1200)) # Resize
                img.save(save_path, "JPEG", quality=85)
            
            # Update Data
            new_id = max([i['id'] for i in self.gallery_data] or [0]) + 1
            self.gallery_data.append({"id": new_id, "src": f"/images/{filename}", "title": title})
            self.save_data()
            self.refresh_photo_list()
            messagebox.showinfo("Success", "Photo added!")

    def delete_photo(self, photo_id):
        self.gallery_data = [i for i in self.gallery_data if i['id'] != photo_id]
        self.save_data()
        self.refresh_photo_list()

    def setup_settings_tab(self):
        ctk.CTkLabel(self.tab_settings, text="Theme Control", font=("Arial", 16)).pack(pady=10)
        
        self.theme_var = ctk.StringVar(value=self.config_data.get('theme', 'default'))
        ctk.CTkOptionMenu(self.tab_settings, variable=self.theme_var, values=["default", "halloween", "newyear"], command=self.update_theme).pack(pady=10)
        
        self.banner_var = ctk.BooleanVar(value=self.config_data.get('showBanner', False))
        ctk.CTkCheckBox(self.tab_settings, text="Show Banner", variable=self.banner_var, command=self.update_banner).pack(pady=10)

    def update_theme(self, choice):
        self.config_data['theme'] = choice
        self.save_data()

    def update_banner(self):
        self.config_data['showBanner'] = self.banner_var.get()
        self.save_data()

    def git_sync(self):
        try:
            self.repo.git.add('.')
            self.repo.index.commit("Update via Ink Admin")
            origin = self.repo.remote(name='origin')
            origin.push()
            messagebox.showinfo("Success", "Website Updated Successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Git Error: {str(e)}")

if __name__ == "__main__":
    app = InkAdminApp()
    app.mainloop()
