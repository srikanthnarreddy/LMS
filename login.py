import sys

from PyQt6.QtCore import Qt, QPointF, pyqtSignal
from PyQt6.QtGui import (
    QColor, QIcon, QLinearGradient, QPainter, QPainterPath, QPen, QPixmap,
)
from PyQt6.QtWidgets import (
    QApplication, QHBoxLayout, QLabel, QLineEdit, QMessageBox, QPushButton,
    QVBoxLayout, QWidget,
)

APP_NAME = "Leads Management Syatem"

# Palette
INK = "#14213A"        # brand panel
INK_DEEP = "#0E1830"
PAPER = "#F7F8FA"      # form side background
TEXT = "#1B2433"
MUTED = "#5B6678"
BORDER = "#BAC3D0"
ACCENT = "#2754D6"     # cobalt
ACCENT_HOVER = "#1F44B3"
ACCENT_PRESSED = "#183894"
ERROR = "#B42318"

STYLESHEET = f"""
* {{
    font-family: "Segoe UI", "Inter", "SF Pro Text", "Helvetica Neue", Arial, sans-serif;
}}
QWidget#root {{ background: {PAPER}; }}
QWidget#form {{ background: transparent; }}

QLabel {{ background: transparent; color: {TEXT}; }}
QLabel#title {{ font-size: 28px; font-weight: 600; }}
QLabel#subtitle {{ font-size: 14px; color: {MUTED}; }}
QLabel#fieldLabel {{ font-size: 13px; font-weight: 600; }}
QLabel#error {{ font-size: 13px; color: {ERROR}; }}
QLabel#footnote {{ font-size: 12px; color: {MUTED}; }}

QLabel#brandName {{ font-size: 20px; font-weight: 600; color: #FFFFFF; }}
QLabel#brandHeadline {{ font-size: 28px; font-weight: 600; color: #FFFFFF; }}
QLabel#brandSub {{ font-size: 14px; color: #A9B7D0; }}

QLineEdit {{
    background: #FFFFFF;
    border: 1px solid {BORDER};
    border-radius: 8px;
    padding: 0 12px;
    font-size: 14px;
    color: {TEXT};
    selection-background-color: #C9D8FB;
    selection-color: {TEXT};
}}
QLineEdit:hover {{ border-color: #8C99AD; }}
QLineEdit:focus {{ border: 2px solid {ACCENT}; padding: 0 11px; }}
QLineEdit[invalid="true"] {{ border: 1px solid {ERROR}; }}
QLineEdit[invalid="true"]:focus {{ border: 2px solid {ERROR}; padding: 0 11px; }}

QPushButton#primary {{
    background: {ACCENT};
    color: #FFFFFF;
    border: 2px solid {ACCENT};
    border-radius: 8px;
    font-size: 14px;
    font-weight: 600;
}}
QPushButton#primary:hover {{ background: {ACCENT_HOVER}; border-color: {ACCENT_HOVER}; }}
QPushButton#primary:pressed {{ background: {ACCENT_PRESSED}; border-color: {ACCENT_PRESSED}; }}
QPushButton#primary:focus {{ border-color: {INK}; }}

QPushButton#link {{
    background: transparent;
    border: 1px solid transparent;
    border-radius: 4px;
    color: {ACCENT};
    font-size: 13px;
    font-weight: 600;
    padding: 2px 4px;
}}
QPushButton#link:hover {{ color: {ACCENT_PRESSED}; }}
QPushButton#link:focus {{ border-color: {ACCENT}; }}
"""


def eye_icon(color: str, slashed: bool = False) -> QIcon:
    """Draws a simple eye (or crossed-out eye) so no image assets are needed."""
    s = 48
    pm = QPixmap(s, s)
    pm.fill(Qt.GlobalColor.transparent)
    p = QPainter(pm)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    pen = QPen(QColor(color), 3.2)
    pen.setCapStyle(Qt.PenCapStyle.RoundCap)
    p.setPen(pen)
    outline = QPainterPath()
    outline.moveTo(s * 0.08, s * 0.5)
    outline.quadTo(s * 0.5, s * 0.08, s * 0.92, s * 0.5)
    outline.quadTo(s * 0.5, s * 0.92, s * 0.08, s * 0.5)
    p.drawPath(outline)
    p.drawEllipse(QPointF(s * 0.5, s * 0.5), s * 0.12, s * 0.12)
    if slashed:
        p.drawLine(QPointF(s * 0.18, s * 0.84), QPointF(s * 0.82, s * 0.16))
    p.end()
    return QIcon(pm)


