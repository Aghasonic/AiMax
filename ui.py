import os
import sys
from PyQt5.QtWidgets import (
    QWidget, QApplication, QLabel, QVBoxLayout, QHBoxLayout, QSlider,
    QAbstractButton, QPushButton, QFrame,
)
from PyQt5.QtCore import Qt, QPoint, QPointF, QRectF, pyqtSignal
from PyQt5.QtGui import (
    QPainter, QColor, QPen, QBrush, QIcon, QPixmap,
    QLinearGradient, QPainterPath,
)

import config
from config import C


# ================= Drawing =================
LINE_STYLES = {"solid": Qt.SolidLine, "dashed": Qt.DashLine, "dotted": Qt.DotLine}


def draw_crosshair(p, cx, cy, s, scale=1.0):
    style = s["style"]
    size = max(1, int(s["size"] * scale))
    gap = int(s["gap"] * scale)
    t = max(1, int(s["thickness"] * scale))
    ls = LINE_STYLES.get(s.get("line_style", "solid"), Qt.SolidLine)
    p.setRenderHint(QPainter.Antialiasing, s.get("anti_aliasing", True))
    base = QColor(s["color"])
    base.setAlpha(s["opacity"])
    p.save()
    p.translate(cx, cy)
    if s.get("rotation"):
        p.rotate(s["rotation"])

    def render(color, w):
        p.setPen(QPen(color, w, ls, Qt.RoundCap))
        p.setBrush(Qt.NoBrush)
        if style in ("cross", "cross_dot", "t_shape", "triple"):
            p.drawLine(-gap - size, 0, -gap, 0)
            p.drawLine(gap, 0, gap + size, 0)
            p.drawLine(0, -gap - size, 0, -gap)
            if style != "t_shape":
                p.drawLine(0, gap, 0, gap + size)
        if style == "triple":
            p.drawLine(-gap - size, gap, gap + size, gap)
        if style == "x_shape":
            k = 0.70710678
            o, i = (gap + size) * k, gap * k
            p.drawLine(int(-o), int(-o), int(-i), int(-i))
            p.drawLine(int(i), int(i), int(o), int(o))
            p.drawLine(int(o), int(-o), int(i), int(-i))
            p.drawLine(int(-i), int(i), int(-o), int(o))
        if style in ("circle", "circle_dot"):
            p.drawEllipse(QPoint(0, 0), size, size)
        if style == "square":
            p.drawRect(-size, -size, size * 2, size * 2)
        dot_v = style in ("dot", "cross_dot", "circle_dot") or (
            s.get("dot") and style in ("cross", "t_shape", "x_shape",
                                        "triple", "circle", "square"))
        if dot_v:
            p.setBrush(QBrush(color))
            p.drawEllipse(QPoint(0, 0), max(1, t), max(1, t))
            p.setBrush(Qt.NoBrush)

    if s.get("glow"):
        gc = QColor(s.get("glow_color", s["color"]))
        n = max(1, s.get("glow_intensity", 3))
        for i in range(n, 0, -1):
            gc.setAlpha(int(s["opacity"] * (i / (n + 1)) * 0.4))
            render(gc, t + i * 2)
    if s.get("outline"):
        ow = max(1, int(s.get("outline_width", 1) * scale))
        render(QColor(0, 0, 0, s["opacity"]), t + ow * 2)
    render(base, t)
    p.restore()


