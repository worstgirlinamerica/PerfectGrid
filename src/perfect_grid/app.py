import sys, os, json, re, tempfile
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QObject, QTimer
from PyQt5.QtGui import QImage, QPixmap
try:
    from .engine import (
        get_video_metadata,
        generate_sheet,
        build_preview_pool_ultrafast,
        build_preview_pool_refined,
        select_frames_from_pool_fast,
        select_frames_from_pool_refined,
        extract_final_frames_from_timestamps,
    )
except ImportError:
    from engine import (
        get_video_metadata,
        generate_sheet,
        build_preview_pool_ultrafast,
        build_preview_pool_refined,
        select_frames_from_pool_fast,
        select_frames_from_pool_refined,
        extract_final_frames_from_timestamps,
    )

APP_NAME = "Perfect Grid"
APP_VERSION = "1.0.0"


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


TMP_DIR = os.path.join(tempfile.gettempdir(), "PerfectGrid_Temp")
PRESET_RESOURCE_FILE = resource_path("presets_v2.json")
USER_PRESET_FILE = app_data_path("presets_v2.json")
SETTINGS_FILE = app_data_path("settings.json")
EXPORT_PROFILES = {
    "Fast 1080p": {"size": (1920, 1080), "frame_width": 1280, "lossless": False},
    "Detail 1440p": {"size": (2560, 1440), "frame_width": 1600, "lossless": False},
    "Maximum 4K": {"size": (3840, 2160), "frame_width": 2160, "lossless": True},
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
    "6x4 Detail Sheet": {"cols": 6, "rows": 4, "spacing": 0, "margin": 30, "f_size": 28, "t_x": 30, "t_y": 30, "mode": "Fill", "vis": DEFAULTS["vis"], "bg_mode": "Black"},
    "8x5 Contact Sheet": {"cols": 8, "rows": 5, "spacing": 0, "margin": 30, "f_size": 28, "t_x": 30, "t_y": 30, "mode": "Fill", "vis": DEFAULTS["vis"], "bg_mode": "Black"},
}


class PreviewPoolWorker(QObject):
    finished = pyqtSignal(object, str)
    error = pyqtSignal(str)
    status = pyqtSignal(str)

    def __init__(self, path, tmp_dir, start, end, meta=None, mode="ultrafast", target_count=12):
        super().__init__()
        self.path = path
        self.tmp_dir = tmp_dir
        self.start = start
        self.end = end
        self.meta = meta
        self.mode = mode
        self.target_count = target_count

    def run(self):
        try:
            if self.mode == "refined":
                pool = build_preview_pool_refined(self.path, self.tmp_dir, self.start, self.end, meta=self.meta, target_count=self.target_count, progress=self.status.emit)
            else:
                pool = build_preview_pool_ultrafast(self.path, self.tmp_dir, self.start, self.end, meta=self.meta, target_count=self.target_count, progress=self.status.emit)
            self.finished.emit(pool, self.mode)
        except Exception as e:
            self.error.emit(str(e))


