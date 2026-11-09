import os
import sys
import json
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFontDatabase

# ================= Version =================
VERSION = "1.0"
VERSION_FA = "۱.۰"

# ================= Themes =================
THEMES = {
    "light": {
        "bg": "#fafafa", "surface": "#ffffff", "surface2": "#f4f4f5",
        "border": "#e4e4e7", "border_h": "#d4d4d8",
        "text": "#18181b", "text2": "#52525b", "text3": "#a1a1aa",
        "accent": "#6366f1", "accent_h": "#4f46e5", "accent_bg": "#eef2ff",
        "success": "#10b981", "danger": "#ef4444", "danger_bg": "#fee2e2",
        "danger_border": "#fecaca", "hover_bg": "#f4f4f5",
    },
    "dark": {
        "bg": "#09090b", "surface": "#18181b", "surface2": "#27272a",
        "border": "#27272a", "border_h": "#3f3f46",
        "text": "#fafafa", "text2": "#a1a1aa", "text3": "#71717a",
        "accent": "#818cf8", "accent_h": "#6366f1", "accent_bg": "#312e81",
        "success": "#34d399", "danger": "#f87171", "danger_bg": "#450a0a",
        "danger_border": "#7f1d1d", "hover_bg": "#27272a",
    },
}
CURRENT_THEME = "dark"
C = dict(THEMES["dark"])


def apply_theme(name):
    global CURRENT_THEME
    if name not in THEMES:
        name = "dark"
    CURRENT_THEME = name
    C.clear()
    C.update(THEMES[name])


# ================= Defaults =================
DEFAULT_SETTINGS = {
    "style": "cross_dot", "color": "#4ADE80", "size": 10, "thickness": 2,
    "gap": 5, "opacity": 255, "dot": False, "offset_x": 0, "offset_y": 0,
    "outline": True, "outline_width": 1, "glow": False,
    "glow_color": "#4ADE80", "glow_intensity": 3, "line_style": "solid",
    "rotation": 0, "anti_aliasing": True, "screen_index": 0,
}
DEFAULT_PREFS = {
    "language": "fa", "theme": "dark",
    "tray_enabled": True, "close_action": "quit", "tray_notifications": True,
    "tray_start_minimized": False, "auto_save": True, "start_hidden": False,
}

PRESETS = {
    "cs2":       {"style": "cross", "color": "#00FF00", "size": 7, "thickness": 2,
                  "gap": 3, "outline": True, "outline_width": 1, "glow": False, "dot": False},
    "valorant":  {"style": "cross", "color": "#00FF00", "size": 5, "thickness": 2,
                  "gap": 2, "outline": True, "outline_width": 1, "glow": False, "dot": False},
    "apex":      {"style": "cross_dot", "color": "#00FF00", "size": 10, "thickness": 2,
                  "gap": 6, "dot": True, "outline": False, "glow": False},
    "minecraft": {"style": "cross_dot", "color": "#FFFFFF", "size": 8, "thickness": 2,
                  "gap": 6, "outline": True, "outline_width": 1, "glow": False, "dot": True},
    "minimal":   {"style": "dot", "color": "#FF3B30", "size": 4, "thickness": 3,
                  "gap": 0, "outline": False, "glow": False, "dot": False},
    "circle":    {"style": "circle_dot", "color": "#00FFFF", "size": 10, "thickness": 2,
                  "gap": 2, "dot": True, "outline": False, "glow": False},
    "sniper":    {"style": "cross", "color": "#FF0000", "size": 20, "thickness": 1,
                  "gap": 30, "dot": True, "outline": True, "outline_width": 1, "glow": False},
    "neon":      {"style": "cross_dot", "color": "#FF00FF", "size": 12, "thickness": 2,
                  "gap": 5, "dot": True, "outline": False, "glow": True,
                  "glow_color": "#FF00FF", "glow_intensity": 4},
}
QUICK_COLORS = ["#4ADE80", "#00FF00", "#FF0000", "#00FFFF", "#FF00FF",
                "#FFFF00", "#FFFFFF", "#FF8800", "#FF69B4", "#A855F7"]
STYLE_KEYS = ["cross_dot", "cross", "dot", "circle_dot", "t_shape",
              "x_shape", "circle", "square", "triple"]
CONFIG_FILE = os.path.join(os.path.expanduser("~"), ".aimax.json")


def load_config():
    d = {"settings": DEFAULT_SETTINGS.copy(),
         "preferences": DEFAULT_PREFS.copy(),
         "profiles": {}}
    try:
        with open(CONFIG_FILE, encoding="utf-8") as f:
            data = json.load(f)
        for sec in d:
            if sec not in data:
                data[sec] = d[sec]
            if isinstance(d[sec], dict):
                for k, v in d[sec].items():
                    data[sec].setdefault(k, v)
        return data
    except Exception:
        return d


def save_config(data):
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print("Save error:", e)


