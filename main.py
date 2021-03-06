"""Analyzing & identifying fraudulent calls"""

import jieba
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import pandas as pd
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn import metrics
from sklearn.model_selection import train_test_split, cross_val_score
import numpy as np
from sklearn.tree import DecisionTreeClassifier, plot_tree
from matplotlib import pyplot as plt


# Import Chinese stopwords
file_name = 'cn_stopwords.csv'
sw_file = pd.read_csv(file_name, header=None, names=['words'])
stop_words = list(sw_file['words'])


# The function cuts sentences into separated words
def cut_word(text):
    return ' '.join(list(jieba.cut(text)))


# Create fraudulent dataset
X_zp = [
    '区块链应用场景落地币躺着也能赚大钱',
    '您的信用额度不够需要刷流水请缴纳现金证明还款能力',
    '某金融服务已经被国家下架需要您配合注销信贷账户否则将影响个人征信',
    '亲爱的我有个发大财的机会',
    '您的审核流程还未完成请点击以下链接尽快完成',
    '加微信躺着都能赚钱',
    '回馈粉丝给我发红包我三倍返还',
    '办理各类职称证书不用考试直接拿证',
    '免费送活动真实有效',
    '招聘快手抖音点赞员',
    '明天来我办公室一趟',
    '外公家的茶叶滞销了可以帮忙买一点吗',
    '你的快递丢了我们将进行双倍赔偿',
    '免费提供长期贷款无担保',
    '您的银行账户涉嫌洗钱',
    '教大家一个网上日赚元的方法手机在家就可以做的兼职',
    '您的微信需要二次实名认证',
    '推荐股票稳赚不赔',
    '低价出售游戏币',
    '加微信先付款马上安排优先发货',
    '最后的额温枪想要先转钱',
    '我都脱了你一个大男人怕什么',
    '学费还没缴的家长请尽快缴费',
    '疫情之下您缺钱金融给您授信100000额度',
    '做任务发旺旺发真实快递垫付元左右佣金立返元',
    '你如果迟到或者瞒报信息就要负刑事责任',
    '你跟北京市公安局联系一下看看是不是身份信息被泄露了我可以通过内部电话帮你接通',
    '你涉及一桩跨国洗钱案主犯叫你跟她有合作通过中国人民银行在北京办理的账户给她洗了钱你有洗钱的嫌疑',
    '跟洗钱案件有关需要请示一下领导如何处理保密协议引渡条款生效快写保证书财产清查报告',
    '往中国工商银行的账户里转账',
    '你在拼多多上多多果园种植的水果到不了了我是理赔公司的人可以办理退赔并且双倍退赔支付宝账号二维码输入姓名身份证号银行卡号验证码',
    '这笔款到了没有我是公司的黄经理你往台州市工程机械租赁有限公司的对公账户转20000元',
    '微信绑定银行卡替我转给朋友3800元朋友的姐姐住院二维码',
    '理财软件一直在理财微信二维码小程序理财官网赚钱只赚不赔大额提现充钱到达黄金段位',
    '支付宝软件里面刷单不需要自己垫付资金每一单可以盈利20到30元扫描二维码使用花呗付款二维码身份验证二维码付款',
    '这边是客服的没有收到您的邀请',
    '我跟你说的让你注销你的学生贷信息你怎么没有添加通过认证呢',
    '我是网贷平台的客服人员',
    '根据国家相关政策需要你配合注销账号否则会影响个人征信',
    '你的身份信息被盗用有人用你的身份证注册了网贷账号有贷款记录甚至未还清需要配合注销否则会影响个人征信',
    '我掌握赌博理财后台跟着做能赚钱',
    '兼职做任务日赚500元',
    '你涉嫌犯罪尽快将资金转入安全账户接受资金审查',
    '需要缴纳手续费工本费公证费服务费',
    '恭喜您升级成网商至尊钻石会员每年缴纳会员费7200元'
    '推荐股票，稳赚不赔',
    '你给公司总联系一下需要转一笔款',
    '你到银行以后按照我的提示或语音提示进行操作不能挂断电话',
    '你先开通登录网上银行然后再下载软件插上优盾',
    '请你登录网站查看最高人民法院最高人民检察院下达的通缉令',
    '这是公安局法院检察院的电话如果你怀疑的话可以拨查询',
    '你必须把存款转入部门在银行开设的安全账户监管账户',
    '我是网店的客服您的订单由于故障卡单了请登录淘宝异常支付处理中心',
    '我是教育局医院民政局的你有学费补助新生儿殡葬费补贴',
    '本集团向小微企业提供优惠贷款有意者请致电',
    '我是交管局的你的车国庆节期间有违章记录需要向账户汇款',
    '低价出售装备',
    '超值额度做任务立返10元',
    '免费提供佣金贷款无压力',
    '跟我投资股票，一定能赚, 我能操控后台，稳赚不赔',
    '我行优质信贷，低风险高收益，有贷款需求吗',
    '我是360网贷客服，你有一笔资金要到账了，扫一下我的二维码',
    '你的信用卡被盗刷，现在需要往这个卡里打钱来解冻',
    '你的姐姐出车祸住院了，你现在微信上给我转5000块钱',
    '你的身份信息被盗用，涉嫌洗钱，现已被公安机关传唤',
    '招聘刷单员，20块一单，立刻提现'
]

