from otree.api import *
import random

class C(BaseConstants):
    NAME_IN_URL = 'try'
    PLAYERS_PER_GROUP = None  # 実験者が入力する

    # 练习与正式轮次 / 練習と本番のラウンド
    PRACTICE_ROUNDS = 4
    OFFICIAL_ROUNDS = 6 #42
    NUM_ROUNDS = PRACTICE_ROUNDS + OFFICIAL_ROUNDS  # 46 total

    # 参数 / パラメータ
    C_1 = 2
    C_2 = 4
    A = 150
    B_HIGH = 0.5
    B_LOW = 1.5

    # 默认 / デフォルト
    DEFAULT_INSTITUTION = 'IND'
    DEFAULT_STOCK_SYMBOL = 'H'

    # 模式定义 / パターン定義
    PRACTICE_PATTERNS = {
        1: {'institution': 'IND',  'stock': 'H'},
        2: {'institution': 'IND',  'stock': 'L'},
        3: {'institution': 'POOL', 'stock': 'H'},
        4: {'institution': 'POOL', 'stock': 'L'},
    }
    OFFICIAL_PATTERNS = {
        1: {'institution': 'IND',  'stock': 'H'},
        2: {'institution': 'IND',  'stock': 'L'},
        3: {'institution': 'POOL', 'stock': 'H'},
        4: {'institution': 'POOL', 'stock': 'L'},
        5: {'institution': 'VOTE', 'stock': 'H'},
        6: {'institution': 'VOTE', 'stock': 'L'},
    }

    # 页面上显示 / ページ上の表示
    STOCK_LABELS = {
        'H': '広い漁場',
        'L': '狭い漁場',
    }
    STOCK_B = {
        'H': B_HIGH,
        'L': B_LOW,
    }

    # フェーズ表示用の日本語辞書を追加
    PHASE_DISPLAY = {
        'practice': '練習',
        'official': '本番',
    }

       
class Subsession(BaseSubsession):
    mode_type   = models.StringField(initial='')
    mode_index  = models.IntegerField(initial=0)
    mode_round  = models.IntegerField(initial=0)
    institution = models.StringField(initial=C.DEFAULT_INSTITUTION)
    stock       = models.StringField(initial=C.DEFAULT_STOCK_SYMBOL)
    import random

