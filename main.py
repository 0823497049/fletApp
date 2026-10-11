import flet as ft
import yt_dlp
import os
import threading

def main(page: ft.Page):
    page.title = "FastSaver"
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20

    link_input = ft.TextField(
        label="Paste TikTok / Instagram Link",
        width=320,
        multiline=True
    )

    status = ft.Text("", size=14, color=ft.Colors.GREEN)
    progress = ft.ProgressBar(width=320, visible=False)

    def download_task(link):
        try:
            status.value = "Downloading... Please wait..."
            progress.visible = True
            page.update()

            # Download folder on Android
            download_path = "/storage/emulated/0/Download"
            if not os.path.exists(download_path):
                download_path = "/tmp"

            ydl_opts = {
                'outtmpl': f'{download_path}/FastSaver_%(title)s.%(ext)s',
                'format': 'mp4',
                'noplaylist': True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([link])

            status.value = "✅ Saved to Download folder!"
            status.color = ft.Colors.GREEN
            progress.visible = False
            page.update()

        except Exception as e:
            status.value = f"❌ Failed: {str(e)[:100]}"
            status.color = ft.Colors.RED
            progress.visible = False
            page.update()

    def download_click(e):
        link = link_input.value.strip()
        if not link:
            status.value = "Paste link first!"
            status.color = ft.Colors.RED
            page.update()
            return

        # Run in background so app doesn't freeze
        threading.Thread(target=download_task, args=(link,), daemon=True).start()

    page.add(
        ft.Text("FastSaver", size=32, weight=ft.FontWeight.BOLD),
        ft.Text("Download videos fast", size=14, color=ft.Colors.GREY),
        ft.Container(height=15),
        link_input,
        ft.Container(height=10),
        ft.ElevatedButton("DOWNLOAD", width=320, height=50, on_click=download_click),
        ft.Container(height=15),
        progress,
        status
    )

ft.app(target=main)