# ================= i18n =================
STR = {
    "en": {
        "app": "AiMax", "tag": "Crosshair Manager",
        "page_cross": "Crosshair", "page_cross_sub": "Customize your perfect reticle",
        "page_ui": "Interface", "page_ui_sub": "Language, theme and appearance",
        "page_sys": "System", "page_sys_sub": "Tray icon and application behavior",
        "page_prof": "Profiles", "page_prof_sub": "Save and manage your configurations",
        "nav_cross": "Crosshair", "nav_ui": "Interface", "nav_sys": "System", "nav_prof": "Profiles",
        "hotkeys": "SHORTCUTS", "hk1": "F8 — Toggle overlay", "hk2": "F9 — Quit",
        "active": "● Active", "hidden": "● Hidden",
        "show": "Show Crosshair", "hide": "Hide Crosshair",
        "card_presets": "Game Presets", "card_shape": "Shape & Size", "card_color": "Color",
        "card_effects": "Effects", "card_pos": "Position",
        "card_lang": "Language", "card_font_info": "Typography", "card_theme": "Theme",
        "card_tray": "System Tray", "card_behavior": "Behavior",
        "lbl_size": "Size", "lbl_thick": "Thickness", "lbl_gap": "Gap", "lbl_rot": "Rotation",
        "lbl_color": "Color", "lbl_opacity": "Opacity", "lbl_quick": "Quick colors",
        "lbl_outline": "Outline", "lbl_outline_w": "Outline width",
        "lbl_glow": "Glow", "lbl_glow_i": "Glow intensity",
        "lbl_dot": "Center dot", "lbl_screen": "Display", "lbl_ox": "Offset X",
        "lbl_oy": "Offset Y", "lbl_lang": "Interface language", "lbl_aa": "Anti-aliasing",
        "lbl_theme": "Dark mode", "lbl_theme_desc": "Use dark theme across the application",
        "lbl_tray": "Enable system tray icon", "lbl_close": "On window close",
        "lbl_notif": "Show tray notifications", "lbl_start_min": "Start minimized",
        "lbl_autosave": "Auto-save on exit", "lbl_start_hidden": "Start with overlay hidden",
        "btn_center": "Snap to center", "btn_reset": "Reset all", "btn_about": "About",
        "btn_save_prof": "Save current as...", "btn_load": "Load", "btn_rename": "Rename",
        "btn_delete": "Delete",
        "act_hide": "Hide to tray", "act_min": "Minimize", "act_quit": "Quit",
        "screen_n": "Screen {n}",
        "no_prof": "No profiles yet.\nClick \"Save current as...\" to create one.",
        "msg_prof_name": "Profile name:", "msg_prof_saved": "Profile saved successfully.",
        "msg_prof_del": "Delete this profile?", "msg_prof_deleted": "Profile deleted.",
        "msg_reset": "Reset all settings to default?",
        "info": "Info", "warning": "Warning",
        "tray_open": "Open AiMax", "tray_toggle": "Toggle crosshair",
        "tray_quit": "Quit", "tray_tip": "AiMax",
        "notif_on": "Crosshair is now visible", "notif_off": "Crosshair is now hidden",
        "about_title": "About AiMax", "about_text": (
            f"<h3>AiMax v{VERSION}</h3><p>A modern, professional crosshair overlay.</p>"
            "<p><b>Shortcuts:</b><br>F8 → Toggle overlay<br>F9 → Quit</p>"
            "<p><b>Tip:</b> Use Borderless Windowed mode in games.</p>"),
        "font_loaded": "Font loaded: <b>{font}</b>",
        "font_note": "The Vazirmatn font is used throughout the entire application and cannot be changed.",
        "styles": {"cross_dot": "Cross + Dot", "cross": "Cross", "dot": "Dot",
                   "circle_dot": "Circle + Dot", "t_shape": "T-Shape", "x_shape": "X-Shape",
                   "circle": "Circle", "square": "Square", "triple": "Triple"},
        "presets": {"cs2": "CS2", "valorant": "Valorant", "apex": "Apex",
                    "minecraft": "Minecraft", "minimal": "Minimal", "circle": "Circle",
                    "sniper": "Sniper", "neon": "Neon"},
        "line_solid": "Solid", "line_dashed": "Dashed", "line_dotted": "Dotted",
    },
    "fa": {
        "app": "AiMax", "tag": "مدیریت کراس‌هیر",
        "page_cross": "کراس‌هیر", "page_cross_sub": "کراس‌هیر دلخواه خود را بسازید",
        "page_ui": "رابط کاربری", "page_ui_sub": "زبان، تم و ظاهر",
        "page_sys": "سیستم", "page_sys_sub": "ناحیه اعلان و رفتار برنامه",
        "page_prof": "پروفایل‌ها", "page_prof_sub": "ذخیره و مدیریت تنظیمات",
        "nav_cross": "کراس‌هیر", "nav_ui": "رابط کاربری", "nav_sys": "سیستم", "nav_prof": "پروفایل‌ها",
        "hotkeys": "کلیدهای میانبر", "hk1": "F8 — نمایش / مخفی", "hk2": "F9 — خروج",
        "active": "● فعال", "hidden": "● مخفی",
        "show": "نمایش کراس‌هیر", "hide": "مخفی کردن",
        "card_presets": "پریست بازی‌ها", "card_shape": "شکل و اندازه", "card_color": "رنگ",
        "card_effects": "افکت‌ها", "card_pos": "موقعیت",
        "card_lang": "زبان", "card_font_info": "تایپوگرافی", "card_theme": "تم",
        "card_tray": "ناحیه اعلان", "card_behavior": "رفتار",
        "lbl_size": "اندازه", "lbl_thick": "ضخامت", "lbl_gap": "فاصله", "lbl_rot": "چرخش",
        "lbl_color": "رنگ", "lbl_opacity": "شفافیت", "lbl_quick": "رنگ‌های سریع",
        "lbl_outline": "خط دور", "lbl_outline_w": "ضخامت خط دور",
        "lbl_glow": "افکت Glow", "lbl_glow_i": "شدت Glow",
        "lbl_dot": "نقطه وسط", "lbl_screen": "نمایشگر", "lbl_ox": "آفست افقی",
        "lbl_oy": "آفست عمودی", "lbl_lang": "زبان رابط", "lbl_aa": "آنتی‌آلیاسینگ",
        "lbl_theme": "حالت تاریک", "lbl_theme_desc": "استفاده از تم تیره در سراسر برنامه",
        "lbl_tray": "فعال بودن آیکون ناحیه اعلان", "lbl_close": "هنگام بستن پنجره",
        "lbl_notif": "نمایش اعلان‌ها", "lbl_start_min": "شروع مینیمایز",
        "lbl_autosave": "ذخیره خودکار در خروج", "lbl_start_hidden": "شروع با اورلی مخفی",
        "btn_center": "وسط‌چین", "btn_reset": "بازنشانی همه", "btn_about": "درباره",
        "btn_save_prof": "ذخیره به نام...", "btn_load": "بارگذاری", "btn_rename": "تغییر نام",
        "btn_delete": "حذف",
        "act_hide": "مخفی در ناحیه اعلان", "act_min": "مینیمایز", "act_quit": "خروج",
        "screen_n": "مانیتور {n}",
        "no_prof": "هنوز پروفایلی ندارید.\nروی «ذخیره به نام...» کلیک کنید.",
        "msg_prof_name": "نام پروفایل:", "msg_prof_saved": "پروفایل ذخیره شد.",
        "msg_prof_del": "این پروفایل حذف شود؟", "msg_prof_deleted": "پروفایل حذف شد.",
        "msg_reset": "همه تنظیمات به پیش‌فرض بازگردد؟",
        "info": "اطلاع", "warning": "هشدار",
        "tray_open": "باز کردن AiMax", "tray_toggle": "تغییر وضعیت کراس‌هیر",
        "tray_quit": "خروج", "tray_tip": "AiMax",
        "notif_on": "کراس‌هیر نمایش داده شد", "notif_off": "کراس‌هیر مخفی شد",
        "about_title": "درباره AiMax", "about_text": (
            f"<h3>AiMax نسخه {VERSION_FA}</h3><p>یک اورلی کراس‌هیر حرفه‌ای و مدرن.</p>"
            "<p><b>کلیدهای میانبر:</b><br>F8 → نمایش / مخفی<br>F9 → خروج</p>"
            "<p><b>نکته:</b> در بازی‌ها از Borderless Windowed استفاده کنید.</p>"),
        "font_loaded": "فونت بارگذاری‌شده: <b>{font}</b>",
        "font_note": "فونت وزیرمتن در سراسر برنامه استفاده می‌شود و قابل تغییر نیست.",
        "styles": {"cross_dot": "صلیبی + نقطه", "cross": "صلیبی", "dot": "نقطه",
                   "circle_dot": "دایره + نقطه", "t_shape": "T شکل", "x_shape": "X شکل",
                   "circle": "دایره", "square": "مربع", "triple": "سه‌خطی"},
        "presets": {"cs2": "CS2", "valorant": "Valorant", "apex": "Apex",
                    "minecraft": "Minecraft", "minimal": "مینیمال", "circle": "دایره",
                    "sniper": "اسنایپر", "neon": "نئون"},
        "line_solid": "توپر", "line_dashed": "خط‌چین", "line_dotted": "نقطه‌چین",
    },
    "ar": {
        "app": "AiMax", "tag": "مدير التصويب",
        "page_cross": "التصويب", "page_cross_sub": "خصّص تصويبك المثالي",
        "page_ui": "الواجهة", "page_ui_sub": "اللغة والسمة والمظهر",
        "page_sys": "النظام", "page_sys_sub": "أيقونة العلبة وسلوك التطبيق",
        "page_prof": "الملفات", "page_prof_sub": "حفظ وإدارة الإعدادات",
        "nav_cross": "التصويب", "nav_ui": "الواجهة", "nav_sys": "النظام", "nav_prof": "الملفات",
        "hotkeys": "الاختصارات", "hk1": "F8 — إظهار / إخفاء", "hk2": "F9 — خروج",
        "active": "● نشط", "hidden": "● مخفي",
        "show": "إظهار", "hide": "إخفاء",
        "card_presets": "إعدادات مسبقة", "card_shape": "الشكل والحجم", "card_color": "اللون",
        "card_effects": "التأثيرات", "card_pos": "الموضع",
        "card_lang": "اللغة", "card_font_info": "الخط", "card_theme": "السمة",
        "card_tray": "علبة النظام", "card_behavior": "السلوك",
        "lbl_size": "الحجم", "lbl_thick": "السماكة", "lbl_gap": "الفجوة", "lbl_rot": "الدوران",
        "lbl_color": "اللون", "lbl_opacity": "الشفافية", "lbl_quick": "ألوان سريعة",
        "lbl_outline": "حدود", "lbl_outline_w": "سماكة الحدود",
        "lbl_glow": "توهج", "lbl_glow_i": "شدة التوهج",
        "lbl_dot": "نقطة مركزية", "lbl_screen": "الشاشة", "lbl_ox": "إزاحة أفقية",
        "lbl_oy": "إزاحة رأسية", "lbl_lang": "لغة الواجهة", "lbl_aa": "تنعيم الحواف",
        "lbl_theme": "الوضع الداكن", "lbl_theme_desc": "استخدام السمة الداكنة في كل التطبيق",
        "lbl_tray": "تفعيل أيقونة العلبة", "lbl_close": "عند إغلاق النافذة",
        "lbl_notif": "إظهار الإشعارات", "lbl_start_min": "بدء مصغر",
        "lbl_autosave": "حفظ تلقائي عند الإغلاق", "lbl_start_hidden": "بدء مخفي",
        "btn_center": "توسيط", "btn_reset": "إعادة تعيين", "btn_about": "حول",
        "btn_save_prof": "حفظ باسم...", "btn_load": "تحميل", "btn_rename": "إعادة تسمية",
        "btn_delete": "حذف",
        "act_hide": "إخفاء في العلبة", "act_min": "تصغير", "act_quit": "خروج",
        "screen_n": "شاشة {n}",
        "no_prof": "لا توجد ملفات بعد.", "msg_prof_name": "اسم الملف:",
        "msg_prof_saved": "تم الحفظ.", "msg_prof_del": "حذف هذا الملف؟",
        "msg_prof_deleted": "تم الحذف.", "msg_reset": "استعادة كل الإعدادات؟",
        "info": "معلومات", "warning": "تحذير",
        "tray_open": "فتح AiMax", "tray_toggle": "تبديل التصويب",
        "tray_quit": "خروج", "tray_tip": "AiMax",
        "notif_on": "تم إظهار التصويب", "notif_off": "تم إخفاء التصويب",
        "about_title": "حول AiMax", "about_text": f"<h3>AiMax v{VERSION}</h3>",
        "font_loaded": "الخط المحمّل: <b>{font}</b>",
        "font_note": "يُستخدم خط Vazirmatn في جميع أنحاء التطبيق ولا يمكن تغييره.",
        "styles": {"cross_dot": "صليب + نقطة", "cross": "صليب", "dot": "نقطة",
                   "circle_dot": "دائرة + نقطة", "t_shape": "T", "x_shape": "X",
                   "circle": "دائرة", "square": "مربع", "triple": "ثلاثي"},
        "presets": {"cs2": "CS2", "valorant": "Valorant", "apex": "Apex",
                    "minecraft": "Minecraft", "minimal": "بسيط", "circle": "دائرة",
                    "sniper": "قناص", "neon": "نيون"},
        "line_solid": "متصل", "line_dashed": "متقطع", "line_dotted": "منقط",
    },
    "tr": {
        "app": "AiMax", "tag": "Nişangah Yöneticisi",
        "page_cross": "Nişangah", "page_cross_sub": "Mükemmel nişangahını özelleştir",
        "page_ui": "Arayüz", "page_ui_sub": "Dil, tema ve görünüm",
        "page_sys": "Sistem", "page_sys_sub": "Tepsi simgesi ve uygulama davranışı",
        "page_prof": "Profiller", "page_prof_sub": "Yapılandırmaları kaydet ve yönet",
        "nav_cross": "Nişangah", "nav_ui": "Arayüz", "nav_sys": "Sistem", "nav_prof": "Profiller",
        "hotkeys": "KISAYOLLAR", "hk1": "F8 — Aç / Kapat", "hk2": "F9 — Çıkış",
        "active": "● Aktif", "hidden": "● Gizli",
        "show": "Göster", "hide": "Gizle",
        "card_presets": "Oyun Hazır Ayarları", "card_shape": "Şekil ve Boyut", "card_color": "Renk",
        "card_effects": "Efektler", "card_pos": "Konum",
        "card_lang": "Dil", "card_font_info": "Tipografi", "card_theme": "Tema",
        "card_tray": "Sistem Tepsisi", "card_behavior": "Davranış",
        "lbl_size": "Boyut", "lbl_thick": "Kalınlık", "lbl_gap": "Boşluk", "lbl_rot": "Döndürme",
        "lbl_color": "Renk", "lbl_opacity": "Saydamlık", "lbl_quick": "Hızlı renkler",
        "lbl_outline": "Kenar", "lbl_outline_w": "Kenar kalınlığı",
        "lbl_glow": "Parlama", "lbl_glow_i": "Parlama yoğunluğu",
        "lbl_dot": "Orta nokta", "lbl_screen": "Ekran", "lbl_ox": "X Ofseti",
        "lbl_oy": "Y Ofseti", "lbl_lang": "Arayüz dili", "lbl_aa": "Kenar yumuşatma",
        "lbl_theme": "Koyu tema", "lbl_theme_desc": "Uygulamada koyu tema kullan",
        "lbl_tray": "Tepsi simgesi", "lbl_close": "Kapatma davranışı",
        "lbl_notif": "Bildirimleri göster", "lbl_start_min": "Küçültülmüş başlat",
        "lbl_autosave": "Çıkışta otomatik kaydet", "lbl_start_hidden": "Gizli başlat",
        "btn_center": "Ortala", "btn_reset": "Sıfırla", "btn_about": "Hakkında",
        "btn_save_prof": "Kaydet...", "btn_load": "Yükle", "btn_rename": "Yeniden Adlandır",
        "btn_delete": "Sil",
        "act_hide": "Tepsiye gizle", "act_min": "Küçült", "act_quit": "Çıkış",
        "screen_n": "Ekran {n}",
        "no_prof": "Henüz profil yok.", "msg_prof_name": "Profil adı:",
        "msg_prof_saved": "Kaydedildi.", "msg_prof_del": "Silinsin mi?",
        "msg_prof_deleted": "Silindi.", "msg_reset": "Tüm ayarlar sıfırlansın mı?",
        "info": "Bilgi", "warning": "Uyarı",
        "tray_open": "AiMax'i Aç", "tray_toggle": "Nişangahı Değiştir",
        "tray_quit": "Çıkış", "tray_tip": "AiMax",
        "notif_on": "Nişangah gösterildi", "notif_off": "Nişangah gizlendi",
        "about_title": "AiMax Hakkında", "about_text": f"<h3>AiMax v{VERSION}</h3>",
        "font_loaded": "Yazı tipi: <b>{font}</b>",
        "font_note": "Vazirmatn yazı tipi tüm uygulamada kullanılır ve değiştirilemez.",
        "styles": {"cross_dot": "Artı + Nokta", "cross": "Artı", "dot": "Nokta",
                   "circle_dot": "Daire + Nokta", "t_shape": "T", "x_shape": "X",
                   "circle": "Daire", "square": "Kare", "triple": "Üçlü"},
        "presets": {"cs2": "CS2", "valorant": "Valorant", "apex": "Apex",
                    "minecraft": "Minecraft", "minimal": "Minimal", "circle": "Daire",
                    "sniper": "Keskin Nişancı", "neon": "Neon"},
        "line_solid": "Düz", "line_dashed": "Kesikli", "line_dotted": "Noktalı",
    },
    "ru": {
        "app": "AiMax", "tag": "Менеджер прицела",
        "page_cross": "Прицел", "page_cross_sub": "Настройте идеальный прицел",
        "page_ui": "Интерфейс", "page_ui_sub": "Язык, тема и внешний вид",
        "page_sys": "Система", "page_sys_sub": "Трей и поведение",
        "page_prof": "Профили", "page_prof_sub": "Сохранение и управление",
        "nav_cross": "Прицел", "nav_ui": "Интерфейс", "nav_sys": "Система", "nav_prof": "Профили",
        "hotkeys": "ГОРЯЧИЕ КЛАВИШИ", "hk1": "F8 — Показать/Скрыть", "hk2": "F9 — Выход",
        "active": "● Активен", "hidden": "● Скрыт",
        "show": "Показать", "hide": "Скрыть",
        "card_presets": "Пресеты игр", "card_shape": "Форма и размер", "card_color": "Цвет",
        "card_effects": "Эффекты", "card_pos": "Позиция",
        "card_lang": "Язык", "card_font_info": "Шрифт", "card_theme": "Тема",
        "card_tray": "Трей", "card_behavior": "Поведение",
        "lbl_size": "Размер", "lbl_thick": "Толщина", "lbl_gap": "Промежуток", "lbl_rot": "Поворот",
        "lbl_color": "Цвет", "lbl_opacity": "Прозрачность", "lbl_quick": "Быстрые цвета",
        "lbl_outline": "Обводка", "lbl_outline_w": "Толщина обводки",
        "lbl_glow": "Свечение", "lbl_glow_i": "Интенсивность",
        "lbl_dot": "Точка в центре", "lbl_screen": "Экран", "lbl_ox": "Смещение X",
        "lbl_oy": "Смещение Y", "lbl_lang": "Язык интерфейса", "lbl_aa": "Сглаживание",
        "lbl_theme": "Тёмная тема", "lbl_theme_desc": "Использовать тёмную тему",
        "lbl_tray": "Иконка в трее", "lbl_close": "При закрытии окна",
        "lbl_notif": "Уведомления", "lbl_start_min": "Запускать свёрнутым",
        "lbl_autosave": "Автосохранение", "lbl_start_hidden": "Запуск без оверлея",
        "btn_center": "По центру", "btn_reset": "Сброс", "btn_about": "О программе",
        "btn_save_prof": "Сохранить как...", "btn_load": "Загрузить", "btn_rename": "Переименовать",
        "btn_delete": "Удалить",
        "act_hide": "Скрыть в трей", "act_min": "Свернуть", "act_quit": "Выход",
        "screen_n": "Экран {n}",
        "no_prof": "Профилей пока нет.", "msg_prof_name": "Имя профиля:",
        "msg_prof_saved": "Сохранено.", "msg_prof_del": "Удалить?",
        "msg_prof_deleted": "Удалено.", "msg_reset": "Сбросить всё?",
        "info": "Инфо", "warning": "Внимание",
        "tray_open": "Открыть AiMax", "tray_toggle": "Переключить прицел",
        "tray_quit": "Выход", "tray_tip": "AiMax",
        "notif_on": "Прицел показан", "notif_off": "Прицел скрыт",
        "about_title": "О AiMax", "about_text": f"<h3>AiMax v{VERSION}</h3>",
        "font_loaded": "Шрифт: <b>{font}</b>",
        "font_note": "Шрифт Vazirmatn используется во всём приложении и не может быть изменён.",
        "styles": {"cross_dot": "Крест + Точка", "cross": "Крест", "dot": "Точка",
                   "circle_dot": "Круг + Точка", "t_shape": "Т", "x_shape": "Х",
                   "circle": "Круг", "square": "Квадрат", "triple": "Тройная"},
        "presets": {"cs2": "CS2", "valorant": "Valorant", "apex": "Apex",
                    "minecraft": "Minecraft", "minimal": "Минимал", "circle": "Круг",
                    "sniper": "Снайпер", "neon": "Неон"},
        "line_solid": "Сплошная", "line_dashed": "Штрих", "line_dotted": "Точки",
    },
    "zh": {
        "app": "AiMax", "tag": "准星管理器",
        "page_cross": "准星", "page_cross_sub": "自定义你的完美准星",
        "page_ui": "界面", "page_ui_sub": "语言、主题和外观",
        "page_sys": "系统", "page_sys_sub": "托盘图标和应用程序行为",
        "page_prof": "配置文件", "page_prof_sub": "保存和管理你的配置",
        "nav_cross": "准星", "nav_ui": "界面", "nav_sys": "系统", "nav_prof": "配置文件",
        "hotkeys": "快捷键", "hk1": "F8 — 切换覆盖层", "hk2": "F9 — 退出",
        "active": "● 活跃", "hidden": "● 隐藏",
        "show": "显示准星", "hide": "隐藏准星",
        "card_presets": "游戏预设", "card_shape": "形状和大小", "card_color": "颜色",
        "card_effects": "效果", "card_pos": "位置",
        "card_lang": "语言", "card_font_info": "字体", "card_theme": "主题",
        "card_tray": "系统托盘", "card_behavior": "行为",
        "lbl_size": "大小", "lbl_thick": "粗细", "lbl_gap": "间隙", "lbl_rot": "旋转",
        "lbl_color": "颜色", "lbl_opacity": "不透明度", "lbl_quick": "快速颜色",
        "lbl_outline": "轮廓", "lbl_outline_w": "轮廓宽度",
        "lbl_glow": "发光", "lbl_glow_i": "发光强度",
        "lbl_dot": "中心点", "lbl_screen": "显示器", "lbl_ox": "X 偏移",
        "lbl_oy": "Y 偏移", "lbl_lang": "界面语言", "lbl_aa": "抗锯齿",
        "lbl_theme": "深色模式", "lbl_theme_desc": "在整个应用程序中使用深色主题",
        "lbl_tray": "启用系统托盘图标", "lbl_close": "关闭窗口时",
        "lbl_notif": "显示托盘通知", "lbl_start_min": "最小化启动",
        "lbl_autosave": "退出时自动保存", "lbl_start_hidden": "启动时隐藏覆盖层",
        "btn_center": "吸附到中心", "btn_reset": "重置全部", "btn_about": "关于",
        "btn_save_prof": "保存为...", "btn_load": "加载", "btn_rename": "重命名",
        "btn_delete": "删除",
        "act_hide": "隐藏到托盘", "act_min": "最小化", "act_quit": "退出",
        "screen_n": "显示器 {n}",
        "no_prof": "还没有配置文件。\n点击「保存为...」创建一个。",
        "msg_prof_name": "配置文件名称：", "msg_prof_saved": "配置文件保存成功。",
        "msg_prof_del": "删除此配置文件？", "msg_prof_deleted": "配置文件已删除。",
        "msg_reset": "将所有设置重置为默认值？",
        "info": "信息", "warning": "警告",
        "tray_open": "打开 AiMax", "tray_toggle": "切换准星",
        "tray_quit": "退出", "tray_tip": "AiMax",
        "notif_on": "准星现在可见", "notif_off": "准星现在已隐藏",
        "about_title": "关于 AiMax", "about_text": (
            f"<h3>AiMax v{VERSION}</h3><p>一个现代、专业的准星覆盖层。</p>"
            "<p><b>快捷键：</b><br>F8 → 切换覆盖层<br>F9 → 退出</p>"
            "<p><b>提示：</b> 在游戏中使用无边框窗口模式。</p>"),
        "font_loaded": "已加载字体：<b>{font}</b>",
        "font_note": "Vazirmatn 字体在整个应用程序中使用，无法更改。",
        "styles": {"cross_dot": "十字 + 点", "cross": "十字", "dot": "点",
                   "circle_dot": "圆 + 点", "t_shape": "T 形", "x_shape": "X 形",
                   "circle": "圆", "square": "方形", "triple": "三线"},
        "presets": {"cs2": "CS2", "valorant": "Valorant", "apex": "Apex",
                    "minecraft": "Minecraft", "minimal": "极简", "circle": "圆",
                    "sniper": "狙击", "neon": "霓虹"},
        "line_solid": "实线", "line_dashed": "虚线", "line_dotted": "点线",
    },
    "de": {
        "app": "AiMax", "tag": "Fadenkreuz-Manager",
        "page_cross": "Fadenkreuz", "page_cross_sub": "Passe dein perfektes Fadenkreuz an",
        "page_ui": "Oberfläche", "page_ui_sub": "Sprache, Theme und Aussehen",
        "page_sys": "System", "page_sys_sub": "Tray-Symbol und Anwendungsverhalten",
        "page_prof": "Profile", "page_prof_sub": "Konfigurationen speichern und verwalten",
        "nav_cross": "Fadenkreuz", "nav_ui": "Oberfläche", "nav_sys": "System", "nav_prof": "Profile",
        "hotkeys": "TASTENKÜRZEL", "hk1": "F8 — Overlay umschalten", "hk2": "F9 — Beenden",
        "active": "● Aktiv", "hidden": "● Versteckt",
        "show": "Fadenkreuz anzeigen", "hide": "Fadenkreuz ausblenden",
        "card_presets": "Spiel-Presets", "card_shape": "Form & Größe", "card_color": "Farbe",
        "card_effects": "Effekte", "card_pos": "Position",
        "card_lang": "Sprache", "card_font_info": "Typografie", "card_theme": "Theme",
        "card_tray": "System-Tray", "card_behavior": "Verhalten",
        "lbl_size": "Größe", "lbl_thick": "Dicke", "lbl_gap": "Abstand", "lbl_rot": "Drehung",
        "lbl_color": "Farbe", "lbl_opacity": "Deckkraft", "lbl_quick": "Schnellfarben",
        "lbl_outline": "Kontur", "lbl_outline_w": "Konturstärke",
        "lbl_glow": "Leuchten", "lbl_glow_i": "Leuchtintensität",
        "lbl_dot": "Mittelpunkt", "lbl_screen": "Bildschirm", "lbl_ox": "X-Versatz",
        "lbl_oy": "Y-Versatz", "lbl_lang": "Oberflächensprache", "lbl_aa": "Kantenglättung",
        "lbl_theme": "Dunkelmodus", "lbl_theme_desc": "Dunkles Theme in der gesamten Anwendung verwenden",
        "lbl_tray": "Tray-Symbol aktivieren", "lbl_close": "Beim Schließen des Fensters",
        "lbl_notif": "Tray-Benachrichtigungen anzeigen", "lbl_start_min": "Minimiert starten",
        "lbl_autosave": "Beim Beenden automatisch speichern", "lbl_start_hidden": "Mit verstecktem Overlay starten",
        "btn_center": "Auf Mitte zentrieren", "btn_reset": "Alles zurücksetzen", "btn_about": "Über",
        "btn_save_prof": "Speichern unter...", "btn_load": "Laden", "btn_rename": "Umbenennen",
        "btn_delete": "Löschen",
        "act_hide": "Ins Tray ausblenden", "act_min": "Minimieren", "act_quit": "Beenden",
        "screen_n": "Bildschirm {n}",
        "no_prof": "Noch keine Profile.\nKlicke auf «Speichern unter...», um eines zu erstellen.",
        "msg_prof_name": "Profilname:", "msg_prof_saved": "Profil erfolgreich gespeichert.",
        "msg_prof_del": "Dieses Profil löschen?", "msg_prof_deleted": "Profil gelöscht.",
        "msg_reset": "Alle Einstellungen auf Standard zurücksetzen?",
        "info": "Info", "warning": "Warnung",
        "tray_open": "AiMax öffnen", "tray_toggle": "Fadenkreuz umschalten",
        "tray_quit": "Beenden", "tray_tip": "AiMax",
        "notif_on": "Fadenkreuz ist jetzt sichtbar", "notif_off": "Fadenkreuz ist jetzt versteckt",
        "about_title": "Über AiMax", "about_text": (
            f"<h3>AiMax v{VERSION}</h3><p>Ein modernes, professionelles Fadenkreuz-Overlay.</p>"
            "<p><b>Tastenkürzel:</b><br>F8 → Overlay umschalten<br>F9 → Beenden</p>"
            "<p><b>Tipp:</b> Verwende den rahmenlosen Fenstermodus in Spielen.</p>"),
        "font_loaded": "Schriftart geladen: <b>{font}</b>",
        "font_note": "Die Vazirmatn-Schriftart wird in der gesamten Anwendung verwendet und kann nicht geändert werden.",
        "styles": {"cross_dot": "Kreuz + Punkt", "cross": "Kreuz", "dot": "Punkt",
                   "circle_dot": "Kreis + Punkt", "t_shape": "T-Form", "x_shape": "X-Form",
                   "circle": "Kreis", "square": "Quadrat", "triple": "Dreifach"},
        "presets": {"cs2": "CS2", "valorant": "Valorant", "apex": "Apex",
                    "minecraft": "Minecraft", "minimal": "Minimal", "circle": "Kreis",
                    "sniper": "Scharfschütze", "neon": "Neon"},
        "line_solid": "Durchgezogen", "line_dashed": "Gestrichelt", "line_dotted": "Gepunktet",
    },
}


