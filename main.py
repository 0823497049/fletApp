import flet as ft
import os, threading, re, requests, datetime
import yt_dlp

MY_WHATSAPP = "27823497049"

def main(page: ft.Page):
    page.title = "FastSaver Pro"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    link = ft.TextField(
        label="Paste Reel Link",
        hint_text="instagram.com/reel/...",
        width=340,
        multiline=True,
        border_color=ft.Colors.BLUE_400
    )

    info = ft.Text("3 Free Downloads Per Day", size=12, color=ft.Colors.GREY_400, width=340, text_align=ft.TextAlign.CENTER)
    status = ft.Text("", width=340, text_align=ft.TextAlign.CENTER, selectable=True, size=13)
    bar = ft.ProgressRing(width=30, height=30, visible=False)

    def get_today_count():
        try:
            path = "/storage/emulated/0/Download/fastsaver_data.txt"
            if not os.path.exists(path):
                return 0
            with open(path, 'r') as f:
                data = f.read().strip().split("|")
                if data[0] == datetime.date.today().isoformat():
                    return int(data[1])
                return 0
        except:
            return 0

    def add_count():
        try:
            path = "/storage/emulated/0/Download/fastsaver_data.txt"
            today = datetime.date.today().isoformat()
            count = get_today_count() + 1
            with open(path, 'w') as f:
                f.write(f"{today}|{count}")
            return count
        except:
            return 0

    def download_task(url):
        try:
            bar.visible = True
            info.value = "Downloading..."
            status.value = ""
            page.update()

            folder = "/storage/emulated/0/Download"
            os.makedirs(folder, exist_ok=True)
            sid = re.search(r"/(?:reel|p)/([A-Za-z0-9_-]+)", url)
            sid = sid.group(1) if sid else datetime.datetime.now().strftime("%H%M%S")

            opts = {'format': 'best[ext=mp4]/best', 'quiet': True, 'noplaylist': True, 'skip_download': True}
            with yt_dlp.YoutubeDL(opts) as ydl:
                data = ydl.extract_info(url, download=False)
                if 'entries' in data:
                    data = data['entries'][0]
                video_url = data.get('url')
                if 'formats' in data:
                    for f in reversed(data['formats']):
                        if f.get('ext') == 'mp4' and f.get('url'):
                            video_url = f['url']
                            break

            full_path = os.path.join(folder, f"FastSaver_{sid}.mp4")
            r = requests.get(video_url, stream=True, headers={'User-Agent':'Mozilla/5.0'}, timeout=60)
            with open(full_path, 'wb') as f:
                for c in r.iter_content(32768):
                    if c:
                        f.write(c)

            add_count()
            left = 3 - get_today_count()
            bar.visible = False
            info.value = f"✅ SAVED! {left} free left today"
            status.value = f"FastSaver_{sid}.mp4 in Download"
            status.color = ft.Colors.GREEN_400
            page.update()

        except Exception as e:
            bar.visible = False
            info.value = "❌ Failed"
            status.value = str(e)[:400]
            status.color = ft.Colors.RED_400
            page.update()

    def on_download(e):
        if get_today_count() >= 3:
            def close_dlg(e):
                dlg.open = False
                page.update()
            def buy_pro(e):
                page.launch_url(f"https://wa.me/{MY_WHATSAPP}?text=Hi%20I%20want%20FastSaver%20PRO%20Unlimited%20R29")
                close_dlg(e)
            dlg = ft.AlertDialog(
                title=ft.Text("Free Limit Reached"),
                content=ft.Text("You used 3 free downloads today.\n\nGet UNLIMITED PRO for R29 once.\nWhatsApp: 0823497049"),
                actions=[
                    ft.TextButton("Later", on_click=close_dlg),
                    ft.ElevatedButton("GET PRO R29", bgcolor=ft.Colors.GREEN_600, color="white", on_click=buy_pro),
                ]
            )
            page.dialog = dlg
            dlg.open = True
            page.update()
            return

        url = link.value.strip()
        if "instagram.com" not in url:
            status.value = "Paste valid Instagram link"
            status.color = ft.Colors.ORANGE_400
            page.update()
            return
        threading.Thread(target=download_task, args=(url,), daemon=True).start()

    def open_wa(e):
        page.launch_url(f"https://wa.me/{MY_WHATSAPP}?text=Hi%20I%20want%20FastSaver%20App")

    btn_dl = ft.ElevatedButton(
        "DOWNLOAD REEL", icon=ft.Icons.DOWNLOAD,
        width=340, height=60, bgcolor="#1565C0", color="white",
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=15), text_style=ft.TextStyle(size=18, weight=ft.FontWeight.BOLD)),
        on_click=on_download
    )

    btn_buy = ft.OutlinedButton(
        "UNLOCK PRO R29 - WhatsApp 0823497049", width=340, height=45,
        style=ft.ButtonStyle(color=ft.Colors.GREEN_400),
        on_click=open_wa
    )

    page.add(
        ft.Column([
            ft.Icon(ft.Icons.VIDEO_LIBRARY, size=55, color=ft.Colors.BLUE_400),
            ft.Text("FastSaver", size=34, weight=ft.FontWeight.BOLD),
            ft.Text(f"Free: {3-get_today_count()} left today", size=12, color=ft.Colors.AMBER_300),
            ft.Container(height=15),
            link,
            ft.Container(height=10),
            btn_dl,
            ft.Container(height=8),
            btn_buy,
            ft.Container(height=15),
            bar,
            info,
            status,
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )

ft.app(main)
