import os

# ============ High-DPI env vars — MUST be set before any PyQt import ============
os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
os.environ["QT_SCALE_FACTOR_ROUNDING_POLICY"] = "PassThrough"

import sys
import ctypes
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont

import config as cfg
from ui import Overlay, make_app_icon
from window import MainWin


class Hotkeys:
    def __init__(self, on_toggle, on_exit):
        self.on_toggle, self.on_exit = on_toggle, on_exit
        self._f8 = self._f9 = False
        if sys.platform != "win32":
            return
        self.t = QTimer()
        self.t.timeout.connect(self._check)
        self.t.start(50)

    def _check(self):
        try:
            f8 = bool(ctypes.windll.user32.GetAsyncKeyState(0x77) & 0x8000)
            f9 = bool(ctypes.windll.user32.GetAsyncKeyState(0x78) & 0x8000)
        except Exception:
            return
        if f8 and not self._f8:
            self.on_toggle()
        if f9 and not self._f9:
            self.on_exit()
        self._f8, self._f9 = f8, f9


def main():
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    font_family = cfg.ensure_vazir_font()
    f = QFont(font_family)
    f.setPointSize(10)
    f.setHintingPreference(QFont.PreferFullHinting)
    f.setStyleStrategy(QFont.PreferAntialias)
    app.setFont(f)

    config = cfg.load_config()
    cfg.apply_theme(config["preferences"].get("theme", "dark"))

    icon = make_app_icon()
    app.setWindowIcon(icon)

    overlay = Overlay(config["settings"])
    overlay.setVisible(not config["preferences"].get("start_hidden", False))

    panel = MainWin(overlay, config)
    panel.setWindowIcon(icon)
    p = config["preferences"]
    if p.get("tray_start_minimized"):
        panel.showMinimized()
    else:
        panel.show()

    if p.get("tray_enabled", True):
        C = cfg.C
        tray = QSystemTrayIcon(icon, app)
        panel.tray = tray
        tray.setToolTip(cfg.T(panel.lang, "tray_tip"))
        menu = QMenu()
        menu.setStyleSheet(f"""
            QMenu {{ background:{C['surface']}; color:{C['text']};
                    border:1px solid {C['border']}; border-radius:8px; padding:6px; }}
            QMenu::item {{ padding:8px 20px; border-radius:6px; }}
            QMenu::item:selected {{ background:{C['accent_bg']}; color:{C['accent']}; }}
            QMenu::separator {{ background:{C['border']}; height:1px; margin:4px 8px; }}
        """)
        panel._act_open = menu.addAction(cfg.T(panel.lang, "tray_open"))
        panel._act_toggle = menu.addAction(cfg.T(panel.lang, "tray_toggle"))
        menu.addSeparator()
        panel._act_quit = menu.addAction(cfg.T(panel.lang, "tray_quit"))
        panel._act_open.triggered.connect(
            lambda: (panel.show(), panel.raise_(), panel.activateWindow()))
        panel._act_toggle.triggered.connect(panel.toggle)
        panel._act_quit.triggered.connect(app.quit)
        tray.setContextMenu(menu)
        tray.activated.connect(
            lambda r: (panel.show(), panel.raise_(), panel.activateWindow())
            if r == QSystemTrayIcon.Trigger else None)
        tray.show()

    Hotkeys(panel.toggle, app.quit)

    def on_quit():
        if config["preferences"].get("auto_save", True):
            config["settings"] = dict(overlay.settings)
            cfg.save_config(config)
    app.aboutToQuit.connect(on_quit)

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()