def creating_session(self):
    ##print(f"=== creating_session triggered for round {self.round_number} ===")
    r = self.round_number

    # ラウンドタイプ設定：練習 or 本番
    if r <= C.PRACTICE_ROUNDS:
        idx = r
        pattern = C.PRACTICE_PATTERNS[idx]
        self.mode_type  = 'practice'
        self.mode_index = idx
        self.mode_round = 1
    else:
        off_r = r - C.PRACTICE_ROUNDS
        block_size = C.OFFICIAL_ROUNDS // len(C.OFFICIAL_PATTERNS)
        idx = ((off_r - 1) // block_size) + 1
        pattern = C.OFFICIAL_PATTERNS[idx]
        self.mode_type  = 'official'
        self.mode_index = idx
        self.mode_round = ((off_r - 1) % block_size) + 1

    self.institution = pattern['institution']
    self.stock       = pattern['stock']

    ##print(f"Round {r}: mode_type={self.mode_type}, pattern_idx={self.mode_index}, institution={self.institution}, stock={self.stock}")


    # 第1ラウンドのみ：役割を割り当ててparticipant.varsに記録
    if r == 1:
        for group in self.get_groups():
            players = group.get_players()
            # 更稳妥的方法：打乱顺序后分配 / より安全な方法：順序をシャッフルしてから割り当て
            ## random.shuffle(players)
            half = len(players) // 2
            for i, p in enumerate(players):
                is_highliner = (i < half)
                p.participant.vars['is_highliner'] = is_highliner
                print(f"[Round 1 Assignment] Player {p.id_in_group} → {'Highliner' if is_highliner else 'Lowliner'}")

    # 毎ラウンド役割変数を読み戻し
    for p in self.get_players():
        print(f"[DEBUG] p.participant.vars['is_highliner'] = {p.participant.vars.get('is_highliner')}")


class Group(BaseGroup):
    is_pooling   = models.BooleanField(initial=False)
    vote_result  = models.BooleanField(initial=False)
    stock_env    = models.StringField()
    total_H      = models.FloatField()

    def set_institution(self):
        inst = self.subsession.institution
        if inst == 'VOTE':
            # Vote result already calculated in VoteWaitPage, just set is_pooling
            self.is_pooling = self.vote_result
        else:
            self.is_pooling = (inst == 'POOL')
            self.vote_result = False

    def set_payoffs(self):
        players = self.get_players()
        self.stock_env = self.subsession.stock
        H = sum(p.effort for p in players)
        self.total_H = H
        b = C.STOCK_B[self.stock_env]
        for p in players:
            h = p.effort
            c = C.C_1 if p.is_highliner else C.C_2
            pi = h * (C.A - b * H) - c * h**2
            p.payoff_raw = pi
            p.payoff     = pi


class Player(BasePlayer):
    voted_for_pooling = models.BooleanField(blank=True, initial=False)
    effort = models.IntegerField(
        min=0, 
        max=24, 
        choices=[(i, str(i)) for i in range(25)],  # 0から24までの選択肢
        initial=0
    )
    payoff_raw = models.FloatField(initial=0.0)

    @property
    def is_highliner(self):
        return self.participant.vars.get('is_highliner', False)


# PAGES
class Instruction(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'Constants': C
        }

class PracticeEnd(Page):
    """练习结束提示 / 練習終了の通知"""
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.PRACTICE_ROUNDS + 1
    def vars_for_template(self):
        return {'msg': '練習はこれで終了です。本番を開始します！'}  


class Vote(Page):
    form_model = 'player'
    form_fields = ['voted_for_pooling']
    
    @staticmethod
    def is_displayed(player: Player):
        return player.subsession.institution == 'VOTE'

    @staticmethod
    def vars_for_template(player: Player):
        """テンプレートで使用する変数を提供"""
        ss = player.subsession
        return {
            'stock_label': C.STOCK_LABELS[ss.stock],  # テンプレートの {{ stock_label }} 用
            'current_round': ss.round_number,
            'total_rounds': C.NUM_ROUNDS,
            'mode_type_display': C.PHASE_DISPLAY.get(ss.mode_type, ss.mode_type),  # テンプレートの {{ mode_type_display }} 用
            'is_practice': (ss.mode_type == 'practice'),
            'mode_index': ss.mode_index,
            'mode_round': ss.mode_round,
            'institution_for_display': ss.institution,
            'Constants': C,  # テンプレートの {{ Constants.NUM_ROUNDS }} 用
            'subsession': ss,  # テンプレートの {{ subsession.mode_index }} などのために必要
        }


class VoteWaitPage(WaitPage):
    title_text = "Please wait for all players to vote"
    body_text  = "Other players are still voting."
    
    @staticmethod
    def is_displayed(player: Player):
        return player.subsession.institution == 'VOTE'
    
    # Add this method to calculate vote result after voting
    @staticmethod
    def after_all_players_arrive(group: Group):
        if group.subsession.institution == 'VOTE':
            group.vote_result = all(p.voted_for_pooling for p in group.get_players())
            group.is_pooling = group.vote_result
    
    @staticmethod
    def vars_for_template(player: Player):
        """テンプレートで使用する変数を提供"""
        ss = player.subsession
        return {
            'stock_label': C.STOCK_LABELS[ss.stock],  # 辞書ルックアップを事前に解決
            'current_round': ss.round_number,
            'total_rounds': C.NUM_ROUNDS,
            'mode_type_display': C.PHASE_DISPLAY.get(ss.mode_type, ss.mode_type),  # 日本語フェーズ名
            'is_practice': (ss.mode_type == 'practice'),
            'mode_index': ss.mode_index,
            'mode_round': ss.mode_round,
            'institution': ss.institution,
            'Constants': C,  # Constants オブジェクト全体も渡す
        }


class Effort_input(Page):
    form_model = 'player'
    form_fields = ['effort']

    @staticmethod
    def vars_for_template(player: Player):
        ss = player.subsession
        gp = player.group  # Add this line
        # 计算一下是练习阶段还是正式阶段 / 練習段階か本番段階かを計算
        is_practice = (ss.mode_type == 'practice')
        # 首字母大写用于展示 / 表示用に最初の文字を大文字にする
        ##mode_type_display = ss.mode_type.capitalize() if ss.mode_type else ''
        # 日本語表示に変更
        mode_type_display = C.PHASE_DISPLAY.get(ss.mode_type, ss.mode_type)
        # Determine institution display text
        if ss.institution == 'VOTE':
            if gp.vote_result:
                institution_display = "プール制（投票結果：全員賛成）"
            else:
                institution_display = "個人制（投票結果：一部反対）"
        elif ss.institution == 'POOL':
            institution_display = "プール制"
        else:  # IND
            institution_display = "個人制"
        return {
            'stock_label': C.STOCK_LABELS[ss.stock],
            'b': C.B_HIGH if ss.stock == 'H' else C.B_LOW,
            'role': 'Highliner' if player.is_highliner else 'Lowliner',
            'current_round': ss.round_number,
            'total_rounds': C.NUM_ROUNDS,
            'mode_type_display': mode_type_display,  # 用于页面上显示 "Practice" 或 "Official" / ページ上で"Practice"または"Official"を表示するため
            'is_practice': is_practice,              # 用于模板里的 if 判断 / テンプレート内のif判断用
            'mode_index': ss.mode_index,
            'mode_round': ss.mode_round,
            'institution_for_display': institution_display,
            'is_highliner': player.is_highliner,
            'vote_result': gp.vote_result if ss.institution == 'VOTE' else None,  # Add this for template use
        }


class EffortWaitPage(WaitPage):
    title_text = "Waiting for all to input efforts"
    body_text  = "Other players are still inputting their efforts."
    @staticmethod
    def after_all_players_arrive(group: Group):
        group.set_institution()
        group.set_payoffs()


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        gp = player.group
        ss = player.subsession

        # 练习/正式 判断 / 練習/本番 判定
        is_practice = (ss.mode_type == 'practice')
        # 首字母大写的 Phase 文本 / 最初の文字を大文字にしたPhaseテキスト
        ##mode_type_display = ss.mode_type.capitalize() if ss.mode_type else ''
        # 日本語表示に変更
        mode_type_display = C.PHASE_DISPLAY.get(ss.mode_type, ss.mode_type)
        # 每个模式的轮数：练习=1，正式=OFFICIAL_ROUNDS/6=7 / 各モードのラウンド数：練習=1、本番=OFFICIAL_ROUNDS/6=7
        pattern_length = 1 if is_practice else C.OFFICIAL_ROUNDS // len(C.OFFICIAL_PATTERNS)
        # 制度表示テキストを決定（投票結果を含む）
        if ss.institution == 'VOTE':
            if gp.vote_result:
                institution_display = "プール制（投票結果：全員賛成）"
            else:
                institution_display = "個人制（投票結果：一部反対）"
        elif ss.institution == 'POOL':
            institution_display = "プール制"
        else:  # IND
            institution_display = "個人制"
        return {
            'stock_env':   C.STOCK_LABELS[gp.stock_env],
            'total_H':     gp.total_H,
            'my_effort':   player.effort,
            'my_payoff':   player.payoff,
            'role':        'Highliner' if player.is_highliner else 'Lowliner',
            'current_round': ss.round_number,
            'total_rounds':  C.NUM_ROUNDS,
            'mode_type_display': mode_type_display,
            'is_practice':      is_practice,
            'mode_index':       ss.mode_index,
            'mode_round':       ss.mode_round,
            'pattern_length':   pattern_length, 
            'institution_for_display': institution_display,  # 追加
            'vote_result': gp.vote_result if ss.institution == 'VOTE' else None,  # 追加（テンプレートで必要な場合）
        
        }


class EndPage(Page):
    """实验结束页 / 実験終了ページ"""
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS
    def vars_for_template(self):
        return {
            'msg': '実験はこれで終了です。ご参加いただきありがとうございました。次に、参加者を対象としたアンケートにお答えください。'
        }


page_sequence = [
    Instruction,
    PracticeEnd,
    Vote,
    VoteWaitPage,
    Effort_input,
    EffortWaitPage,
    Results,
    EndPage,
]