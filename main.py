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

    link_input = ft.TextField(label="Paste TikTok / Instagram Link", width=320, multiline=True, value="https://vt.tiktok.com/ZSb3HbhXD/")
    status = ft.Text("", size=14, color=ft.Colors.GREEN)
    progress = ft.ProgressBar(width=320, visible=False)

    def download_task(link):
        try:
            status.value = "Resolving TikTok link..."
            status.color = ft.Colors.YELLOW
            progress.visible = True
            page.update()

            # Resolve short vt.tiktok.com link
            try:
                r = requests.head(link, allow_redirects=True, timeout=10)
                if r.url!= link:
                    link = r.url
                    print(f"Resolved to: {link}")
            except:
                pass

            download_path = "/storage/emulated/0/Download"
            if not os.path.exists(download_path):
                download_path = "/tmp"

            # NEW COBALT API LIST - main is co.wuk.sh
            apis = [
                "https://co.wuk.sh/api/json",
                "https://api.cobalt.blackcat.sweeux.org",
                "https://cobalt.meowing.de",
            ]

            video_url = None
            for api_url in apis:
                try:
                    status.value = f"Trying {api_url.split('/')[2]}..."
                    page.update()
                    headers = {"Accept": "application/json", "Content-Type": "application/json"}
                    payload = {"url": link}
                    resp = requests.post(api_url, json=payload, headers=headers, timeout=20)
                    data = resp.json()
                    print(f"{api_url} => {data}")

                    video_url = data.get("url")
                    if not video_url and data.get("picker"):
                        video_url = data["picker"][0].get("url")
                    if not video_url and isinstance(data.get("data"), dict):
                        video_url = data["data"].get("url")

                    if video_url:
                        break
                except Exception as e:
                    print(f"{api_url} failed: {e}")
                    continue

            if not video_url:
                raise Exception("All Cobalt servers busy - try again in 1 min")

            status.value = "Downloading video..."
            page.update()

            video_resp = requests.get(video_url, stream=True, timeout=30)
            file_name = f"FastSaver_{os.urandom(3).hex()}.mp4"
            file_path = os.path.join(download_path, file_name)

            with open(file_path, "wb") as f:
                for chunk in video_resp.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            status.value = f"✅ SAVED! {file_name}"
            status.color = ft.Colors.GREEN
            progress.visible = False
            page.update()

        except Exception as e:
            status.value = f"❌ {str(e)[:150]}"
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
