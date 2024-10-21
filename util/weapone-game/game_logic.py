# game_logic.py

import random
from constants import weapons, character_traits, random_events, weapon_advantages, victory_messages
from game_state import GameState

def assign_traits(game_state):
    for name in game_state.participants:
        game_state.participant_traits[name] = random.choice(character_traits)

def assign_weapons(game_state):
    weapons_list = list(weapons.keys())
    random.shuffle(weapons_list)
    # for i, name in enumerate(game_state.participants):
    #     game_state.assigned_weapons[name] = weapons_list[i % len(weapons_list)]
    for name in game_state.participants:
        game_state.assigned_weapons[name] = random.choice(weapons_list)  # 무기를 무작위로 선택
    

def assign_event(game_state):
    game_state.event = random.choice(random_events + [None])

def prepare_battles(game_state):
    game_state.battle_results = []
    participants = game_state.participants.copy()
    random.shuffle(participants)
    if len(participants) % 2 == 1:
        bye_player = participants.pop()
        game_state.next_round_participants.append(bye_player)
    while participants:
        name1 = participants.pop()
        name2 = participants.pop()
        game_state.battle_results.append((name1, name2))
    game_state.current_battle = 0

def simulate_battle(game_state):
    name1, name2 = game_state.battle_results[game_state.current_battle]
    winner, victory_message = run_battle_simulation(name1, name2, game_state)
    game_state.next_round_participants.append(winner)
    game_state.victory_message = victory_message  # 승리 메시지 저장


def run_battle_simulation(name1, name2, game_state):
    weapon1 = game_state.assigned_weapons[name1]
    weapon2 = game_state.assigned_weapons[name2]
    prob = calculate_win_probability(name1, name2, game_state.assigned_weapons, game_state.event, game_state)
    winner = random.choices([name1, name2], weights=[prob, 1 - prob])[0]
    loser = name2 if winner == name1 else name1

    # 승리 메시지 생성
    message_template = random.choice(victory_messages)
    victory_message = message_template.format(winner=winner, loser=loser)

    return winner, victory_message


def calculate_win_probability(p1, p2, assigned_weapons, event, game_state):
    weapon1 = assigned_weapons[p1]
    weapon2 = assigned_weapons[p2]
    stats1 = weapons[weapon1].copy()
    stats2 = weapons[weapon2].copy()


    # 참가자 능력치 적용
    participant_stats1 = game_state.participant_stats[p1]
    participant_stats2 = game_state.participant_stats[p2]

    stats1["공격력"] += participant_stats1["공격력"]
    stats1["방어력"] += participant_stats1["방어력"]
    stats1["속도"] += participant_stats1["속도"]

    stats2["공격력"] += participant_stats2["공격력"]
    stats2["방어력"] += participant_stats2["방어력"]
    stats2["속도"] += participant_stats2["속도"]
    
    # 캐릭터 특성 적용
    trait1 = game_state.participant_traits[p1]
    trait2 = game_state.participant_traits[p2]
    
    if trait1 == "힘":
        stats1["공격력"] += 10
    elif trait1 == "민첩성":
        stats1["속도"] += 10
    elif trait1 == "지능":
        stats1["방어력"] += 10

    if trait2 == "힘":
        stats2["공격력"] += 10
    elif trait2 == "민첩성":
        stats2["속도"] += 10
    elif trait2 == "지능":
        stats2["방어력"] += 10
    
    # 랜덤 이벤트 적용
    if event:
        for weapon in [weapon1, weapon2]:
            if weapon in event["영향"]:
                if weapon == weapon1:
                    stats1["공격력"] += event["영향"][weapon]
                else:
                    stats2["공격력"] += event["영향"][weapon]
        if "속도" in event["영향"]:
            stats1["속도"] += event["영향"]["속도"]
            stats2["속도"] += event["영향"]["속도"]
    
    # 무기 상성 적용
    if weapon2 in weapon_advantages.get(weapon1, []):
        stats1["공격력"] += 15
    if weapon1 in weapon_advantages.get(weapon2, []):
        stats2["공격력"] += 15
    
    # **랜덤 요소 추가**
    random_factor1 = random.uniform(0.8, 1.2)  # 0.8에서 1.2 사이의 랜덤 값
    random_factor2 = random.uniform(0.8, 1.2)

    # 승리 확률 계산 (랜덤 요소 포함)
    score1 = (stats1["공격력"] + stats1["속도"]) * random_factor1
    score2 = (stats2["공격력"] + stats2["속도"]) * random_factor2
    total = score1 + score2
    prob1 = score1 / total

    return prob1