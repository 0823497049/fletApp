import flet as ft
import os, threading, re, requests, datetime
import yt_dlp

MY_WA = "27823497049" # Your 0823497049
PRO_CODE = "PRO2026"

def main(page: ft.Page):
    page.title = "FastSaver Pro"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    link = ft.TextField(label="Paste Reel Link", hint_text="instagram.com/reel/...", width=340, multiline=True, border_color=ft.Colors.BLUE_400)
    unlock = ft.TextField(label="Enter PRO Code", width=340, visible=False)
    info = ft.Text("3 Free Downloads Per Day", size=12, color=ft.Colors.GREY_400, width=340, text_align=ft.TextAlign.CENTER)
    status = ft.Text("Ready", width=340, text_align=ft.TextAlign.CENTER, selectable=True, size=13)
    bar = ft.ProgressRing(width=30, height=30, visible=False)

    # WORKING PATH - NO PERMISSION NEEDED
    def get_path(name):
        base = os.getcwd()
        os.makedirs(base, exist_ok=True)
        return os.path.join(base, name)

    def is_pro():
        try:
            with open(get_path("pro.txt"), 'r') as f:
                return f.read().strip() == PRO_CODE
        except:
            return False

    def get_count():
        try:
            with open(get_path("data.txt"), 'r') as f:
                d, c = f.read().strip().split("|")
                if d == datetime.date.today().isoformat():
                    return int(c)
                return 0
        except:
            return 0

    def add_count():
        try:
            c = get_count() + 1
            with open(get_path("data.txt"), 'w') as f:
                f.write(f"{datetime.date.today().isoformat()}|{c}")
        except:
            pass

    def download_task(url):
        try:
            bar.visible = True
            status.value = "⏳ Getting link..."
            status.color = "white"
            page.update()

            sid = re.search(r"/(?:reel|p)/([A-Za-z0-9_-]+)", url)
            sid = sid.group(1) if sid else datetime.datetime.now().strftime("%H%M%S")

            opts = {'format':'best[ext=mp4]/best','quiet':True,'noplaylist':True,'skip_download':True}
            with yt_dlp.YoutubeDL(opts) as ydl:
                data = ydl.extract_info(url, download=False)
                if 'entries' in data: data = data['entries'][0]
                vurl = data.get('url')
                for fm in reversed(data.get('formats', [])):
                    if fm.get('ext')=='mp4' and fm.get('url'):
                        vurl = fm['url']
                        break

            save_to = get_path(f"FastSaver_{sid}.mp4")
            r = requests.get(vurl, stream=True, headers={'User-Agent':'Mozilla/5.0'}, timeout=90)
            with open(save_to, 'wb') as out:
                for chunk in r.iter_content(32768):
                    if chunk: out.write(chunk)

            add_count()
            bar.visible = False
            left = "UNLIMITED ♾️" if is_pro() else f"{3-get_count()} left today"
            info.value = f"✅ SAVED! {left}"
            status.value = f"{os.path.basename(save_to)}\nSaved inside app - Check Gallery"
            status.color = ft.Colors.GREEN_400
            page.update()
        except Exception as e:
            bar.visible = False
            status.value = f"❌ {str(e)[:400]}"
            status.color = ft.Colors.RED_400
            page.update()

    def show_paywall():
        def close(e):
            dlg.open=False
            page.update()
        def buy(e):
            page.launch_url(f"https://wa.me/{MY_WA}?text=Hi%20I%20want%20FastSaver%20PRO%20R29")
            close(e)
        dlg = ft.AlertDialog(
            title=ft.Text("Free Limit Reached - 3/3"),
            content=ft.Text("You used 3 free downloads today.\n\nGet UNLIMITED PRO for R29 once-off.\nWhatsApp: 0823497049\nYou get code: PRO2026"),
            actions=[ft.TextButton("Later", on_click=close), ft.ElevatedButton("GET PRO R29", bgcolor=ft.Colors.GREEN_700, color="white", on_click=buy)]
        )
        page.dialog=dlg
        dlg.open=True
        page.update()

    def on_download(e):
        if not is_pro() and get_count() >= 3:
            show_paywall()
            return
        url = link.value.strip()
        if "instagram.com" not in url:
            status.value="Paste valid Instagram link"
            status.color=ft.Colors.ORANGE_400
            page.update()
            return
        threading.Thread(target=download_task, args=(url,), daemon=True).start()

    def on_unlock(e):
        if unlock.value.strip() == PRO_CODE:
            with open(get_path("pro.txt"), 'w') as f:
                f.write(PRO_CODE)
            info.value = "✅ PRO UNLOCKED - UNLIMITED ♾️"
            info.color = ft.Colors.GREEN_400
            unlock.visible=False
            btn_unlock.visible=False
            status.value="PRO Active! Restart app"
            status.color=ft.Colors.GREEN_400
            page.update()
        else:
            status.value="Wrong code. WhatsApp 0823497049 for correct code"
            status.color=ft.Colors.RED_400
            page.update()

    def open_wa(e):
        page.launch_url(f"https://wa.me/{MY_WA}?text=Hi%20I%20want%20FastSaver%20PRO%20R29%20-%20My%20code?")

    btn_dl = ft.ElevatedButton("DOWNLOAD REEL", icon=ft.Icons.DOWNLOAD, width=340, height=60, bgcolor="#1565C0", color="white", style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=15), text_style=ft.TextStyle(size=18, weight=ft.FontWeight.BOLD)), on_click=on_download)
    btn_buy = ft.OutlinedButton("UNLOCK PRO R29 - 0823497049", width=340, height=45, style=ft.ButtonStyle(color=ft.Colors.GREEN_400), on_click=open_wa)
    btn_unlock = ft.ElevatedButton("ACTIVATE PRO", width=340, height=40, bgcolor=ft.Colors.GREEN_800, color="white", on_click=on_unlock, visible=False)

    # Show unlock field if they click buy
    def show_unlock_field(e):
        unlock.visible=True
        btn_unlock.visible=True
        page.update()
        open_wa(e)

    btn_buy.on_click = show_unlock_field

    if is_pro():
        info.value="✅ PRO UNLIMITED ♾️ Active"
        info.color=ft.Colors.GREEN_400
    else:
        info.value=f"Free: {3-get_count()} left today - PRO R29"

    page.add(ft.Column([
        ft.Icon(ft.Icons.VIDEO_LIBRARY, size=55, color=ft.Colors.BLUE_400),
        ft.Text("FastSaver", size=34, weight=ft.FontWeight.BOLD),
        info,
        ft.Container(height=15),
        link,
        ft.Container(height=10),
        btn_dl,
        ft.Container(height=8),
        btn_buy,
        unlock,
        btn_unlock,
        ft.Container(height=15),
        bar,
        status,
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER))

ft.app(main)
