# -*- coding: utf-8 -*-
"""
Shared styled message box component.

A frameless, rounded dialog matching the app's design language.
Use this instead of QMessageBox for all error/warning/info dialogs.

Usage:
    from ui.components.styled_message_box import StyledMessageBox

    # Warning
    StyledMessageBox.warning(parent, "تحذير", "رقم الوحدة مكرر")

    # Error
    StyledMessageBox.error(parent, "خطأ", "فشل في إنشاء الوحدة")

    # Info
    StyledMessageBox.info(parent, "معلومات", "تمت العملية بنجاح")

    # Confirmation (returns True if OK clicked)
    if StyledMessageBox.confirm(parent, "تأكيد", "هل أنت متأكد؟"):
        ...
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor


class StyledMessageBox(QDialog):
    """Frameless styled message box matching the app design."""

    # Dialog types: (icon_text, icon_bg, icon_border, icon_color, btn_color, btn_hover)
    WARNING = ("⚠", "#FEF3C7", "#FCD34D", "#D97706", "#F59E0B", "#D97706")
    ERROR = ("✕", "#FEE2E2", "#FCA5A5", "#DC2626", "#EF4444", "#DC2626")
    INFO = ("i", "#DBEAFE", "#93C5FD", "#2563EB", "#3B82F6", "#2563EB")
    SUCCESS = ("✓", "#D1FAE5", "#6EE7B7", "#059669", "#10B981", "#059669")

    def __init__(self, parent, title: str, message: str,
                 dialog_type=None, ok_text: str = "موافق",
                 cancel_text: str = "إلغاء", show_cancel: bool = False):
        super().__init__(parent)

        if dialog_type is None:
            dialog_type = self.WARNING

        self._dialog_type = dialog_type
        self._show_cancel = show_cancel

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(380, 240 if not show_cancel else 260)
        self.setModal(True)

        self._build_ui(title, message, ok_text, cancel_text)

    def _build_ui(self, title: str, message: str, ok_text: str, cancel_text: str):
        icon_text, icon_bg, icon_border, icon_color, btn_color, btn_hover = self._dialog_type

        outer = QVBoxLayout(self)
        outer.setContentsMargins(12, 12, 12, 12)

        # Card with shadow
        card = QFrame()
        card.setObjectName("StyledMsgCard")
        card.setStyleSheet("""
            QFrame#StyledMsgCard {
                background-color: #FFFFFF;
                border: 1px solid #E5E7EB;
                border-radius: 16px;
            }
        """)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setOffset(0, 4)
        shadow.setColor(QColor(0, 0, 0, 40))
        card.setGraphicsEffect(shadow)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 24, 20, 20)
        card_layout.setSpacing(12)
        card_layout.setAlignment(Qt.AlignCenter)

        # Circular icon
        icon_label = QLabel(icon_text)
        icon_label.setFixedSize(56, 56)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet(f"""
            QLabel {{
                background-color: {icon_bg};
                border: 2px solid {icon_border};
                border-radius: 28px;
                font-size: 24px;
                color: {icon_color};
            }}
        """)
        card_layout.addWidget(icon_label, alignment=Qt.AlignCenter)

        # Title
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                color: #1F2937;
                font-size: 15px;
                font-weight: 700;
                background: transparent;
                border: none;
            }
        """)
        card_layout.addWidget(title_label)

        # Message
        msg_label = QLabel(message)
        msg_label.setAlignment(Qt.AlignCenter)
        msg_label.setWordWrap(True)
        msg_label.setStyleSheet("""
            QLabel {
                color: #6B7280;
                font-size: 12px;
                background: transparent;
                border: none;
            }
        """)
        card_layout.addWidget(msg_label)

        card_layout.addSpacing(4)

        # Buttons
        if self._show_cancel:
            btn_layout = QHBoxLayout()
            btn_layout.setSpacing(12)

            cancel_btn = QPushButton(cancel_text)
            cancel_btn.setFixedHeight(36)
            cancel_btn.setCursor(Qt.PointingHandCursor)
            cancel_btn.setStyleSheet("""
                QPushButton {
                    background-color: #F3F4F6;
                    color: #374151;
                    border: 1px solid #D1D5DB;
                    border-radius: 8px;
                    font-size: 13px;
                    font-weight: 600;
                    padding: 0 24px;
                }
                QPushButton:hover {
                    background-color: #E5E7EB;
                }
            """)
            cancel_btn.clicked.connect(self.reject)

            ok_btn = QPushButton(ok_text)
            ok_btn.setFixedHeight(36)
            ok_btn.setCursor(Qt.PointingHandCursor)
            ok_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {btn_color};
                    color: white;
                    border: none;
                    border-radius: 8px;
                    font-size: 13px;
                    font-weight: 600;
                    padding: 0 24px;
                }}
                QPushButton:hover {{
                    background-color: {btn_hover};
                }}
            """)
            ok_btn.clicked.connect(self.accept)

            btn_layout.addStretch()
            btn_layout.addWidget(cancel_btn)
            btn_layout.addWidget(ok_btn)
            btn_layout.addStretch()
            card_layout.addLayout(btn_layout)
        else:
            ok_btn = QPushButton(ok_text)
            ok_btn.setFixedHeight(36)
            ok_btn.setCursor(Qt.PointingHandCursor)
            ok_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {btn_color};
                    color: white;
                    border: none;
                    border-radius: 8px;
                    font-size: 13px;
                    font-weight: 600;
                    padding: 0 32px;
                }}
                QPushButton:hover {{
                    background-color: {btn_hover};
                }}
            """)
            ok_btn.clicked.connect(self.accept)
            card_layout.addWidget(ok_btn, alignment=Qt.AlignCenter)

        outer.addWidget(card)

    @staticmethod
    def warning(parent, title: str, message: str, ok_text: str = "موافق"):
        """Show a styled warning dialog."""
        dialog = StyledMessageBox(parent, title, message, StyledMessageBox.WARNING, ok_text)
        dialog.exec_()

    @staticmethod
    def error(parent, title: str, message: str, ok_text: str = "موافق"):
        """Show a styled error dialog."""
        dialog = StyledMessageBox(parent, title, message, StyledMessageBox.ERROR, ok_text)
        dialog.exec_()

    @staticmethod
    def info(parent, title: str, message: str, ok_text: str = "موافق"):
        """Show a styled info dialog."""
        dialog = StyledMessageBox(parent, title, message, StyledMessageBox.INFO, ok_text)
        dialog.exec_()

    @staticmethod
    def success(parent, title: str, message: str, ok_text: str = "موافق"):
        """Show a styled success dialog."""
        dialog = StyledMessageBox(parent, title, message, StyledMessageBox.SUCCESS, ok_text)
        dialog.exec_()

    @staticmethod
    def confirm(parent, title: str, message: str,
                ok_text: str = "تأكيد", cancel_text: str = "إلغاء") -> bool:
        """Show a styled confirmation dialog. Returns True if OK clicked."""
        dialog = StyledMessageBox(
            parent, title, message, StyledMessageBox.WARNING,
            ok_text, cancel_text, show_cancel=True
        )
        return dialog.exec_() == QDialog.Accepted
