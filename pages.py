from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QComboBox, QGridLayout,
    QHBoxLayout, QButtonGroup, QColorDialog, QInputDialog, QMessageBox,
    QListWidget, QListWidgetItem,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

import config
from config import (
    C, T, T_sub, save_config, apply_theme,
    DEFAULT_SETTINGS, PRESETS, QUICK_COLORS, STYLE_KEYS,
)
from ui import Card, Preview, PillButton, ColorSwatch


# ================= Crosshair page =================
class CrosshairPageMixin:
    def _page_crosshair(self):
        w, v = self._page_wrapper()
        self.t_cross, self.s_cross = self._page_header(v, "page_cross", "page_cross_sub")

        prev_card = Card()
        self.preview = Preview(self.overlay)
        prev_card.v.addWidget(self.preview)
        st_row = QHBoxLayout()
        self.lbl_status = QLabel()
        self.lbl_status.setStyleSheet(
            f"color:{C['success']};font-size:13px;font-weight:700;background:transparent;")
        self.btn_toggle = QPushButton()
        self.btn_toggle.setMinimumHeight(40)
        self.btn_toggle.setMinimumWidth(200)
        self.btn_toggle.setCursor(Qt.PointingHandCursor)
        self.btn_toggle.clicked.connect(self.toggle)
        st_row.addWidget(self.lbl_status)
        st_row.addStretch()
        st_row.addWidget(self.btn_toggle)
        prev_card.v.addLayout(st_row)
        v.addWidget(prev_card)

        self.card_presets = Card()
        self._card_title(self.card_presets, "card_presets")
        pres_row = QHBoxLayout()
        pres_row.setSpacing(8)
        self.preset_btns = {}
        for key in PRESETS:
            b = PillButton("")
            b.setProperty("preset_key", key)
            b.clicked.connect(lambda _, k=key: self._apply_preset(k))
            self.preset_btns[key] = b
            pres_row.addWidget(b)
        pres_row.addStretch()
        self.card_presets.v.addLayout(pres_row)
        v.addWidget(self.card_presets)

        self.card_shape = Card()
        self._card_title(self.card_shape, "card_shape")
        grid = QGridLayout()
        grid.setSpacing(8)
        self.style_grp = QButtonGroup(self)
        self.style_grp.setExclusive(True)
        self.style_btns = {}
        for i, k in enumerate(STYLE_KEYS):
            b = PillButton("")
            b.setCheckable(True)
            b.setProperty("style_key", k)
            b.clicked.connect(lambda _, key=k: self._update(style=key))
            self.style_grp.addButton(b)
            self.style_btns[k] = b
            grid.addWidget(b, i // 3, i % 3)
        self.card_shape.v.addLayout(grid)
        self.sl_size = self._slider(self.card_shape, "lbl_size", 1, 100, 10)
        self.sl_size.valueChanged.connect(lambda x: self._update(size=x))
        self.sl_thick = self._slider(self.card_shape, "lbl_thick", 1, 20, 2)
        self.sl_thick.valueChanged.connect(lambda x: self._update(thickness=x))
        self.sl_gap = self._slider(self.card_shape, "lbl_gap", 0, 50, 5)
        self.sl_gap.valueChanged.connect(lambda x: self._update(gap=x))
        self.sl_rot = self._slider(self.card_shape, "lbl_rot", 0, 360, 0, "°")
        self.sl_rot.valueChanged.connect(lambda x: self._update(rotation=x))
        v.addWidget(self.card_shape)

        self.card_color = Card()
        self._card_title(self.card_color, "card_color")
        self.lbl_quick = QLabel()
        self.lbl_quick.setStyleSheet(f"color:{C['text2']};font-size:12px;background:transparent;")
        self.lbl_quick.setProperty("key", "lbl_quick")
        self.card_color.v.addWidget(self.lbl_quick)
        sw_row = QHBoxLayout()
        sw_row.setSpacing(8)
        for c in QUICK_COLORS:
            sw = ColorSwatch(c)
            sw.clicked.connect(lambda _, col=c: self._set_color(col))
            sw_row.addWidget(sw)
        sw_row.addStretch()
        self.card_color.v.addLayout(sw_row)
        self.btn_color = QPushButton()
        self.btn_color.setMinimumHeight(38)
        self.btn_color.setCursor(Qt.PointingHandCursor)
        self.btn_color.clicked.connect(self._pick_color)
        self.card_color.v.addWidget(self.btn_color)
        self.sl_opacity = self._slider(self.card_color, "lbl_opacity", 20, 255, 255)
        self.sl_opacity.valueChanged.connect(lambda x: self._update(opacity=x))
        v.addWidget(self.card_color)

        self.card_effects = Card()
        self._card_title(self.card_effects, "card_effects")
        self.tog_outline = self._toggle_row(self.card_effects, "lbl_outline", False)
        self.tog_outline.toggled.connect(lambda x: self._update(outline=x))
        self.sl_ow = self._slider(self.card_effects, "lbl_outline_w", 1, 10, 1)
        self.sl_ow.valueChanged.connect(lambda x: self._update(outline_width=x))
        self.tog_glow = self._toggle_row(self.card_effects, "lbl_glow", False)
        self.tog_glow.toggled.connect(lambda x: self._update(glow=x))
        self.sl_gi = self._slider(self.card_effects, "lbl_glow_i", 1, 10, 3)
        self.sl_gi.valueChanged.connect(lambda x: self._update(glow_intensity=x))
        self.tog_dot = self._toggle_row(self.card_effects, "lbl_dot", False)
        self.tog_dot.toggled.connect(lambda x: self._update(dot=x))
        self.tog_aa = self._toggle_row(self.card_effects, "lbl_aa", True)
        self.tog_aa.toggled.connect(lambda x: self._update(anti_aliasing=x))
        v.addWidget(self.card_effects)

        self.card_pos = Card()
        self._card_title(self.card_pos, "card_pos")
        scr_row = QHBoxLayout()
        self.lbl_screen = QLabel()
        self.lbl_screen.setStyleSheet(f"color:{C['text2']};font-size:12px;background:transparent;")
        self.lbl_screen.setProperty("key", "lbl_screen")
        self.combo_screen = QComboBox()
        self.combo_screen.currentIndexChanged.connect(self._on_screen)
        scr_row.addWidget(self.lbl_screen)
        scr_row.addWidget(self.combo_screen, 1)
        self.card_pos.v.addLayout(scr_row)
        self.sl_ox = self._slider(self.card_pos, "lbl_ox", -500, 500, 0)
        self.sl_ox.valueChanged.connect(lambda x: self._update(offset_x=x))
        self.sl_oy = self._slider(self.card_pos, "lbl_oy", -500, 500, 0)
        self.sl_oy.valueChanged.connect(lambda x: self._update(offset_y=x))
        self.btn_center = QPushButton()
        self.btn_center.setMinimumHeight(38)
        self.btn_center.setCursor(Qt.PointingHandCursor)
        self.btn_center.clicked.connect(self._snap)
        self.btn_center.setStyleSheet(f"""
            QPushButton {{ background:{C['surface2']}; border:1px solid {C['border']};
                          border-radius:8px; color:{C['text']}; font-weight:600; font-size:13px; }}
            QPushButton:hover {{ background:{C['accent_bg']}; border-color:{C['accent']};
                                 color:{C['accent']}; }}
        """)
        self.card_pos.v.addWidget(self.btn_center)
        v.addWidget(self.card_pos)
        v.addStretch()
        return w

    def _apply_preset(self, key):
        p = PRESETS[key].copy()
        for k, dv in DEFAULT_SETTINGS.items():
            p.setdefault(k, dv)
        p["screen_index"] = self.overlay.settings.get("screen_index", 0)
        self.overlay.settings.update(p)
        self.overlay.update()
        self._sync()
        self.preview.update()

    def _set_color(self, c):
        self._update(color=c)
        self._update_color_btn()

    def _pick_color(self):
        c = QColorDialog.getColor(QColor(self.overlay.settings["color"]), self)
        if c.isValid():
            self._set_color(c.name())

    def _update_color_btn(self):
        hx = self.overlay.settings["color"]
        col = QColor(hx)
        txt = "#000" if (col.red() + col.green() + col.blue()) / 3 > 128 else "#fff"
        self.btn_color.setText(hx.upper())
        self.btn_color.setStyleSheet(f"""
            QPushButton {{ background:{hx}; color:{txt}; border:1px solid {C['border']};
                          border-radius:10px; font-weight:700; font-size:13px; }}
            QPushButton:hover {{ border-color:{C['accent']}; }}
        """)

    def _snap(self):
        self.sl_ox.setValue(0)
        self.sl_oy.setValue(0)
        self._update(offset_x=0, offset_y=0)

    def _on_screen(self, i):
        v = self.combo_screen.itemData(i)
        if v is not None:
            self.overlay.set_screen(v)
            self.preview.update()


# ================= Interface page =================
class InterfacePageMixin:
    def _page_interface(self):
        w, v = self._page_wrapper()
        self.t_ui, self.s_ui = self._page_header(v, "page_ui", "page_ui_sub")

        self.card_theme = Card()
        self._card_title(self.card_theme, "card_theme")
        self.tog_theme = self._toggle_row(
            self.card_theme, "lbl_theme",
            self.config["preferences"].get("theme", "dark") == "dark",
            desc_key="lbl_theme_desc")
        self.tog_theme.toggled.connect(self._on_theme_toggle)
        v.addWidget(self.card_theme)

        self.card_lang = Card()
        self._card_title(self.card_lang, "card_lang")
        lr = QHBoxLayout()
        l1 = QLabel()
        l1.setStyleSheet(f"color:{C['text2']};font-size:13px;background:transparent;")
        l1.setProperty("key", "lbl_lang")
        self.combo_lang = QComboBox()
        for txt, code in [
            ("فارسی", "fa"),
            ("English", "en"),
            ("العربية", "ar"),
            ("Türkçe", "tr"),
            ("Русский", "ru"),
            ("中文", "zh"),
            ("Deutsch", "de"),
        ]:
            self.combo_lang.addItem(txt, code)
        self.combo_lang.currentIndexChanged.connect(self._on_lang)
        lr.addWidget(l1)
        lr.addWidget(self.combo_lang, 1)
        self.card_lang.v.addLayout(lr)
        v.addWidget(self.card_lang)

        self.card_font_info = Card()
        self._card_title(self.card_font_info, "card_font_info")
        self.lbl_font_loaded = QLabel()
        self.lbl_font_loaded.setStyleSheet(
            f"color:{C['success']};font-size:13px;font-weight:600;background:transparent;")
        self.lbl_font_note = QLabel()
        self.lbl_font_note.setWordWrap(True)
        self.lbl_font_note.setStyleSheet(f"color:{C['text3']};font-size:12px;background:transparent;")
        self.lbl_font_note.setProperty("key", "font_note")
        self.card_font_info.v.addWidget(self.lbl_font_loaded)
        self.card_font_info.v.addWidget(self.lbl_font_note)
        v.addWidget(self.card_font_info)
        v.addStretch()
        return w

    def _on_theme_toggle(self, checked):
        new_theme = "dark" if checked else "light"
        if new_theme == self.config["preferences"].get("theme"):
            return
        current_page = self.stack.currentIndex()
        self.config["preferences"]["theme"] = new_theme
        save_config(self.config)
        apply_theme(new_theme)
        self._rebuild_ui()
        self._switch_page(current_page)

    def _rebuild_ui(self):
        old = self.centralWidget()
        self._build()
        if old is not None:
            old.deleteLater()
        self._apply_lang()
        self._sync()

    def _on_lang(self, idx):
        self.lang = self.combo_lang.itemData(idx)
        self.config["preferences"]["language"] = self.lang
        self._apply_lang()
        self._refresh_profiles()
        self._update_tray_text()


# ================= System page =================
class SystemPageMixin:
    def _page_system(self):
        w, v = self._page_wrapper()
        self.t_sys, self.s_sys = self._page_header(v, "page_sys", "page_sys_sub")

        self.card_tray = Card()
        self._card_title(self.card_tray, "card_tray")
        self.tog_tray = self._toggle_row(self.card_tray, "lbl_tray", True)
        self.tog_tray.toggled.connect(self._on_tray_enabled)
        self.tog_notif = self._toggle_row(self.card_tray, "lbl_notif", True)
        self.tog_notif.toggled.connect(self._on_notif)
        self.tog_startmin = self._toggle_row(self.card_tray, "lbl_start_min", False)
        self.tog_startmin.toggled.connect(self._on_startmin)
        close_row = QHBoxLayout()
        lc = QLabel()
        lc.setStyleSheet(f"color:{C['text2']};font-size:13px;background:transparent;")
        lc.setProperty("key", "lbl_close")
        self.combo_close = QComboBox()
        self.combo_close.currentIndexChanged.connect(self._on_close)
        close_row.addWidget(lc)
        close_row.addWidget(self.combo_close, 1)
        self.card_tray.v.addLayout(close_row)
        v.addWidget(self.card_tray)

        self.card_behavior = Card()
        self._card_title(self.card_behavior, "card_behavior")
        self.tog_autosave = self._toggle_row(self.card_behavior, "lbl_autosave", True)
        self.tog_autosave.toggled.connect(self._on_autosave)
        self.tog_starthidden = self._toggle_row(self.card_behavior, "lbl_start_hidden", False)
        self.tog_starthidden.toggled.connect(self._on_starthidden)
        v.addWidget(self.card_behavior)

        self.btn_reset = QPushButton()
        self.btn_reset.setMinimumHeight(42)
        self.btn_reset.setCursor(Qt.PointingHandCursor)
        self.btn_reset.setStyleSheet(f"""
            QPushButton {{ background:{C['danger_bg']}; border:1px solid {C['danger_border']};
                          border-radius:10px; color:{C['danger']}; font-weight:600; }}
            QPushButton:hover {{ background:{C['danger_border']}; }}
        """)
        self.btn_reset.clicked.connect(self._reset)
        self.btn_about = QPushButton()
        self.btn_about.setMinimumHeight(42)
        self.btn_about.setCursor(Qt.PointingHandCursor)
        self.btn_about.setStyleSheet(f"""
            QPushButton {{ background:{C['surface']}; border:1px solid {C['border']};
                          border-radius:10px; color:{C['text']}; font-weight:600; }}
            QPushButton:hover {{ background:{C['surface2']}; }}
        """)
        self.btn_about.clicked.connect(self._about)
        v.addWidget(self.btn_reset)
        v.addWidget(self.btn_about)
        v.addStretch()
        return w

    def _on_tray_enabled(self, v): self.config["preferences"]["tray_enabled"] = v
    def _on_notif(self, v): self.config["preferences"]["tray_notifications"] = v
    def _on_startmin(self, v): self.config["preferences"]["tray_start_minimized"] = v
    def _on_close(self, i): self.config["preferences"]["close_action"] = self.combo_close.itemData(i)
    def _on_autosave(self, v): self.config["preferences"]["auto_save"] = v
    def _on_starthidden(self, v): self.config["preferences"]["start_hidden"] = v

    def _reset(self):
        if QMessageBox.question(self, T(self.lang, "btn_reset"),
                                 T(self.lang, "msg_reset")) != QMessageBox.Yes:
            return
        si = self.overlay.settings.get("screen_index", 0)
        self.overlay.settings.update(DEFAULT_SETTINGS)
        self.overlay.settings["screen_index"] = si
        self.overlay.update()
        self._sync()
        self.preview.update()

    def _about(self):
        QMessageBox.about(self, T(self.lang, "about_title"), T(self.lang, "about_text"))


# ================= Profiles page =================
class ProfilesPageMixin:
    def _page_profiles(self):
        w, v = self._page_wrapper()
        self.t_prof, self.s_prof = self._page_header(v, "page_prof", "page_prof_sub")
        self.lbl_no_prof = QLabel()
        self.lbl_no_prof.setAlignment(Qt.AlignCenter)
        self.lbl_no_prof.setStyleSheet(f"color:{C['text3']};font-size:13px;padding:40px;background:transparent;")
        v.addWidget(self.lbl_no_prof)
        self.list_prof = QListWidget()
        self.list_prof.setStyleSheet(f"""
            QListWidget {{ background:{C['surface']}; border:1px solid {C['border']};
                          border-radius:12px; padding:8px; font-size:13px; color:{C['text']}; }}
            QListWidget::item {{ padding:12px; border-radius:8px; margin:2px; }}
            QListWidget::item:hover {{ background:{C['surface2']}; }}
            QListWidget::item:selected {{ background:{C['accent_bg']}; color:{C['accent']};
                                          font-weight:600; }}
        """)
        self.list_prof.itemDoubleClicked.connect(lambda _: self._load_prof())
        v.addWidget(self.list_prof, 1)
        save_row = QHBoxLayout()
        save_row.setSpacing(8)
        self.btn_save_prof = self._primary_btn()
        self.btn_save_prof.clicked.connect(self._save_prof)
        self.btn_load = self._secondary_btn()
        self.btn_load.clicked.connect(self._load_prof)
        save_row.addWidget(self.btn_save_prof, 2)
        save_row.addWidget(self.btn_load, 1)
        v.addLayout(save_row)
        row2 = QHBoxLayout()
        row2.setSpacing(8)
        self.btn_rename = self._secondary_btn()
        self.btn_rename.clicked.connect(self._rename_prof)
        self.btn_delete = self._secondary_btn()
        self.btn_delete.clicked.connect(self._delete_prof)
        row2.addWidget(self.btn_rename)
        row2.addWidget(self.btn_delete)
        v.addLayout(row2)
        return w

    def _refresh_profiles(self):
        self.list_prof.clear()
        profs = self.config.get("profiles", {})
        for name in sorted(profs):
            self.list_prof.addItem(QListWidgetItem(f"◆  {name}"))
        show = bool(profs)
        self.list_prof.setVisible(show)
        self.lbl_no_prof.setVisible(not show)

    def _save_prof(self):
        name, ok = QInputDialog.getText(self, T(self.lang, "btn_save_prof"),
                                         T(self.lang, "msg_prof_name"))
        if not ok or not name.strip():
            return
        self.config["profiles"][name.strip()] = dict(self.overlay.settings)
        save_config(self.config)
        self._refresh_profiles()
        QMessageBox.information(self, T(self.lang, "info"), T(self.lang, "msg_prof_saved"))

    def _load_prof(self):
        it = self.list_prof.currentItem()
        if not it:
            return
        name = it.text().replace("◆  ", "")
        d = self.config["profiles"].get(name)
        if not d:
            return
        si = self.overlay.settings.get("screen_index", 0)
        self.overlay.settings.update(d)
        self.overlay.settings["screen_index"] = si
        self.overlay.update()
        self._sync()
        self.preview.update()

    def _rename_prof(self):
        it = self.list_prof.currentItem()
        if not it:
            return
        old = it.text().replace("◆  ", "")
        new, ok = QInputDialog.getText(self, T(self.lang, "btn_rename"),
                                        T(self.lang, "msg_prof_name"), text=old)
        if not ok or not new.strip() or new == old:
            return
        self.config["profiles"][new.strip()] = self.config["profiles"].pop(old)
        save_config(self.config)
        self._refresh_profiles()

    def _delete_prof(self):
        it = self.list_prof.currentItem()
        if not it:
            return
        name = it.text().replace("◆  ", "")
        if QMessageBox.question(self, T(self.lang, "warning"),
                                 T(self.lang, "msg_prof_del")) != QMessageBox.Yes:
            return
        self.config["profiles"].pop(name, None)
        save_config(self.config)
        self._refresh_profiles()
        QMessageBox.information(self, T(self.lang, "info"), T(self.lang, "msg_prof_deleted"))