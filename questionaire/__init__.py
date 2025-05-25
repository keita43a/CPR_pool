from otree.api import *


doc = """
実験終了後の参加者アンケート
"""


class C(BaseConstants):
    NAME_IN_URL = 'questionnaire'
    PLAYERS_PER_GROUP = None
    # 一人のときはNoneを記述する
    NUM_ROUNDS = 1
    # 質問は1度だけ


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    q_gender = models.CharField(initial = None,
                                choices = ['男性','女性','その他','回答を回避'],
                                verbose_name = 'あなたの性別を以下よりお選びください。',
                                widget = widgets.RadioSelect)
    # ラジオボランを使うときはwidget = widgets.RadioSelectを記述する

    q_age = models.IntegerField(Initial = None, 
                                verbose_name = 'あなたの年齢を教えて下さい',
                                choices = range(18,100)
                                )
    # 数字の場合は"choices"を使うことで範囲をしてできる
    # 18 <= q_age < 100 になるので、表示される値は 最小値は0, 最大値は99

    q_degree = models.CharField(initial = None,
                              choices = ['学士','修士','博士（課程修了を含む）','その他',
                                         '回答を回避'],
                            verbose_name = 'あなたが現在在籍しているか、修了した学位の最高位をお選びください。'
                            )
    
    q_degree2 = models.StringField(initial = None,
                                   blank=True, 
                                   verbose_name = 'あなたが現在在籍しているか、修了した学位の専攻をお答えください。（回答回避の場合は次へ進んでください。）')
    
    q_tsuri1 = models.CharField(initial = None,
                                blank=True,
                                  choices = ['はい','いいえ','回答を回避'],
                                  verbose_name = 'あなた自身、漁業や遊漁・釣りなどの経験や関わりがある又は過去にありましたか。',
                                  widget = widgets.RadioSelect
                                  )
    
    q_tsuri2 = models.CharField(initial = None,
                                blank=True,
                                  choices = ['はい','いいえ','回答を回避'],
                                  verbose_name = 'あなたのご家族に、漁業や遊漁・釣りなどの経験や関わりがある又は過去にあった方はいますか。',
                                  widget = widgets.RadioSelect
                                  )
    q_tryad1 = models.CharField(initial = None,
                                blank=True,
                                   choices = ['カモメ','空','犬'],
                                   verbose_name = '次の３つの言葉の中で、仲間外れだと思うものを一つだけお選びください。正解・不正解はありませんので感じたとおりにお答えください。',
                                   widget = widgets.RadioSelect
    )
    q_tryad2 = models.CharField(initial = None,
                                blank=True,
                                   choices = ['黒','白','青'],
                                   verbose_name = '次の３つの言葉の中で、仲間外れだと思うものを一つだけお選びください。**正解・不正解はありませんので感じたとおりにお答えください**。',
                                   widget = widgets.RadioSelect
    )

    q_tryad3 = models.CharField(initial = None,
                                blank=True,
                                   choices = ['医者','教師','宿題'],
                                   verbose_name = '次の３つの言葉の中で、仲間外れだと思うものを一つだけお選びください。**正解・不正解はありませんので感じたとおりにお答えください**。',
                                   widget = widgets.RadioSelect
    )

    q_tryad4 = models.CharField(initial = None,
                                blank=True,
                                   choices = ['りんご','オレンジ','洋子'],
                                   verbose_name = '次の３つの言葉の中で、仲間外れだと思うものを一つだけお選びください。**正解・不正解はありませんので感じたとおりにお答えください**。',
                                   widget = widgets.RadioSelect
    )

    q_tryad5 = models.CharField(initial = None,
                                blank=True,
                                   choices = ['靴','ブーツ','スリッパ'],
                                   verbose_name = '次の３つの言葉の中で、仲間外れだと思うものを一つだけお選びください。**正解・不正解はありませんので感じたとおりにお答えください**。',
                                   widget = widgets.RadioSelect
    )

    q_tryad6 = models.CharField(initial = None,
                                blank=True,
                                   choices = ['電車','バス','線路'],
                                   verbose_name = '次の３つの言葉の中で、仲間外れだと思うものを一つだけお選びください。**正解・不正解はありませんので感じたとおりにお答えください**。',
                                   widget = widgets.RadioSelect
    )

    q_tryad7 = models.CharField(initial = None,
                                blank=True,
                                   choices = ['インピーダンス','アンテナ','テレビ'],
                                   verbose_name = '次の３つの言葉の中で、仲間外れだと思うものを一つだけお選びください。**正解・不正解はありませんので感じたとおりにお答えください**。',
                                   widget = widgets.RadioSelect
    )

    q_tryad8 = models.CharField(initial = None,
                                blank=True,
                                   choices = ['病院','銀行','映画館'],
                                   verbose_name = '次の３つの言葉の中で、仲間外れだと思うものを一つだけお選びください。**正解・不正解はありませんので感じたとおりにお答えください**。',
                                   widget = widgets.RadioSelect
    )

    q_tryad9 = models.CharField(initial = None,
                                blank=True,
                                   choices = ['にんじん','なす','ウサギ'],
                                   verbose_name = '次の３つの言葉の中で、仲間外れだと思うものを一つだけお選びください。**正解・不正解はありませんので感じたとおりにお答えください**。',
                                   widget = widgets.RadioSelect
    )

    q_tryad10 = models.CharField(initial = None,
                                 blank=True,
                                    choices = ['警','馬','雨'],
                                    verbose_name = '次の３つの言葉の中で、仲間外れだと思うものを一つだけお選びください。**正解・不正解はありませんので感じたとおりにお答えください**。',
                                    widget = widgets.RadioSelect
    )

    q_tryad11 = models.CharField(initial = None,
                                    blank=True,
                                    choices = ['パンダ','バナナ','サル'],
                                    verbose_name = '次の３つの言葉の中で、仲間外れだと思うものを一つだけお選びください。**正解・不正解はありませんので感じたとおりにお答えください**。',
                                    widget = widgets.RadioSelect
    )

    q_tryad12 = models.CharField(initial = None,
                                    blank=True,
                                    choices = ['シャツ','帽子','ズボン'],
                                    verbose_name = '次の３つの言葉の中で、仲間外れだと思うものを一つだけお選びください。**正解・不正解はありませんので感じたとおりにお答えください**。',
                                    widget = widgets.RadioSelect
    )

    q_tryad13 = models.CharField(initial = None,
                                    blank=True,
                                    choices = ['風','バスケ','テニス'],
                                    verbose_name = '次の３つの言葉の中で、仲間外れだと思うものを一つだけお選びください。**正解・不正解はありませんので感じたとおりにお答えください**。',
                                    widget = widgets.RadioSelect
    )

    q_tryad14 = models.CharField(initial = None,
                                    blank=True,
                                    choices = ['農夫','トウモロコシ','パン'],
                                    verbose_name = '次の３つの言葉の中で、仲間外れだと思うものを一つだけお選びください。**正解・不正解はありませんので感じたとおりにお答えください**。',
                                    widget = widgets.RadioSelect
    )

    q_tryad15 = models.CharField(initial = None,
                                    blank=True,
                                    choices = ['シャンプー','髪','ひげ'],
                                    verbose_name = '次の３つの言葉の中で、仲間外れだと思うものを一つだけお選びください。**正解・不正解はありませんので感じたとおりにお答えください**。',
                                    widget = widgets.RadioSelect
    )

    q_tryad16 = models.CharField(initial = None,
                                    blank=True,
                                    choices = ['橋','トンネル','高速道路'],
                                    verbose_name = '次の３つの言葉の中で、仲間外れだと思うものを一つだけお選びください。**正解・不正解はありませんので感じたとおりにお答えください**。',
                                    widget = widgets.RadioSelect
    )

    q_tryad17 = models.CharField(initial = None,
                                    blank=True,
                                    choices = ['ピアノ','バイオリン','ギター'],
                                    verbose_name = '次の３つの言葉の中で、仲間外れだと思うものを一つだけお選びください。**正解・不正解はありませんので感じたとおりにお答えください**。',
                                    widget = widgets.RadioSelect
    )

    q_tryad18 = models.CharField(initial = None,
                                    blank=True,
                                    choices = ['子ども','男','女'],
                                    verbose_name = '次の３つの言葉の中で、仲間外れだと思うものを一つだけお選びください。**正解・不正解はありませんので感じたとおりにお答えください**。',
                                    widget = widgets.RadioSelect
    )

    q_tryad19 = models.CharField(initial = None,
                                    blank=True,
                                    choices = ['郵便配達員','警官','制服'],
                                    verbose_name = '次の３つの言葉の中で、仲間外れだと思うものを一つだけお選びください。**正解・不正解はありませんので感じたとおりにお答えください**。',
                                    widget = widgets.RadioSelect
    )

    q_tryad20 = models.CharField(initial = None,
                                    blank=True,
                                    choices = ['手紙','明子','はがき'],
                                    verbose_name = '次の３つの言葉の中で、仲間外れだと思うものを一つだけお選びください。**正解・不正解はありませんので感じたとおりにお答えください**。',
                                    widget = widgets.RadioSelect
    )

    q_comment = models.LongStringField(initial = None,
                                       blank=True,
                                       verbose_name = '今回の実験やこのアンケートに関する感想や漁業管理についての所見などご自由にご記入ください。特に何もなければ空欄のままで構いません。')

# PAGES
class Page1(Page):
    form_model = 'player'
    # 各フィールドはplayerクラスで定義されている
    form_fields = [
        'q_gender','q_age','q_degree','q_degree2','q_tsuri1','q_tsuri2'
    ]
    #質問項目は４つある

class Page2(Page):
    form_model = 'player'
    # 各フィールドはplayerクラスで定義されている
    form_fields = [
        'q_tryad1',
        'q_tryad2',
        'q_tryad3',
        'q_tryad4',
        'q_tryad5',
        'q_tryad6',
        'q_tryad7',
        'q_tryad8',
        'q_tryad9',
        'q_tryad10',
        'q_tryad11',
        'q_tryad12',
        'q_tryad13',
        'q_tryad14',
        'q_tryad15',
        'q_tryad16',
        'q_tryad17',
        'q_tryad18',
        'q_tryad19',
        'q_tryad20',
        'q_comment'
    ]

class Page3(Page):
    form_model = 'player'
    # 各フィールドはplayerクラスで定義されている
    form_fields = [
        'q_comment'
    ]

class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [Page1,Page2,Page3]