def draw_icon(p, name, rect, color):
    p.setPen(QPen(color, 1.7, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
    p.setBrush(Qt.NoBrush)
    x, y, w, h = rect.x(), rect.y(), rect.width(), rect.height()
    cx, cy = x + w / 2, y + h / 2
    if name == "crosshair":
        r = w * 0.34
        p.drawLine(QPointF(cx - r, cy), QPointF(cx - r * 0.35, cy))
        p.drawLine(QPointF(cx + r * 0.35, cy), QPointF(cx + r, cy))
        p.drawLine(QPointF(cx, cy - r), QPointF(cx, cy - r * 0.35))
        p.drawLine(QPointF(cx, cy + r * 0.35), QPointF(cx, cy + r))
    elif name == "palette":
        p.drawEllipse(QPointF(cx, cy), w * 0.34, h * 0.34)
        p.setBrush(color)
        p.setPen(Qt.NoPen)
        p.drawEllipse(QPointF(cx - w * 0.12, cy - h * 0.1), 1.4, 1.4)
        p.drawEllipse(QPointF(cx + w * 0.12, cy - h * 0.1), 1.4, 1.4)
        p.drawEllipse(QPointF(cx, cy + h * 0.14), 1.4, 1.4)
    elif name == "gear":
        p.drawEllipse(QPointF(cx, cy), w * 0.33, h * 0.33)
        p.setBrush(color)
        p.setPen(Qt.NoPen)
        p.drawEllipse(QPointF(cx, cy), w * 0.1, h * 0.1)
    elif name == "layers":
        p.drawLine(QPointF(cx - w * 0.3, cy - h * 0.12), QPointF(cx + w * 0.3, cy - h * 0.12))
        p.drawLine(QPointF(cx - w * 0.3, cy + h * 0.05), QPointF(cx + w * 0.3, cy + h * 0.05))
        p.drawLine(QPointF(cx - w * 0.3, cy + h * 0.22), QPointF(cx + w * 0.3, cy + h * 0.22))


# ================= Overlay =================
class Overlay(QWidget):
    def __init__(self, settings):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint |
                            Qt.Tool | Qt.WindowTransparentForInput)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        self.settings = settings
        self._apply_screen(settings.get("screen_index", 0))
        self.show()

    def _apply_screen(self, idx):
        screens = QApplication.screens()
        idx = min(idx, len(screens) - 1)
        self.setGeometry(screens[idx].geometry())
        self.settings["screen_index"] = idx
        self.update()

    def set_screen(self, idx):
        self._apply_screen(idx)

    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        draw_crosshair(p, self.width() // 2 + self.settings["offset_x"],
                       self.height() // 2 + self.settings["offset_y"], self.settings)


# ================= Widgets =================
class Preview(QWidget):
    def __init__(self, overlay):
        super().__init__()
        self.overlay = overlay
        self.setMinimumHeight(180)

    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), 14, 14)
        p.setClipPath(path)
        grad = QLinearGradient(0, 0, self.width(), self.height())
        if config.CURRENT_THEME == "dark":
            grad.setColorAt(0, QColor("#050507"))
            grad.setColorAt(1, QColor("#0f0f12"))
        else:
            grad.setColorAt(0, QColor("#1a1a1d"))
            grad.setColorAt(1, QColor("#252529"))
        p.fillRect(self.rect(), grad)
        p.setPen(QPen(QColor(255, 255, 255, 14), 1.5))
        for x in range(0, self.width(), 22):
            for y in range(0, self.height(), 22):
                p.drawPoint(x, y)
        s = self.overlay.settings
        cx, cy = self.width() // 2, self.height() // 2
        max_d = (s["size"] + s["gap"] + s["thickness"]) * 2 + 30
        if s["style"] in ("x_shape", "square"):
            max_d = int(max_d * 1.4)
        scale = min(1.5, (min(self.width(), self.height()) - 40) / max_d) if max_d else 1.0
        draw_crosshair(p, cx, cy, s, scale)


class ToggleSwitch(QAbstractButton):
    def __init__(self, checked=False):
        super().__init__()
        self.setCheckable(True)
        self.setChecked(checked)
        self.setFixedSize(42, 24)
        self.setCursor(Qt.PointingHandCursor)
        self.toggled.connect(lambda _: self.update())

    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        p.setPen(Qt.NoPen)
        on = self.isChecked()
        p.setBrush(QColor(C["accent"] if on else C["border_h"]))
        p.drawRoundedRect(0, 0, 42, 24, 12, 12)
        p.setBrush(QColor("#ffffff") if on or config.CURRENT_THEME == "light"
                   else QColor("#d4d4d8"))
        p.drawEllipse(22 if on else 2, 2, 20, 20)


