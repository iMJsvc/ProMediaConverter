import os
import subprocess
import threading
from tkinter import filedialog, messagebox
import customtkinter as ctk
from PIL import Image

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class MediaConverterApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Pro Media Converter & Resizer")
        self.geometry("600x540")
        self.resizable(False, False)

        ctk.CTkLabel(self, text="All-in-One Lossless Media Tool", font=("Arial", 22, "bold")).pack(pady=15)

        self.tabview = ctk.CTkTabview(self, width=540, height=440)
        self.tabview.pack(pady=5)

        self.tab_image = self.tabview.add("Image Converter")
        self.tab_video = self.tabview.add("Video Converter")

        self.setup_image_tab()
        self.setup_video_tab()

    def setup_image_tab(self):
        self.img_path = ""
        ctk.CTkButton(self.tab_image, text="Select Image", command=self.select_image, width=200).pack(pady=15)
        self.lbl_img_name = ctk.CTkLabel(self.tab_image, text="No image selected", text_color="gray")
        self.lbl_img_name.pack(pady=5)

        ctk.CTkLabel(self.tab_image, text="Output Format:", font=("Arial", 13, "bold")).pack(pady=(15, 5))
        self.img_format_var = ctk.StringVar(value="PNG")
        ctk.CTkOptionMenu(self.tab_image, values=["PNG", "JPG", "WEBP", "BMP", "TIFF", "ICO"], variable=self.img_format_var).pack(pady=5)

        ctk.CTkLabel(self.tab_image, text="Custom Resize (Leave blank for original size):", font=("Arial", 12)).pack(pady=(15, 5))
        sf = ctk.CTkFrame(self.tab_image, fg_color="transparent")
        sf.pack(pady=5)
        self.entry_img_w = ctk.CTkEntry(sf, placeholder_text="Width (px)", width=110)
        self.entry_img_w.pack(side="left", padx=5)
        self.entry_img_h = ctk.CTkEntry(sf, placeholder_text="Height (px)", width=110)
        self.entry_img_h.pack(side="left", padx=5)

        ctk.CTkButton(self.tab_image, text="Convert & Save Image", fg_color="green", hover_color="darkgreen", command=self.process_image, width=220, height=40).pack(pady=25)

    def select_image(self):
        fp = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.webp;*.bmp;*.tiff;*.ico")])
        if fp:
            self.img_path = fp
            self.lbl_img_name.configure(text=os.path.basename(fp), text_color="white")

    def process_image(self):
        if not self.img_path:
            messagebox.showerror("Error", "Please select an image first!")
            return
        try:
            img = Image.open(self.img_path)
            fmt = self.img_format_var.get()
            w, h = self.entry_img_w.get().strip(), self.entry_img_h.get().strip()
            if w and h:
                img = img.resize((int(w), int(h)), Image.Resampling.LANCZOS)
            elif w or h:
                messagebox.showwarning("Warning", "Enter both Width and Height, or leave both blank.")
                return
            sp = filedialog.asksaveasfilename(defaultextension=f".{fmt.lower()}", filetypes=[(f"{fmt} File", f"*.{fmt.lower()}")])
            if not sp:
                return
            pfmt = "JPEG" if fmt == "JPG" else fmt
            if pfmt in ["JPEG", "BMP"] and img.mode in ("RGBA", "LA", "P"):
                bg = Image.new("RGB", img.size, (255, 255, 255))
                if img.mode == "P":
                    img = img.convert("RGBA")
                bg.paste(img, mask=img.convert("RGBA").split().pop())
                img = bg
            elif img.mode == "P":
                img = img.convert("RGB")
            if pfmt == "JPEG":
                img.save(sp, format="JPEG", quality=100, subsampling=0)
            elif pfmt == "WEBP":
                img.save(sp, format="WEBP", lossless=True, quality=100)
            elif pfmt == "PNG":
                img.save(sp, format="PNG", optimize=True)
            else:
                img.save(sp, format=pfmt)
            messagebox.showinfo("Success", "Image converted and saved without quality loss!")
        except Exception as e:
            messagebox.showerror("Conversion Error", f"Details: {str(e)}")

    def setup_video_tab(self):
        self.vid_path = ""
        ctk.CTkButton(self.tab_video, text="Select Video", command=self.select_video, width=200).pack(pady=15)
        self.lbl_vid_name = ctk.CTkLabel(self.tab_video, text="No video selected", text_color="gray")
        self.lbl_vid_name.pack(pady=5)

        ctk.CTkLabel(self.tab_video, text="Output Format:", font=("Arial", 13, "bold")).pack(pady=(10, 5))
        self.vid_format_var = ctk.StringVar(value="mp4")
        ctk.CTkOptionMenu(self.tab_video, values=["mp4", "mkv", "avi", "mov", "webm"], variable=self.vid_format_var).pack(pady=5)

        ctk.CTkLabel(self.tab_video, text="Preset Resolution:", font=("Arial", 13, "bold")).pack(pady=(10, 5))
        self.vid_res_var = ctk.StringVar(value="Original (No Resize)")
        ctk.CTkOptionMenu(self.tab_video, values=["Original (No Resize)", "1080p (1920x1080)", "720p (1280x720)", "480p (854x480)", "Custom Size"], variable=self.vid_res_var).pack(pady=5)

        vsf = ctk.CTkFrame(self.tab_video, fg_color="transparent")
        vsf.pack(pady=5)
        self.entry_vid_w = ctk.CTkEntry(vsf, placeholder_text="Custom Width", width=110)
        self.entry_vid_w.pack(side="left", padx=5)
        self.entry_vid_h = ctk.CTkEntry(vsf, placeholder_text="Custom Height", width=110)
        self.entry_vid_h.pack(side="left", padx=5)

        self.lbl_vid_status = ctk.CTkLabel(self.tab_video, text="", text_color="yellow")
        self.lbl_vid_status.pack(pady=5)

        self.btn_convert_vid = ctk.CTkButton(self.tab_video, text="Convert & Save Video", fg_color="green", hover_color="darkgreen", command=self.start_video_thread, width=220, height=40)
        self.btn_convert_vid.pack(pady=10)

    def select_video(self):
        fp = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4;*.mkv;*.avi;*.mov;*.webm;*.flv")])
        if fp:
            self.vid_path = fp
            self.lbl_vid_name.configure(text=os.path.basename(fp), text_color="white")

    def start_video_thread(self):
        if not self.vid_path:
            messagebox.showerror("Error", "Please select a video first!")
            return
        threading.Thread(target=self.process_video, daemon=True).start()

    def process_video(self):
        tfmt = self.vid_format_var.get()
        rc = self.vid_res_var.get()
        rmap = {"1080p (1920x1080)": "1920:1080", "720p (1280x720)": "1280:720", "480p (854x480)": "854:480"}
        if rc == "Custom Size":
            vw, vh = self.entry_vid_w.get().strip(), self.entry_vid_h.get().strip()
            if not vw or not vh:
                messagebox.showerror("Error", "Enter both Custom Width and Height for video!")
                return
            res = f"{vw}:{vh}"
        elif rc in rmap:
            res = rmap.get(rc)
        else:
            res = None

        sp = filedialog.asksaveasfilename(defaultextension=f".{tfmt}", filetypes=[(f"{tfmt.upper()} File", f"*.{tfmt}")])
        if not sp:
            return

        self.lbl_vid_status.configure(text="Processing... Please wait...", text_color="yellow")
        self.btn_convert_vid.configure(state="disabled")

        try:
            if res is None:
                cmd = ["ffmpeg", "-y", "-i", self.vid_path, "-c", "copy", sp]
            else:
                cmd = ["ffmpeg", "-y", "-i", self.vid_path, "-vf", f"scale={res}", "-crf", "18", "-preset", "fast", sp]
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            self.lbl_vid_status.configure(text="Done! Video saved successfully.", text_color="lightgreen")
            messagebox.showinfo("Success", "Video converted and saved successfully!")
        except Exception:
            self.lbl_vid_status.configure(text="Conversion Failed!", text_color="red")
            messagebox.showerror("Error", "Failed to convert video. Make sure FFmpeg is installed properly.")
        finally:
            self.btn_convert_vid.configure(state="normal")

if __name__ == "__main__":
    app = MediaConverterApp()
    app.mainloop()