def T(lang, key):
    d = STR.get(lang, {})
    if key in d and d[key] not in ({}, ""):
        return d[key]
    return STR["en"].get(key, key)


def T_sub(lang, key, sub):
    d = STR.get(lang, {}).get(key, {})
    if sub in d and d[sub]:
        return d[sub]
    return STR["en"].get(key, {}).get(sub, sub)


# ================= Font =================
LOADED_FONT_FAMILY = "Sans Serif"


def _script_dir():
    if getattr(sys, "frozen", False):
        return getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
    try:
        if __file__ and os.path.exists(__file__):
            return os.path.dirname(os.path.abspath(__file__))
    except NameError:
        pass
    return os.getcwd()


def _try_load_font_file(path):
    if not os.path.isfile(path):
        return None
    fid = QFontDatabase.addApplicationFont(path)
    if fid < 0:
        return None
    fams = QFontDatabase.applicationFontFamilies(fid)
    return fams[0] if fams else None


def _download_font(urls, target):
    import urllib.request
    for url in urls:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=10) as r:
                data = r.read()
            if len(data) < 10000:
                continue
            os.makedirs(os.path.dirname(target), exist_ok=True)
            with open(target, "wb") as f:
                f.write(data)
            return target
        except Exception as e:
            print(f"Download failed ({url}): {e}")
    return None