class SliderRow(QWidget):
    valueChanged = pyqtSignal(int)

    def __init__(self, label="", mn=0, mx=100, val=0, suffix=""):
        super().__init__()
        self.suffix = suffix
        v = QVBoxLayout(self)
        v.setContentsMargins(0, 0, 0, 0)
        v.setSpacing(6)
        row = QHBoxLayout()
        self.lbl = QLabel(label)
        self.lbl.setStyleSheet(f"color:{C['text2']};font-size:12px;font-weight:500;")
        self.val = QLabel(f"{val}{suffix}")
        self.val.setStyleSheet(f"color:{C['accent']};font-size:12px;font-weight:700;")
        self.val.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.val.setFixedWidth(50)
        row.addWidget(self.lbl)
        row.addStretch()
        row.addWidget(self.val)
        v.addLayout(row)
        self.s = QSlider(Qt.Horizontal)
        self.s.setRange(mn, mx)
        self.s.setValue(val)
        self.s.setCursor(Qt.PointingHandCursor)
        self.s.setStyleSheet(f"""
            QSlider::groove:horizontal {{ height:6px; background:{C['border']}; border-radius:3px; }}
            QSlider::sub-page:horizontal {{ background:{C['accent']}; border-radius:3px; }}
            QSlider::handle:horizontal {{ background:{C['surface']}; width:18px; height:18px;
                margin:-6px 0; border-radius:9px; border:2px solid {C['accent']}; }}
            QSlider::handle:horizontal:hover {{ background:{C['accent_bg']}; }}
        """)
        self.s.valueChanged.connect(self._on)
        v.addWidget(self.s)

    def _on(self, v):
        self.val.setText(f"{v}{self.suffix}")
        self.valueChanged.emit(v)

    def setValue(self, v):
        self.s.blockSignals(True)
        self.s.setValue(v)
        self.s.blockSignals(False)
        self.val.setText(f"{v}{self.suffix}")


class ColorSwatch(QAbstractButton):
    def __init__(self, color, size=28):
        super().__init__()
        self.color = color
        self.setFixedSize(size, size)
        self.setCursor(Qt.PointingHandCursor)

    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        p.setPen(QPen(QColor(C["border"]), 2))
        p.setBrush(QColor(self.color))
        p.drawEllipse(1, 1, self.width() - 2, self.height() - 2)
        if self.underMouse():
            p.setPen(QPen(QColor(C["text"]), 2))
            p.setBrush(Qt.NoBrush)
            p.drawEllipse(1, 1, self.width() - 2, self.height() - 2)

    def enterEvent(self, e): self.update()
    def leaveEvent(self, e): self.update()


class PillButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setCheckable(True)
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumHeight(34)
        self.setStyleSheet(f"""
            QPushButton {{
                background: {C['surface2']}; border: 1.5px solid {C['border']};
                border-radius: 8px; padding: 6px 14px;
                color: {C['text2']}; font-size: 12px; font-weight: 500;
            }}
            QPushButton:hover {{ border-color: {C['border_h']}; color: {C['text']}; }}
            QPushButton:checked {{
                background: {C['accent_bg']}; border-color: {C['accent']};
                color: {C['accent']}; font-weight: 600;
            }}
        """)


