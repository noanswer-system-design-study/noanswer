# render.py

import pygame
import random
from constants import WHITE, BLACK, weapon_descriptions, victory_messages
import resources  # 모듈 자체를 임포트합니다.
from game_state import GameState

def render_input_screen(screen, input_text, font):
    screen.fill(WHITE)
    bg_image = pygame.transform.scale(resources.background_image, (screen.get_width(), screen.get_height()))
    screen.blit(bg_image, (0, 0))

    prompt_text = "참가자 이름들을 입력하세요 (쉼표로 구분):"
    prompt_surface = font.render(prompt_text, True, BLACK)
    screen.blit(prompt_surface, (50, 50))

    input_surface = font.render(input_text, True, BLACK)
    screen.blit(input_surface, (50, 100))



def render_participant_info(screen, game_state, font):
    screen.fill(WHITE)
    bg_image = pygame.transform.scale(resources.background_image, (screen.get_width(), screen.get_height()))
    screen.blit(bg_image, (0, 0))

    title_text = f"참가자 정보 (스페이스바를 눌러 진행)"
    title_surface = font.render(title_text, True, BLACK)
    screen.blit(title_surface, (50, 20))

    y_offset = 70
    for name in game_state.participants:
        trait = game_state.participant_traits[name]
        weapon = game_state.assigned_weapons.get(name, "무기 미할당")
        info_text = f"{name} - 특성: {trait}, 무기: {weapon}"
        info_surface = font.render(info_text, True, BLACK)
        screen.blit(info_surface, (150, y_offset + 10))  # 텍스트 위치 조정

        # 캐릭터 이미지 표시
        if trait in resources.character_images:
            print(f"{name}의 이미지 블릿 시작")
            character_image = resources.character_images[trait]
            # 이미지 크기 조정 (필요한 경우)
            character_image = pygame.transform.scale(character_image, (80, 80))
            image_rect = character_image.get_rect()
            image_rect.topleft = (50, y_offset)
            screen.blit(character_image, image_rect)
            print(f"{name}의 이미지 블릿 완료")
        else:
            print(f"{name}의 특성에 해당하는 이미지가 없습니다: {trait}")
            # 특성에 해당하는 이미지가 없을 경우 기본 이미지 사용
            pass  # 필요에 따라 처리

        y_offset += 100  # 각 참가자마다 Y 좌표를 늘려서 위치 조정



def render_round_start_notification(screen, game_state, font):
    # 배경 이미지 표시
    bg_image = pygame.transform.scale(resources.background_image, (screen.get_width(), screen.get_height()))
    screen.blit(bg_image, (0, 0))
    
    # 라운드 시작 공지 텍스트
    notification_text = f"라운드 {game_state.round_number} 시작"
    text_surface = font.render(notification_text, True, BLACK)
    text_rect = text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    screen.blit(text_surface, text_rect)
    
    # 안내 문구
    info_text = "스페이스바를 눌러서 진행하세요."
    info_surface = font.render(info_text, True, BLACK)
    info_rect = info_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 50))
    screen.blit(info_surface, info_rect)



def render_stat_adjustment(screen, game_state, font, selected_participant, stat_inputs, total_points):
    # 배경 이미지 표시
    bg_image = pygame.transform.scale(resources.background_image, (screen.get_width(), screen.get_height()))
    screen.blit(bg_image, (0, 0))

    participant_rects = {}
    y_offset = 50

    # 참가자 목록 표시
    title_text = f"라운드 {game_state.round_number} - 능력치 조정"
    title_surface = font.render(title_text, True, BLACK)
    screen.blit(title_surface, (50, 20))

    info_text = "각 참가자마다 5포인트의 능력치를 분배하세요."
    info_surface = font.render(info_text, True, BLACK)
    screen.blit(info_surface, (50, y_offset))
    y_offset += 30

    for name in game_state.participants:
        participant_surface = font.render(name, True, BLACK)
        participant_rect = participant_surface.get_rect(topleft=(50, y_offset))
        screen.blit(participant_surface, participant_rect)
        participant_rects[name] = participant_rect
        y_offset += 30

    # 선택된 참가자에 대한 능력치 조정 UI 표시
    stat_button_rects = {}
    if selected_participant:
        # 왼쪽에 참가자 정보 표시
        y_offset = 100
        info_surface = font.render(f"{selected_participant}의 능력치 조정", True, BLACK)
        screen.blit(info_surface, (300, y_offset))
        y_offset += 30

        # 능력치 입력 필드 표시
        for stat_name in ["공격력", "방어력", "속도"]:
            stat_value = stat_inputs[stat_name]
            stat_surface = font.render(f"{stat_name}: {stat_value}", True, BLACK)
            screen.blit(stat_surface, (300, y_offset))

            # 증가 버튼 (+)
            inc_button_surface = font.render("+", True, WHITE)
            inc_button_rect = inc_button_surface.get_rect(topleft=(450, y_offset))
            pygame.draw.rect(screen, BLACK, inc_button_rect.inflate(10, 10))
            screen.blit(inc_button_surface, inc_button_rect)

            # 감소 버튼 (-)
            dec_button_surface = font.render("-", True, WHITE)
            dec_button_rect = dec_button_surface.get_rect(topleft=(480, y_offset))
            pygame.draw.rect(screen, BLACK, dec_button_rect.inflate(10, 10))
            screen.blit(dec_button_surface, dec_button_rect)

            # 버튼 위치 저장
            stat_button_rects[stat_name] = (inc_button_rect.inflate(10, 10), dec_button_rect.inflate(10, 10))

            y_offset += 40

        # 남은 포인트 표시
        points_surface = font.render(f"남은 포인트: {total_points}", True, BLACK)
        screen.blit(points_surface, (300, y_offset))
        y_offset += 30

        # "스탯 반영" 버튼 표시
        apply_button_surface = font.render("스탯 반영", True, WHITE)
        apply_button_rect = apply_button_surface.get_rect(center=(500, y_offset + 20))
        pygame.draw.rect(screen, BLACK, apply_button_rect.inflate(20, 10))
        screen.blit(apply_button_surface, apply_button_rect)
    else:
        apply_button_rect = None

    return participant_rects, apply_button_rect, stat_button_rects


    

