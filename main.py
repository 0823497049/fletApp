import flet as ft
import yt_dlp
import os
import threading
import requests

def main(page: ft.Page):
    page.title = "FastSaver"
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20

    link_input = ft.TextField(label="Paste TikTok / Instagram Link", width=320, multiline=True)
    status = ft.Text("", size=14, color=ft.Colors.GREEN)
    progress = ft.ProgressBar(width=320, visible=False)

    def download_with_backup(link):
        download_path = "/storage/emulated/0/Download"
        if not os.path.exists(download_path):
            download_path = "/tmp"

        # TRY 1: yt-dlp
        try:
            status.value = "Trying direct download..."
            progress.visible = True
            page.update()

            ydl_opts = {
                'outtmpl': f'{download_path}/FastSaver_%(title)s.%(ext)s',
                'format': 'mp4',
                'noplaylist': True,
                'quiet': True,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([link])

            status.value = "✅ Saved to Download folder!"
            status.color = ft.Colors.GREEN
            progress.visible = False
            page.update()
            return
        except Exception as e:
            print(f"yt-dlp failed: {e}")

        # TRY 2: TikWM API Backup for TikTok
        try:
            status.value = "TikTok blocked, trying backup server..."
            page.update()

            api_url = "https://www.tikwm.com/api/"
            data = {"url": link, "count": 12, "cursor": 0, "web": 1, "hd": 1}
            r = requests.post(api_url, data=data, timeout=20)
            res = r.json()

            if res.get("data") and res["data"].get("play"):
                video_url = res["data"]["play"]
                title = res["data"].get("title", "tiktok_video")[:30]

                # Download video file
                video_data = requests.get(video_url, timeout=30).content
                file_path = f"{download_path}/FastSaver_{title}.mp4"
                with open(file_path, "wb") as f:
                    f.write(video_data)

                status.value = "✅ Saved via backup server!"
                status.color = ft.Colors.GREEN
                progress.visible = False
                page.update()
                return
            else:
                raise Exception("Backup server no link")

        except Exception as e2:
            status.value = f"❌ Both failed: TikTok blocking. Try another link!"
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
        threading.Thread(target=download_with_backup, args=(link,), daemon=True).start()

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
