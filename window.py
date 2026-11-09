from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QStackedWidget, QFrame, QLabel, QPushButton, QScrollArea, QSizeGrip,
    QSystemTrayIcon,
)
from PyQt5.QtCore import Qt

import config
from config import C, T, T_sub
from ui import SidebarButton, SliderRow, ToggleSwitch
from pages import (
    CrosshairPageMixin, InterfacePageMixin, SystemPageMixin, ProfilesPageMixin,
)


class MainWin(CrosshairPageMixin, InterfacePageMixin,
              SystemPageMixin, ProfilesPageMixin, QMainWindow):
    def __init__(self, overlay, config):
        super().__init__()
        self.overlay = overlay
        self.config = config
        self.lang = config["preferences"].get("language", "fa")
        self.tray = None
        self._drag = None
        self._is_maximized = False
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)

        avail = QApplication.primaryScreen().availableGeometry()
        w = min(1040, int(avail.width() * 0.85))
        h = min(780, int(avail.height() * 0.85))
        self.resize(w, h)
        self.setMinimumSize(700, 500)

        self._build()
        self._apply_lang()
        self._sync()
        self.move(avail.x() + (avail.width() - w) // 2,
                  avail.y() + (avail.height() - h) // 2)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        if hasattr(self, "_grip") and self._grip is not None:
            self._grip.move(self.width() - 22, self.height() - 22)
            self._grip.raise_()

    def _toggle_max(self):
        if self._is_maximized:
            self.showNormal()
            self._is_maximized = False
        else:
            self.showMaximized()
            self._is_maximized = True

    def _base_stylesheet(self):
        return f"""
            QComboBox {{
                background: {C['surface2']}; color: {C['text']};
                border: 1px solid {C['border']}; border-radius: 8px;
                padding: 6px 10px; min-height: 22px;
            }}
            QComboBox:hover {{ border-color: {C['border_h']}; }}
            QComboBox::drop-down {{ border: none; width: 20px; }}
            QComboBox QAbstractItemView {{
                background: {C['surface']}; color: {C['text']};
                border: 1px solid {C['border']}; border-radius: 6px;
                selection-background-color: {C['accent_bg']};
                selection-color: {C['accent']}; outline: none; padding: 4px;
            }}
            QSpinBox {{
                background: {C['surface2']}; color: {C['text']};
                border: 1px solid {C['border']}; border-radius: 6px;
                padding: 4px 8px;
            }}
            QToolTip {{
                background: {C['surface']}; color: {C['text']};
                border: 1px solid {C['border']}; padding: 4px; border-radius: 4px;
            }}
            QMessageBox, QInputDialog {{ background: {C['surface']}; }}
            QMessageBox QLabel, QInputDialog QLabel {{ color: {C['text']}; }}
        """

    def _build(self):
        central = QWidget()
        central.setObjectName("root")
        central.setStyleSheet(f"QWidget#root {{ background: {C['bg']}; }}")
        self.setCentralWidget(central)
        self.setStyleSheet(self._base_stylesheet())

        root = QVBoxLayout(central)
        root.setContentsMargins(1, 1, 1, 1)
        root.setSpacing(0)

        wrap = QFrame()
        wrap.setObjectName("wrap")
        wrap.setStyleSheet(f"""
            QFrame#wrap {{ background: {C['bg']}; border: 1px solid {C['border']};
                          border-radius: 12px; }}
        """)
        wl = QVBoxLayout(wrap)
        wl.setContentsMargins(0, 0, 0, 0)
        wl.setSpacing(0)
        wl.addWidget(self._build_titlebar())

        body = QWidget()
        bl = QHBoxLayout(body)
        bl.setContentsMargins(0, 0, 0, 0)
        bl.setSpacing(0)
        bl.addWidget(self._build_sidebar())
        self.stack = QStackedWidget()
        self.stack.addWidget(self._page_crosshair())
        self.stack.addWidget(self._page_interface())
        self.stack.addWidget(self._page_system())
        self.stack.addWidget(self._page_profiles())
        bl.addWidget(self.stack, 1)
        wl.addWidget(body, 1)
        root.addWidget(wrap)

        self._grip = QSizeGrip(central)
        self._grip.setFixedSize(16, 16)
        self._grip.move(self.width() - 22, self.height() - 22)
        self._grip.raise_()

    def _build_titlebar(self):
        bar = QFrame()
        bar.setFixedHeight(58)
        bar.setStyleSheet(f"background: {C['surface']}; border-top-left-radius:12px;"
                          f"border-top-right-radius:12px; border-bottom:1px solid {C['border']};")
        lay = QHBoxLayout(bar)
        lay.setContentsMargins(20, 0, 12, 0)
        lay.setSpacing(12)
        logo = QLabel("◈")
        logo.setStyleSheet(f"color:{C['accent']};font-size:22px;font-weight:bold;background:transparent;")
        self.lbl_app = QLabel()
        self.lbl_app.setStyleSheet(f"color:{C['text']};font-size:14px;font-weight:700;background:transparent;")
        self.lbl_tag = QLabel()
        self.lbl_tag.setStyleSheet(f"color:{C['text3']};font-size:12px;background:transparent;")
        lay.addWidget(logo)
        lay.addWidget(self.lbl_app)
        lay.addWidget(self.lbl_tag)
        lay.addStretch()
        btn_min = self._win_btn("−")
        btn_min.clicked.connect(self.showMinimized)
        btn_max = self._win_btn("□")
        btn_max.clicked.connect(self._toggle_max)
        btn_close = self._win_btn("✕", danger=True)
        btn_close.clicked.connect(self.close)
        lay.addWidget(btn_min)
        lay.addWidget(btn_max)
        lay.addWidget(btn_close)
        bar.mousePressEvent = self._bar_press
        bar.mouseMoveEvent = self._bar_move
        bar.mouseReleaseEvent = self._bar_release
        return bar

    def _win_btn(self, text, danger=False):
        b = QPushButton(text)
        b.setFixedSize(34, 34)
        b.setCursor(Qt.PointingHandCursor)
        hover_bg = C["danger_bg"] if danger else C["surface2"]
        hover_c = C["danger"] if danger else C["text"]
        b.setStyleSheet(f"""
            QPushButton {{ background:transparent; border:none; border-radius:8px;
                          color:{C['text2']}; font-size:16px; }}
            QPushButton:hover {{ background:{hover_bg}; color:{hover_c}; }}
        """)
        return b

    def _bar_press(self, e):
        if e.button() == Qt.LeftButton and not self._is_maximized:
            self._drag = e.globalPos() - self.frameGeometry().topLeft()

    def _bar_move(self, e):
        if self._drag and (e.buttons() & Qt.LeftButton):
            self.move(e.globalPos() - self._drag)

    def _bar_release(self, e):
        self._drag = None

    def _build_sidebar(self):
        w = QFrame()
        w.setFixedWidth(220)
        w.setStyleSheet(f"background:{C['surface']}; border-right:1px solid {C['border']};"
                        f"border-bottom-left-radius:12px;")
        lay = QVBoxLayout(w)
        lay.setContentsMargins(12, 18, 12, 18)
        lay.setSpacing(4)
        self.nav = []
        items = [("crosshair", "nav_cross"), ("palette", "nav_ui"),
                 ("gear", "nav_sys"), ("layers", "nav_prof")]
        for i, (icon, key) in enumerate(items):
            btn = SidebarButton(icon, "")
            btn.clicked.connect(lambda _, idx=i: self._switch_page(idx))
            self.nav.append((btn, key))
            lay.addWidget(btn)
        self.nav[0][0].setChecked(True)
        lay.addStretch()

        hotkey_card = QFrame()
        hotkey_card.setStyleSheet(f"background:{C['surface2']};border-radius:10px;")
        hl = QVBoxLayout(hotkey_card)
        hl.setContentsMargins(14, 12, 14, 12)
        hl.setSpacing(6)
        self.lbl_hk_title = QLabel()
        self.lbl_hk_title.setStyleSheet(
            f"color:{C['text3']};font-size:10px;font-weight:700;letter-spacing:1px;background:transparent;")
        self.lbl_hk1 = QLabel()
        self.lbl_hk1.setStyleSheet(f"color:{C['text2']};font-size:11px;background:transparent;")
        self.lbl_hk2 = QLabel()
        self.lbl_hk2.setStyleSheet(f"color:{C['text2']};font-size:11px;background:transparent;")
        hl.addWidget(self.lbl_hk_title)
        hl.addWidget(self.lbl_hk1)
        hl.addWidget(self.lbl_hk2)
        lay.addWidget(hotkey_card)
        return w

    def _switch_page(self, idx):
        for i, (btn, _) in enumerate(self.nav):
            btn.setChecked(i == idx)
        self.stack.setCurrentIndex(idx)

    def _page_wrapper(self):
        w = QWidget()
        outer = QVBoxLayout(w)
        outer.setContentsMargins(0, 0, 0, 0)
        sa = QScrollArea()
        sa.setWidgetResizable(True)
        sa.setFrameShape(QFrame.NoFrame)
        sa.setStyleSheet(f"""
            QScrollArea {{ background:{C['bg']}; border:none; }}
            QScrollBar:vertical {{ background:transparent; width:8px; }}
            QScrollBar::handle:vertical {{ background:{C['border_h']}; border-radius:4px; min-height:30px; }}
            QScrollBar::handle:vertical:hover {{ background:{C['accent']}; }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height:0; }}
        """)
        inner = QWidget()
        inner.setStyleSheet(f"background:{C['bg']};")
        v = QVBoxLayout(inner)
        v.setContentsMargins(28, 24, 28, 24)
        v.setSpacing(16)
        sa.setWidget(inner)
        outer.addWidget(sa)
        return w, v

    def _page_header(self, v, title_key, sub_key):
        t = QLabel()
        t.setStyleSheet(f"color:{C['text']};font-size:24px;font-weight:700;background:transparent;")
        s = QLabel()
        s.setStyleSheet(f"color:{C['text3']};font-size:13px;background:transparent;")
        t.setProperty("key", title_key)
        s.setProperty("key", sub_key)
        v.addWidget(t)
        v.addWidget(s)
        return t, s

    def _card_title(self, card, key):
        lbl = QLabel()
        lbl.setStyleSheet(f"color:{C['text']};font-size:14px;font-weight:700;background:transparent;")
        lbl.setProperty("key", key)
        card.v.insertWidget(0, lbl)
        return lbl

    def _slider(self, card, label_key, mn, mx, val, suffix=""):
        r = SliderRow("", mn, mx, val, suffix)
        r.lbl.setProperty("key", label_key)
        card.v.addWidget(r)
        return r

    def _toggle_row(self, card, label_key, default, desc_key=None):
        row = QWidget()
        h = QHBoxLayout(row)
        h.setContentsMargins(0, 0, 0, 0)
        v = QVBoxLayout()
        v.setContentsMargins(0, 0, 0, 0)
        v.setSpacing(2)
        lbl = QLabel()
        lbl.setStyleSheet(f"color:{C['text']};font-size:13px;font-weight:500;background:transparent;")
        lbl.setProperty("key", label_key)
        v.addWidget(lbl)
        if desc_key:
            d = QLabel()
            d.setStyleSheet(f"color:{C['text3']};font-size:11px;background:transparent;")
            d.setProperty("key", desc_key)
            v.addWidget(d)
        h.addLayout(v)
        h.addStretch()
        t = ToggleSwitch(default)
        h.addWidget(t)
        card.v.addWidget(row)
        return t

    def _primary_btn(self):
        b = QPushButton()
        b.setMinimumHeight(42)
        b.setCursor(Qt.PointingHandCursor)
        b.setStyleSheet(f"""
            QPushButton {{ background:{C['accent']}; border:none; border-radius:10px;
                          color:#ffffff; font-weight:600; font-size:13px; }}
            QPushButton:hover {{ background:{C['accent_h']}; }}
        """)
        return b

    def _secondary_btn(self):
        b = QPushButton()
        b.setMinimumHeight(42)
        b.setCursor(Qt.PointingHandCursor)
        b.setStyleSheet(f"""
            QPushButton {{ background:{C['surface']}; border:1px solid {C['border']};
                          border-radius:10px; color:{C['text']}; font-weight:600; font-size:13px; }}
            QPushButton:hover {{ background:{C['surface2']}; border-color:{C['border_h']}; }}
        """)
        return b

    # ---------- i18n / sync ----------
    def _apply_lang(self):
        s = lambda k: T(self.lang, k)
        self.lbl_app.setText(s("app"))
        self.lbl_tag.setText(s("tag"))
        self.t_cross.setText(s("page_cross"))
        self.s_cross.setText(s("page_cross_sub"))
        self.t_ui.setText(s("page_ui"))
        self.s_ui.setText(s("page_ui_sub"))
        self.t_sys.setText(s("page_sys"))
        self.s_sys.setText(s("page_sys_sub"))
        self.t_prof.setText(s("page_prof"))
        self.s_prof.setText(s("page_prof_sub"))
        for btn, key in self.nav:
            btn.text_lbl.setText(s(key))
        self.lbl_hk_title.setText(s("hotkeys"))
        self.lbl_hk1.setText(s("hk1"))
        self.lbl_hk2.setText(s("hk2"))
        for lbl in self.findChildren(QLabel):
            k = lbl.property("key")
            if k:
                lbl.setText(s(k))
        for key, btn in self.preset_btns.items():
            btn.setText(T_sub(self.lang, "presets", key))
        for key, btn in self.style_btns.items():
            btn.setText(T_sub(self.lang, "styles", key))
        self.combo_close.blockSignals(True)
        self.combo_close.clear()
        for k, lk in (("hide", "act_hide"), ("min", "act_min"), ("quit", "act_quit")):
            self.combo_close.addItem(s(lk), k)
        self.combo_close.blockSignals(False)
        self._update_color_btn()
        self.btn_reset.setText(s("btn_reset"))
        self.btn_about.setText(s("btn_about"))
        self.btn_save_prof.setText(s("btn_save_prof"))
        self.btn_load.setText(s("btn_load"))
        self.btn_rename.setText(s("btn_rename"))
        self.btn_delete.setText(s("btn_delete"))
        self.lbl_no_prof.setText(s("no_prof"))
        self.lbl_font_loaded.setText(
            T(self.lang, "font_loaded").replace("{font}", config.LOADED_FONT_FAMILY))
        self._update_toggle_btn(self.overlay.isVisible())

    def _sync(self):
        st = self.overlay.settings
        p = self.config["preferences"]
        for k, btn in self.style_btns.items():
            btn.blockSignals(True)
            btn.setChecked(k == st["style"])
            btn.blockSignals(False)
        self.sl_size.setValue(st["size"])
        self.sl_thick.setValue(st["thickness"])
        self.sl_gap.setValue(st["gap"])
        self.sl_rot.setValue(st["rotation"])
        self.sl_opacity.setValue(st["opacity"])
        for tog, key in ((self.tog_outline, "outline"), (self.tog_glow, "glow"),
                         (self.tog_dot, "dot"), (self.tog_aa, "anti_aliasing")):
            tog.blockSignals(True)
            tog.setChecked(st[key])
            tog.blockSignals(False)
        self.sl_ow.setValue(st["outline_width"])
        self.sl_gi.setValue(st["glow_intensity"])
        self.sl_ox.setValue(st["offset_x"])
        self.sl_oy.setValue(st["offset_y"])
        for i in range(self.combo_lang.count()):
            if self.combo_lang.itemData(i) == self.lang:
                self.combo_lang.blockSignals(True)
                self.combo_lang.setCurrentIndex(i)
                self.combo_lang.blockSignals(False)
                break
        for tog, key in ((self.tog_theme, None), (self.tog_tray, "tray_enabled"),
                         (self.tog_notif, "tray_notifications"),
                         (self.tog_startmin, "tray_start_minimized"),
                         (self.tog_autosave, "auto_save"),
                         (self.tog_starthidden, "start_hidden")):
            val = p.get("theme", "dark") == "dark" if key is None else p[key]
            tog.blockSignals(True)
            tog.setChecked(val)
            tog.blockSignals(False)
        for i in range(self.combo_close.count()):
            if self.combo_close.itemData(i) == p["close_action"]:
                self.combo_close.blockSignals(True)
                self.combo_close.setCurrentIndex(i)
                self.combo_close.blockSignals(False)
                break
        self.combo_screen.blockSignals(True)
        self.combo_screen.clear()
        for i in range(len(QApplication.screens())):
            self.combo_screen.addItem(
                T(self.lang, "screen_n").replace("{n}", str(i + 1)), i)
        for i in range(self.combo_screen.count()):
            if self.combo_screen.itemData(i) == st["screen_index"]:
                self.combo_screen.setCurrentIndex(i)
                break
        self.combo_screen.blockSignals(False)
        self._update_color_btn()
        self._update_toggle_btn(self.overlay.isVisible())

    def _update(self, **kw):
        self.overlay.settings.update(kw)
        self.overlay.update()
        self.preview.update()

    def toggle(self):
        v = not self.overlay.isVisible()
        self.overlay.setVisible(v)
        self._update_toggle_btn(v)
        p = self.config["preferences"]
        if p.get("tray_enabled") and p.get("tray_notifications") and self.tray:
            self.tray.showMessage(T(self.lang, "tray_tip"),
                                   T(self.lang, "notif_on" if v else "notif_off"),
                                   QSystemTrayIcon.Information, 1500)

    def _update_toggle_btn(self, v):
        s = lambda k: T(self.lang, k)
        self.btn_toggle.setText(s("hide") if v else s("show"))
        self.btn_toggle.setStyleSheet(f"""
            QPushButton {{ background:{C['accent']};
                          border:none; border-radius:10px;
                          color:#ffffff; font-weight:700; font-size:13px; }}
            QPushButton:hover {{ background:{C['accent_h']}; }}
        """)
        self.lbl_status.setText(s("active") if v else s("hidden"))
        self.lbl_status.setStyleSheet(
            f"color:{C['success'] if v else C['danger']};font-size:13px;font-weight:700;background:transparent;")

    def _update_tray_text(self):
        if not self.tray:
            return
        self.tray.setToolTip(T(self.lang, "tray_tip"))
        if hasattr(self, "_act_open"):
            self._act_open.setText(T(self.lang, "tray_open"))
            self._act_toggle.setText(T(self.lang, "tray_toggle"))
            self._act_quit.setText(T(self.lang, "tray_quit"))

    def showEvent(self, e):
        super().showEvent(e)
        self._update_toggle_btn(self.overlay.isVisible())

    def closeEvent(self, e):
        p = self.config["preferences"]
        if not p.get("tray_enabled") or p.get("close_action") == "quit":
            QApplication.instance().quit()
            return
        e.ignore()
        if p.get("close_action") == "min":
            self.showMinimized()
        else:
            self.hide()
        if p.get("tray_notifications") and self.tray:
            self.tray.showMessage(T(self.lang, "tray_tip"),
                                   T(self.lang, "notif_off"),
                                   QSystemTrayIcon.Information, 1200)