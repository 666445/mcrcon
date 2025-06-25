import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QFrame
)
from rcon.source import Client

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("服务器操作窗口")
        self.setGeometry(100, 100, 600, 400)

        # 创建中心部件
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # 创建布局
        self.layout = QVBoxLayout(self.central_widget)

        # 创建输入服务器 IP 的区域
        self.ip_label = QLabel("服务器 IP:")
        self.layout.addWidget(self.ip_label)
        self.ip_input = QLineEdit()
        self.layout.addWidget(self.ip_input)

        # 创建输入端口的区域
        self.port_label = QLabel("端口:")
        self.layout.addWidget(self.port_label)
        self.port_input = QLineEdit()
        self.layout.addWidget(self.port_input)

        # 创建输入密码的区域
        self.password_label = QLabel("密码:")
        self.layout.addWidget(self.password_label)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.layout.addWidget(self.password_input)

        # 创建连接按钮
        self.connect_button = QPushButton("连接")
        self.layout.addWidget(self.connect_button)
        self.connect_button.clicked.connect(self.connect_to_server)

        # 创建输入指令的区域
        self.command_label = QLabel("指令:")
        self.layout.addWidget(self.command_label)
        self.command_input = QLineEdit()
        self.layout.addWidget(self.command_input)

        # 创建发送指令按钮
        self.send_button = QPushButton("发送指令")
        self.layout.addWidget(self.send_button)
        self.send_button.clicked.connect(self.send_command)

        # 创建显示服务器输出的区域
        self.output_label = QLabel("服务器输出:")
        self.layout.addWidget(self.output_label)
        self.output_display = QTextEdit()
        self.output_display.setReadOnly(True)
        self.layout.addWidget(self.output_display)

        # 创建分割线
        self.line = QFrame()
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)
        self.layout.addWidget(self.line)

        # 创建显示玩家列表的区域
        self.player_list_label = QLabel("玩家列表:")
        self.layout.addWidget(self.player_list_label)
        self.player_list_display = QTextEdit()
        self.player_list_display.setReadOnly(True)
        self.layout.addWidget(self.player_list_display)

        #创建分割线
        self.line2 = QFrame()
        self.line2.setFrameShape(QFrame.Shape.HLine)
        self.line2.setFrameShadow(QFrame.Shadow.Sunken)
        self.layout.addWidget(self.line2)
        # 创建关于标签
        self.link_label = QLabel('<a href="https://github.com/666445">作者github空间</a>')
        self.link_label.setOpenExternalLinks(True)  # 允许打开外部链接
        self.layout.addWidget(self.link_label)

    def connect_to_server(self):
        # 获取输入内容
        ip = self.ip_input.text()
        port = int(self.port_input.text())
        password = self.password_input.text()

        try:
            # 使用 rcon 客户端发送指令
            with Client(ip, port, passwd=password) as client:
                response = client.run("list")
                # 将服务器响应显示在输出区域
                self.output_display.append(f"服务器响应: {response}")
                # 更新玩家列表
                self.update_player_list(response)
        except Exception as e:
            # 如果发生错误，将错误信息显示在输出区域
            self.output_display.append(f"发生错误: {e}")

    def send_command(self):
        # 获取输入内容
        ip = self.ip_input.text()
        port = int(self.port_input.text())
        password = self.password_input.text()
        command = self.command_input.text()

        try:
            # 使用 rcon 客户端发送指令
            with Client(ip, port, passwd=password) as client:
                response = client.run(command)
                # 将服务器响应显示在输出区域
                self.output_display.append(f"服务器响应: {response}")
                # 如果发送的是 /list 命令，解析并显示玩家列表
                if command.lower() == "list":
                    self.update_player_list(response)
        except Exception as e:
            # 如果发生错误，将错误信息显示在输出区域
            self.output_display.append(f"发生错误: {e}")

        # 清空指令输入框
        self.command_input.clear()

    def update_player_list(self, response):
        # 清空玩家列表显示区域
        self.player_list_display.clear()
        # 解析玩家列表
        parts = response.split(": ")
        if len(parts) > 1:
            players = parts[1].strip()
            if players:
                player_list = players.split(", ")
                for player in player_list:
                    self.player_list_display.append(player)
            else:
                self.player_list_display.append("没有玩家在线")
        else:
            self.player_list_display.append("无法获取玩家列表")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())