class PerfectGrid(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Perfect Grid")
        self.resize(1400, 950)

        self.video_path = None
        self.current_frames = []
        self.font_family = "Arial"
        self.visibility = {k: True for k in ["name", "size", "res", "dur", "video", "audio"]}
        self.all_presets = {}
        self.extract_thread = None
        self.extract_worker = None
        self._pending_extract = False
        self._cursor_busy = False
        self.video_meta_cache = {}
        self.theme = "Dark"
        self.preview_pool = None
        self.preview_pool_key = None
        self.pool_mode = "ultrafast"
        self.auto_refine = False
        self.current_preset_name = None
        self.preview_update_timer = QTimer(self)
        self.preview_update_timer.setSingleShot(True)
        self.preview_update_timer.setInterval(80)
        self.preview_update_timer.timeout.connect(self.update_preview)

        menubar = self.menuBar()
        file_menu = menubar.addMenu("&File")
        open_action = QAction("Open...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file_dialog)
        file_menu.addAction(open_action)

        settings_menu = menubar.addMenu("&Settings")
        settings_action = QAction("Preferences...", self)
        settings_action.setShortcut("Ctrl+,")
        settings_action.triggered.connect(self.open_settings_dialog)
        settings_menu.addAction(settings_action)

        central = QWidget()
        self.setCentralWidget(central)
        self.main_layout = QHBoxLayout(central)

        self.left_panel = QWidget()
        self.left_panel.setMinimumWidth(360)
        self.left_panel.setMaximumWidth(450)
        self.left_layout = QVBoxLayout(self.left_panel)
        self.left_layout.setContentsMargins(0, 0, 0, 0)

        self.sidebar_content = QWidget()
        self.sidebar = QVBoxLayout(self.sidebar_content)
        self.sidebar.setContentsMargins(0, 0, 0, 0)
        self.tabs = QTabWidget()
        self.sidebar.addWidget(self.tabs)

        self.init_grid_tab()
        self.init_text_tab()
        self.init_range_tab()
        self.init_preset_tab()
        self.init_batch_tab()

        self.controls_scroll = QScrollArea()
        self.controls_scroll.setWidgetResizable(True)
        self.controls_scroll.setFrameShape(QFrame.NoFrame)
        self.controls_scroll.setWidget(self.sidebar_content)
        self.left_layout.addWidget(self.controls_scroll, 1)

        self.bottom_controls = QWidget()
        self.bottom_layout = QVBoxLayout(self.bottom_controls)
        self.bottom_layout.setContentsMargins(0, 8, 0, 0)

        self.btn_refresh = QPushButton("Refresh Preview")
        self.btn_refresh.setObjectName("SecondaryButton")
        self.btn_refresh.setMinimumHeight(40)
        self.btn_refresh.clicked.connect(self.load_video_range)
        self.bottom_layout.addWidget(self.btn_refresh)

        self.btn_export = QPushButton("Export PNG")
        self.btn_export.setObjectName("PrimaryButton")
        self.btn_export.setMinimumHeight(46)
        self.btn_export.clicked.connect(self.export_sheet)
        self.bottom_layout.addWidget(self.btn_export)

        self.loading_bar = QProgressBar()
        self.loading_bar.setRange(0, 0)
        self.loading_bar.setTextVisible(False)
        self.loading_bar.setFixedHeight(3)
        self.loading_bar.hide()
        self.bottom_layout.addWidget(self.loading_bar)

        self.status_label = QLabel("Ready")
        self.status_label.setWordWrap(True)
        self.status_label.setMinimumHeight(36)
        self.bottom_layout.addWidget(self.status_label)
        self.left_layout.addWidget(self.bottom_controls, 0)

        self.main_layout.addWidget(self.left_panel, 1)

        self.preview_label = QLabel("Drag & Drop Video Here")
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setObjectName("PreviewPane")
        self.main_layout.addWidget(self.preview_label, 3)

        self.setAcceptDrops(True)
        self.load_presets_from_file()
        self.load_settings()
        self.apply_theme()

    def create_slider(self, layout, name, mini, maxi, default, is_grid_size=False):
        container = QWidget()
        v_lay = QVBoxLayout(container)
        v_lay.setContentsMargins(0, 2, 0, 2)
        lbl = QLabel(name)
        lbl.setObjectName("FieldLabel")
        h_lay = QHBoxLayout()
        slider = QSlider(Qt.Horizontal)
        slider.setRange(mini, maxi)
        slider.setValue(default)
        spin = QSpinBox()
        spin.setRange(mini, maxi)
        spin.setValue(default)
        spin.setFixedWidth(76)
        slider.valueChanged.connect(spin.setValue)
        spin.valueChanged.connect(slider.setValue)
        if is_grid_size:
            slider.valueChanged.connect(self.reselect_from_pool_or_reload)
        else:
            slider.valueChanged.connect(self.schedule_preview_update)
        h_lay.addWidget(slider)
        h_lay.addWidget(spin)
        v_lay.addWidget(lbl)
        v_lay.addLayout(h_lay)
        layout.addWidget(container)
        return slider

    def init_grid_tab(self):
        tab = QWidget()
        v = QVBoxLayout(tab)
        v.addWidget(QLabel("<b>Image Scaling Mode:</b>"))
        self.scale_mode = QComboBox()
        self.scale_mode.addItems(["Fill", "Fit", "Stretch"])
        self.scale_mode.currentIndexChanged.connect(self.update_preview)
        v.addWidget(self.scale_mode)
        self.cols = self.create_slider(v, "Columns", 1, 15, 4, is_grid_size=True)
        self.rows = self.create_slider(v, "Rows", 1, 15, 3, is_grid_size=True)
        self.spacing = self.create_slider(v, "Gap Spacing", 0, 100, 0)
        self.margin = self.create_slider(v, "Page Margins", 0, 400, 30)
        self.grid_x = self.create_slider(v, "Grid X Offset", -800, 800, 0)
        self.grid_y = self.create_slider(v, "Grid Y Offset", -800, 800, 0)
        reset = QPushButton("Reset Grid")
        reset.clicked.connect(self.reset_grid_defaults)
        v.addWidget(reset)
        v.addStretch()
        self.tabs.addTab(tab, "Grid")

    def init_text_tab(self):
        tab = QWidget()
        v = QVBoxLayout(tab)
        v.addWidget(QLabel("<b>Metadata Visibility:</b>"))
        grid_v = QGridLayout()
        self.checks = {}
        fields = [("name","File Name"),("size","File Size"),("res","Resolution"),("dur","Duration"),("video","Video"),("audio","Audio")]
        for i, (k, label) in enumerate(fields):
            cb = QCheckBox(label)
            cb.setChecked(True)
            cb.stateChanged.connect(self.update_vis)
            self.checks[k] = cb
            grid_v.addWidget(cb, i // 2, i % 2)
        v.addLayout(grid_v)

        btn_font = QPushButton("Change Font Family")
        btn_font.clicked.connect(self.pick_font)
        v.addWidget(btn_font)

        self.font_size = self.create_slider(v, "Header Font Size", 10, 80, 28)
        self.text_x = self.create_slider(v, "Header X Pos", 0, 1000, 30)
        self.text_y = self.create_slider(v, "Header Y Pos", 0, 500, 30)

        v.addSpacing(10)
        v.addWidget(QLabel("<b>Timecode:</b>"))
        self.tc_toggle = QCheckBox("Enable TC")
        self.tc_toggle.setChecked(True)
        self.tc_toggle.stateChanged.connect(self.update_preview)
        v.addWidget(self.tc_toggle)
        self.tc_size = self.create_slider(v, "TC Size", 10, 80, 24)
        self.tc_opacity = self.create_slider(v, "TC Text Opacity", 0, 255, 255)
        self.tc_shadow_toggle = QCheckBox("Enable Shadow")
        self.tc_shadow_toggle.setChecked(True)
        self.tc_shadow_toggle.stateChanged.connect(self.update_preview)
        v.addWidget(self.tc_shadow_toggle)
        self.tc_shadow_opacity = self.create_slider(v, "Shadow Opacity", 0, 255, 180)

        v.addSpacing(10)
        v.addWidget(QLabel("<b>Sheet Background:</b>"))
        self.bg_mode = QComboBox()
        self.bg_mode.addItems(["White", "Black"])
        self.bg_mode.currentIndexChanged.connect(self.schedule_preview_update)
        v.addWidget(self.bg_mode)
        reset = QPushButton("Reset Text")
        reset.clicked.connect(self.reset_text_defaults)
        v.addWidget(reset)
        v.addStretch()
        self.tabs.addTab(tab, "Text")

    def init_range_tab(self):
        tab = QWidget()
        v = QVBoxLayout(tab)
        self.start_p = self.create_slider(v, "Start Time %", 0, 99, 0)
        self.end_p = self.create_slider(v, "End Time %", 1, 100, 100)
        self.start_p.valueChanged.connect(self.load_video_range)
        self.end_p.valueChanged.connect(self.load_video_range)
        v.addWidget(QLabel("Export Quality"))
        self.export_quality = QComboBox()
        self.export_quality.addItems(EXPORT_PROFILES.keys())
        self.export_quality.setCurrentText(DEFAULT_EXPORT_PROFILE)
        v.addWidget(self.export_quality)
        btn = QPushButton("Refine Picks")
        btn.clicked.connect(self.run_refine_pass)
        v.addWidget(btn)
        self.auto_refine_toggle = QCheckBox("Auto refine after fast preview")
        self.auto_refine_toggle.setChecked(False)
        self.auto_refine_toggle.stateChanged.connect(self.set_auto_refine)
        v.addWidget(self.auto_refine_toggle)
        reset = QPushButton("Reset Range")
        reset.clicked.connect(self.reset_range_defaults)
        v.addWidget(reset)
        v.addStretch()
        self.tabs.addTab(tab, "Range")

    def init_preset_tab(self):
        tab = QWidget()
        v = QVBoxLayout(tab)
        self.preset_list = QListWidget()
        v.addWidget(self.preset_list)
        h = QHBoxLayout()
        for name, fn in [("Save", self.save_preset), ("Load", self.load_selected_preset), ("Delete", self.delete_preset)]:
            b = QPushButton(name)
            b.clicked.connect(fn)
            h.addWidget(b)
        v.addLayout(h)
        reset_all = QPushButton("Reset All Defaults")
        reset_all.clicked.connect(self.reset_all_defaults)
        v.addWidget(reset_all)
        v.addStretch()
        self.tabs.addTab(tab, "Presets")

    def init_batch_tab(self):
        tab = QWidget()
        v = QVBoxLayout(tab)
        self.batch_list = QListWidget()
        v.addWidget(self.batch_list)
        btn_c = QPushButton("Clear List")
        btn_c.clicked.connect(self.batch_list.clear)
        v.addWidget(btn_c)
        btn_r = QPushButton("Run Batch")
        btn_r.clicked.connect(self.run_batch_processing)
        v.addWidget(btn_r)
        v.addStretch()
        self.tabs.addTab(tab, "Batch")

    def bg_color(self):
        return (0, 0, 0) if self.bg_mode.currentText() == "Black" else (255, 255, 255)

    def update_vis(self):
        for k, cb in self.checks.items():
            self.visibility[k] = cb.isChecked()
        self.schedule_preview_update()

    def schedule_preview_update(self):
        self.preview_update_timer.start()

    def get_pool_key(self):
        return (self.video_path, self.start_p.value(), self.end_p.value())

    def reselect_from_pool_or_reload(self):
        if self.preview_pool and self.preview_pool_key == self.get_pool_key():
            self.reselect_from_pool()
        else:
            self.load_video_range()

    def reselect_from_pool(self):
        if not self.preview_pool or not self.preview_pool.get("frames"):
            self.current_frames = []
            self.preview_label.setText("No preview frames found")
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
            self.load_video_range()
            return
        self.set_status(("Refined" if self.pool_mode == "refined" else "Fast") + f" preview ready - {len(self.current_frames)} frames.")
        self.update_preview()

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
        self.preview_label.setPixmap(QPixmap.fromImage(qimg).scaled(self.preview_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def get_tc_opts(self):
        return {
            "show": self.tc_toggle.isChecked(),
            "size": self.tc_size.value(),
            "opacity": self.tc_opacity.value(),
            "shadow_show": self.tc_shadow_toggle.isChecked(),
            "shadow_opacity": self.tc_shadow_opacity.value(),
        }

    def get_cached_meta(self, path):
        if not path:
            return None
        if path in self.video_meta_cache:
            return self.video_meta_cache[path]
        meta = get_video_metadata(path)
        if meta:
            self.video_meta_cache[path] = meta
        return meta

    def set_status(self, text):
        self.status_label.setText(text)

    def set_auto_refine(self):
        self.auto_refine = self.auto_refine_toggle.isChecked()

    def reset_grid_defaults(self):
        self.cols.setValue(DEFAULTS["cols"])
        self.rows.setValue(DEFAULTS["rows"])
        self.spacing.setValue(DEFAULTS["spacing"])
        self.margin.setValue(DEFAULTS["margin"])
        self.grid_x.setValue(DEFAULTS["grid_x"])
        self.grid_y.setValue(DEFAULTS["grid_y"])
        self.scale_mode.setCurrentText(DEFAULTS["mode"])
        self.reselect_from_pool_or_reload()

    def reset_text_defaults(self):
        self.font_size.setValue(DEFAULTS["f_size"])
        self.text_x.setValue(DEFAULTS["t_x"])
        self.text_y.setValue(DEFAULTS["t_y"])
        self.bg_mode.setCurrentText(DEFAULTS["bg_mode"])
        self.tc_toggle.setChecked(DEFAULTS["tc_show"])
        self.tc_size.setValue(DEFAULTS["tc_size"])
        self.tc_opacity.setValue(DEFAULTS["tc_opacity"])
        self.tc_shadow_toggle.setChecked(DEFAULTS["tc_shadow"])
        self.tc_shadow_opacity.setValue(DEFAULTS["tc_shadow_opacity"])
        self.visibility = DEFAULTS["vis"].copy()
        for k, cb in self.checks.items():
            cb.setChecked(self.visibility.get(k, True))
        self.schedule_preview_update()

    def reset_range_defaults(self):
        self.start_p.setValue(0)
        self.end_p.setValue(100)
        self.load_video_range()

    def reset_all_defaults(self):
        self.reset_grid_defaults()
        self.reset_text_defaults()
        self.reset_range_defaults()

    def open_settings_dialog(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("Perfect Grid Settings")
        dlg.setModal(True)
        lay = QVBoxLayout(dlg)
        lay.addWidget(QLabel("<b>Appearance</b>"))
        theme_row = QHBoxLayout()
        theme_row.addWidget(QLabel("Skin / Theme:"))
        theme_box = QComboBox()
        theme_box.addItems(["Dark", "Light", "Slate"])
        idx = theme_box.findText(self.theme)
        if idx >= 0:
            theme_box.setCurrentIndex(idx)
        theme_row.addWidget(theme_box)
        lay.addLayout(theme_row)
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        btn_ok = QPushButton("OK")
        btn_cancel = QPushButton("Cancel")
        btn_row.addWidget(btn_cancel)
        btn_row.addWidget(btn_ok)
        lay.addLayout(btn_row)
        def accept():
            self.theme = theme_box.currentText()
            self.save_settings()
            self.apply_theme()
            dlg.accept()
        btn_ok.clicked.connect(accept)
        btn_cancel.clicked.connect(dlg.reject)
        dlg.exec_()

    def apply_theme(self):
        if self.theme == "Light":
            style = '''
                QMainWindow, QWidget {background-color:#f6f7f9;color:#1f2328;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Arial;font-size:13px;}
                QTabWidget::pane {border:1px solid #d8dee4;border-radius:8px;background:#ffffff;}
                QTabBar::tab {padding:8px 12px;border:1px solid transparent;border-bottom:none;color:#57606a;}
                QTabBar::tab:selected {background:#ffffff;border-color:#d8dee4;color:#1f2328;border-top-left-radius:8px;border-top-right-radius:8px;}
                QScrollArea {background:transparent;border:0;}
                QLabel#FieldLabel {font-weight:600;color:#57606a;}
                QPushButton {background-color:#ffffff;border:1px solid #c9d1d9;border-radius:7px;padding:8px 12px;color:#24292f;}
                QPushButton:hover {background-color:#eef1f4;}
                QPushButton#PrimaryButton {background:#24292f;color:#ffffff;border-color:#24292f;font-weight:600;}
                QComboBox, QSpinBox, QListWidget {background:#ffffff;border:1px solid #d0d7de;border-radius:6px;padding:5px;color:#1f2328;}
                QSlider::groove:horizontal {height:5px;background:#d8dee4;border-radius:2px;}
                QSlider::handle:horizontal {width:16px;margin:-6px 0;background:#24292f;border-radius:8px;}
                QProgressBar {border:0;background:transparent;} QProgressBar::chunk {background:#57606a;border-radius:1px;}
                QLabel#PreviewPane {background:#0d1117;border:1px solid #30363d;border-radius:8px;color:#8b949e;}
            '''
        elif self.theme == "Slate":
            style = '''
                QMainWindow, QWidget {background-color:#202329;color:#e7e9ed;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Arial;font-size:13px;}
                QTabWidget::pane {border:1px solid #3a3f48;border-radius:8px;background:#272b33;}
                QTabBar::tab {padding:8px 12px;border:1px solid transparent;border-bottom:none;color:#aeb6c2;}
                QTabBar::tab:selected {background:#272b33;border-color:#3a3f48;color:#ffffff;border-top-left-radius:8px;border-top-right-radius:8px;}
                QScrollArea {background:transparent;border:0;}
                QLabel#FieldLabel {font-weight:600;color:#b8c0cc;}
                QPushButton {background-color:#303640;border:1px solid #4a515d;border-radius:7px;padding:8px 12px;color:#f0f2f4;}
                QPushButton:hover {background-color:#3a414d;}
                QPushButton#PrimaryButton {background:#e7e9ed;color:#1f2328;border-color:#e7e9ed;font-weight:600;}
                QComboBox, QSpinBox, QListWidget {background:#181b20;border:1px solid #3a3f48;border-radius:6px;padding:5px;color:#e7e9ed;}
                QSlider::groove:horizontal {height:5px;background:#3a414d;border-radius:2px;}
                QSlider::handle:horizontal {width:16px;margin:-6px 0;background:#d8dee4;border-radius:8px;}
                QProgressBar {border:0;background:transparent;} QProgressBar::chunk {background:#b8c0cc;border-radius:1px;}
                QLabel#PreviewPane {background:#111318;border:1px solid #3a3f48;border-radius:8px;color:#9aa4b2;}
            '''
        else:
            style = '''
                QMainWindow, QWidget {background-color:#151719;color:#eceff3;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Arial;font-size:13px;}
                QTabWidget::pane {border:1px solid #30343a;border-radius:8px;background:#1b1e22;}
                QTabBar::tab {padding:8px 12px;border:1px solid transparent;border-bottom:none;color:#b9c0c8;}
                QTabBar::tab:selected {background:#1b1e22;border-color:#30343a;color:#ffffff;border-top-left-radius:8px;border-top-right-radius:8px;}
                QScrollArea {background:transparent;border:0;}
                QLabel#FieldLabel {font-weight:600;color:#b9c0c8;}
                QPushButton {background-color:#24282d;border:1px solid #3a4048;border-radius:7px;padding:8px 12px;color:#f2f4f7;}
                QPushButton:hover {background-color:#2e343b;}
                QPushButton#PrimaryButton {background:#f2f4f7;color:#151719;border-color:#f2f4f7;font-weight:600;}
                QComboBox, QSpinBox, QListWidget {background:#101214;border:1px solid #30343a;border-radius:6px;padding:5px;color:#eceff3;}
                QSlider::groove:horizontal {height:5px;background:#30343a;border-radius:2px;}
                QSlider::handle:horizontal {width:16px;margin:-6px 0;background:#c9d1d9;border-radius:8px;}
                QProgressBar {border:0;background:transparent;} QProgressBar::chunk {background:#c9d1d9;border-radius:1px;}
                QLabel#PreviewPane {background:#080a0c;border:1px solid #30343a;border-radius:8px;color:#8b949e;}
            '''
        QApplication.instance().setStyleSheet(style)

    def load_settings(self):
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.theme = data.get("theme", self.theme)
            except Exception:
                pass

    def save_settings(self):
        try:
            ensure_parent_dir(SETTINGS_FILE)
            with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
                json.dump({"theme": self.theme}, f)
        except Exception:
            pass

    def reset_current_video_state(self):
        self.current_frames = []
        self.preview_pool = None
        self.preview_pool_key = None
        self.pool_mode = "ultrafast"
        self.preview_label.setText("Loading...")
        self.preview_label.setPixmap(QPixmap())
        if hasattr(self, "loading_bar"):
            self.loading_bar.show()

    def _start_worker(self, mode):
        meta = self.get_cached_meta(self.video_path)
        target_count = self.cols.value() * self.rows.value()
        self.extract_thread = QThread()
        self.extract_worker = PreviewPoolWorker(self.video_path, TMP_DIR, self.start_p.value(), self.end_p.value(), meta=meta, mode=mode, target_count=target_count)
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

    def load_video_range(self):
        if not self.video_path:
            return
        if self.extract_thread is not None and self.extract_thread.isRunning():
            self._pending_extract = True
            return
        self._pending_extract = False
        self.current_frames = []
        self.preview_pool = None
        self.preview_pool_key = None
        self.pool_mode = "ultrafast"
        self.set_status("Fast preview: seeking thumbnails...")
        self.preview_label.setText("Loading fast preview...")
        self.preview_label.setPixmap(QPixmap())
        self.loading_bar.show()
        self.loading_bar.setRange(0, 0)
        self._start_worker("ultrafast")

    def on_preview_pool_ready(self, pool, mode):
        self.preview_pool = pool
        self.preview_pool_key = self.get_pool_key()
        self.pool_mode = "ultrafast"
        if self.extract_thread is not None:
            self.extract_thread.quit()
            self.extract_thread.wait()
            self.extract_thread = None
        self.extract_worker = None
        self.reselect_from_pool()
        if self._pending_extract:
            self.load_video_range()
            return
        if self._cursor_busy:
            QApplication.restoreOverrideCursor()
            self._cursor_busy = False
        self.loading_bar.hide()
        self.loading_bar.setRange(0, 0)

        if self.auto_refine:
            QTimer.singleShot(150, self.run_refine_pass)

    def run_refine_pass(self):
        if not self.video_path:
            return
        if self.extract_thread is not None and self.extract_thread.isRunning():
            return
        self.set_status("Refine: starting smarter pick pass...")
        self.loading_bar.show()
        self.loading_bar.setRange(0, 0)
        self._start_worker("refined")

    def on_refine_ready(self, pool, mode):
        self.preview_pool = pool
        self.preview_pool_key = self.get_pool_key()
        self.pool_mode = "refined"
        if self.extract_thread is not None:
            self.extract_thread.quit()
            self.extract_thread.wait()
            self.extract_thread = None
        self.extract_worker = None
        self.reselect_from_pool()
        if self._cursor_busy:
            QApplication.restoreOverrideCursor()
            self._cursor_busy = False
        self.loading_bar.hide()
        self.loading_bar.setRange(0, 0)

    def on_extract_error(self, msg):
        print(f"Frame extraction error: {msg}")
        self.set_status(f"Extraction error: {msg}")
        if self.extract_thread is not None:
            self.extract_thread.quit()
            self.extract_thread.wait()
            self.extract_thread = None
        self.extract_worker = None
        if self._pending_extract:
            self.load_video_range()
        elif self._cursor_busy:
            QApplication.restoreOverrideCursor()
            self._cursor_busy = False
        self.loading_bar.hide()
        self.loading_bar.setRange(0, 0)

    def open_file_dialog(self):
        fn, _ = QFileDialog.getOpenFileName(self, "Open Video", "", "Video Files (*.mp4 *.mov *.mkv *.avi *.webm);;All Files (*)")
        if fn:
            self.video_path = fn
            self.reset_current_video_state()
            self.get_cached_meta(self.video_path)
            self.load_video_range()

    def export_sheet(self):
        if not self.video_path or not self.current_frames:
            return
        video_dir = os.path.dirname(self.video_path)
        base_name = os.path.splitext(os.path.basename(self.video_path))[0]
        suffix = self.safe_filename_part(self.current_preset_name) if self.current_preset_name else "Sheet"
        target_path = os.path.join(video_dir, f"{base_name}_{suffix}.png")
        counter = 1
        while os.path.exists(target_path):
            target_path = os.path.join(video_dir, f"{base_name}_{suffix}_v{counter}.png")
            counter += 1
        fn, _ = QFileDialog.getSaveFileName(self, "Save Sheet", target_path, "PNG (*.png)")
        if not fn:
            return
        meta = self.get_cached_meta(self.video_path)
        if not meta:
            QMessageBox.warning(self, "Error", "Could not read video metadata.")
            return
        timestamps = [f.get("timestamp", 0.0) for f in self.current_frames]
        profile = EXPORT_PROFILES.get(self.export_quality.currentText(), EXPORT_PROFILES[DEFAULT_EXPORT_PROFILE])
        export_width = max(960, min(int(meta.get("width", profile["frame_width"]) or profile["frame_width"]), profile["frame_width"]))
        self.loading_bar.show()
        self.loading_bar.setRange(0, len(timestamps))
        def export_progress(done, total):
            self.loading_bar.setRange(0, total)
            self.loading_bar.setValue(done)
            self.set_status(f"Export: extracting frames {done}/{total}...")
            QApplication.processEvents()
        full_frames = extract_final_frames_from_timestamps(self.video_path, timestamps, TMP_DIR, scale_width=export_width, meta=meta, progress=export_progress, lossless=profile["lossless"])
        if not full_frames:
            QMessageBox.warning(self, "Error", "Could not extract any frames.")
            self.loading_bar.hide()
            self.loading_bar.setRange(0, 0)
            return
        self.set_status(f"Export: rendering {self.export_quality.currentText()} PNG sheet...")
        QApplication.processEvents()
        generate_sheet(full_frames, meta, fn, self.bg_color(), self.margin.value(), self.cols.value(), self.rows.value(), self.spacing.value(), self.font_size.value(), (self.text_x.value(), self.text_y.value()), (self.grid_x.value(), self.grid_y.value()), self.visibility, self.font_family, self.get_tc_opts(), self.scale_mode.currentText(), output_size=profile["size"])
        self.loading_bar.hide()
        self.loading_bar.setRange(0, 0)
        self.set_status(f"Saved: {fn}")

    def save_preset(self):
        name, ok = QInputDialog.getText(self, "Save Look", "Name:")
        if ok and name:
            self.all_presets[name] = {"cols": self.cols.value(), "rows": self.rows.value(), "spacing": self.spacing.value(), "margin": self.margin.value(), "f_size": self.font_size.value(), "t_x": self.text_x.value(), "t_y": self.text_y.value(), "mode": self.scale_mode.currentText(), "vis": self.visibility.copy(), "bg_mode": self.bg_mode.currentText()}
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
            self.cols.setValue(p["cols"]); self.rows.setValue(p["rows"]); self.spacing.setValue(p["spacing"]); self.margin.setValue(p["margin"]); self.font_size.setValue(p["f_size"]); self.text_x.setValue(p.get("t_x", 30)); self.text_y.setValue(p.get("t_y", 30)); self.scale_mode.setCurrentText(p.get("mode", "Fill")); self.bg_mode.setCurrentText(p.get("bg_mode", "White"))
            self.visibility = p.get("vis", {k: True for k in self.checks.keys()})
            for k, cb in self.checks.items():
                cb.setChecked(self.visibility.get(k, True))
            self.reselect_from_pool_or_reload()

    def safe_filename_part(self, text):
        text = (text or "").strip()
        text = re.sub(r"[^A-Za-z0-9]+", "_", text)
        return text.strip("_") or "Sheet"

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

    def pick_font(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.font_family = font.family()
            self.update_preview()

    def run_batch_processing(self):
        out = QFileDialog.getExistingDirectory(self, "Select Folder")
        if not out:
            return
        for i in range(self.batch_list.count()):
            p = self.batch_list.item(i).text()
            m = self.get_cached_meta(p)
            if not m:
                continue
            pool = build_preview_pool_ultrafast(p, TMP_DIR, self.start_p.value(), self.end_p.value(), meta=m, target_count=self.cols.value() * self.rows.value())
            frames = select_frames_from_pool_fast(pool, self.cols.value() * self.rows.value())
            if not frames:
                continue
            timestamps = [f.get("timestamp", 0.0) for f in frames]
            profile = EXPORT_PROFILES.get(self.export_quality.currentText(), EXPORT_PROFILES[DEFAULT_EXPORT_PROFILE])
            export_width = max(960, min(int(m.get("width", profile["frame_width"]) or profile["frame_width"]), profile["frame_width"]))
            final_frames = extract_final_frames_from_timestamps(p, timestamps, TMP_DIR, scale_width=export_width, meta=m, lossless=profile["lossless"])
            if not final_frames:
                continue
            out_name = os.path.join(out, f"{os.path.basename(p)}_Sheet.png")
            generate_sheet(final_frames, m, out_name, self.bg_color(), self.margin.value(), self.cols.value(), self.rows.value(), self.spacing.value(), self.font_size.value(), (self.text_x.value(), self.text_y.value()), (self.grid_x.value(), self.grid_y.value()), self.visibility, self.font_family, self.get_tc_opts(), self.scale_mode.currentText(), output_size=profile["size"])
        QMessageBox.information(self, "Done", "Batch Complete!")

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)
    app.setOrganizationName("Perfect Grid")
    win = PerfectGrid()
    win.show()
    sys.exit(app.exec_())