def ensure_vazir_font():
    global LOADED_FONT_FAMILY
    script_dir = _script_dir()
    cache_dir = os.path.join(os.path.expanduser("~"), ".aimax", "fonts")
    cache_path = os.path.join(cache_dir, "Vazirmatn-Regular.ttf")

    for p in [
        os.path.join(script_dir, "font", "Vazir.ttf"),
        os.path.join(script_dir, "font", "Vazirmatn-Regular.ttf"),
        os.path.join(script_dir, "font", "Vazirmatn.ttf"),
        os.path.join(script_dir, "fonts", "Vazir.ttf"),
        os.path.join(script_dir, "fonts", "Vazirmatn-Regular.ttf"),
        os.path.join(script_dir, "Vazir.ttf"),
        os.path.join(script_dir, "Vazirmatn-Regular.ttf"),
        cache_path,
    ]:
        fam = _try_load_font_file(p)
        if fam:
            LOADED_FONT_FAMILY = fam
            print(f"[Font] Loaded '{fam}' from {p}")
            return fam

    system_families = QFontDatabase().families()
    for name in ("Vazirmatn", "Vazir", "Vazirmatn RD"):
        if name in system_families:
            LOADED_FONT_FAMILY = name
            return name

    urls = [
        "https://cdn.jsdelivr.net/gh/rastikerdar/vazirmatn@master/fonts/ttf/Vazirmatn-Regular.ttf",
        "https://raw.githubusercontent.com/rastikerdar/vazirmatn/master/fonts/ttf/Vazirmatn-Regular.ttf",
    ]
    try:
        saved = _download_font(urls, cache_path)
        if saved:
            fam = _try_load_font_file(saved)
            if fam:
                LOADED_FONT_FAMILY = fam
                return fam
    except Exception:
        pass

    for name in ("Segoe UI", "Tahoma", "Arial", "DejaVu Sans"):
        if name in system_families:
            LOADED_FONT_FAMILY = name
            return name
    LOADED_FONT_FAMILY = QApplication.font().family()
    return LOADED_FONT_FAMILY