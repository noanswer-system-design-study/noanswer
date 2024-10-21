# main.py

import pygame
import sys
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK
import resources  # resources 모듈 전체를 임포트
from game_state import GameState
from game_logic import (
    assign_traits, assign_weapons, assign_event,
    prepare_battles, simulate_battle
)
from render import (
    render_input_screen, render_participant_info,
    render_battle_result, render_game_over,
    render_round_start_notification,
    render_stat_adjustment  # 추가
)

def main():
    pygame.init()
    # 로컬 변수로 화면 크기를 관리
    screen_width = SCREEN_WIDTH
    screen_height = SCREEN_HEIGHT
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
    pygame.display.set_caption("전투 시뮬레이션 게임")

    clock = pygame.time.Clock()
    resources.load_resources()
    resources.load_font(18)  # 폰트 크기는 필요에 따라 조절 가능합니다.

    game_state = GameState()
    input_active = True
    input_text = ""
    restart_button_rect = None  # 게임 종료 화면에서의 재시작 버튼 위치 저장

    # 능력치 조정 관련 변수
    selected_participant = None
    stat_inputs = {"공격력": 0, "방어력": 0, "속도": 0}
    total_points = 5
    apply_button_rect = None

    while True:
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # 화면 크기 조정 이벤트 처리
            elif event.type == pygame.VIDEORESIZE:
                screen_width, screen_height = event.w, event.h
                screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
            # 키보드 및 마우스 입력 처리
            elif event.type == pygame.KEYDOWN:
                if game_state.state == "입력 대기":
                    if input_active:
                        if event.key == pygame.K_RETURN:
                            # 참가자 입력 완료
                            game_state.participants = [name.strip() for name in input_text.split(",")]
                            assign_traits(game_state)
                            assign_weapons(game_state)
                            # 참가자 능력치 초기화
                            for name in game_state.participants:
                                game_state.participant_stats[name] = {"공격력": 0, "방어력": 0, "속도": 0}
                            game_state.state = "참가자 정보"
                            input_active = False
                        elif event.key == pygame.K_BACKSPACE:
                            input_text = input_text[:-1]
                        else:
                            input_text += event.unicode
                elif game_state.state == "참가자 정보":
                    if event.key == pygame.K_SPACE:
                        game_state.state = "라운드 시작 알림"
                elif game_state.state == "라운드 시작 알림":
                    if event.key == pygame.K_SPACE:
                        game_state.state = "능력치 조정"
                elif game_state.state == "능력치 조정":
                    if selected_participant:
                        if event.key == pygame.K_BACKSPACE:
                            # 마지막 입력 삭제
                            pass  # 입력 필드 구현 시 구체적으로 처리
                        elif event.unicode.isdigit():
                            # 숫자 입력 처리
                            pass  # 입력 필드 구현 시 구체적으로 처리
                elif game_state.state == "전투 결과":
                    if event.key == pygame.K_SPACE:
                        # 다음 전투로 진행
                        game_state.current_battle += 1
                        if game_state.current_battle >= len(game_state.battle_results):
                            # 라운드 종료, 다음 라운드 시작 알림 상태로 전환
                            game_state.participants = game_state.next_round_participants
                            game_state.next_round_participants = []
                            game_state.round_number += 1
                            if len(game_state.participants) <= 1:
                                game_state.state = "게임 종료"
                            else:
                                game_state.state = "라운드 시작 알림"
                            game_state.current_battle = 0
                        else:
                            game_state.state = "전투 진행"
                elif game_state.state == "게임 종료":
                    pass  # 게임 종료 시 키보드 입력 처리 (필요에 따라 추가)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game_state.state == "능력치 조정":
                    mouse_pos = event.pos
                    # 참가자 선택 처리
                    for name, rect in participant_rects.items():
                        if rect.collidepoint(mouse_pos):
                            selected_participant = name
                            stat_inputs = {"공격력": 0, "방어력": 0, "속도": 0}
                            total_points = 5
                            break  # 선택된 참가자를 찾았으므로 반복문 종료

                    if selected_participant:
                        # 능력치 증가/감소 버튼 클릭 처리
                        for stat_name, buttons in stat_button_rects.items():
                            inc_button_rect, dec_button_rect = buttons
                            if inc_button_rect.collidepoint(mouse_pos) and total_points > 0:
                                stat_inputs[stat_name] += 1
                                total_points -= 1
                            elif dec_button_rect.collidepoint(mouse_pos) and stat_inputs[stat_name] > 0:
                                stat_inputs[stat_name] -= 1
                                total_points += 1

                        # "스탯 반영" 버튼 클릭 처리
                        if apply_button_rect and apply_button_rect.collidepoint(mouse_pos):
                            if selected_participant:
                                # 능력치 적용
                                game_state.participant_stats[selected_participant]["공격력"] += stat_inputs["공격력"]
                                game_state.participant_stats[selected_participant]["방어력"] += stat_inputs["방어력"]
                                game_state.participant_stats[selected_participant]["속도"] += stat_inputs["속도"]
                                selected_participant = None
                                # 모든 참가자의 능력치 조정이 완료되었는지 확인
                                all_points_assigned = True
                                for name in game_state.participants:
                                    total_assigned = sum(game_state.participant_stats[name].values())
                                    expected_total = (game_state.round_number) * 5  # 라운드마다 5포인트씩 누적
                                    if total_assigned < expected_total:
                                        all_points_assigned = False
                                        break
                                if all_points_assigned:
                                    game_state.state = "라운드 준비"
                elif game_state.state == "게임 종료" and restart_button_rect:
                    if restart_button_rect.collidepoint(event.pos):
                        # 게임 상태 초기화
                        game_state.reset()
                        input_active = True
                        input_text = ""
                        restart_button_rect = None
            # 마우스 커서 변경 (선택 사항)
            elif event.type == pygame.MOUSEMOTION:
                if game_state.state == "게임 종료" and restart_button_rect:
                    if restart_button_rect.collidepoint(event.pos):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    else:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        # 상태에 따른 렌더링
        if game_state.state == "입력 대기":
            # 참가자 이름 입력 화면
            render_input_screen(screen, input_text, resources.font)
        elif game_state.state == "참가자 정보":
            # 참가자 정보 화면
            render_participant_info(screen, game_state, resources.font)
        elif game_state.state == "라운드 시작 알림":
            # 라운드 시작 알림 화면 렌더링
            render_round_start_notification(screen, game_state, resources.font)
       
        elif game_state.state == "능력치 조정":
            # 능력치 조정 화면 렌더링
            participant_rects, apply_button_rect, stat_button_rects = render_stat_adjustment(screen, game_state, resources.font, selected_participant, stat_inputs, total_points)

        elif game_state.state == "라운드 준비":
            # 라운드 준비 단계
            assign_event(game_state)
            if game_state.round_number > 1:
                assign_weapons(game_state)  # 2라운드부터 무기 재할당
            prepare_battles(game_state)
            game_state.state = "전투 진행"
        elif game_state.state == "전투 진행":
            # 전투 진행 화면
            simulate_battle(game_state)
            game_state.state = "전투 결과"
        elif game_state.state == "전투 결과":
            # 전투 결과 화면
            render_battle_result(screen, game_state, resources.font)
        elif game_state.state == "게임 종료":
            # 게임 종료 화면
            restart_button_rect = render_game_over(screen, game_state, resources.font)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
