import sys, os, json, re, tempfile
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QObject, QTimer, QRect, QRectF
from PyQt5.QtGui import QImage, QPixmap, QColor, QPainter, QPen, QBrush, QPainterPath

try:
    from .engine import (
        get_video_metadata, generate_sheet,
        build_preview_pool_ultrafast, build_preview_pool_refined,
        select_frames_from_pool_fast, select_frames_from_pool_refined,
        extract_final_frames_from_timestamps,
    )
except ImportError:
    try:
        from perfect_grid.engine import (
            get_video_metadata, generate_sheet,
            build_preview_pool_ultrafast, build_preview_pool_refined,
            select_frames_from_pool_fast, select_frames_from_pool_refined,
            extract_final_frames_from_timestamps,
        )
    except ImportError:
        from engine import (
            get_video_metadata, generate_sheet,
            build_preview_pool_ultrafast, build_preview_pool_refined,
            select_frames_from_pool_fast, select_frames_from_pool_refined,
            extract_final_frames_from_timestamps,
        )

try:
    from .pg_i18n import get_tr, language_display_names
except ImportError:
    try:
        from perfect_grid.pg_i18n import get_tr, language_display_names
    except ImportError:
        from pg_i18n import get_tr, language_display_names

APP_NAME    = "Perfect Grid"
APP_VERSION = "1.0.0"


# ─── paths ────────────────────────────────────────────────────────────────────

def resource_path(name):
    base = getattr(sys, "_MEIPASS", os.path.abspath(os.path.dirname(__file__)))
    return os.path.join(base, name)

def app_data_path(name):
    if sys.platform == "win32":
        base = os.path.join(os.environ.get("APPDATA", os.path.expanduser("~")), APP_NAME)
    elif sys.platform == "darwin":
        base = os.path.join(os.path.expanduser("~/Library/Application Support"), APP_NAME)
    else:
        base = os.path.join(os.path.expanduser("~"), ".perfect-grid")
    return os.path.join(base, name)

def ensure_parent_dir(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)


# ─── constants ─────────────────────────────────────────────────────────────────

TMP_DIR              = os.path.join(tempfile.gettempdir(), "PerfectGrid_Temp")
PRESET_RESOURCE_FILE = resource_path("presets_v2.json")
USER_PRESET_FILE     = app_data_path("presets_v2.json")
SETTINGS_FILE        = app_data_path("settings.json")

EXPORT_PROFILES = {
    "Fast 1080p":   {"size": (1920, 1080), "frame_width": 1280, "lossless": False},
    "Detail 1440p": {"size": (2560, 1440), "frame_width": 1600, "lossless": False},
    "Maximum 4K":   {"size": (3840, 2160), "frame_width": 2160, "lossless": True},
}
DEFAULT_EXPORT_PROFILE = "Fast 1080p"

DEFAULTS = {
    "cols": 4, "rows": 3, "spacing": 0, "margin": 30, "f_size": 28,
    "t_x": 30, "t_y": 30, "mode": "Fill", "bg_mode": "Black",
    "grid_x": 0, "grid_y": 0, "tc_show": True, "tc_size": 24,
    "tc_opacity": 255, "tc_shadow": True, "tc_shadow_opacity": 180,
    "vis": {k: True for k in ["name", "size", "res", "dur", "video", "audio"]},
}

BUILT_IN_PRESETS = {
    "6x4 Detail Sheet": {"cols": 6, "rows": 4, "spacing": 0, "margin": 30, "f_size": 28,
                          "t_x": 30, "t_y": 30, "mode": "Fill", "vis": DEFAULTS["vis"], "bg_mode": "Black"},
    "8x5 Contact Sheet": {"cols": 8, "rows": 5, "spacing": 0, "margin": 30, "f_size": 28,
                           "t_x": 30, "t_y": 30, "mode": "Fill", "vis": DEFAULTS["vis"], "bg_mode": "Black"},
}

# ─── design tokens (mirrors watch.usbx.live uploader) ─────────────────────────
# These are injected into the QSS strings below; update here to retheme globally.
_T = {
    # backgrounds
    "bg":          "#050505",
    "bg_card":     "#0f0f0f",
    "bg_input":    "#111111",
    "bg_hover":    "#1a1a1a",
    "bg_active":   "#222222",
    "bg_sidebar":  "#080808",
    # borders
    "border":      "rgba(255,255,255,0.10)",
    "border_focus":"rgba(255,255,255,0.22)",
    # text
    "text":        "#f0f0f0",
    "text_muted":  "#888888",
    "text_dim":    "#555555",
    # accent (pill / slider fill)
    "accent":      "#ffffff",
    "accent_dim":  "rgba(255,255,255,0.18)",
    # tab selected indicator
    "tab_sel_bg":  "#0f0f0f",
    "tab_sel_line": "#ffffff",
}

DARK_QSS = """
QMainWindow, QDialog {{background:{bg};color:{text};font-family:-apple-system,BlinkMacSystemFont,"SF Pro Text","Segoe UI",Arial;font-size:13px;}}
QWidget {{background:transparent;color:{text};}}
QMainWindow::centralWidget {{background:{bg};}}

/* ── menu bar ── */
QMenuBar {{background:{bg};color:{text_muted};border-bottom:1px solid {border};padding:0 4px;}}
QMenuBar::item {{padding:6px 10px;border-radius:6px;}}
QMenuBar::item:selected {{background:{bg_hover};color:{text};}}
QMenu {{background:{bg_card};border:1px solid {border};border-radius:8px;padding:4px;}}
QMenu::item {{padding:7px 14px;border-radius:6px;}}
QMenu::item:selected {{background:{bg_hover};}}

/* ── scroll area ── */
QScrollArea {{background:transparent;border:0;}}
QScrollBar:vertical {{background:transparent;width:4px;margin:0;}}
QScrollBar::handle:vertical {{background:{border_focus};border-radius:2px;min-height:24px;}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{height:0;}}

/* ── tabs ── */
QTabWidget::pane {{border:1px solid {border};border-radius:10px;background:{bg_card};margin-top:-1px;}}
QTabBar::tab {{padding:8px 14px;border:none;color:{text_muted};background:transparent;font-size:12px;font-weight:500;}}
QTabBar::tab:selected {{color:{text};background:{tab_sel_bg};border-bottom:2px solid {tab_sel_line};border-top-left-radius:10px;border-top-right-radius:10px;}}
QTabBar::tab:hover:!selected {{color:{text};}}

/* ── labels ── */
QLabel {{background:transparent;color:{text};}}
QLabel#FieldLabel {{font-weight:600;color:{text_muted};font-size:11px;letter-spacing:0.5px;text-transform:uppercase;}}
QLabel#PreviewPane {{background:{bg_card};border:1px solid {border};border-radius:10px;color:{text_muted};}}
QLabel#StatusLabel {{color:{text_muted};font-size:12px;padding:4px 0;}}

/* ── buttons ── */
QPushButton {{
    background:{bg_card};
    border:1px solid {border};
    border-radius:8px;
    padding:8px 14px;
    color:{text};
    font-weight:500;
    font-size:13px;
}}
QPushButton:hover {{background:{bg_hover};border-color:{border_focus};}}
QPushButton:pressed {{background:{bg_active};}}
QPushButton#PrimaryButton {{
    background:{accent};
    color:#000000;
    border:none;
    font-weight:700;
    letter-spacing:0.2px;
}}
QPushButton#PrimaryButton:hover {{background:#e0e0e0;}}
QPushButton#PrimaryButton:pressed {{background:#c8c8c8;}}
QPushButton#SecondaryButton {{
    background:{bg_card};
    color:{text_muted};
    border:1px solid {border};
}}
QPushButton#SecondaryButton:hover {{background:{bg_hover};color:{text};border-color:{border_focus};}}
QPushButton#ColorSwatch {{
    border-radius:6px;
    border:1px solid {border};
    min-width:28px;
    max-width:28px;
    min-height:28px;
    max-height:28px;
    padding:0;
}}

/* ── inputs ── */
QComboBox, QSpinBox, QLineEdit {{
    background:{bg_input};
    border:1px solid {border};
    border-radius:8px;
    padding:6px 10px;
    color:{text};
    selection-background-color:{bg_hover};
}}
QComboBox:focus, QSpinBox:focus, QLineEdit:focus {{border-color:{border_focus};}}
QComboBox::drop-down {{border:none;width:28px;}}
QComboBox::down-arrow {{image:none;width:0;height:0;}}
QComboBox QAbstractItemView {{
    background:{bg_card};
    border:1px solid {border};
    border-radius:8px;
    selection-background-color:{bg_hover};
    padding:4px;
    outline:0;
    font-size:13px;
}}
QComboBox QAbstractItemView::item {{
    min-height:34px;
    padding:6px 14px;
    color:{text};
    border-radius:6px;
}}
QComboBox QAbstractItemView::item:selected {{
    background:{bg_hover};
    color:{text};
}}
QSpinBox::up-button, QSpinBox::down-button {{width:0;border:0;}}

/* ── checkboxes — handled by PixelCheckBox custom widget ── */
QCheckBox {{color:{text};spacing:0px;}}
QCheckBox::indicator {{width:0;height:0;}}

/* ── list widget ── */
QListWidget {{
    background:{bg_input};
    border:1px solid {border};
    border-radius:8px;
    padding:4px;
    outline:0;
}}
QListWidget::item {{padding:7px 8px;border-radius:6px;color:{text_muted};}}
QListWidget::item:selected {{background:{bg_hover};color:{text};}}
QListWidget::item:hover {{background:{bg_hover};color:{text};}}

/* ── progress bar (3px pill at bottom of sidebar) ── */
QProgressBar {{border:0;background:{bg_card};border-radius:1px;}}
QProgressBar::chunk {{background:{accent};border-radius:1px;}}

/* ── message boxes / dialogs ── */
QMessageBox, QInputDialog {{background:{bg_card};}}
QMessageBox QLabel, QInputDialog QLabel {{color:{text};}}
""".format(**_T)


