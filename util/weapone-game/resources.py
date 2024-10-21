# resources.py

import pygame
import os
from constants import FONT_PATH

# 이미지 로드
character_images = {}
weapon_images = {}
background_image = None

# 폰트 변수 초기화
font = None

def load_font(size):
    global font
    print(f"폰트 로드 시도: {FONT_PATH}")
    font = None
    if os.path.isfile(FONT_PATH):
        try:
            font = pygame.font.Font(FONT_PATH, size)
            print("폰트 파일을 성공적으로 로드했습니다.")
        except Exception as e:
            print(f"폰트 로드 중 오류 발생: {e}")
    else:
        print(f"폰트 파일을 찾을 수 없습니다: {FONT_PATH}")

    if font is None:
        available_fonts = pygame.font.get_fonts()
        preferred_fonts = ["malgungothic", "nanumgothic", "unbatang", "arialunicode", "applegothic"]
        font_name = None
        for preferred_font in preferred_fonts:
            if preferred_font.lower() in available_fonts:
                font_name = preferred_font
                break
        if font_name is None:
            font_name = pygame.font.get_default_font()
            print("선호하는 폰트를 찾을 수 없어 기본 폰트를 사용합니다. 텍스트가 깨질 수 있습니다.")
        else:
            print(f"시스템 폰트 '{font_name}'을(를) 사용합니다.")
        font = pygame.font.SysFont(font_name, size)


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def load_resources():
    global character_images, weapon_images, background_image
    # 캐릭터 이미지 로드
    character_images = {}
    for trait in ["힘", "민첩성", "지능"]:
        image_filename = f"{trait}.png"  # 이미지 파일명이 특성명과 동일한 경우
        # image_path = os.path.join("images", image_filename)
        image_path = resource_path(os.path.join("images", image_filename))
        try:
            character_images[trait] = pygame.image.load(image_path).convert_alpha()
            print(f"{trait} 이미지 로드 성공: {image_path}")
        except pygame.error as e:
            print(f"{trait} 이미지 로드 실패: {e}")
            # 기본 이미지 사용 또는 빈 Surface 생성
            character_images[trait] = pygame.Surface((80, 80))
            character_images[trait].fill((255, 0, 0))  # 빨간색 사각형으로 표시

    # 무기 이미지 로드
    weapon_images = {
        "레이저 칼": pygame.image.load(os.path.join("images", "laser_sword.png")),
        "RPG 로켓 런처": pygame.image.load(os.path.join("images", "rpg.png")),
        "전기 톱": pygame.image.load(os.path.join("images", "chainsaw.png")),
        "전투 드론": pygame.image.load(os.path.join("images", "drone.png")),
        "사제 폭탄": pygame.image.load(os.path.join("images", "bomb.png")),
        "무적의 방패": pygame.image.load(os.path.join("images", "shield.png")),
        "고대 마법 지팡이": pygame.image.load(os.path.join("images", "magic_staff.png")),
        "스나이퍼 라이플": pygame.image.load(os.path.join("images", "sniper_rifle.png")),
        "무중력 수트": pygame.image.load(os.path.join("images", "gravity_suit.png")),
        "생화학 무기": pygame.image.load(os.path.join("images", "bio_weapon.png")),
        "거대 로봇": pygame.image.load(os.path.join("images", "giant_robot.png"))
    }
    # 배경 이미지 로드
    background_image_path = resource_path(os.path.join("images", "background.png"))
    background_image = pygame.image.load(background_image_path).convert()
    # background_image = pygame.image.load("images/background.png")