class SidebarButton(QPushButton):
    def __init__(self, icon_name, text):
        super().__init__("")
        self.icon_name = icon_name
        self.setCheckable(True)
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumHeight(44)
        self.setFlat(True)
        lay = QHBoxLayout(self)
        lay.setContentsMargins(14, 8, 14, 8)
        lay.setSpacing(10)
        self.icon_lbl = QLabel()
        self.icon_lbl.setFixedSize(18, 18)
        self.icon_lbl.setStyleSheet("background:transparent;")
        self.text_lbl = QLabel(text)
        lay.addWidget(self.icon_lbl)
        lay.addWidget(self.text_lbl)
        lay.addStretch()
        self.setStyleSheet(f"""
            QPushButton {{ background: transparent; border: none; border-radius: 8px; padding: 0; }}
            QPushButton:hover {{ background: {C['surface2']}; }}
            QPushButton:checked {{ background: {C['accent_bg']}; }}
        """)
        self.toggled.connect(self._refresh)
        self._refresh()

    def _refresh(self):
        ch = self.isChecked()
        color = QColor(C["accent"] if ch else C["text2"])
        dpr = self.devicePixelRatioF() or 1.0
        px = max(1, int(round(18 * dpr)))
        pm = QPixmap(px, px)
        pm.setDevicePixelRatio(dpr)
        pm.fill(Qt.transparent)
        p = QPainter(pm)
        p.setRenderHint(QPainter.Antialiasing, True)
        p.setRenderHint(QPainter.SmoothPixmapTransform, True)
        p.setRenderHint(QPainter.HighQualityAntialiasing, True)
        draw_icon(p, self.icon_name, QRectF(0, 0, 18, 18), color)
        p.end()
        self.icon_lbl.setPixmap(pm)
        self.text_lbl.setStyleSheet(
            f"color:{C['accent'] if ch else C['text2']};"
            f"font-size:13px; font-weight:{600 if ch else 500};"
            f"background:transparent;")


class Card(QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(f"""
            QFrame {{ background: {C['surface']}; border: 1px solid {C['border']};
                     border-radius: 14px; }}
        """)
        self.v = QVBoxLayout(self)
        self.v.setContentsMargins(22, 20, 22, 20)
        self.v.setSpacing(14)


# ================= App icon =================
def make_app_icon():
    if getattr(sys, "frozen", False):
        script_dir = getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
    else:
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__)) if __file__ else os.getcwd()
        except NameError:
            script_dir = os.getcwd()

    for p in (
        os.path.join(script_dir, "logo.png"),
        os.path.join(script_dir, "assets", "logo.png"),
        os.path.join(script_dir, "icon", "logo.png"),
    ):
        if os.path.isfile(p):
            ic = QIcon(p)
            if not ic.isNull():
                print(f"[Icon] Loaded from {p}")
                return ic

    icon = QIcon()
    for size in (16, 24, 32, 48, 64, 128, 256):
        pm = QPixmap(size, size)
        pm.fill(Qt.transparent)
        p = QPainter(pm)
        p.setRenderHint(QPainter.Antialiasing, True)
        p.setRenderHint(QPainter.HighQualityAntialiasing, True)
        s = size / 64.0
        grad = QLinearGradient(0, 0, size, size)
        grad.setColorAt(0, QColor(C["accent"]))
        grad.setColorAt(1, QColor(C["accent_h"]))
        p.setPen(QPen(QBrush(grad), max(1.0, 5 * s), Qt.SolidLine, Qt.RoundCap))
        p.drawLine(int(32 * s), int(10 * s), int(32 * s), int(24 * s))
        p.drawLine(int(32 * s), int(40 * s), int(32 * s), int(54 * s))
        p.drawLine(int(10 * s), int(32 * s), int(24 * s), int(32 * s))
        p.drawLine(int(40 * s), int(32 * s), int(54 * s), int(32 * s))
        p.setPen(Qt.NoPen)
        p.setBrush(QBrush(QColor(C["accent"])))
        p.drawEllipse(QPoint(int(32 * s), int(32 * s)),
                      max(1, int(4 * s)), max(1, int(4 * s)))
        p.end()
        icon.addPixmap(pm)
    return icon