# ─── custom widgets ────────────────────────────────────────────────────────────

class SlimSlider(QWidget):
    """
    Custom slider that matches the uploader site aesthetic:
    - Thin 3px track
    - Pill-shaped filled portion (white) to the left of the handle
    - 14px circular handle with slight glow on hover
    - No QSS slider ugliness — all drawn via QPainter
    """
    valueChanged = pyqtSignal(int)

    _TRACK_H   = 3
    _HANDLE_R  = 7   # radius (diameter = 14px)
    _HANDLE_R_HOVER = 8

    def __init__(self, minimum=0, maximum=100, value=0, parent=None):
        super().__init__(parent)
        self._min     = minimum
        self._max     = maximum
        self._val     = max(minimum, min(maximum, value))
        self._default = value   # stored for double-click reset
        self._hover   = False
        self._drag    = False
        self.setFixedHeight(28)
        self.setCursor(Qt.PointingHandCursor)
        self.setMouseTracking(True)

    # public API mirrors QSlider
    def minimum(self): return self._min
    def maximum(self): return self._max
    def value(self):   return self._val

    def setRange(self, lo, hi):
        self._min = lo; self._max = hi
        self._val = max(lo, min(hi, self._val))
        self.update()

    def setValue(self, v):
        v = max(self._min, min(self._max, int(v)))
        if v != self._val:
            self._val = v
            self.valueChanged.emit(v)
            self.update()

    # geometry helpers
    def _track_rect(self):
        cy = self.height() // 2
        return QRect(self._HANDLE_R_HOVER + 1, cy - self._TRACK_H // 2,
                     self.width() - 2 * (self._HANDLE_R_HOVER + 1), self._TRACK_H)

    def _val_to_x(self, val):
        tr = self._track_rect()
        span = self._max - self._min
        if span == 0:
            return tr.left()
        frac = (val - self._min) / span
        return tr.left() + int(frac * tr.width())

    def _x_to_val(self, x):
        tr = self._track_rect()
        frac = max(0.0, min(1.0, (x - tr.left()) / max(1, tr.width())))
        return self._min + int(round(frac * (self._max - self._min)))

    def paintEvent(self, _):
        p   = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        tr  = self._track_rect()
        hx  = self._val_to_x(self._val)
        cy  = self.height() // 2
        r   = self._HANDLE_R_HOVER if self._hover else self._HANDLE_R

        # full track (dark)
        p.setPen(Qt.NoPen)
        p.setBrush(QBrush(QColor(45, 45, 45)))
        p.drawRoundedRect(tr, 2, 2)

        # filled portion (white pill)
        filled = QRect(tr.left(), tr.top(), max(0, hx - tr.left()), tr.height())
        if filled.width() > 0:
            p.setBrush(QBrush(QColor(255, 255, 255)))
            p.drawRoundedRect(filled, 2, 2)

        # handle glow (subtle, only on hover/drag)
        if self._hover or self._drag:
            glow = QColor(255, 255, 255, 30)
            p.setBrush(QBrush(glow))
            p.drawEllipse(hx - r - 4, cy - r - 4, (r + 4) * 2, (r + 4) * 2)

        # handle
        p.setBrush(QBrush(QColor(255, 255, 255)))
        p.setPen(QPen(QColor(80, 80, 80), 0.5))
        p.drawEllipse(hx - r, cy - r, r * 2, r * 2)
        p.end()

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self._drag = True
            self.setValue(self._x_to_val(e.x()))

    def mouseMoveEvent(self, e):
        if self._drag:
            self.setValue(self._x_to_val(e.x()))
        # hover state for handle glow
        hx  = self._val_to_x(self._val)
        cy  = self.height() // 2
        r   = self._HANDLE_R_HOVER + 4
        was = self._hover
        self._hover = (abs(e.x() - hx) <= r and abs(e.y() - cy) <= r)
        if was != self._hover:
            self.update()

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            self._drag = False
            self.update()

    def leaveEvent(self, _):
        self._hover = False
        self.update()

    def mouseDoubleClickEvent(self, e):
        if e.button() == Qt.LeftButton and self._default is not None:
            self.setValue(self._default)

    def wheelEvent(self, e):
        delta = 1 if e.angleDelta().y() > 0 else -1
        self.setValue(self._val + delta)


class PixelCheckBox(QWidget):
    """
    Fully custom checkbox — painted with QPainter.
    Box: dark bg, 1px rgba border, 6px radius.
    Checked: white fill + minimal SVG-style checkmark drawn with QPainter lines.
    Label: plain QLabel to the right.
    """
    stateChanged = pyqtSignal(int)

    _BOX = 15  # box size px

    def __init__(self, label="", checked=True, parent=None):
        super().__init__(parent)
        self._checked = checked
        self._hover   = False

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        self._box = _CheckBoxIndicator(self)
        self._lbl = QLabel(label)
        self._lbl.setStyleSheet("color:#c8c8c8;font-size:13px;background:transparent;")
        layout.addWidget(self._box)
        layout.addWidget(self._lbl)
        layout.addStretch()

        self.setFixedHeight(28)
        self.setCursor(Qt.PointingHandCursor)

    def isChecked(self):  return self._checked
    def setChecked(self, v):
        self._checked = bool(v)
        self._box.update()
        self.stateChanged.emit(2 if self._checked else 0)

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.setChecked(not self._checked)

    def enterEvent(self, _):
        self._hover = True;  self._box.update()
    def leaveEvent(self, _):
        self._hover = False; self._box.update()