class BrandPanel(QWidget):
    """Left panel: deep navy with concentric arcs drawn from the lower-right corner."""

    def __init__(self):
        super().__init__()
        self.setMinimumWidth(340)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(48, 44, 48, 52)

        name = QLabel(APP_NAME)
        name.setObjectName("brandName")

        headline = QLabel("One place for orders, stock and reports.")
        headline.setObjectName("brandHeadline")
        headline.setWordWrap(True)

        sub = QLabel("Log in to pick up where your team left off.")
        sub.setObjectName("brandSub")
        sub.setWordWrap(True)

        layout.addWidget(name)
        layout.addStretch()
        layout.addWidget(headline)
        layout.addSpacing(10)
        layout.addWidget(sub)

    def paintEvent(self, _event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        grad = QLinearGradient(0, 0, self.width(), self.height())
        grad.setColorAt(0.0, QColor(INK))
        grad.setColorAt(1.0, QColor(INK_DEEP))
        p.fillRect(self.rect(), grad)

        # Concentric arcs, fading outward; one arc in the accent color.
        cx, cy = self.width() * 0.92, self.height() * 0.98
        p.setBrush(Qt.BrushStyle.NoBrush)
        for i in range(1, 9):
            radius = 62 * i
            if i == 4:
                pen = QPen(QColor(ACCENT), 2.0)
            else:
                alpha = max(14, 70 - i * 8)
                pen = QPen(QColor(140, 170, 235, alpha), 1.2)
            p.setPen(pen)
            p.drawEllipse(QPointF(cx, cy), radius, radius)


class LoginWindow(QWidget):
    login_succeeded = pyqtSignal(str)
    forgot_password_requested = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setObjectName("root")
        self.setWindowTitle(f"{APP_NAME} - Log in")
        self.setMinimumSize(480, 580)
        self.resize(960, 620)
        self.setStyleSheet(STYLESHEET)

        outer = QHBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        self.brand = BrandPanel()
        outer.addWidget(self.brand, 5)

        right = QWidget()
        right_layout = QVBoxLayout(right)
        right_layout.setContentsMargins(40, 40, 40, 40)
        right_layout.addStretch()
        right_layout.addWidget(self._build_form(), alignment=Qt.AlignmentFlag.AlignHCenter)
        right_layout.addStretch()
        outer.addWidget(right, 6)

        self.setTabOrder(self.username, self.password)
        self.setTabOrder(self.password, self.login_button)
        self.setTabOrder(self.login_button, self.forgot_button)
        self.username.setFocus()

    # ---- UI construction -------------------------------------------------
    def _build_form(self) -> QWidget:
        form = QWidget()
        form.setObjectName("form")
        form.setFixedWidth(360)
        layout = QVBoxLayout(form)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        title = QLabel("Log in")
        title.setObjectName("title")
        subtitle = QLabel("Use your work account to continue.")
        subtitle.setObjectName("subtitle")
        layout.addWidget(title)
        layout.addSpacing(6)
        layout.addWidget(subtitle)
        layout.addSpacing(32)

        # Username
        user_label = QLabel("Username")
        user_label.setObjectName("fieldLabel")
        self.username = QLineEdit()
        self.username.setPlaceholderText("e.g. jordan.lee")
        self.username.setFixedHeight(44)
        self.username.setClearButtonEnabled(False)
        self.username.textChanged.connect(self._clear_error)
        layout.addWidget(user_label)
        layout.addSpacing(6)
        layout.addWidget(self.username)
        layout.addSpacing(20)

        # Password label row with the forgot-password link on the right
        pass_row = QHBoxLayout()
        pass_row.setContentsMargins(0, 0, 0, 0)
        pass_label = QLabel("Password")
        pass_label.setObjectName("fieldLabel")
        self.forgot_button = QPushButton("Forgot password?")
        self.forgot_button.setObjectName("link")
        self.forgot_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.forgot_button.setFlat(True)
        self.forgot_button.clicked.connect(self._on_forgot_password)
        pass_row.addWidget(pass_label)
        pass_row.addStretch()
        pass_row.addWidget(self.forgot_button)
        layout.addLayout(pass_row)
        layout.addSpacing(4)

        self.password = QLineEdit()
        self.password.setPlaceholderText("Enter your password")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.setFixedHeight(44)
        self.password.textChanged.connect(self._clear_error)
        self.password.returnPressed.connect(self._attempt_login)
        self.username.returnPressed.connect(self.password.setFocus)

        self._icon_show = eye_icon(MUTED, slashed=False)
        self._icon_hide = eye_icon(MUTED, slashed=True)
        self.toggle_action = self.password.addAction(
            self._icon_show, QLineEdit.ActionPosition.TrailingPosition
        )
        self.toggle_action.setToolTip("Show password")
        self.toggle_action.triggered.connect(self._toggle_password)
        layout.addWidget(self.password)

        # Inline error (hidden until needed)
        self.error_label = QLabel("")
        self.error_label.setObjectName("error")
        self.error_label.setWordWrap(True)
        self.error_label.setVisible(False)
        layout.addSpacing(10)
        layout.addWidget(self.error_label)

        layout.addSpacing(22)
        self.login_button = QPushButton("Log in")
        self.login_button.setObjectName("primary")
        self.login_button.setFixedHeight(46)
        self.login_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.login_button.setDefault(True)
        self.login_button.clicked.connect(self._attempt_login)
        layout.addWidget(self.login_button)

        layout.addSpacing(24)
        footnote = QLabel("Need access? Ask your administrator to create an account.")
        footnote.setObjectName("footnote")
        footnote.setWordWrap(True)
        layout.addWidget(footnote)

        return form

    # ---- Behaviour -------------------------------------------------------
    def resizeEvent(self, event):
        # Drop the brand panel on narrow windows so the form always has room.
        self.brand.setVisible(self.width() >= 760)
        super().resizeEvent(event)

    def _toggle_password(self):
        hidden = self.password.echoMode() == QLineEdit.EchoMode.Password
        self.password.setEchoMode(
            QLineEdit.EchoMode.Normal if hidden else QLineEdit.EchoMode.Password
        )
        self.toggle_action.setIcon(self._icon_hide if hidden else self._icon_show)
        self.toggle_action.setToolTip("Hide password" if hidden else "Show password")

    def _set_invalid(self, widget: QLineEdit, invalid: bool):
        widget.setProperty("invalid", invalid)
        widget.style().unpolish(widget)
        widget.style().polish(widget)

    def _show_error(self, message: str, *fields: QLineEdit):
        self.error_label.setText(message)
        self.error_label.setVisible(True)
        for field in (self.username, self.password):
            self._set_invalid(field, field in fields)

    def _clear_error(self):
        if self.error_label.isVisible():
            self.error_label.setVisible(False)
        for field in (self.username, self.password):
            self._set_invalid(field, False)

    def _attempt_login(self):
        username = self.username.text().strip()
        password = self.password.text()

        if not username and not password:
            self._show_error("Enter your username and password.", self.username, self.password)
            self.username.setFocus()
            return
        if not username:
            self._show_error("Enter your username.", self.username)
            self.username.setFocus()
            return
        if not password:
            self._show_error("Enter your password.", self.password)
            self.password.setFocus()
            return

        if not authenticate(username, password):
            self._show_error(
                "Username or password is incorrect. Check them and try again.",
                self.username, self.password,
            )
            self.password.selectAll()
            self.password.setFocus()
            return

        self.login_succeeded.emit(username)

    def _on_forgot_password(self):
        self.forgot_password_requested.emit()


def authenticate(username: str, password: str) -> bool:
    """Placeholder check. Replace with your real authentication (API, database, LDAP...)."""
    return username == "demo" and password == "demo1234"


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # consistent rendering of the stylesheet on every OS

    window = LoginWindow()
    window.login_succeeded.connect(
        lambda user: QMessageBox.information(window, APP_NAME, f"Logged in as {user}.")
    )
    window.forgot_password_requested.connect(
        lambda: QMessageBox.information(
            window, APP_NAME, "Password reset: connect this signal to your reset flow."
        )
    )
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()