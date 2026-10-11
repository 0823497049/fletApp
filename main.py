import flet as ft
import requests
import os
import threading

def main(page: ft.Page):
    page.title = "FastSaver"
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20

    link_input = ft.TextField(label="Paste TikTok / Instagram Link", width=320, multiline=True)
    status = ft.Text("", size=14, color=ft.Colors.GREEN)
    progress = ft.ProgressBar(width=320, visible=False)

    def download_task(link):
        try:
            status.value = "Connecting to Cobalt server..."
            status.color = ft.Colors.YELLOW
            progress.visible = True
            page.update()

            download_path = "/storage/emulated/0/Download"
            if not os.path.exists(download_path):
                download_path = "/tmp"

            # COBALT API - works when TikTok blocks yt-dlp
            api_url = "https://api.cobalt.tools/api/json"
            headers = {"Accept": "application/json", "Content-Type": "application/json"}
            payload = {"url": link}

            r = requests.post(api_url, json=payload, headers=headers, timeout=20)
            data = r.json()
            print(f"Cobalt response: {data}")

            video_url = data.get("url") or data.get("data", {}).get("url")

            # Sometimes cobalt returns picker
            if not video_url and data.get("picker"):
                video_url = data["picker"][0].get("url")

            if not video_url:
                raise Exception(f"No video url: {data}")

            status.value = "Downloading video..."
            page.update()

            # Download video file
            video_resp = requests.get(video_url, stream=True, timeout=30)
            file_name = f"FastSaver_{os.urandom(4).hex()}.mp4"
            file_path = os.path.join(download_path, file_name)

            with open(file_path, "wb") as f:
                for chunk in video_resp.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            status.value = f"✅ Saved! {file_name}"
            status.color = ft.Colors.GREEN
            progress.visible = False
            page.update()

        except Exception as e:
            status.value = f"❌ Error: {str(e)[:120]}"
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