class _CheckBoxIndicator(QWidget):
    """Inner painter widget for the box+tick — kept separate so sizing is exact."""
    def __init__(self, owner):
        super().__init__(owner)
        self._o = owner
        self.setFixedSize(PixelCheckBox._BOX, PixelCheckBox._BOX)

    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        s = PixelCheckBox._BOX

        checked = self._o._checked
        hover   = self._o._hover

        # box fill
        if checked:
            p.setBrush(QBrush(QColor(255, 255, 255)))
        else:
            p.setBrush(QBrush(QColor(17, 17, 17)))

        # border
        if hover and not checked:
            border_col = QColor(255, 255, 255, 80)
        elif checked:
            border_col = QColor(255, 255, 255)
        else:
            border_col = QColor(255, 255, 255, 28)

        p.setPen(QPen(border_col, 1.0))
        p.drawRoundedRect(QRectF(0.5, 0.5, s - 1, s - 1), 5, 5)

        # checkmark (two line segments, tuned for 15px box)
        if checked:
            pen = QPen(QColor(0, 0, 0), 1.5, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
            p.setPen(pen)
            p.drawLine(3, 8, 6, 11)
            p.drawLine(6, 11, 12, 3)
        p.end()


class StyledCombo(QComboBox):
    """QComboBox subclass that paints its own ▾ arrow so macOS doesn't mangle it."""
    def paintEvent(self, event):
        super().paintEvent(event)
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        # draw ▾ in the right gutter
        p.setPen(QPen(QColor(120, 120, 120)))
        p.setFont(self.font())
        arrow_rect = self.rect().adjusted(self.width() - 22, 0, 0, 0)
        p.drawText(arrow_rect, Qt.AlignVCenter | Qt.AlignHCenter, "▾")
        p.end()


# ─── background worker ──────────────────────────────────────────────────────────

class PreviewPoolWorker(QObject):
    finished = pyqtSignal(object, str)
    error    = pyqtSignal(str)
    status   = pyqtSignal(str)

    def __init__(self, path, tmp_dir, start, end, meta=None, mode="ultrafast", target_count=12):
        super().__init__()
        self.path         = path
        self.tmp_dir      = tmp_dir
        self.start        = start
        self.end          = end
        self.meta         = meta
        self.mode         = mode
        self.target_count = target_count

    def run(self):
        try:
            if self.mode == "refined":
                pool = build_preview_pool_refined(self.path, self.tmp_dir, self.start, self.end,
                                                  meta=self.meta, target_count=self.target_count,
                                                  progress=self.status.emit)
            else:
                pool = build_preview_pool_ultrafast(self.path, self.tmp_dir, self.start, self.end,
                                                    meta=self.meta, target_count=self.target_count,
                                                    progress=self.status.emit)
            self.finished.emit(pool, self.mode)
        except Exception as e:
            self.error.emit(str(e))


# ─── main window ───────────────────────────────────────────────────────────────

class PerfectGrid(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Perfect Grid")
        self.resize(1400, 950)
        self.setMinimumSize(900, 600)

        # state
        self.video_path        = None
        self.current_frames    = []
        self.font_family       = "Arial"
        self.visibility        = {k: True for k in ["name", "size", "res", "dur", "video", "audio"]}
        self.all_presets       = {}
        self.extract_thread    = None
        self.extract_worker    = None
        self._pending_extract  = False
        self._cursor_busy      = False
        self.video_meta_cache  = {}
        self.theme             = "Dark"
        self.language          = "en"
        self.default_output_dir= ""
        self.default_preset    = ""
        self.preview_pool      = None
        self.preview_pool_key  = None
        self.pool_mode         = "ultrafast"
        self.auto_refine       = False
        self.current_preset_name = None
        self.custom_bg_color   = None   # None = use bg_mode black/white

        self.preview_update_timer = QTimer(self)
        self.preview_update_timer.setSingleShot(True)
        self.preview_update_timer.setInterval(80)
        self.preview_update_timer.timeout.connect(self.update_preview)

        # Debounce range-slider changes: wait 400ms before re-extracting.
        self._extraction_debounce = QTimer(self)
        self._extraction_debounce.setSingleShot(True)
        self._extraction_debounce.setInterval(400)
        self._extraction_debounce.timeout.connect(self._do_reload)

        # tr() will be set properly after load_settings
        self._tr = get_tr("en")

        self._build_ui()
        self.load_presets_from_file()
        self.load_settings()
        self._tr = get_tr(self.language)
        if self.language != 'en':
            self.retranslate_ui()
        self.apply_theme()
        if self.default_preset and self.default_preset in self.all_presets:
            self.current_preset_name = self.default_preset
            p = self.all_presets[self.default_preset]
            self.cols.setValue(p["cols"]); self.rows.setValue(p["rows"])
            self.spacing.setValue(p["spacing"]); self.margin.setValue(p["margin"])
            self.bg_mode.setCurrentText(p.get("bg_mode", "Black"))
            self.visibility = p.get("vis", {k: True for k in self.checks.keys()})
            for k, cb in self.checks.items():
                cb.setChecked(self.visibility.get(k, True))

    def tr(self, key):
        return self._tr(key)

    def retranslate_ui(self):
        """Update all visible widget text after a language change."""
        # Bottom bar
        self.btn_refresh.setText(self.tr("refresh"))
        self.btn_export.setText(self.tr("export_png"))
        if self.status_label.text() in ("Ready", "就绪", "Pronto", "Listo",
                                        "準備完了", "Prêt", "Bereit", "준비됨"):
            self.status_label.setText(self.tr("ready"))
        if not self.video_path:
            self.preview_label.setText(self.tr("drag_drop"))

        # Tab names
        tab_keys = ["tab_grid", "tab_text", "tab_range", "tab_presets", "tab_batch"]
        for i, key in enumerate(tab_keys):
            self.tabs.setTabText(i, self.tr(key))

        # Grid tab
        self.lbl_scale.setText(self.tr("scaling"))
        self.btn_reset_grid.setText(self.tr("reset_grid"))

        # Text tab
        self.lbl_meta_vis.setText(self.tr("meta_vis"))
        for k, cb in self.checks.items():
            cb._lbl.setText(self.tr(cb._tr_key))
        self.btn_font.setText(self.tr("change_font"))
        self.lbl_tc.setText(self.tr("tc_label"))
        self.tc_toggle._lbl.setText(self.tr("tc_enable"))
        self.tc_shadow_toggle._lbl.setText(self.tr("tc_shadow"))
        self.lbl_bg.setText(self.tr("bg_label"))
        self.btn_reset_text.setText(self.tr("reset_text"))

        # Range tab
        self.lbl_export_q.setText(self.tr("export_q") + ":")
        self.btn_refine.setText(self.tr("refine"))
        self.auto_refine_toggle._lbl.setText(self.tr("auto_refine"))
        self.btn_reset_range.setText(self.tr("reset_range"))

        # Presets tab
        self.btn_save_look.setText(self.tr("save_look"))
        self.btn_load_preset.setText(self.tr("load"))
        self.btn_del_preset.setText(self.tr("delete"))
        self.btn_reset_all.setText(self.tr("reset_all"))

        # Batch tab
        self.btn_clear_batch.setText(self.tr("clear_list"))
        self.btn_run_batch.setText(self.tr("run_batch"))

        # Slider labels
        if hasattr(self, "_slider_labels"):
            for key, lbl in self._slider_labels.items():
                lbl.setText(self.tr(key))

    # ─── ui construction ────────────────────────────────────────────────────────

    def _build_ui(self):
        menubar = self.menuBar()
        menubar.setNativeMenuBar(True)   # macOS: shows in the system menu bar at top

        file_menu = menubar.addMenu("&File")
        open_action = QAction("Open…", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file_dialog)
        file_menu.addAction(open_action)

        save_action = QAction("Export PNG…", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.export_sheet)
        file_menu.addAction(save_action)
        file_menu.addSeparator()

        batch_action = QAction("Batch Mode…", self)
        batch_action.triggered.connect(lambda: self.tabs.setCurrentIndex(4))
        file_menu.addAction(batch_action)

        # Edit menu (macOS expects one — lets standard copy/paste shortcuts work)
        edit_menu = menubar.addMenu("&Edit")
        pref_action = QAction("Preferences…", self)
        pref_action.setShortcut("Ctrl+,")
        pref_action.triggered.connect(self.open_settings_dialog)
        edit_menu.addAction(pref_action)

        # View menu
        view_menu = menubar.addMenu("&View")
        refresh_action = QAction("Refresh Preview", self)
        refresh_action.setShortcut("Ctrl+R")
        refresh_action.triggered.connect(self.load_video_range)
        view_menu.addAction(refresh_action)

        refine_action = QAction("Refine Picks", self)
        refine_action.setShortcut("Ctrl+Shift+R")
        refine_action.triggered.connect(self.run_refine_pass)
        view_menu.addAction(refine_action)

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(12, 8, 12, 12)
        main_layout.setSpacing(12)

        # ── left panel ──────────────────────────────────────────────────────────
        self.left_panel = QWidget()
        self.left_panel.setMinimumWidth(360)
        self.left_panel.setMaximumWidth(440)
        self.left_panel.setObjectName("LeftPanel")
        left_layout = QVBoxLayout(self.left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(8)

        self.sidebar_content = QWidget()
        self.sidebar_content.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sidebar = QVBoxLayout(self.sidebar_content)
        sidebar.setContentsMargins(0, 0, 0, 0)
        self.tabs = QTabWidget()
        sidebar.addWidget(self.tabs)

        self.init_grid_tab()
        self.init_text_tab()
        self.init_range_tab()
        self.init_preset_tab()
        self.init_batch_tab()

        controls_scroll = QScrollArea()
        controls_scroll.setWidgetResizable(True)
        controls_scroll.setFrameShape(QFrame.NoFrame)
        controls_scroll.setWidget(self.sidebar_content)
        left_layout.addWidget(controls_scroll, 1)

        # ── bottom buttons ───────────────────────────────────────────────────────
        bottom = QWidget()
        bottom_lay = QVBoxLayout(bottom)
        bottom_lay.setContentsMargins(0, 4, 0, 0)
        bottom_lay.setSpacing(6)

        self.btn_refresh = QPushButton(self.tr("refresh"))
        self.btn_refresh.setObjectName("SecondaryButton")
        self.btn_refresh.setMinimumHeight(38)
        self.btn_refresh.clicked.connect(self.load_video_range)
        bottom_lay.addWidget(self.btn_refresh)

        self.btn_export = QPushButton(self.tr("export_png"))
        self.btn_export.setObjectName("PrimaryButton")
        self.btn_export.setMinimumHeight(44)
        self.btn_export.clicked.connect(self.export_sheet)
        bottom_lay.addWidget(self.btn_export)

        self.loading_bar = QProgressBar()
        self.loading_bar.setRange(0, 0)
        self.loading_bar.setTextVisible(False)
        self.loading_bar.setFixedHeight(3)
        self.loading_bar.hide()
        bottom_lay.addWidget(self.loading_bar)

        self.status_label = QLabel(self.tr("ready"))
        self.status_label.setObjectName("StatusLabel")
        self.status_label.setWordWrap(True)
        self.status_label.setMinimumHeight(32)
        bottom_lay.addWidget(self.status_label)

        left_layout.addWidget(bottom, 0)
        main_layout.addWidget(self.left_panel, 1)

        # ── preview pane ─────────────────────────────────────────────────────────
        self.preview_label = QLabel(self.tr("drag_drop"))
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setObjectName("PreviewPane")
        main_layout.addWidget(self.preview_label, 3)

        self.setAcceptDrops(True)

    # ─── slider factory ──────────────────────────────────────────────────────────

    def create_slider(self, layout, name, mini, maxi, default, is_grid_size=False, tr_key=None):
        container = QWidget()
        v = QVBoxLayout(container)
        v.setContentsMargins(0, 4, 0, 4)
        v.setSpacing(4)

        lbl = QLabel(name)
        lbl.setObjectName("FieldLabel")
        if tr_key:
            if not hasattr(self, "_slider_labels"):
                self._slider_labels = {}
            self._slider_labels[tr_key] = lbl

        row = QHBoxLayout()
        row.setSpacing(8)

        slider = SlimSlider(mini, maxi, default)
        spin   = QSpinBox()
        spin.setRange(mini, maxi)
        spin.setValue(default)
        spin.setFixedWidth(64)
        spin.setStyleSheet("QSpinBox{border:none;background:transparent;color:#888;font-size:12px;}")

        # keep in sync
        slider.valueChanged.connect(spin.setValue)
        spin.valueChanged.connect(slider.setValue)

        if is_grid_size:
            slider.valueChanged.connect(self.reselect_from_pool_or_reload)
        else:
            slider.valueChanged.connect(self.schedule_preview_update)

        row.addWidget(slider, 1)
        row.addWidget(spin)
        v.addWidget(lbl)
        v.addLayout(row)
        layout.addWidget(container)
        return slider

    # ─── tabs ────────────────────────────────────────────────────────────────────

    def init_grid_tab(self):
        tab = QWidget()
        v = QVBoxLayout(tab)
        v.setContentsMargins(10, 10, 10, 10)
        v.setSpacing(2)

        self.lbl_scale = QLabel(self.tr("scaling"))
        self.lbl_scale.setObjectName("FieldLabel")
        v.addWidget(self.lbl_scale)
        self.scale_mode = StyledCombo()
        self.scale_mode.addItems(["Fill", "Fit", "Stretch"])
        self.scale_mode.currentIndexChanged.connect(self.update_preview)
        v.addWidget(self.scale_mode)
        v.addSpacing(6)

        self.cols    = self.create_slider(v, self.tr("sl_cols"),    1,    15,  4, is_grid_size=True, tr_key="sl_cols")
        self.rows    = self.create_slider(v, self.tr("sl_rows"),    1,    15,  3, is_grid_size=True, tr_key="sl_rows")
        self.spacing = self.create_slider(v, self.tr("sl_spacing"), 0,   100,  0, tr_key="sl_spacing")
        self.margin  = self.create_slider(v, self.tr("sl_margin"),  0,   400, 30, tr_key="sl_margin")
        self.grid_x  = self.create_slider(v, self.tr("sl_grid_x"), -800, 800,  0, tr_key="sl_grid_x")
        self.grid_y  = self.create_slider(v, self.tr("sl_grid_y"), -800, 800,  0, tr_key="sl_grid_y")

        v.addSpacing(8)
        self.btn_reset_grid = QPushButton(self.tr("reset_grid"))
        self.btn_reset_grid.clicked.connect(self.reset_grid_defaults)
        v.addWidget(self.btn_reset_grid)
        v.addStretch()
        self.tabs.addTab(tab, self.tr("tab_grid"))

    def init_text_tab(self):
        tab = QWidget()
        v = QVBoxLayout(tab)
        v.setContentsMargins(10, 10, 10, 10)
        v.setSpacing(2)

        self.lbl_meta_vis = QLabel(self.tr("meta_vis"))
        self.lbl_meta_vis.setObjectName("FieldLabel")
        v.addWidget(self.lbl_meta_vis)

        grid_v = QGridLayout()
        grid_v.setHorizontalSpacing(6)
        grid_v.setVerticalSpacing(4)
        self.checks = {}
        check_keys = [("name","cb_name"),("size","cb_size"),("res","cb_res"),
                      ("dur","cb_dur"),("video","cb_video"),("audio","cb_audio")]
        for i, (k, tr_key) in enumerate(check_keys):
            cb = PixelCheckBox(self.tr(tr_key), checked=True)
            cb.stateChanged.connect(self.update_vis)
            cb._tr_key = tr_key
            self.checks[k] = cb
            grid_v.addWidget(cb, i // 2, i % 2)
        v.addLayout(grid_v)
        v.addSpacing(8)

        self.btn_font = QPushButton(self.tr("change_font"))
        self.btn_font.clicked.connect(self.pick_font)
        v.addWidget(self.btn_font)
        v.addSpacing(4)

        self.font_size = self.create_slider(v, self.tr("sl_fsize"), 10,  80, 28, tr_key="sl_fsize")
        self.text_x    = self.create_slider(v, self.tr("sl_tx"),     0, 1000, 30, tr_key="sl_tx")
        self.text_y    = self.create_slider(v, self.tr("sl_ty"),     0,  500, 30, tr_key="sl_ty")

        v.addSpacing(10)
        self.lbl_tc = QLabel(self.tr("tc_label"))
        self.lbl_tc.setObjectName("FieldLabel")
        v.addWidget(self.lbl_tc)
        self.tc_toggle = PixelCheckBox(self.tr("tc_enable"), checked=True)
        self.tc_toggle.stateChanged.connect(self.update_preview)
        v.addWidget(self.tc_toggle)
        self.tc_size           = self.create_slider(v, self.tr("sl_tcsize"),    10, 80,  24, tr_key="sl_tcsize")
        self.tc_opacity        = self.create_slider(v, self.tr("sl_tcopacity"),  0, 255, 255, tr_key="sl_tcopacity")
        self.tc_shadow_toggle  = PixelCheckBox(self.tr("tc_shadow"), checked=True)
        self.tc_shadow_toggle.stateChanged.connect(self.update_preview)
        v.addWidget(self.tc_shadow_toggle)
        self.tc_shadow_opacity = self.create_slider(v, self.tr("sl_shopacity"),  0, 255, 180, tr_key="sl_shopacity")

        v.addSpacing(10)
        self.lbl_bg = QLabel(self.tr("bg_label"))
        self.lbl_bg.setObjectName("FieldLabel")
        v.addWidget(self.lbl_bg)

        bg_row = QHBoxLayout()
        self.bg_mode = StyledCombo()
        self.bg_mode.addItems(["Black", "White", "Custom"])
        self.bg_mode.currentIndexChanged.connect(self._on_bg_mode_changed)
        bg_row.addWidget(self.bg_mode, 1)

        self.bg_color_swatch = QPushButton()
        self.bg_color_swatch.setObjectName("ColorSwatch")
        self.bg_color_swatch.clicked.connect(self.pick_bg_color)
        self._update_swatch()
        bg_row.addWidget(self.bg_color_swatch)
        v.addLayout(bg_row)

        v.addSpacing(6)
        self.btn_reset_text = QPushButton(self.tr("reset_text"))
        self.btn_reset_text.clicked.connect(self.reset_text_defaults)
        v.addWidget(self.btn_reset_text)
        v.addStretch()
        self.tabs.addTab(tab, self.tr("tab_text"))

    def init_range_tab(self):
        tab = QWidget()
        v = QVBoxLayout(tab)
        v.setContentsMargins(10, 10, 10, 10)
        v.setSpacing(2)

        self.start_p = self.create_slider(v, self.tr("sl_start"), 0,  99,   0, tr_key="sl_start")
        self.end_p   = self.create_slider(v, self.tr("sl_end"),   1, 100, 100, tr_key="sl_end")
        self.start_p.valueChanged.connect(self.load_video_range)
        self.end_p.valueChanged.connect(self.load_video_range)

        v.addSpacing(8)
        self.lbl_export_q = QLabel(self.tr("export_q") + ":")
        self.lbl_export_q.setObjectName("FieldLabel")
        v.addWidget(self.lbl_export_q)
        self.export_quality = StyledCombo()
        self.export_quality.addItems(EXPORT_PROFILES.keys())
        self.export_quality.setCurrentText(DEFAULT_EXPORT_PROFILE)
        v.addWidget(self.export_quality)
        v.addSpacing(8)

        self.btn_refine = QPushButton(self.tr("refine"))
        self.btn_refine.clicked.connect(self.run_refine_pass)
        v.addWidget(self.btn_refine)

        self.auto_refine_toggle = PixelCheckBox(self.tr("auto_refine"), checked=False)
        self.auto_refine_toggle.stateChanged.connect(self.set_auto_refine)
        v.addWidget(self.auto_refine_toggle)

        v.addSpacing(8)
        self.btn_reset_range = QPushButton(self.tr("reset_range"))
        self.btn_reset_range.clicked.connect(self.reset_range_defaults)
        v.addWidget(self.btn_reset_range)
        v.addStretch()
        self.tabs.addTab(tab, self.tr("tab_range"))

    def init_preset_tab(self):
        tab = QWidget()
        v = QVBoxLayout(tab)
        v.setContentsMargins(10, 10, 10, 10)
        v.setSpacing(6)
        self.preset_list = QListWidget()
        v.addWidget(self.preset_list)
        h = QHBoxLayout()
        h.setSpacing(6)
        self.btn_save_look   = QPushButton(self.tr("save_look"))
        self.btn_load_preset = QPushButton(self.tr("load"))
        self.btn_del_preset  = QPushButton(self.tr("delete"))
        self.btn_save_look.clicked.connect(self.save_preset)
        self.btn_load_preset.clicked.connect(self.load_selected_preset)
        self.btn_del_preset.clicked.connect(self.delete_preset)
        for b in [self.btn_save_look, self.btn_load_preset, self.btn_del_preset]:
            h.addWidget(b)
        v.addLayout(h)
        self.btn_reset_all = QPushButton(self.tr("reset_all"))
        self.btn_reset_all.clicked.connect(self.reset_all_defaults)
        v.addWidget(self.btn_reset_all)
        v.addStretch()
        self.tabs.addTab(tab, self.tr("tab_presets"))

    def init_batch_tab(self):
        tab = QWidget()
        v = QVBoxLayout(tab)
        v.setContentsMargins(10, 10, 10, 10)
        v.setSpacing(6)
        self.batch_list = QListWidget()
        v.addWidget(self.batch_list)
        self.btn_clear_batch = QPushButton(self.tr("clear_list"))
        self.btn_clear_batch.clicked.connect(self.batch_list.clear)
        v.addWidget(self.btn_clear_batch)
        self.btn_run_batch = QPushButton(self.tr("run_batch"))
        self.btn_run_batch.clicked.connect(self.run_batch_processing)
        v.addWidget(self.btn_run_batch)
        v.addStretch()
        self.tabs.addTab(tab, self.tr("tab_batch"))

    # ─── background color ────────────────────────────────────────────────────────

    def _on_bg_mode_changed(self):
        is_custom = self.bg_mode.currentText() == "Custom"
        self.bg_color_swatch.setVisible(is_custom)
        self.schedule_preview_update()

    def _update_swatch(self):
        c = self.custom_bg_color or "#000000"
        self.bg_color_swatch.setStyleSheet(
            f"QPushButton#ColorSwatch{{background:{c};border:1px solid rgba(255,255,255,0.15);border-radius:6px;}}"
        )
        self.bg_color_swatch.setVisible(self.bg_mode.currentText() == "Custom")

    def pick_bg_color(self):
        initial = QColor(self.custom_bg_color) if self.custom_bg_color else QColor(0, 0, 0)
        c = QColorDialog.getColor(initial, self, "Pick Background Color")
        if c.isValid():
            self.custom_bg_color = c.name()
            self._update_swatch()
            self.schedule_preview_update()

    def bg_color(self):
        mode = self.bg_mode.currentText()
        if mode == "White":
            return (255, 255, 255)
        if mode == "Custom" and self.custom_bg_color:
            c = QColor(self.custom_bg_color)
            return (c.red(), c.green(), c.blue())
        return (0, 0, 0)

    # ─── theme ───────────────────────────────────────────────────────────────────

    def apply_theme(self):
        # Currently only the one dark theme matching your site.
        # Add Light/Slate branches here if needed — same token approach.
        QApplication.instance().setStyleSheet(DARK_QSS)

    # ─── settings ────────────────────────────────────────────────────────────────

    def load_settings(self):
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.theme              = data.get("theme", self.theme)
                self.language           = data.get("language", "en")
                self.default_output_dir = data.get("default_output_dir", "")
                self.default_preset     = data.get("default_preset", "")
                self.custom_bg_color    = data.get("custom_bg_color", None)
            except Exception:
                pass

    def save_settings(self):
        try:
            ensure_parent_dir(SETTINGS_FILE)
            with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
                json.dump({
                    "theme":              self.theme,
                    "language":           self.language,
                    "default_output_dir": self.default_output_dir,
                    "default_preset":     self.default_preset,
                    "custom_bg_color":    self.custom_bg_color,
                }, f)
        except Exception:
            pass

    def open_settings_dialog(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("Perfect Grid Settings")
        dlg.setModal(True)
        dlg.setMinimumWidth(380)
        lay = QVBoxLayout(dlg)
        lay.setSpacing(12)
        lay.setContentsMargins(20, 20, 20, 20)

        # ── language ──
        lay.addWidget(self._section_label("Language"))
        lang_box = StyledCombo()
        for code, display in language_display_names():
            lang_box.addItem(display, code)
        cur_idx = next((i for i in range(lang_box.count()) if lang_box.itemData(i) == self.language), 0)
        lang_box.setCurrentIndex(cur_idx)
        lay.addWidget(lang_box)

        # ── output dir ──
        lay.addWidget(self._section_label("Default Output Directory"))
        dir_row = QHBoxLayout()
        dir_edit = QLineEdit(self.default_output_dir)
        btn_browse = QPushButton("Browse…")
        def browse():
            folder = QFileDialog.getExistingDirectory(self, "Choose Output Folder")
            if folder:
                dir_edit.setText(folder)
        btn_browse.clicked.connect(browse)
        dir_row.addWidget(dir_edit, 1)
        dir_row.addWidget(btn_browse)
        lay.addLayout(dir_row)

        # ── default preset ──
        lay.addWidget(self._section_label("Default Preset"))
        preset_box = StyledCombo()
        preset_box.addItem("— none —")
        preset_box.addItems(list(self.all_presets.keys()))
        if self.default_preset in self.all_presets:
            preset_box.setCurrentText(self.default_preset)
        lay.addWidget(preset_box)

        # ── buttons ──
        lay.addSpacing(8)
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        btn_cancel = QPushButton("Cancel")
        btn_ok     = QPushButton("OK")
        btn_ok.setObjectName("PrimaryButton")
        btn_row.addWidget(btn_cancel)
        btn_row.addWidget(btn_ok)
        lay.addLayout(btn_row)

        def accept():
            self.language           = lang_box.currentData()
            self._tr                = get_tr(self.language)
            self.default_output_dir = dir_edit.text().strip()
            self.default_preset     = preset_box.currentText() if preset_box.currentText() != self.tr("none") else ""
            self.save_settings()
            self.apply_theme()
            self.retranslate_ui()
            dlg.accept()

        btn_ok.clicked.connect(accept)
        btn_cancel.clicked.connect(dlg.reject)
        dlg.exec_()

    def _section_label(self, text):
        lbl = QLabel(text)
        lbl.setObjectName("FieldLabel")
        return lbl

    # ─── presets ─────────────────────────────────────────────────────────────────

    def load_presets_from_file(self):
        self.all_presets = BUILT_IN_PRESETS.copy()
        for path in (PRESET_RESOURCE_FILE, USER_PRESET_FILE):
            if not os.path.exists(path):
                continue
            try:
                with open(path, "r", encoding="utf-8") as f:
                    self.all_presets.update(json.load(f))
            except Exception:
                pass
        self.preset_list.addItems(self.all_presets.keys())

    def save_user_presets(self):
        user_presets = {k: v for k, v in self.all_presets.items() if k not in BUILT_IN_PRESETS}
        ensure_parent_dir(USER_PRESET_FILE)
        with open(USER_PRESET_FILE, "w", encoding="utf-8") as f:
            json.dump(user_presets, f, indent=2)

    def save_preset(self):
        name, ok = QInputDialog.getText(self, "Save Look", "Name:")
        if ok and name:
            self.all_presets[name] = {
                "cols": self.cols.value(), "rows": self.rows.value(),
                "spacing": self.spacing.value(), "margin": self.margin.value(),
                "f_size": self.font_size.value(), "t_x": self.text_x.value(),
                "t_y": self.text_y.value(), "mode": self.scale_mode.currentText(),
                "vis": self.visibility.copy(), "bg_mode": self.bg_mode.currentText(),
            }
            self.save_user_presets()
            if not self.preset_list.findItems(name, Qt.MatchExactly):
                self.preset_list.addItem(name)

    def delete_preset(self):
        item = self.preset_list.currentItem()
        if item:
            name = item.text()
            if name in self.all_presets:
                if name in BUILT_IN_PRESETS:
                    QMessageBox.information(self, "Built-in Preset", "Built-in presets stay available for every user.")
                    return
                del self.all_presets[name]
                self.save_user_presets()
                self.preset_list.takeItem(self.preset_list.row(item))

    def load_selected_preset(self):
        item = self.preset_list.currentItem()
        if item and item.text() in self.all_presets:
            self.current_preset_name = item.text()
            p = self.all_presets[item.text()]
            self.cols.setValue(p["cols"]); self.rows.setValue(p["rows"])
            self.spacing.setValue(p["spacing"]); self.margin.setValue(p["margin"])
            self.font_size.setValue(p["f_size"]); self.text_x.setValue(p.get("t_x", 30))
            self.text_y.setValue(p.get("t_y", 30))
            self.scale_mode.setCurrentText(p.get("mode", "Fill"))
            self.bg_mode.setCurrentText(p.get("bg_mode", "Black"))
            self.visibility = p.get("vis", {k: True for k in self.checks.keys()})
            for k, cb in self.checks.items():
                cb.setChecked(self.visibility.get(k, True))
            self.reselect_from_pool_or_reload()

    # ─── video ops ───────────────────────────────────────────────────────────────

    def open_file_dialog(self):
        fn, _ = QFileDialog.getOpenFileName(
            self, "Open Video", "",
            "Video Files (*.mp4 *.mov *.mkv *.avi *.webm *.ts *.m2ts *.mts *.wmv *.flv *.mpg *.mpeg);;All Files (*)"
        )
        if fn:
            self.video_path = fn
            self.reset_current_video_state()
            self.get_cached_meta(self.video_path)
            self.load_video_range()

    def get_cached_meta(self, path):
        if not path:
            return None
        if path in self.video_meta_cache:
            return self.video_meta_cache[path]
        meta = get_video_metadata(path)
        if meta:
            self.video_meta_cache[path] = meta
        return meta

    def reset_current_video_state(self):
        self.current_frames  = []
        self.preview_pool    = None
        self.preview_pool_key= None
        self.pool_mode       = "ultrafast"
        self.preview_label.setText(self.tr("loading"))
        self.preview_label.setPixmap(QPixmap())
        if hasattr(self, "loading_bar"):
            self.loading_bar.show()

    def load_video_range(self):
        if not self.video_path:
            return
        if self.extract_thread is not None and self.extract_thread.isRunning():
            self._pending_extract = True
            return
        self._pending_extract = False
        self.current_frames   = []
        self.preview_pool     = None
        self.preview_pool_key = None
        self.pool_mode        = "ultrafast"
        self.set_status("Fast preview: seeking thumbnails…")
        self.preview_label.setText(self.tr("loading"))
        self.preview_label.setPixmap(QPixmap())
        self.loading_bar.show()
        self.loading_bar.setRange(0, 0)
        self._prune_cache_if_large()   # prune before each extraction, not just after
        self._start_worker("ultrafast")

    def _start_worker(self, mode):
        meta         = self.get_cached_meta(self.video_path)
        target_count = self.cols.value() * self.rows.value()
        self.extract_thread = QThread()
        self.extract_worker = PreviewPoolWorker(
            self.video_path, TMP_DIR,
            self.start_p.value(), self.end_p.value(),
            meta=meta, mode=mode, target_count=target_count,
        )
        self.extract_worker.moveToThread(self.extract_thread)
        self.extract_thread.started.connect(self.extract_worker.run)
        if mode == "refined":
            self.extract_worker.finished.connect(self.on_refine_ready)
        else:
            self.extract_worker.finished.connect(self.on_preview_pool_ready)
        self.extract_worker.error.connect(self.on_extract_error)
        self.extract_worker.status.connect(self.on_extract_status)
        self.extract_worker.finished.connect(self.extract_worker.deleteLater)
        self.extract_thread.finished.connect(self.extract_thread.deleteLater)
        self.extract_thread.start()

    def on_extract_status(self, msg):
        match = re.search(r"(\d+)/(\d+)", msg)
        if match and hasattr(self, "loading_bar"):
            self.loading_bar.setRange(0, int(match.group(2)))
            self.loading_bar.setValue(int(match.group(1)))
        self.set_status(msg)

    def on_preview_pool_ready(self, pool, mode):
        self.preview_pool     = pool
        self.preview_pool_key = self.get_pool_key()
        self.pool_mode        = "ultrafast"
        if self.extract_thread is not None:
            self.extract_thread.quit(); self.extract_thread.wait()
            self.extract_thread = None
        self.extract_worker = None
        self._prune_cache_if_large()
        self.reselect_from_pool()
        if self._pending_extract:
            self.load_video_range(); return
        if self._cursor_busy:
            QApplication.restoreOverrideCursor(); self._cursor_busy = False
        self.loading_bar.hide(); self.loading_bar.setRange(0, 0)
        if self.auto_refine:
            QTimer.singleShot(150, self.run_refine_pass)

    def run_refine_pass(self):
        if not self.video_path: return
        if self.extract_thread is not None and self.extract_thread.isRunning(): return
        self.set_status("Refine: starting smarter pick pass…")
        self.loading_bar.show(); self.loading_bar.setRange(0, 0)
        self._start_worker("refined")

    def on_refine_ready(self, pool, mode):
        self.preview_pool     = pool
        self.preview_pool_key = self.get_pool_key()
        self.pool_mode        = "refined"
        if self.extract_thread is not None:
            self.extract_thread.quit(); self.extract_thread.wait()
            self.extract_thread = None
        self.extract_worker = None
        self.reselect_from_pool()
        if self._cursor_busy:
            QApplication.restoreOverrideCursor(); self._cursor_busy = False
        self.loading_bar.hide(); self.loading_bar.setRange(0, 0)

    def on_extract_error(self, msg):
        print(f"Frame extraction error: {msg}")
        self.set_status(f"Extraction error: {msg}")
        if self.extract_thread is not None:
            self.extract_thread.quit(); self.extract_thread.wait()
            self.extract_thread = None
        self.extract_worker = None
        if self._pending_extract:
            self.load_video_range()
        elif self._cursor_busy:
            QApplication.restoreOverrideCursor(); self._cursor_busy = False
        self.loading_bar.hide(); self.loading_bar.setRange(0, 0)

    # ─── preview / export ────────────────────────────────────────────────────────

    def get_pool_key(self):
        return (self.video_path, self.start_p.value(), self.end_p.value())

    def reselect_from_pool_or_reload(self):
        if self.preview_pool and self.preview_pool_key == self.get_pool_key():
            self.reselect_from_pool()
        else:
            # Debounce: don't fire a new extraction on every slider tick
            self._extraction_debounce.start()

    def _do_reload(self):
        # Debounce callback: only re-extract after 400ms of range-slider inactivity.
        if not self.preview_pool or self.preview_pool_key != self.get_pool_key():
            self.load_video_range()

    def reselect_from_pool(self):
        if not self.preview_pool or not self.preview_pool.get("frames"):
            self.current_frames = []
            self.preview_label.setText(self.tr("no_frames"))
            self.set_status("No preview frames found. Try a different range or use an H.264 MP4 for fastest loading.")
            if hasattr(self, "loading_bar"):
                self.loading_bar.hide()
            return
        needed = self.cols.value() * self.rows.value()
        if self.pool_mode == "refined":
            self.current_frames = select_frames_from_pool_refined(self.preview_pool, needed)
        else:
            self.current_frames = select_frames_from_pool_fast(self.preview_pool, needed)
        if not self.current_frames:
            self.load_video_range(); return
        self.set_status(("Refined" if self.pool_mode == "refined" else "Fast") + f" preview ready — {len(self.current_frames)} frames.")
        self.update_preview()

    def schedule_preview_update(self):
        self.preview_update_timer.start()

    def update_preview(self):
        if not self.video_path or not self.current_frames:
            return
        meta = self.get_cached_meta(self.video_path)
        if not meta:
            return
        img = generate_sheet(
            self.current_frames, meta, None, self.bg_color(), self.margin.value(),
            self.cols.value(), self.rows.value(), self.spacing.value(),
            self.font_size.value(), (self.text_x.value(), self.text_y.value()),
            (self.grid_x.value(), self.grid_y.value()), self.visibility,
            self.font_family, self.get_tc_opts(), self.scale_mode.currentText(),
        )
        qimg = QImage(img.tobytes("raw", "RGB"), img.size[0], img.size[1], QImage.Format_RGB888)
        self.preview_label.setPixmap(
            QPixmap.fromImage(qimg).scaled(self.preview_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )

    def get_tc_opts(self):
        return {
            "show":           self.tc_toggle.isChecked(),
            "size":           self.tc_size.value(),
            "opacity":        self.tc_opacity.value(),
            "shadow_show":    self.tc_shadow_toggle.isChecked(),
            "shadow_opacity": self.tc_shadow_opacity.value(),
        }

    def export_sheet(self):
        if not self.video_path or not self.current_frames:
            return
        video_dir  = self.default_output_dir if self.default_output_dir and os.path.isdir(self.default_output_dir) else os.path.dirname(self.video_path)
        base_name  = os.path.splitext(os.path.basename(self.video_path))[0]
        suffix     = self.safe_filename_part(self.current_preset_name) if self.current_preset_name else "Sheet"
        target     = os.path.join(video_dir, f"{base_name}_{suffix}.png")
        counter    = 1
        while os.path.exists(target):
            target = os.path.join(video_dir, f"{base_name}_{suffix}_v{counter}.png")
            counter += 1
        fn, _ = QFileDialog.getSaveFileName(self, "Save Sheet", target, "PNG (*.png)")
        if not fn:
            return
        meta = self.get_cached_meta(self.video_path)
        if not meta:
            QMessageBox.warning(self, "Error", "Could not read video metadata.")
            return
        timestamps  = [f.get("timestamp", 0.0) for f in self.current_frames]
        profile     = EXPORT_PROFILES.get(self.export_quality.currentText(), EXPORT_PROFILES[DEFAULT_EXPORT_PROFILE])
        export_width= max(960, min(int(meta.get("width", profile["frame_width"]) or profile["frame_width"]), profile["frame_width"]))
        self.loading_bar.show()
        self.loading_bar.setRange(0, len(timestamps))
        def export_progress(done, total):
            self.loading_bar.setRange(0, total)
            self.loading_bar.setValue(done)
            self.set_status(f"Export: extracting frames {done}/{total}…")
            QApplication.processEvents()
        full_frames = extract_final_frames_from_timestamps(
            self.video_path, timestamps, TMP_DIR,
            scale_width=export_width, meta=meta,
            progress=export_progress, lossless=profile["lossless"],
        )
        if not full_frames:
            QMessageBox.warning(self, "Error", "Could not extract any frames.")
            self.loading_bar.hide(); self.loading_bar.setRange(0, 0)
            return
        self.set_status(f"Export: rendering {self.export_quality.currentText()} PNG sheet…")
        QApplication.processEvents()
        generate_sheet(
            full_frames, meta, fn, self.bg_color(), self.margin.value(),
            self.cols.value(), self.rows.value(), self.spacing.value(),
            self.font_size.value(), (self.text_x.value(), self.text_y.value()),
            (self.grid_x.value(), self.grid_y.value()), self.visibility,
            self.font_family, self.get_tc_opts(), self.scale_mode.currentText(),
            output_size=profile["size"],
        )
        self.loading_bar.hide(); self.loading_bar.setRange(0, 0)
        self.set_status(f"Saved: {fn}")

    # ─── misc helpers ────────────────────────────────────────────────────────────

    def update_vis(self):
        for k, cb in self.checks.items():
            self.visibility[k] = cb.isChecked()
        self.schedule_preview_update()

    def set_status(self, text):
        self.status_label.setText(text)

    def set_auto_refine(self):
        self.auto_refine = self.auto_refine_toggle.isChecked()

    def pick_font(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.font_family = font.family()
            self.update_preview()

    def safe_filename_part(self, text):
        text = (text or "").strip()
        text = re.sub(r"[^A-Za-z0-9]+", "_", text)
        return text.strip("_") or "Sheet"

    # ─── resets ──────────────────────────────────────────────────────────────────

    def reset_grid_defaults(self):
        self.cols.setValue(DEFAULTS["cols"]); self.rows.setValue(DEFAULTS["rows"])
        self.spacing.setValue(DEFAULTS["spacing"]); self.margin.setValue(DEFAULTS["margin"])
        self.grid_x.setValue(DEFAULTS["grid_x"]); self.grid_y.setValue(DEFAULTS["grid_y"])
        self.scale_mode.setCurrentText(DEFAULTS["mode"])
        self.reselect_from_pool_or_reload()

    def reset_text_defaults(self):
        self.font_size.setValue(DEFAULTS["f_size"])
        self.text_x.setValue(DEFAULTS["t_x"]); self.text_y.setValue(DEFAULTS["t_y"])
        self.bg_mode.setCurrentText(DEFAULTS["bg_mode"])
        self.tc_toggle.setChecked(DEFAULTS["tc_show"]); self.tc_size.setValue(DEFAULTS["tc_size"])
        self.tc_opacity.setValue(DEFAULTS["tc_opacity"]); self.tc_shadow_toggle.setChecked(DEFAULTS["tc_shadow"])
        self.tc_shadow_opacity.setValue(DEFAULTS["tc_shadow_opacity"])
        self.visibility = DEFAULTS["vis"].copy()
        for k, cb in self.checks.items():
            cb.setChecked(self.visibility.get(k, True))
        self.schedule_preview_update()

    def reset_range_defaults(self):
        self.start_p.setValue(0); self.end_p.setValue(100)
        self.load_video_range()

    def reset_all_defaults(self):
        self.reset_grid_defaults(); self.reset_text_defaults(); self.reset_range_defaults()

    # ─── batch ───────────────────────────────────────────────────────────────────

    def run_batch_processing(self):
        out = QFileDialog.getExistingDirectory(self, "Select Folder")
        if not out:
            return
        for i in range(self.batch_list.count()):
            p = self.batch_list.item(i).text()
            m = self.get_cached_meta(p)
            if not m:
                continue
            pool = build_preview_pool_ultrafast(p, TMP_DIR, self.start_p.value(), self.end_p.value(),
                                                meta=m, target_count=self.cols.value() * self.rows.value())
            frames = select_frames_from_pool_fast(pool, self.cols.value() * self.rows.value())
            if not frames:
                continue
            timestamps   = [f.get("timestamp", 0.0) for f in frames]
            profile      = EXPORT_PROFILES.get(self.export_quality.currentText(), EXPORT_PROFILES[DEFAULT_EXPORT_PROFILE])
            export_width = max(960, min(int(m.get("width", profile["frame_width"]) or profile["frame_width"]), profile["frame_width"]))
            final_frames = extract_final_frames_from_timestamps(p, timestamps, TMP_DIR, scale_width=export_width, meta=m, lossless=profile["lossless"])
            if not final_frames:
                continue
            out_name = os.path.join(out, f"{os.path.basename(p)}_Sheet.png")
            generate_sheet(final_frames, m, out_name, self.bg_color(), self.margin.value(),
                           self.cols.value(), self.rows.value(), self.spacing.value(),
                           self.font_size.value(), (self.text_x.value(), self.text_y.value()),
                           (self.grid_x.value(), self.grid_y.value()), self.visibility,
                           self.font_family, self.get_tc_opts(), self.scale_mode.currentText(),
                           output_size=profile["size"])
        QMessageBox.information(self, "Done", "Batch Complete!")

    # ─── drag & drop ─────────────────────────────────────────────────────────────

    def dragEnterEvent(self, e):
        e.accept() if e.mimeData().hasUrls() else e.ignore()

    def dropEvent(self, e):
        urls = e.mimeData().urls()
        if self.tabs.currentIndex() == self.tabs.count() - 1:
            for u in urls:
                self.batch_list.addItem(u.toLocalFile())
        else:
            self.video_path = urls[0].toLocalFile()
            self.reset_current_video_state()
            self.get_cached_meta(self.video_path)
            self.load_video_range()

    # ─── cleanup ──────────────────────────────────────────────────────────────────

    def closeEvent(self, e):
        """Wipe the preview cache on exit so we don't leave GB of JPEGs behind."""
        import shutil
        cache_dir = os.path.join(TMP_DIR, "preview_cache")
        try:
            if os.path.isdir(cache_dir):
                shutil.rmtree(cache_dir, ignore_errors=True)
        except Exception:
            pass
        super().closeEvent(e)

    def _prune_cache_if_large(self, max_mb=50):
        """Keep preview cache under max_mb during a session — drop oldest subdirs first."""
        import shutil
        cache_dir = os.path.join(TMP_DIR, "preview_cache")
        if not os.path.isdir(cache_dir):
            return
        try:
            subdirs = [
                (os.path.getmtime(os.path.join(cache_dir, d)), os.path.join(cache_dir, d))
                for d in os.listdir(cache_dir)
                if os.path.isdir(os.path.join(cache_dir, d))
            ]
            subdirs.sort()  # oldest first
            total = sum(
                sum(os.path.getsize(os.path.join(r, f)) for f in files)
                for sd in [d for _, d in subdirs]
                for r, _, files in os.walk(sd)
            )
            for mtime, sd in subdirs:
                if total <= max_mb * 1024 * 1024:
                    break
                size = sum(
                    os.path.getsize(os.path.join(r, f))
                    for r, _, files in os.walk(sd) for f in files
                )
                shutil.rmtree(sd, ignore_errors=True)
                total -= size
        except Exception:
            pass

# ─── entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)
    app.setOrganizationName("Perfect Grid")
    win = PerfectGrid()
    win.show()
    sys.exit(app.exec_())
