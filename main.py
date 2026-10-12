import flet as ft
import requests
import os
import threading
import re

def main(page: ft.Page):
    page.title = "FastSaver"
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20

    link_input = ft.TextField(label="Paste Reel Link", width=320, multiline=True, value="https://www.instagram.com/reel/DeXVwH8oS-n/")
    status = ft.Text("", size=13, color=ft.Colors.GREEN, selectable=True)
    progress = ft.ProgressBar(width=320, visible=False)

    def get_shortcode(url):
        m = re.search(r"/(?:reel|p)/([A-Za-z0-9_-]+)", url)
        return m.group(1) if m else None

    def download_task(link):
        try:
            status.value = "Bypassing Cobalt..."
            status.color = ft.Colors.YELLOW
            progress.visible = True
            page.update()

            download_path = "/storage/emulated/0/Download"
            if not os.path.exists(download_path):
                download_path = "/tmp"

            shortcode = get_shortcode(link)
            link_clean = f"https://www.instagram.com/reel/{shortcode}/" if shortcode else link
            
            video_url = None

            # METHOD 1: SnapInsta API
            try:
                status.value = "Trying SnapInsta..."
                page.update()
                headers = {"User-Agent":"Mozilla/5.0","Content-Type":"application/x-www-form-urlencoded"}
                r = requests.post("https://snapinsta.app/action.php", data={"url":link_clean, "action":"post"}, headers=headers, timeout=20)
                print(r.text[:500])
                m = re.search(r'href="(https://[^"]+\.mp4[^"]*)"', r.text)
                if not m:
                    m = re.search(r'"downloadUrl":\s*"([^"]+)"', r.text)
                if m:
                    video_url = m.group(1).replace("\\/","/").replace("&amp;","&")
            except Exception as e:
                print(f"Snap fail {e}")

            # METHOD 2: SaveInsta / SaveIG
            if not video_url:
                try:
                    status.value = "Trying SaveInsta..."
                    page.update()
                    r = requests.post("https://saveinsta.app/api/ajaxSearch", data={"q":link_clean,"t":"media","lang":"en"}, headers={"User-Agent":"Mozilla/5.0","X-Requested-With":"XMLHttpRequest"}, timeout=20)
                    j = r.json()
                    html = j.get("data","")
                    m = re.search(r'href="(https://[^"]+\.mp4[^"]*)"', html)
                    if m:
                        video_url = m.group(1).replace("&amp;","&")
                        print(f"SaveInsta: {video_url[:100]}")
                except Exception as e:
                    print(f"SaveInsta fail {e}")

            # METHOD 3: DDInstagram CDN
            if not video_url:
                try:
                    status.value = "Trying DD proxy..."
                    page.update()
                    # ddinstagram gives direct mp4
                    dd_link = f"https://www.ddinstagram.com/reel/{shortcode}/"
                    r = requests.get(dd_link, headers={"User-Agent":"Mozilla/5.0"}, timeout=15, allow_redirects=True)
                    m = re.search(r'"contentUrl":\s*"([^"]+\.mp4[^"]*)"', r.text)
                    if not m:
                        m = re.search(r'property="og:video" content="([^"]+)"', r.text)
                    if m:
                        video_url = m.group(1)
                except Exception as e:
                    print(f"DD fail {e}")

            if not video_url:
                raise Exception("Servers busy - OPEN IN CHROME: saveig.app and paste link there - works 100% without app")

            status.value = "Downloading..."
            page.update()
            vr = requests.get(video_url, stream=True, timeout=30, headers={"User-Agent":"Mozilla/5.0","Referer":"https://www.instagram.com/"})
            file_name = f"FastSaver_{shortcode}.mp4"
            file_path = os.path.join(download_path, file_name)
            with open(file_path,"wb") as f:
                for chunk in vr.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            status.value = f"✅ SAVED! {file_name}"
            status.color = ft.Colors.GREEN
            progress.visible = False
            page.update()

        except Exception as e:
            status.value = f"❌ {str(e)[:350]}"
            status.color = ft.Colors.RED
            progress.visible = False
            page.update()

    def download_click(e):
        link = link_input.value.strip()
        if not link:
            return
        threading.Thread(target=download_task, args=(link,), daemon=True).start()

    page.add(
        ft.Text("FastSaver", size=32, weight=ft.FontWeight.BOLD),
        ft.Text("V47 - NO Cobalt, direct IG", size=14, color=ft.Colors.GREY),
        ft.Container(height=10),
        link_input,
        ft.Container(height=10),
        ft.ElevatedButton("DOWNLOAD", width=320, height=50, on_click=download_click),
        ft.Container(height=15),
        progress,
        status,
        ft.Text("If fail: Go to saveig.app in Chrome - no app needed", size=10, color=ft.Colors.GREY_400)
    )

ft.app(target=main)