# Create non-fraudulent dataset
X_fzp = [
    '我今天不回家吃饭了',
    '面试不错阿里巴巴的领导很好',
    '但这几天李开复领衔讨伐节目组网上民意汹汹',
    '范加江驾驶收割机在收获小麦',
    '德国对荷兰的比赛将在乌克兰的哈尔科夫进行',
    '一位疑似脸谱网站创始人扎克伯格的群众演员成最大牌的'
    '除此之外扎实推进农村益民书屋流动文化服务进农村进社区等文化惠民工程落到实处保障基层特别是偏远地区群众的基本文化权益',
    '朝鲜国防委员会第一委员长金正恩为他们自安排的宴会',
    '中央企业的改革发展依旧取得了很大成绩经营管理水平也有所提高',
    '根据该规定上市公司停牌进入重大资产重组程序后证券交易所将立即启动股票异常交易核查程序并及时将股票异常交易信息上报证监会',
    '今日两市成交额并未出现大幅放大，截至收盘沪市成交额八百六十九亿元',
    '回去微信联系现在坐车回家不方便打电话',
    '今天吃饭的钱我回去转给你吧',
    '其中三人被送往医院救治路易斯安那州新奥尔良市的一名儿童上周死亡',
    '瑞信亚洲区首席经济学家陶冬表示欧债危机的恶化将带来全球央行的新一轮量化',
    '根据方案，恒泰艾普拟以每股元的价格向标的公司各股东定向发行股票，合计六百九十九万股',
    '各地方各部门在安排创业投资引导基金时对于在中国境内设立依照国家有关规定备案',
    '包括民间投资在内的各类创业投资企业均可以采用参股融资担保和跟进投资等方式进行扶持',
    '有关人士表示从东北来看随着老工业基地进入全面振兴的新阶段迫切需要一个功能强辐射作用大的新引擎来带动',
    '需要一个改革开放基础好的地区率先探索转变发展方式和产业优化升级的新模式为东北老工业基地科学发展积累新经验为东北全面振兴提供强大动力和服务保障',
    '今天有很多学习任务需要一起努力',
    '证监会近日召开新闻通气会，就《关于加强与上市公司重大资产重组相关股票异常交易监管的暂行规定（征求意见稿）》向社会公开征求意见。',
    '根据该规定，上市公司停牌进入重大资产重组程序后，证券交易所将立即启动股票异常交易核查程序，并及时将股票异常交易信息上报证监会',
    '今日两市成交额并未出现大幅放大，截至收盘沪市成交额８６９亿元，'
    '与沪综指全日近６４点的下跌幅度，以及击穿重要技术支撑位的走势并不相称，显示下方承接盘不多',
    '战士围攻“敌对武装分子”。昨晚，酒泉卫星发射基地，军方进行了演习，假想对象为持有重火力的武装分子，目标是保卫神九正常发射',
    '张欣表示，事件发生后，对海天公司的销售和品牌都造成了很大的影响',
    '黎巴嫩北部港口城市的黎波里持续达一天之久的支持叙利亚总统巴沙尔的阿拉维派武装分子和反对巴沙尔的逊尼派武装'
    '分子的激烈交火已经造成至少１２人死亡，４９人受伤',
    '今天有很多学习',
    '为推进自由贸易区谈判提供有力支撑',
    '今天天气晴朗',
    '钥匙落在家里忘记带了，应该是在昨天的衣服口袋里面',
    '坐公交车回家应该会很方便，走回去太慢了',
    '今天早上下了很大的雨，衣服都淋湿了',
    '我先去商店等你，不着急，你慢慢骑车过来就行',
    '明天一起出去玩吧，一起去商场吃饭打球',
    '晚上要加班，不回家吃饭了，加完班坐公交车回去',
    '我一会去超市买点东西，顺便交水费',
    '夫妻俩各自分工，丈夫收割，妻子负责量地、看路、买油、替农户装粮袋等。忙的时候，一天能收割６０多亩，一个麦季下来能挣２万多元',
    '除了这个中心舞台外，还建设有古香古色的博物馆、村级阅览室、活动室等，每到夏天都会有很多演出',
    '在这个狂暴的热区，巨大的阿拉伯板块正从一个新的裂缝处被挤走，这个裂缝将非洲板块一分为二',
    '据黎巴嫩《每日星报》报道，黎巴嫩北部港口城市的黎波里持续达一天之久的支持叙利亚总统巴沙尔的阿拉维派武装分子'
    '和反对巴沙尔的逊尼派武装分子的激烈交火已经造成至少12人死亡，49人受伤',
    '野田在新闻发布会上说，改组内阁的目的是为了建立有利于社会保障与税制一体化改革相关法案获得国会通过的环境',
    '发生事故的是南安水头一座在建的高架桥，因在作业时突然发生倾覆，大型的钢制架桥机连同梁体一同翻落，'
    '不仅砸中桥下的何先生，还导致一名在10米高空作业的工人坠落',
    '今年以来，受到“鼓励刚需”的政策支持，商业银行首套房贷利率连续下滑，从年前的基准利率1.1倍降至目前的8.5折优惠',
    '华兴银行工作人员向记者证实了这一消息，但其表示，由于银行网点少，购买北京房产无法办理相关贷款，目前只办理广州市或汕头的业务',
    '该大棚用于土豆种植基地，由于承包人经营管理不善效益较差，导致无法经营',
    '记者昨天拨打汤灿本人的电话，其电话处于关机状态，随后记者联系到了她的私人助理小草，她给出了否认答案，“我现在可以告诉你，消息是假的',
    '晚上和同学一起去打羽毛球，晚点回家',
    '手机充电线还在单位没拿，你帮我捎过来吧，或者我回去拿',
    '最近学习挺紧张的，老师布置了很多作业，然后也快考试了',
    '下周要出具一个报告，这两天得加班，最近工作比较忙',
    '我刚到楼下，是不是来早了，你收拾好就下来吧，我在下面等你',
    '他找了一份新工作，就在你家附近，每天开车上班，单位给提供停车位，挺方便的',
    '博物馆挺好玩的，下次咱们一起去吧，叫上你那几个朋友，然后去吃饭打牌',
    '今天特别堵车，才刚走到山大路，前面好像是有事故，来了好多警察',
    ''
]

