# game_state.py

class GameState:
    def __init__(self):
        self.participants = []
        self.round_number = 1
        self.assigned_weapons = {}
        self.participant_traits = {}
        self.participant_stats = {}  # 참가자 능력치 추가
        self.next_round_participants = []
        self.event = None
        self.current_battle = 0
        self.battle_results = []
        self.state = "입력 대기"  # 가능한 상태: 입력 대기, 참가자 정보, 라운드 시작 알림, 라운드 준비, 전투 진행, 전투 결과, 게임 종료
        self.victory_message = ""

    def reset(self):
        self.round_number = 1
        self.assigned_weapons = {}
        self.participant_traits = {}
        self.next_round_participants = []
        self.event = None
        self.current_battle = 0
        self.battle_results = []
        self.state = "입력 대기"