def render_battle_result(screen, game_state, font):
    screen.fill(WHITE)
    bg_image = pygame.transform.scale(resources.background_image, (screen.get_width(), screen.get_height()))
    screen.blit(bg_image, (0, 0))

    name1, name2 = game_state.battle_results[game_state.current_battle]
    weapon1 = game_state.assigned_weapons[name1]
    weapon2 = game_state.assigned_weapons[name2]
    trait1 = game_state.participant_traits[name1]
    trait2 = game_state.participant_traits[name2]

    # 전투 정보 표시
    battle_text = f"라운드 {game_state.round_number} - 전투 {game_state.current_battle + 1}"
    battle_surface = font.render(battle_text, True, BLACK)
    screen.blit(battle_surface, (50, 20))

    # 참가자 정보 표시
    info1 = f"{name1} ({trait1}) - 무기: {weapon1}"
    info2 = f"{name2} ({trait2}) - 무기: {weapon2}"
    info1_surface = font.render(info1, True, BLACK)
    info2_surface = font.render(info2, True, BLACK)
    screen.blit(info1_surface, (50, 70))
    screen.blit(info2_surface, (50, 100))

    # 무기 설명 표시
    weapon1_desc = weapon_descriptions.get(weapon1, "")
    weapon2_desc = weapon_descriptions.get(weapon2, "")
    weapon1_surface = font.render(f"{weapon1}: {weapon1_desc}", True, BLACK)
    weapon2_surface = font.render(f"{weapon2}: {weapon2_desc}", True, BLACK)
    screen.blit(weapon1_surface, (50, 140))
    screen.blit(weapon2_surface, (50, 170))

    # 랜덤 이벤트 표시
    if game_state.event:
        event_text = f"랜덤 이벤트 발생: {game_state.event['이름']} - {game_state.event['설명']}"
        event_surface = font.render(event_text, True, BLACK)
        screen.blit(event_surface, (50, 210))

    # 결과 텍스트 표시
    # 매 프레임마다 랜덤 메시지를 선택하지 않고, 저장된 메시지를 사용합니다.
    result_text = game_state.victory_message
    result_surface = font.render(result_text, True, BLACK)
    screen.blit(result_surface, (50, 250))


  # 캐릭터 이미지 표시
    x_pos = 100
    y_pos = 350  # y 좌표를 텍스트가 끝나는 지점 아래로 이동
    for name in [name1, name2]:
        trait = game_state.participant_traits[name]
        if trait in resources.character_images:
            character_image = resources.character_images[trait]
            character_image = pygame.transform.scale(character_image, (100, 100))
            image_rect = character_image.get_rect()
            image_rect.center = (x_pos, y_pos)
            screen.blit(character_image, image_rect)
        x_pos += 300  # 다음 이미지의 x 위치 조정


    # 안내 문구
    info_text = "스페이스바를 눌러서 진행하세요."
    info_surface = font.render(info_text, True, BLACK)
    screen.blit(info_surface, (50, 500))


def render_game_over(screen, game_state, font):
    screen.fill(WHITE)
    bg_image = pygame.transform.scale(resources.background_image, (screen.get_width(), screen.get_height()))
    screen.blit(bg_image, (0, 0))

    winner = game_state.participants[0]
    game_over_text = f"최종 우승자는 {winner}입니다! 축하합니다!"
    text_surface = font.render(game_over_text, True, BLACK)
    text_rect = text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 50))
    screen.blit(text_surface, text_rect)

    # "다시 시작하기" 버튼 생성
    button_text = "다시 시작하기"
    button_surface = font.render(button_text, True, WHITE)
    button_rect = button_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 50))
    # 버튼 배경 그리기
    pygame.draw.rect(screen, BLACK, button_rect.inflate(20, 10))
    # 버튼 텍스트 그리기
    screen.blit(button_surface, button_rect)

    return button_rect  # 버튼의 위치 정보를 반환