# Arrange them into X, y
X = X_zp + X_fzp
y = [1] * len(X_zp) + [0] * len(X_fzp)

"""Investigate the mean/std of accuracy scores"""

# iterations = 100
#
# total_scores = []
# for iteration in range(iterations):
#     bnb = BernoulliNB(alpha=1e-8)
#     mnb = MultinomialNB()
#     knn = KNeighborsClassifier()
#     lr = LogisticRegression()
#     rfc = RandomForestClassifier()
#     abc = AdaBoostClassifier(n_estimators=100)
#     gbc = GradientBoostingClassifier()
#     dtc = DecisionTreeClassifier()
#     algorithms = [dtc]
#
#     vect = CountVectorizer(stop_words=stop_words)
#
#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
#
#     X_train_cut = []
#     for data in X_train:
#         data_cut = cut_word(data)
#         X_train_cut.append(data_cut)
#
#     X_train_counts = vect.fit_transform(X_train_cut)
#
#     tfidf = TfidfTransformer()
#     X_train_tfidf = tfidf.fit_transform(X_train_counts)
#
#     X_test_cut = []
#     for data in X_test:
#         X_test_cut.append(cut_word(data))
#
#     X_test_counts = vect.transform(X_test_cut)
#     X_test_tfidf = tfidf.transform(X_test_counts)
#
#     scores = []
#     for algorithm in algorithms:
#         algorithm.fit(X_train_tfidf, y_train)
#         pred = algorithm.predict(X_test_tfidf)
#         # print(y_test)
#         # print(list(pred))
#         # print(algorithm.predict_proba(X_test_tfidf))
#         score = metrics.accuracy_score(y_test, pred)
#         scores.append(score)
#
#     total_scores.append(scores)
#
# total_scores_df = pd.DataFrame(total_scores)
# means = []
# stds = []
# for col_name in range(len(algorithms)):
#     means.append(np.mean(total_scores_df[col_name]))
#     stds.append(np.std(total_scores_df[col_name]))
#
# print(means)
# print(stds)

