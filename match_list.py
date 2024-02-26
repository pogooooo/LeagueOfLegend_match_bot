import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QFont, QFontDatabase, QPixmap
from PyQt5.QtCore import Qt

app = QApplication(sys.argv)

# 폰트 경로 설정
font_path = "C:/Users/poggo/Downloads/Programing/lol_team_match/CHANEY-ULTRA-EXTENDED/Desktop/CHANEY-UltraExtended.otf"

# 폰트 로드
font_id = QFontDatabase.addApplicationFont(font_path)
font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
chaney = QFont(font_family)


def print_match_list(matchs) :
    window = QWidget()
    window.setWindowTitle("Match List")
    window.setStyleSheet("background-color: #1C192B;")

    layout = QVBoxLayout(window)

    chaney.setPointSize(50)

    title_label = QLabel(window)
    title_label.setText("match list")
    title_label.setGeometry(0, 10, 400, 100)
    title_label.setAlignment(Qt.AlignCenter)
    title_label.setStyleSheet("color: #E2E4F2;"
                              "margin-top: 20px;")
    title_label.setFont(chaney)
    layout.addWidget(title_label)

    line = QLabel(window)
    line.setGeometry(25, 0, 350, 1)
    line.setStyleSheet("border-top: 7px solid #E2E4F2;"
                       "margin-top: 30px;")
    line.setFont(chaney)
    layout.addWidget(line)

    for i in matchs :
        chaney.setPointSize(30)
        match_label = QLabel(window)
        match_label.setGeometry(0, 0, 200, 10)
        if i[0] == 1 : match_label.setText(f"{i[0]}.    {i[1]}   02/30   {i[2]}   {i[5][:2]}P")
        else : match_label.setText(f"{i[0]}.   {i[1]}   02/30   {i[2]}   {i[5][:2]}P")
        match_label.setAlignment(Qt.AlignCenter)
        match_label.setFont(chaney)
        match_label.setStyleSheet("color: #E2E4F2;"
                                  "margin-bottom: 20px;")
        layout.addWidget(match_label)


    window.setGeometry(100, 100, 400, 0)

    window.setLayout(layout)
    window.show()

    screenshot = QPixmap(window.size())
    window.render(screenshot)

    # 이미지를 QImage로 변환
    image = screenshot.toImage()

    # QImage를 파일로 저장
    image.save("match_list_screenshot.png", "png")
    app.quit()

def print_start_match(owner, day, time, people, number) :
    window = QWidget()
    window.setWindowTitle("start match")
    window.setStyleSheet("background-color: #1C192B;")

    layout = QVBoxLayout(window)
    layout.setContentsMargins(0, 0, 0, 0)

    chaney.setPointSize(30)

    title_label = QLabel(window)
    title_label.setText(f"{owner}'s match")
    title_label.setStyleSheet("color: #E2E4F2;"
                              "margin-right: 100px;"
                              "margin-top: 30px;")
    title_label.setFont(chaney)
    layout.addWidget(title_label)

    start_time = QLabel(window)
    start_time.setText(f"{day}  {time}")
    start_time.setStyleSheet("color: #E2E4F2;"
                             "margin-right:10px;"
                             "margin-top: 30px;"
                             "margin-bottom: 30px;")
    start_time.setFont(chaney)
    layout.addWidget(start_time)

    h_layout = QHBoxLayout()

    chaney.setPointSize(25)
    beige_box = QLabel(window)
    beige_box.setText(f"{number}")
    beige_box.setFixedSize(80, 80)
    beige_box.setAlignment(Qt.AlignCenter)
    beige_box.setFont(chaney)
    beige_box.setStyleSheet("background-color: #FBC3AE;"
                            "color: #1C192B;")
    h_layout.addWidget(beige_box)

    match_people = QLabel(window)
    if people == "10인" : match_people.setText("   5   vs   5")
    else : match_people.setText("   5   vs   5    |    5   vs   5")
    match_people.setStyleSheet("color: #1C192B;"
                               "background-color: #E2E4F2;")
    match_people.setFont(chaney)
    h_layout.addWidget(match_people)

    h_layout.setSpacing(0)
    layout.addLayout(h_layout)

    window.setGeometry(200, 100, 0, 240)

    window.setLayout(layout)
    window.show()

    screenshot = QPixmap(window.size())
    window.render(screenshot)

    # 이미지를 QImage로 변환
    image = screenshot.toImage()

    # QImage를 파일로 저장
    image.save("start_match_screenshot.png", "png")
    app.quit()

print_start_match(".hyunjung", "02/08", "11:00", "20인", 1)