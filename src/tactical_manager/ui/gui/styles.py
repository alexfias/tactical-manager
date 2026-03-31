def main_stylesheet() -> str:
    return """
        #titleLabel {
            color: white;
            background-color: rgba(0, 0, 0, 110);
            border: 1px solid rgba(255, 255, 255, 35);
            border-radius: 10px;
            padding: 10px 14px;
            letter-spacing: 2px;
        }

        #menuPanel {
            background-color: rgba(0, 0, 0, 140);
            border: 1px solid rgba(255, 255, 255, 24);
            border-radius: 16px;
        }

        #contentPanel {
            background-color: rgba(0, 0, 0, 145);
            border: 1px solid rgba(255, 255, 255, 30);
            border-radius: 16px;
        }

        #sectionTitle {
            color: white;
            background-color: rgba(255, 255, 255, 18);
            border-radius: 8px;
            padding: 8px 10px;
        }

        #matchResultCard {
            background-color: rgba(8, 8, 8, 205);
            border: 1px solid rgba(255, 255, 255, 30);
            border-radius: 14px;
        }

        #matchStatus {
            color: rgba(255, 255, 255, 180);
            font-size: 13px;
            padding: 4px;
        }

        #teamName {
            color: white;
            font-size: 18px;
            font-weight: bold;
            padding: 8px;
        }

        #scoreLine {
            color: white;
            font-size: 28px;
            font-weight: bold;
            padding: 8px;
        }

        #summaryTitle {
            color: white;
            font-size: 14px;
            font-weight: bold;
            padding-top: 10px;
            padding-bottom: 4px;
        }

        QPushButton {
            background-color: rgba(18, 18, 18, 210);
            color: white;
            border: 1px solid rgba(255, 255, 255, 28);
            border-radius: 10px;
            padding: 10px 12px;
            font-size: 14px;
            text-align: left;
        }

        QPushButton:hover {
            background-color: rgba(38, 38, 38, 230);
            border: 1px solid rgba(255, 255, 255, 55);
        }

        QPushButton:pressed {
            background-color: rgba(55, 55, 55, 230);
        }

        QPushButton[active="true"] {
            background-color: rgba(70, 90, 120, 220);
            border: 1px solid rgba(255, 255, 255, 70);
        }

        QTextEdit {
            background-color: rgba(8, 8, 8, 205);
            color: white;
            border: 1px solid rgba(255, 255, 255, 30);
            border-radius: 12px;
            padding: 14px;
            font-size: 13px;
        }

        QLabel {
            color: white;
        }

        QComboBox {
            background-color: rgba(25, 25, 25, 230);
            color: white;
            border: 1px solid rgba(255, 255, 255, 40);
            border-radius: 6px;
            padding: 6px;
            min-height: 28px;
        }

        QDialog {
            background-color: #1e1e1e;
            color: white;
        }
        
        #statLabel {
            color: rgba(255, 255, 255, 180);
            font-size: 13px;
            padding: 4px;
        }
        
        #statValue {
            color: white;
            font-size: 14px;
            font-weight: bold;
            padding: 4px;
        }
    """
