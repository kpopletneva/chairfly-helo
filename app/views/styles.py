class StyleSheet:
    @staticmethod
    def red_rounded_button(radius: int =6) -> str:
        return f"""
        QPushButton {{
            background-color: red;
            color: white;
            font-weight: bold;
            border: 2px solid #cc0000;
            border-radius: {radius}px;
            padding: 10px;
        }}
        QPushButton:hover {{
                background-color: #cc0000; /* slightly darker red */
        }}
            QPushButton:pressed {{
                background-color: #990000; /* even darker red for pressed state */
        }}
        """

    @staticmethod
    def dropdown_style() -> str:
        return """
        QComboBox {
            padding: 4px;
            font-size: 14px;
        }
        """

    @staticmethod
    def toggle_style() -> str:
        return """
            text-align: right;
            padding: 4px;
            font-size: 14px;
            background-color: transparent;
            border: none;
            color: black;
        """

    @staticmethod
    def frame_style(background_color: str) -> str:
        return f"""
            background-color: {background_color};
            font-size: 14px;
            padding: 4px;
        """