"""Apply to new data"""

vect = CountVectorizer(stop_words=stop_words)
tfidf = TfidfTransformer()
bnb = BernoulliNB(alpha=1e-8)
mnb = MultinomialNB()
knn = KNeighborsClassifier()
lr = LogisticRegression()
rfc = RandomForestClassifier()


def predict(texts, algorithm=bnb):
    if isinstance(texts, str):
        texts = [texts]
    X_cut = []
    for data in X:
        data_cut = cut_word(data)
        X_cut.append(data_cut)
    X_counts = vect.fit_transform(X_cut)
    X_tfidf = tfidf.fit_transform(X_counts)
    algorithm.fit(X_tfidf, y)
    texts_cut = []
    for text in texts:
        text_cut = cut_word(text)
        texts_cut.append(text_cut)
    texts_counts = vect.transform(texts_cut)
    texts_tfidf = tfidf.transform(texts_counts)
    pred = algorithm.predict(texts_tfidf)
    pred_prob = algorithm.predict_proba(texts_tfidf)
    pred_text = ''
    for i in range(len(texts)):
        if pred[i] == 1:
            pred_text = 'Fraudulent'
        elif pred[i] == 0:
            pred_text = 'Non fraudulent'
        pred_prob_text = f"Fraudulent probablity: {pred_prob[i][1]}\nNon fradulent probablity: {pred_prob[i][0]}"
        print(pred_text)
        print(pred_prob_text)


pred = predict(['你有一笔贷款即将到帐，请查收', '家里的电脑需要换新的了'])

"""Investigate performance of rfc"""

# X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=10, test_size=0.15)
# rfc = RandomForestClassifier(random_state=10, max_depth=5)
# vect = CountVectorizer()
#
# X_train_cut = []
# for data in X_train:
#     data_cut = cut_word(data)
#     X_train_cut.append(data_cut)
#
# X_train_counts = vect.fit_transform(X_train_cut)
#
# tfidf = TfidfTransformer()
# X_train_tfidf = tfidf.fit_transform(X_train_counts)
#
# X_test_cut = []
# for data in X_test:
#     X_test_cut.append(cut_word(data))
#
# X_test_counts = vect.transform(X_test_cut)
# X_test_tfidf = tfidf.transform(X_test_counts)
#
# rfc.fit(X_train_tfidf, y_train)
# pred = rfc.predict(X_test_tfidf)
# print(metrics.accuracy_score(y_test, pred))
# print(y_test)
# print(list(pred))
# print(rfc.predict_proba(X_test_tfidf))


"""Output texts & labels to csv"""
# file_name_X = 'text.csv'
# file_name_y = 'target.csv'

# with open(file_name_X, 'w', encoding='utf-8-sig') as file:
#     for text in X:
#         file.write(text + '\n')

# with open(file_name_y, 'w') as file:
#     for number in y:
#         file.write(str(number) + '\n')

