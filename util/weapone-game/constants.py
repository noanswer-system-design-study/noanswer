# constants.py

import os

# 화면 설정
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 폰트 파일 경로
FONT_PATH = os.path.join("fonts", "maruburi", "TTF", "MaruBuri-Regular.ttf")

# 무기 목록 및 속성
weapons = {
    "레이저 칼": {"공격력": 80, "방어력": 20, "속도": 70},
    "RPG 로켓 런처": {"공격력": 90, "방어력": 10, "속도": 40},
    "전기 톱": {"공격력": 70, "방어력": 30, "속도": 60},
    "전투 드론": {"공격력": 85, "방어력": 15, "속도": 80},
    "사제 폭탄": {"공격력": 95, "방어력": 5, "속도": 30},
    "무적의 방패": {"공격력": 50, "방어력": 100, "속도": 20},
    "고대 마법 지팡이": {"공격력": 90, "방어력": 20, "속도": 50},
    "스나이퍼 라이플": {"공격력": 85, "방어력": 15, "속도": 75},
    "무중력 수트": {"공격력": 60, "방어력": 40, "속도": 90},
    "생화학 무기": {"공격력": 88, "방어력": 12, "속도": 50},
    "거대 로봇": {"공격력": 95, "방어력": 80, "속도": 30}
}

weapon_descriptions = {
    "레이저 칼": "레이저 칼은 강력한 근접 무기로, 빛의 속도로 적을 베어낼 수 있습니다.",
    "RPG 로켓 런처": "RPG 로켓 런처는 강력한 폭발로 넓은 범위를 공격할 수 있는 무기입니다.",
    "전기 톱": "전기 톱은 근접전에서 치명적인 피해를 줄 수 있는 무기입니다.",
    "전투 드론": "전투 드론은 원거리 공격과 정밀 타격에 강합니다.",
    "사제 폭탄": "사제 폭탄은 강력하지만 취급이 어려운 폭발물입니다.",
    "무적의 방패": "무적의 방패는 모든 공격을 막아낼 수 있는 방어용 무기입니다.",
    "고대 마법 지팡이": "고대 마법 지팡이는 신비한 힘을 발휘하여 적을 제압합니다.",
    "스나이퍼 라이플": "스나이퍼 라이플은 먼 거리에서 적을 제거할 수 있는 무기입니다.",
    "무중력 수트": "무중력 수트는 중력을 무시하고 자유롭게 움직일 수 있게 합니다.",
    "생화학 무기": "생화학 무기는 광범위한 지역을 오염시키는 치명적인 무기입니다.",
    "거대 로봇": "거대 로봇은 엄청난 파괴력과 방어력을 가진 무기입니다."
}

victory_messages = [
    "{winner}는 {loser}의 공격을 피하고 반격하여 승리했습니다!",
    "{loser}는 {winner}의 강력한 공격에 무너졌습니다!",
    "{winner}의 전략적인 플레이로 {loser}를 제압했습니다!",
    "{loser}는 {winner}의 속도를 따라가지 못했습니다!",
    "{winner}의 무기가 빛을 발하여 {loser}를 쓰러뜨렸습니다!",
    "{loser}는 예상치 못한 공격에 당하고 말았습니다!",
    "{winner}는 놀라운 힘을 발휘하여 {loser}를 압도했습니다!",
    "{loser}는 최선을 다했지만 {winner}를 막을 수 없었습니다!",
    "{winner}의 무기와 특성이 완벽히 조화를 이루었습니다!",
    "{loser}는 운이 따르지 않았습니다. {winner}가 승리합니다!"
]

random_events = [
    {"이름": "폭우", "설명": "폭우로 인해 전기 계열 무기의 효율이 감소합니다.", "영향": {"전기 톱": -20, "전투 드론": -10}},
    {"이름": "안개", "설명": "짙은 안개로 인해 원거리 무기의 명중률이 감소합니다.", "영향": {"스나이퍼 라이플": -30, "전투 드론": -15}},
    {"이름": "태양 폭발", "설명": "태양 폭발로 마법 무기의 위력이 증가합니다.", "영향": {"고대 마법 지팡이": 20}},
    {"이름": "지진", "설명": "지진으로 인해 이동 속도가 느려집니다.", "영향": {"속도": -10}},
    {"이름": "바람", "설명": "강한 바람이 불어 폭발물의 위력이 증가합니다.", "영향": {"RPG 로켓 런처": 15, "사제 폭탄": 15}}
]

weapon_advantages = {
    "레이저 칼": ["전기 톱", "생화학 무기"],
    "무적의 방패": ["레이저 칼", "RPG 로켓 런처"],
    "고대 마법 지팡이": ["무적의 방패", "거대 로봇"],
    # 나머지 무기들의 상성도 추가 가능
}

# 캐릭터 특성 목록
character_traits = ["힘", "민첩성", "지능"]