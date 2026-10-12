import flet as ft
import os
import threading
import re
import yt_dlp

def main(page: ft.Page):
    page.title = "FastSaver"
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO

    link_input = ft.TextField(
        label="Paste Reel Link",
        hint_text="https://www.instagram.com/reel/...",
        width=340,
        multiline=True,
        min_lines=2,
        max_lines=4,
        value="https://www.instagram.com/reel/DeXVwH8oS-n/"
    )

    status = ft.Text("", size=13, color=ft.Colors.GREEN_300, selectable=True, width=340)
    progress = ft.ProgressBar(width=340, visible=False, color=ft.Colors.BLUE_400)
    log_box = ft.Text("", size=11, color=ft.Colors.GREY_400, selectable=True, width=340)

    def get_shortcode(url):
        m = re.search(r"/(?:reel|p|tv)/([A-Za-z0-9_-]+)", url)
        return m.group(1) if m else "video"

    def download_task(link):
        try:
            page.run_thread(lambda: None) # ensure thread
            status.value = "⏳ Starting download..."
            status.color = ft.Colors.YELLOW_300
            progress.visible = True
            log_box.value = f"Link: {link}\n"
            page.update()

            # Phone download folder
            download_path = "/storage/emulated/0/Download"
            if not os.path.exists(download_path):
                download_path = "/storage/emulated/0/DCIM"
            if not os.path.exists(download_path):
                download_path = os.getcwd()

            shortcode = get_shortcode(link)
            log_box.value += f"ID: {shortcode}\nPath: {download_path}\n"
            page.update()

            # yt-dlp config - this is what downloads Instagram
            ydl_opts = {
                'outtmpl': os.path.join(download_path, f'FastSaver_{shortcode}.%(ext)s'),
                'format': 'bestvideo+bestaudio/best',
                'merge_output_format': 'mp4',
                'quiet': True,
                'no_warnings': True,
                'noplaylist': True,
                'extractor_args': {'instagram': {'skip_auth': True}},
            }

            status.value = "📥 Downloading from Instagram CDN..."
            page.update()

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([link])

            status.value = f"✅ SAVED!\nFastSaver_{shortcode}.mp4\nCheck Gallery > Download"
            status.color = ft.Colors.GREEN_300
            log_box.value += f"\nDone! File: FastSaver_{shortcode}.mp4"
            progress.visible = False
            page.update()

        except Exception as e:
            err = str(e)
            log_box.value += f"\nError: {err[:500]}"
            if "private" in err.lower():
                status.value = "❌ Private account - can't download"
            elif "login" in err.lower() or "rate" in err.lower():
                status.value = "❌ Instagram limit. Wait 2 min and retry"
            else:
                status.value = f"❌ {err[:300]}"
            status.color = ft.Colors.RED_300
            progress.visible = False
            page.update()

    def on_download(e):
        link = link_input.value.strip()
        if not link:
            status.value = "⚠️ Paste link first!"
            status.color = ft.Colors.ORANGE_300
            page.update()
            return
        if "instagram.com" not in link:
            status.value = "⚠️ Not an Instagram link!"
            page.update()
            return
        threading.Thread(target=download_task, args=(link,), daemon=True).start()

    def on_clear(e):
        link_input.value = ""
        status.value = ""
        log_box.value = ""
        progress.visible = False
        page.update()

    page.add(
        ft.Text("FastSaver", size=36, weight=ft.FontWeight.BOLD),
        ft.Text("V48 - Your Own Downloader", size=14, color=ft.Colors.GREY_400),
        ft.Container(height=15),
        link_input,
        ft.Container(height=10),
        ft.ElevatedButton("DOWNLOAD", width=340, height=55, on_click=on_download, style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_700, color=ft.Colors.WHITE)),
        ft.TextButton("CLEAR", width=340, on_click=on_clear),
        ft.Container(height=10),
        progress,
        ft.Container(height=10),
        status,
        ft.Container(height=10),
        log_box,
    )

ft.app(target=main)
