import flet as ft
import os, threading, re
import yt_dlp

def main(page: ft.Page):
    page.title = "FastSaver"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO

    link_input = ft.TextField(label="Paste Reel Link", width=340, multiline=True, value="https://www.instagram.com/reel/DeXVwH8oS-n/")
    status = ft.Text("", size=13, width=340, selectable=True, color=ft.Colors.GREEN_300)
    progress = ft.ProgressBar(width=340, visible=False)

    def get_id(url):
        m=re.search(r"/(?:reel|p)/([A-Za-z0-9_-]+)", url)
        return m.group(1) if m else "reel"

    def task(link):
        try:
            progress.visible=True
            status.value="⏳ Downloading..."
            page.update()
            save_dir="/storage/emulated/0/Download"
            os.makedirs(save_dir, exist_ok=True)
            sid=get_id(link)

            # FIXED - NO FFMPEG NEEDED
            ydl_opts = {
                'outtmpl': os.path.join(save_dir, f'FastSaver_{sid}.%(ext)s'),
                'format': 'best[ext=mp4]/best', # single file, no merge
                'quiet': True,
                'noplaylist': True,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([link])

            status.value=f"✅ DONE!\nFastSaver_{sid}.mp4 saved in Download\nCheck Gallery!"
            status.color=ft.Colors.GREEN_300
            progress.visible=False
            page.update()
        except Exception as e:
            status.value=f"❌ {str(e)[:600]}"
            status.color=ft.Colors.RED_300
            progress.visible=False
            page.update()

    def on_download(e):
        threading.Thread(target=task, args=(link_input.value.strip(),), daemon=True).start()

    page.add(
        ft.Text("FastSaver", size=32, weight=ft.FontWeight.BOLD),
        ft.Text("V50 - No FFmpeg Fix", size=13, color=ft.Colors.GREY),
        ft.Container(height=15),
        link_input,
        ft.Container(height=15),
        ft.ElevatedButton("DOWNLOAD", width=340, height=55, on_click=on_download),
        ft.TextButton("CLEAR", width=340, on_click=lambda e: (setattr(link_input,'value',''), page.update())),
        ft.Container(height=15),
        progress,
        status
    )

ft.app(target=main)
