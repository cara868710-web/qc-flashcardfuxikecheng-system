import telebot
from telebot import types
import os
import difflib
import re
import unicodedata
from datetime import datetime

# ════════════════════════════════════════════
#   XDS Smart QC Assistant Bot — Version 3.0
# ════════════════════════════════════════════

API_TOKEN = 
TARGET_GROUP_ID = 

bot = telebot.TeleBot(API_TOKEN)

# ════════════════════════════════════════════
#   វចនានុក្រម QC (ក្រុមតាមប្រភេទ)
# ════════════════════════════════════════════
qc_data = [
    # ── ពិការភាព Painting ──
    {"cn": "起泡",         "km": "ពង / ចូលខ្យល់",              "cat": "🎨 Painting",  "img": "images/qipao.jpg"},
    {"cn": "标纸不良",     "km": "តែមមិនល្អ",                  "cat": "🎨 Painting",  "img": "images/biaozhibuliang.jpg"},
    {"cn": "修补痕",       "km": "ស្នាមជួសជុល",                 "cat": "🎨 Painting",  "img": "images/xiubuhen.jpg"},
    {"cn": "杂质",         "km": "ធូលី / កំទេចកំទី",            "cat": "🎨 Painting",  "img": "images/zhazhi.jpg"},
    {"cn": "脏污",         "km": "ប្រឡាក់",                    "cat": "🎨 Painting",  "img": "images/zangwu.jpg"},
    {"cn": "标纸位置不对", "km": "បិទតែមខុសទីតាំង",             "cat": "🎨 Painting",  "img": "images/biaozhiweizhibudui.jpg"},
    {"cn": "标纸不对称",   "km": "បិទតែមមិនស្មើគ្នា",            "cat": "🎨 Painting",  "img": "images/biaozhibuduiceng.jpg"},
    {"cn": "雾面",         "km": "ស្រអាប់",                    "cat": "🎨 Painting",  "img": "images/wumian.jpg"},
    {"cn": "橘皮",         "km": "សំបកក្រូច",                   "cat": "🎨 Painting",  "img": "images/jupi.jpg"},
    {"cn": "针孔",         "km": "រន្ធម្ជុល",                   "cat": "🎨 Painting",  "img": "images/zhengkong.jpg"},
    {"cn": "消光不良",     "km": "ទឹកថ្នាំស្រអាប់មិនល្អ",         "cat": "🎨 Painting",  "img": "images/xiaoguangbuliang.jpg"},
    {"cn": "防漆不良",     "km": "ការពារទឹកថ្នាំមិនបានល្អ",       "cat": "🎨 Painting",  "img": "images/fangqibuliang.jpg"},
    {"cn": "划痕",         "km": "ស្នាមឆ្កូត",                  "cat": "🎨 Painting",  "img": "images/划痕.jpg"},
    {"cn": "掉漆",         "km": "របកថ្នាំ",                   "cat": "🎨 Painting",  "img": "images/掉漆.jpg"},
    {"cn": "喷漆",         "km": "បាញ់ថ្នាំ",                  "cat": "🎨 Painting",  "img": "images/喷漆.jpg"},
    {"cn": "烤漆",         "km": "ដុតថ្នាំ",                   "cat": "🎨 Painting",  "img": "images/烤漆.jpg"},
    {"cn": "打蜡",         "km": "ខាត់ប៉ូលា",                  "cat": "🎨 Painting",  "img": "images/打蜡.jpg"},
    {"cn": "底漆",         "km": "ថ្នាំទ្រនាប់ /ថ្នាំបាត",       "cat": "🎨 Painting",  "img": "images/底漆.jpg"},
    {"cn": "面漆",         "km": "ថ្នាំពណ៌/ថ្នាំពណ៌បង្ហើយ",      "cat": "🎨 Painting",  "img": "images/面漆.jpg"},
    {"cn": "附着力",       "km": "កម្លាំងស្អិតជាប់",             "cat": "🎨 Painting",  "img": "images/附着力.jpg"},
    {"cn": "色差",         "km": "ខុសពណ៌",                    "cat": "🎨 Painting",  "img": "images/色差.jpg"},
    {"cn": "透底",         "km": "ឃើញពណ៌បាត",                 "cat": "🎨 Painting",  "img": "images/透底.jpg"},
    {"cn": "流挂",         "km": "ហៀរថ្នាំ",                   "cat": "🎨 Painting",  "img": "images/流挂.jpg"},
    {"cn": "颗粒",         "km": "គ្រាប់ខ្សាច់ / ធូលី",          "cat": "🎨 Painting",  "img": "images/颗粒.jpg"},
    {"cn": "溶剂",         "km": "ទឹកលាយថ្នាំ",                "cat": "🎨 Painting",  "img": "images/溶剂.jpg"},
    {"cn": "贴花",         "km": "បិទតែមទឹក",                  "cat": "🎨 Painting",  "img": "images/贴花.jpg"},

    # ── ពិការភាព Welding ──
    {"cn": "开裂",         "km": "ប្រេះ (Crack)",               "cat": "🔧 Welding",   "img": "images/kailie.jpg"},
    {"cn": "焊破",         "km": "ផ្សារធ្លុះ",                  "cat": "🔧 Welding",   "img": "images/hanpo.jpg"},
    {"cn": "漏焊",         "km": "ភ្លេចផ្សារ",                  "cat": "🔧 Welding",   "img": "images/louhan.jpg"},
    {"cn": "针眼",         "km": "ភ្នែកម្ជុល",                  "cat": "🔧 Welding",   "img": "images/zhenyan.jpg"},
    {"cn": "凹陷",         "km": "កំពិត / ផត",                  "cat": "🔧 Welding",   "img": "images/aoxian.jpg"},
    {"cn": "焊道偏心",     "km": "ផ្សារវៀច",                    "cat": "🔧 Welding",   "img": "images/handaobianxin.jpg"},
    {"cn": "电击伤",       "km": "ឆេះម៉ាស",                    "cat": "🔧 Welding",   "img": "images/dianjishang.jpg"},
    {"cn": "堆焊",         "km": "ផ្សារទូល (Overlap)",           "cat": "🔧 Welding",   "img": "images/duihan.jpg"},
    {"cn": "咬边",         "km": "ស៊ីសាច់បំពង់",                "cat": "🔧 Welding",   "img": "images/yaobian.jpg"},
    {"cn": "间隙",         "km": "ចន្លោះ / ហើប",               "cat": "🔧 Welding",   "img": "images/jianxi.jpg"},
    {"cn": "焊渣",         "km": "កំទេចផ្សារ",                  "cat": "🔧 Welding",   "img": "images/hanzha.jpg"},

    # ── ពិការភាព Assembly ──
    {"cn": "碰刮伤",       "km": "ប៉ះទង្គិច / កោស",             "cat": "🔩 Assembly",  "img": "images/pengguashang.jpg"},
    {"cn": "刹车失灵",     "km": "ហ្វ្រាំងមិនស៊ី",              "cat": "🔩 Assembly",  "img": "images/刹车失灵.jpg"},
    {"cn": "变速不准",     "km": "ដូរលេខមិនចូល",                "cat": "🔩 Assembly",  "img": "images/变速不准.jpg"},
    {"cn": "轮胎漏气",     "km": "សំបកកង់ធ្លាយ",                "cat": "🔩 Assembly",  "img": "images/轮胎漏气.jpg"},
    {"cn": "螺丝松动",     "km": "ខ្ចៅធូរ",                    "cat": "🔩 Assembly",  "img": "images/螺丝松动.jpg"},
    {"cn": "异响",         "km": "សំឡេងរំខាន",                 "cat": "🔩 Assembly",  "img": "images/异响.jpg"},
    {"cn": "生锈",         "km": "ច្រែះ",                      "cat": "🔩 Assembly",  "img": "images/生锈.jpg"},
    {"cn": "错件",         "km": "ដាក់គ្រឿងខុស",               "cat": "🔩 Assembly",  "img": "images/错件.jpg"},
    {"cn": "漏装",         "km": "ភ្លេចដាក់គ្រឿង",             "cat": "🔩 Assembly",  "img": "images/漏装.jpg"},
    {"cn": "歪斜",         "km": "វៀច / មិនត្រង់",             "cat": "🔩 Assembly",  "img": "images/歪斜.jpg"},
    {"cn": "返工",         "km": "ធ្វើឡើងវិញ / កែឡើងវិញ",       "cat": "🔩 Assembly",  "img": "images/返工.jpg"},

    # ── គ្រឿងបន្លាស់ ──
    {"cn": "车架",         "km": "តួកង់",                      "cat": "🚲 Parts",     "img": "images/chejia.jpg"},
    {"cn": "前叉",         "km": "ឆ្ពោះមុខ (Fork)",             "cat": "🚲 Parts",     "img": "images/qiancha.jpg"},
    {"cn": "车把",         "km": "ដៃកង់",                      "cat": "🚲 Parts",     "img": "images/cheba.jpg"},
    {"cn": "车圈",         "km": "ខ្នងកង់",                    "cat": "🚲 Parts",     "img": "images/chequan.jpg"},
    {"cn": "外胎",         "km": "សំបកកង់",                    "cat": "🚲 Parts",     "img": "images/waitai.jpg"},
    {"cn": "脚踏",         "km": "ឈ្នាន់",                     "cat": "🚲 Parts",     "img": "images/jiaota.jpg"},
    {"cn": "链条",         "km": "ច្រវាក់",                    "cat": "🚲 Parts",     "img": "images/liantiao.jpg"},
    {"cn": "座垫",         "km": "កែប",                        "cat": "🚲 Parts",     "img": "images/zuodian.jpg"},
    {"cn": "刹车",         "km": "ហ្វ្រាំង",                   "cat": "🚲 Parts",     "img": "images/shache.jpg"},

    # ── ម៉ែត្រ QC ──
    {"cn": "测量值",       "km": "តម្លៃវាស់ជាក់ស្តែង",           "cat": "📏 QC Metrics","img": "images/celiangzhi.jpg"},
    {"cn": "标准值",       "km": "តម្លៃស្តង់ដា",                "cat": "📏 QC Metrics","img": "images/biaozhunzhi.jpg"},
    {"cn": "上限",         "km": "ដែនកំណត់ លើ",                "cat": "📏 QC Metrics","img": "images/shangxian.jpg"},
    {"cn": "下限",         "km": "ដែនកំណត់ ក្រោម",             "cat": "📏 QC Metrics","img": "images/xiaxian.jpg"},
    {"cn": "趋势图",       "km": "ក្រាបនិន្នាការ",              "cat": "📏 QC Metrics","img": "images/qushitu.jpg"},
    {"cn": "合格",         "km": "ជាប់ (OK)",                   "cat": "📏 QC Metrics","img": "images/hege.jpg"},
    {"cn": "不合格",       "km": "ធ្លាក់ (NG)",                 "cat": "📏 QC Metrics","img": "images/buhege.jpg"},

    # ── ឧបករណ៍ ──
    {"cn": "扳手",         "km": "សោ",                         "cat": "🛠 Tools",     "img": "images/扳手.jpg"},
    {"cn": "内六角",       "km": "សោ6ជ្រុង / សោតាន់",          "cat": "🛠 Tools",     "img": "images/内六角.jpg"},
    {"cn": "螺丝刀",       "km": "ទួរណឺវីស",                   "cat": "🛠 Tools",     "img": "images/螺丝刀.jpg"},
    {"cn": "游标卡尺",     "km": "ម៉ែគាបនាឡិការ",              "cat": "🛠 Tools",     "img": "images/游标卡尺.jpg"},
    {"cn": "卷尺",         "km": "ម៉ែត្រខ្សែ",                 "cat": "🛠 Tools",     "img": "images/卷尺.jpg"},
    {"cn": "扭力扳手",     "km": "សោតរឹតកម្លាំងខ្ចៅ",           "cat": "🛠 Tools",     "img": "images/扭力扳手.jpg"},
    {"cn": "电钻",         "km": "ម៉ូទ័រស្វាន",                "cat": "🛠 Tools",     "img": "images/电钻.jpg"},
    {"cn": "气枪",         "km": "កាំភ្លើងខ្យល់",              "cat": "🛠 Tools",     "img": "images/气枪.jpg"},
    {"cn": "叉车",         "km": "អេឡេវ៉ាទ័រ",                 "cat": "🛠 Tools",     "img": "images/叉车.jpg"},
    {"cn": "焊枪",         "km": "ក្បាលផ្សា",                  "cat": "🛠 Tools",     "img": "images/焊枪.jpg"},
    {"cn": "焊条",         "km": "ធូបផ្សារ",                   "cat": "🛠 Tools",     "img": "images/焊条.jpg"},
    {"cn": "氩气",         "km": "ឧស្ម័នអាកុង",                "cat": "🛠 Tools",     "img": "images/氩气.jpg"},

    # ── ប្រតិបត្តិការ ──
    {"cn": "锁紧",         "km": "រឹតតឹង",                     "cat": "⚙️ Operations","img": "images/锁紧.jpg"},
    {"cn": "拆卸",         "km": "ដោះចេញ / រុះរើ",             "cat": "⚙️ Operations","img": "images/拆卸.jpg"},
    {"cn": "校正",         "km": "កែតម្រូវ / ពត់",             "cat": "⚙️ Operations","img": "images/校正.jpg"},
    {"cn": "打磨",         "km": "ខាត់ / ប៉ូលើ",               "cat": "⚙️ Operations","img": "images/打磨.jpg"},
    {"cn": "点焊",         "km": "ផ្សារភ្ជាប់",                "cat": "⚙️ Operations","img": "images/点焊.jpg"},
    {"cn": "满焊",         "km": "ផ្សារពេញ",                   "cat": "⚙️ Operations","img": "images/满焊.jpg"},

    # ── ទូទៅ ──
    {"cn": "工厂",         "km": "រោងចក្រ",                    "cat": "🏭 General",   "img": "images/gongchang.jpg"},
    {"cn": "车间",         "km": "រោងជាង / អាគារ",             "cat": "🏭 General",   "img": "images/chejian.jpg"},
    {"cn": "办公室",       "km": "ការិយាល័យ",                  "cat": "🏭 General",   "img": "images/bangongshi.jpg"},
    {"cn": "班长",         "km": "ប្រធានក្រុម",                "cat": "🏭 General",   "img": "images/banzhang.jpg"},
    {"cn": "翻译",         "km": "បកប្រែ",                     "cat": "🏭 General",   "img": "images/fanyi.jpg"},
    {"cn": "注意安全",     "km": "ប្រយ័ត្នសុវត្ថិភាព",          "cat": "🏭 General",   "img": "images/zhuyianquan.jpg"},
    {"cn": "上班",         "km": "ចូលធ្វើការ",                 "cat": "🏭 General",   "img": "images/shangban.jpg"},
    {"cn": "下班",         "km": "ចេញពីធ្វើការ",               "cat": "🏭 General",   "img": "images/xiaban.jpg"},
    {"cn": "请假",         "km": "សុំច្បាប់",                   "cat": "🏭 General",   "img": "images/qingjia.jpg"},
    {"cn": "夹具",         "km": "ពុម្ពគាប",                   "cat": "🏭 General",   "img": "images/夹具.jpg"},
    {"cn": "电流",         "km": "ចរន្តភ្លើង",                 "cat": "🏭 General",   "img": "images/电流.jpg"},
    {"cn": "模具",         "km": "ពុម្ព",                      "cat": "🏭 General",   "img": "images/模具.jpg"},
    {"cn": "护目镜",       "km": "វ៉ែនតាការពារ",               "cat": "🏭 General",   "img": "images/护目镜.jpg"},
    {"cn": "手套",         "km": "ស្រោមដៃ",                    "cat": "🏭 General",   "img": "images/手套.jpg"},
    {"cn": "通风",         "km": "ខ្យល់ចេញចូល",               "cat": "🏭 General",   "img": "images/通风.jpg"},
]

# ════════════════════════════════════════════
#   ការស្វែងរក (Fuzzy + Partial Match)
# ════════════════════════════════════════════

def normalize(text):
    return text.lower().strip().replace(" ", "")

def fuzzy_search(query, threshold=0.45):
    q = normalize(query)
    results = []
    for item in qc_data:
        cn = normalize(item['cn'])
        km = normalize(item['km'])
        score = 0.0
        if q == cn or q == km:
            score = 1.0
        elif q in cn or q in km:
            score = 0.9
        elif cn in q or km in q:
            score = 0.75
        else:
            r1 = difflib.SequenceMatcher(None, q, cn).ratio()
            r2 = difflib.SequenceMatcher(None, q, km).ratio()
            score = max(r1, r2)
            if len(q) >= 2:
                for i in range(len(q) - 1):
                    bigram = q[i:i+2]
                    if bigram in cn or bigram in km:
                        score = max(score, 0.55)
                        break
        if score >= threshold:
            results.append((score, item))
    results.sort(key=lambda x: -x[0])
    return [item for _, item in results[:5]]

# ════════════════════════════════════════════
#   Keyboards (Menus)
# ════════════════════════════════════════════

def main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.row('🔍 ស្វែងរកពាក្យ', '📚 មើលតាមប្រភេទ')
    markup.row('📦 来料异常报告', '⚙️ 制程异常报告')
    markup.row('🗓️ សម្រង់វត្តមាន', '📖 មេរៀនភាសាចិន')
    markup.row('📊 តេស្តសមត្ថភាព', '📅 កាលវិភាគ')
    markup.row('ℹ️ ជំនួយ / Help')
    return markup

def category_menu():
    cats = sorted(set(d['cat'] for d in qc_data))
    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = [types.InlineKeyboardButton(c, callback_data=f"cat:{c}") for c in cats]
    markup.add(*buttons)
    markup.add(types.InlineKeyboardButton("🔙 ត្រឡប់ក្រោយ", callback_data="back:main"))
    return markup

def result_inline(item):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🔍 ស្វែងរកទៀត", callback_data="search:again"),
        types.InlineKeyboardButton("📂 មើលប្រភេទ", callback_data=f"cat:{item['cat']}"),
    )
    return markup

def cancel_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('❌ បោះបង់')
    return markup

# ════════════════════════════════════════════
#   State Management
# ════════════════════════════════════════════
user_state = {}
user_data  = {}

# ════════════════════════════════════════════
#   /start & /help
# ════════════════════════════════════════════

@bot.message_handler(commands=['start'])
def send_welcome(message):
    name = message.from_user.first_name or "បង"
    txt = (
        f"🙏 សួស្តី *{name}*!\n\n"
        "ខ្ញុំជា *XDS QC Assistant v3.0* — ជំនួយការ QC ឆ្លាតវៃ 🤖\n\n"
        "💡 *អ្វីដែលខ្ញុំធ្វើបាន:*\n"
        "• 🔍 ស្វែងរកពាក្យចិន↔ខ្មែរ\n"
        "• 📸 មើលរូបភាពពិការភាព\n"
        "• 📝 ធ្វើរបាយការណ៍ DPU ផ្ញើ Group\n"
        "• 🗓️ *សម្រង់វត្តមានប្រចាំថ្ងៃ* _(ថ្មី!✨)_\n"
        "• 📚 មើលពាក្យតាមប្រភេទ\n\n"
        "👇 ចុចប៊ូតុងខាងក្រោម!"
    )
    bot.send_message(message.chat.id, txt, parse_mode='Markdown', reply_markup=main_menu())

@bot.message_handler(commands=['getid'])
def get_id(message):
    ctype = message.chat.type
    cid   = message.chat.id
    if ctype == 'private':
        text = (
            f"*Your Private Chat ID:* `{cid}`\n\n"
            "ចំណាំ: ដើម្បីបាន *Group ID* សូម:\n"
            "1. Add Bot ចូល Group\n"
            "2. វាយ /getid ក្នុង Group នោះ"
        )
    else:
        text = (
            f"*Group Name:* {message.chat.title}\n"
            f"*Group ID:* `{cid}`\n\n"
            "Copy ID នេះ ហើយដាក់ក្នុង `TARGET_GROUP_ID`"
        )
    bot.reply_to(message, text, parse_mode='Markdown')

# ════════════════════════════════════════════
#   ប៊ូតុង: ស្វែងរក
# ════════════════════════════════════════════

@bot.message_handler(func=lambda m: m.text == '🔍 ស្វែងរកពាក្យ')
def ask_search(message):
    user_state[message.chat.id] = 'searching'
    bot.send_message(
        message.chat.id,
        "🔍 *វាយពាក្យចិន ឬ ខ្មែរ* ដែលចង់ស្វែងរក:\n_(វាយស្រដៀងក៏ស្វែងរកបានដែរ!)_",
        parse_mode='Markdown',
        reply_markup=cancel_markup()
    )

@bot.message_handler(func=lambda m: m.text == '❌ បោះបង់')
def cancel_action(message):
    user_state.pop(message.chat.id, None)
    user_data.pop(message.chat.id, None)
    bot.send_message(message.chat.id, "✅ បោះបង់រួចរាល់!", reply_markup=main_menu())

# ════════════════════════════════════════════
#   ប៊ូតុង: មើលតាមប្រភេទ
# ════════════════════════════════════════════

@bot.message_handler(func=lambda m: m.text == '📚 មើលតាមប្រភេទ')
def show_categories(message):
    bot.send_message(
        message.chat.id,
        "📂 *ជ្រើសរើសប្រភេទ:*",
        parse_mode='Markdown',
        reply_markup=category_menu()
    )

@bot.callback_query_handler(func=lambda c: c.data.startswith("cat:"))
def show_category_items(call):
    cat = call.data[4:]
    items = [d for d in qc_data if d['cat'] == cat]
    lines = [f"📂 *{cat}* — ពាក្យ {len(items)} :\n"]
    for i, item in enumerate(items, 1):
        lines.append(f"{i}. 🇨🇳 `{item['cn']}` → 🇰🇭 {item['km']}")
    text = "\n".join(lines)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔙 ត្រឡប់ក្រោយ", callback_data="back:cats"))
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                          parse_mode='Markdown', reply_markup=markup)
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda c: c.data == "back:cats")
def back_to_cats(call):
    bot.edit_message_text("📂 *ជ្រើសរើសប្រភេទ:*",
                          call.message.chat.id, call.message.message_id,
                          parse_mode='Markdown', reply_markup=category_menu())
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda c: c.data == "back:main")
def back_to_main(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.send_message(call.message.chat.id, "🏠 Menu ចម្បង:", reply_markup=main_menu())
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda c: c.data == "search:again")
def search_again(call):
    user_state[call.message.chat.id] = 'searching'
    bot.send_message(call.message.chat.id, "🔍 វាយពាក្យចង់ស្វែងរក:", reply_markup=cancel_markup())
    bot.answer_callback_query(call.id)

# ════════════════════════════════════════════
#   HELPER
# ════════════════════════════════════════════

def rate_status(rate):
    if rate == 0:    return "🟢 ល្អឥតខ្ចោះ"
    elif rate <= 1:  return "🟡 ល្អ"
    elif rate <= 5:  return "🟠 ត្រូវប្រយ័ត្ន"
    else:            return "🔴 ចាំបាច់ធ្វើ Action"

def send_report_to_group(chat_id, call, report, retry_cb):
    try:
        bot.send_message(TARGET_GROUP_ID, report, parse_mode='Markdown')
        try:
            bot.edit_message_reply_markup(chat_id, call.message.message_id, reply_markup=None)
        except Exception:
            pass
        bot.send_message(chat_id, "✅ *ផ្ញើចូល Group រួចរាល់ហើយ!*",
                         parse_mode='Markdown', reply_markup=main_menu())
    except Exception as e:
        err = str(e)
        if "chat not found" in err:
            tip = (
                "⚠️ *ផ្ញើ Group មិនកើត!*\n\n"
                "*មូលហេតុ:* Group ID មិនត្រូវ ឬ Bot មិនទាន់ចូល Group\n\n"
                "*របៀបដោះស្រាយ:*\n"
                "1. បន្ថែម Bot ចូល Group ជាមុន\n"
                "2. វាយ /getid ក្នុង Group ដើម្បីយក ID\n"
                "3. ប្រាប់ Admin ឱ្យ Update ID ក្នុង code\n\n"
                f"*ID បច្ចុប្បន្ន:* `{TARGET_GROUP_ID}`"
            )
        elif "bot was kicked" in err or "not a member" in err:
            tip = (
                "⚠️ *Bot ត្រូវបាន Kick ចេញពី Group!*\n\n"
                "សូម Add Bot ចូល Group ឡើងវិញ"
            )
        elif "PEER_ID_INVALID" in err:
            tip = (
                "⚠️ *Group ID មិនត្រឹមត្រូវ!*\n\n"
                "Group ID ត្រូវតែចាប់ផ្ដើម `-100...`\n"
                "វាយ /getid ក្នុង Group ដើម្បីបាន ID ត្រឹមត្រូវ"
            )
        else:
            tip = f"⚠️ *Error:* `{err}`"
        bot.send_message(chat_id, tip, parse_mode='Markdown', reply_markup=main_menu())

def preview_markup(send_cb, retry_cb):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("📤 ផ្ញើ Group", callback_data=send_cb),
        types.InlineKeyboardButton("🔁 ធ្វើម្តងទៀត", callback_data=retry_cb),
    )
    return markup

def step_header(step, total_steps, icon, label, hint=""):
    return (
        f"*ជំហានទី {step}/{total_steps}* {icon} *{label}*"
        + (f"\n_{hint}_" if hint else "")
    )

# ════════════════════════════════════════════════════════════════
#   🗓 ATTENDANCE REPORT — 考勤日报
# ════════════════════════════════════════════════════════════════

DEPARTMENTS = [
    "进料品管", "焊接品管", "焊接备料品管","涂装品管", "总装品管",
    "验室品管",   "仓库部",  
]

LEAVE_REASONS = ["病假", "事假", "产假/陪产假", "特假", "产检假", "旷工","其他原因"]

def attn_dept_markup():
    markup = types.InlineKeyboardMarkup(row_width=2)
    for d in DEPARTMENTS:
        markup.add(types.InlineKeyboardButton(d, callback_data=f"attn_dept:{d}"))
    markup.add(types.InlineKeyboardButton("手动输入部门名称", callback_data="attn_dept:custom"))
    return markup

def attn_shift_markup():
    markup = types.InlineKeyboardMarkup(row_width=3)
    markup.add(
        types.InlineKeyboardButton("上午", callback_data="attn_shift:上午"),
        types.InlineKeyboardButton("下午", callback_data="attn_shift:下午"),
        types.InlineKeyboardButton("夜班", callback_data="attn_shift:夜班"),
    )
    return markup

def leave_reason_markup():
    markup = types.InlineKeyboardMarkup(row_width=2)
    for r in LEAVE_REASONS:
        markup.add(types.InlineKeyboardButton(r, callback_data=f"attn_reason:{r}"))
    return markup

def add_more_markup():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("继续添加缺勤人员", callback_data="attn_add_more"),
        types.InlineKeyboardButton("完成  预览报告",   callback_data="attn_done"),
    )
    return markup

@bot.message_handler(func=lambda m: m.text == '🗓️ សម្រង់វត្តមាន')
def start_attendance(message):
    chat_id = message.chat.id
    user_state[chat_id] = 'attn'
    now = datetime.now()
    user_data[chat_id] = {
        'type': 'attendance',
        'date': now.strftime('%Y年%m月%d日'),
        'time': now.strftime('%H:%M'),
        'absentees': [],
    }
    msg = bot.send_message(
        chat_id,
        "*【考勤日报登记】*\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        "*第 1/6 步 — 部门*\n"
       "_请选择，或直接输入部门名称_",
        parse_mode='Markdown',
        reply_markup=cancel_markup()
    )
    bot.send_message(chat_id, "请选择部门：", reply_markup=attn_dept_markup())
    bot.register_next_step_handler(msg, _attn_typed_dept)

def _attn_typed_dept(message):
    """User typed department name directly instead of pressing button."""
    if message.text == '❌ បោះបង់': return cancel_action(message)
    if user_data.get(message.chat.id, {}).get('dept'):
        return  # already set via button
    chat_id = message.chat.id
    user_data[chat_id]['dept'] = message.text.strip()
    user_state[chat_id] = 'attn'
    _ask_shift(chat_id)

@bot.callback_query_handler(func=lambda c: c.data.startswith("attn_dept:"))
def attn_got_dept(call):
    chat_id = call.message.chat.id
    dept = call.data[len("attn_dept:"):]
    if dept == "custom":
        bot.answer_callback_query(call.id)
        msg = bot.send_message(chat_id, "请输入部门名称：")
        bot.register_next_step_handler(msg, _custom_dept_step)
        return
    user_data[chat_id]['dept'] = dept
    bot.answer_callback_query(call.id, f"已选：{dept}")
    _ask_shift(chat_id)

def _custom_dept_step(message):
    if message.text == '❌ បោះបង់': return cancel_action(message)
    chat_id = message.chat.id
    user_data[chat_id]['dept'] = message.text.strip()
    user_state[chat_id] = 'attn'
    _ask_shift(chat_id)

def _ask_shift(chat_id):
    bot.send_message(
        chat_id,
        "*第 2/6 步 — 时间*",
        parse_mode='Markdown',
        reply_markup=cancel_markup()
    )
    bot.send_message(chat_id, "请选择时间：", reply_markup=attn_shift_markup())

@bot.callback_query_handler(func=lambda c: c.data.startswith("attn_shift:"))
def attn_got_shift(call):
    chat_id = call.message.chat.id
    shift = call.data[len("attn_shift:"):]
    user_data[chat_id]['shift'] = shift
    bot.answer_callback_query(call.id, f"已选：{shift}")
    msg = bot.send_message(
        chat_id,
        f"*已选时间：{shift}*\n\n"
        "*第 3/6 步 — 应到人数*\n"
        "_请输入应到岗总人数（例如：25）_",
        parse_mode='Markdown', reply_markup=cancel_markup()
    )
    user_state[chat_id] = 'attn_expected'
    bot.register_next_step_handler(msg, attn_step_expected)

def attn_step_expected(message):
    if message.text == '❌ បោះបង់': return cancel_action(message)
    chat_id = message.chat.id
    if not message.text.strip().isdigit():
        msg = bot.reply_to(message, "请输入数字！")
        bot.register_next_step_handler(msg, attn_step_expected); return
    user_data[chat_id]['expected'] = int(message.text.strip())
    msg = bot.send_message(
        chat_id,
        f"*应到人数：{message.text.strip()} 人*\n\n"
        "*第 4/6 步 — 实到人数*\n"
        "_请输入实际到岗人数（例如：22）_",
        parse_mode='Markdown', reply_markup=cancel_markup()
    )
    user_state[chat_id] = 'attn_present'
    bot.register_next_step_handler(msg, attn_step_present)

def attn_step_present(message):
    if message.text == '❌ បោះបង់': return cancel_action(message)
    chat_id = message.chat.id
    if not message.text.strip().isdigit():
        msg = bot.reply_to(message, "请输入数字！")
        bot.register_next_step_handler(msg, attn_step_present); return
    present = int(message.text.strip())
    expected = user_data[chat_id]['expected']
    if present > expected:
        msg = bot.reply_to(message, f"实到人数不能大于应到人数({expected})，请重新输入：")
        bot.register_next_step_handler(msg, attn_step_present); return
    user_data[chat_id]['present'] = present
    absent_count = expected - present
    user_data[chat_id]['absent_count'] = absent_count
    user_state[chat_id] = 'attn_leave'
    if absent_count == 0:
        user_data[chat_id]['leave_count'] = 0
        _preview_attendance(message)
    else:
        msg = bot.send_message(
            chat_id,
            f"*实到：{present} 人 / 缺勤：{absent_count} 人*\n\n"
            "*第 5/6 步 — 请假人数*\n"
            f"_在 {absent_count} 名缺勤中，请假人数是多少？（例如：2）_",
            parse_mode='Markdown', reply_markup=cancel_markup()
        )
        bot.register_next_step_handler(msg, attn_step_leave_count)

def attn_step_leave_count(message):
    if message.text == '❌ បោះបង់': return cancel_action(message)
    chat_id = message.chat.id
    if not message.text.strip().isdigit():
        msg = bot.reply_to(message, "请输入数字！")
        bot.register_next_step_handler(msg, attn_step_leave_count); return
    leave = int(message.text.strip())
    absent = user_data[chat_id]['absent_count']
    if leave > absent:
        msg = bot.reply_to(message, f"请假人数不能超过缺勤人数({absent})，请重新输入：")
        bot.register_next_step_handler(msg, attn_step_leave_count); return
    user_data[chat_id]['leave_count'] = leave
    user_data[chat_id]['absentees'] = []
    user_state[chat_id] = 'attn_absentee'
    if absent == 0:
        _preview_attendance(message)
    else:
        user_data[chat_id]['_to_record'] = absent
        user_data[chat_id]['_recorded'] = 0
        _ask_absentee(chat_id)

def _ask_absentee(chat_id):
    recorded = user_data[chat_id]['_recorded']
    total    = user_data[chat_id]['_to_record']
    n = recorded + 1
    msg = bot.send_message(
        chat_id,
        f"*第 6/6 步 — 缺勤人员信息 ({n}/{total})*\n\n"
        "*请输入工号 / 姓名*\n"
        "_例如：KH001 / 陈大华_",
        parse_mode='Markdown',
        reply_markup=cancel_markup()
    )
    user_state[chat_id] = 'attn_absentee_id'
    bot.register_next_step_handler(msg, attn_got_absentee_id)

def attn_got_absentee_id(message):
    if message.text == '❌ បោះបង់': return cancel_action(message)
    chat_id = message.chat.id
    user_data[chat_id]['_current_absentee'] = {'id_name': message.text.strip()}
    user_state[chat_id] = 'attn_waiting_reason'
    bot.send_message(
        chat_id,
        f"工号/姓名：`{message.text.strip()}`\n\n*请选择请假/缺勤原因：*",
        parse_mode='Markdown',
        reply_markup=leave_reason_markup()
    )

@bot.callback_query_handler(func=lambda c: c.data.startswith("attn_reason:"))
def attn_got_reason(call):
    chat_id = call.message.chat.id
    if user_state.get(chat_id) not in ('attn_waiting_reason', 'attn_absentee_id'):
        bot.answer_callback_query(call.id); return
    reason = call.data[len("attn_reason:"):]
    bot.answer_callback_query(call.id, "已保存")
    if reason == "其他原因":
        msg = bot.send_message(chat_id, "请输入具体原因：")
        user_state[chat_id] = 'attn_custom_reason'
        bot.register_next_step_handler(msg, attn_custom_reason)
        return
    _save_absentee(chat_id, reason)

@bot.message_handler(func=lambda m: user_state.get(m.chat.id) == 'attn_custom_reason')
def attn_custom_reason(message):
    if message.text == '❌ បោះបង់': return cancel_action(message)
    _save_absentee(message.chat.id, message.text.strip())

def _save_absentee(chat_id, reason):
    current = user_data[chat_id].get('_current_absentee', {})
    current['reason'] = reason
    user_data[chat_id]['absentees'].append(dict(current))
    user_data[chat_id]['_recorded'] += 1
    recorded = user_data[chat_id]['_recorded']
    total    = user_data[chat_id]['_to_record']
    if recorded < total:
        bot.send_message(chat_id, f"已保存 {recorded}/{total} 人", parse_mode='Markdown')
        _ask_absentee(chat_id)
    else:
        bot.send_message(chat_id,
            f"*已录入缺勤人员 {recorded}/{total} 人，登记完毕！*\n\n"
            "点击「完成 预览报告」或继续添加：",
            parse_mode='Markdown', reply_markup=add_more_markup())
        user_state.pop(chat_id, None)

@bot.callback_query_handler(func=lambda c: c.data == "attn_add_more")
def attn_add_more(call):
    chat_id = call.message.chat.id
    user_data[chat_id]['_to_record'] += 1
    bot.answer_callback_query(call.id)
    _ask_absentee(chat_id)

@bot.callback_query_handler(func=lambda c: c.data == "attn_done")
def attn_done(call):
    bot.answer_callback_query(call.id)
    _preview_attendance(call.message, is_call=True, chat_id=call.message.chat.id)

def _build_attendance_report(d, reporter_name):
    expected   = d.get('expected', 0)
    present    = d.get('present', 0)
    absent_all = expected - present
    leave      = d.get('leave_count', 0)
    no_reason  = absent_all - leave
    rate_pct   = (present / expected * 100) if expected > 0 else 0

    # ── Status text ──────────────────────────────────────
    if rate_pct == 100:
        status_line = "◆ 状态：*全勤达标* ✔"
    elif rate_pct >= 90:
        status_line = "◆ 状态：*出勤良好*"
    elif rate_pct >= 75:
        status_line = "◆ 状态：*偏低 — 请注意*"
    else:
        status_line = "◆ 状态：*严重不足 — 需处理*"

    # ── Progress bar ──────────────────────────────────────
    filled = round(rate_pct / 10)
    bar = "▓" * filled + "░" * (10 - filled)

    # ── Color-coded numbers ──────────────────────────────
    # present   → bold (positive)
    # absent    → italic (caution)
    # leave     → normal
    # no_reason → bold+italic if > 0
    absent_fmt  = f"*{absent_all}*" if absent_all == 0 else f"_{absent_all}_"
    noreason_fmt = f"*{no_reason}*" if no_reason == 0 else f"*_{no_reason}_*"

    # ── Absentee block ────────────────────────────────────
    absentee_block = ""
    if d.get('absentees'):
        absentee_block = (
            "\n"
            "▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔\n"
            "*缺勤人员详情*\n"
            "▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔\n"
        )
        for i, ab in enumerate(d['absentees'], 1):
            absentee_block += f"  *{i}.*  `{ab['id_name']}`\n"
            absentee_block += f"        原因：_{ab['reason']}_\n"

    # ── Title centered with ideographic spaces ────────────
    # U+3000 = ideographic space (same width as CJK char in Telegram)
    title = "　　　*考　勤　日　报*"

    report = (
        "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
        f"{title}\n"
        "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
        f"◆ 日期：*{d['date']}*\n"
        f"◆ 时间：*{d['time']}*\n"
        f"◆ 部门：*{d['dept']}*\n"
        f"◆ 时间：*{d['shift']}*\n"
        "▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔\n"
        f"◆ 应到人数：  *{expected} 人*\n"
        f"◆ 实到人数：  *{present} 人*\n"
        f"◆ 缺勤人数：  {absent_fmt} 人\n"
        f"◆ 请假人数：  *{leave} 人*\n"
        f"◆ 旷工人数：  {noreason_fmt} 人\n"
        "▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔\n"
        f"◆ 出勤率：  *{rate_pct:.1f}%*\n"
        f"   `{bar}`\n"
        f"{status_line}\n"
        + absentee_block +
        "\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
        f"◆ 汇报人：*{reporter_name}*"
    )
    return report

def _preview_attendance(message, is_call=False, chat_id=None):
    if chat_id is None:
        chat_id = message.chat.id
    d = user_data.get(chat_id, {})
    # Get reporter name: from_user on call object vs message object
    try:
        if is_call:
            reporter = message.chat.first_name or message.chat.title or "QC"
        else:
            reporter = message.from_user.first_name or "QC"
    except Exception:
        reporter = "QC"
    report = _build_attendance_report(d, reporter)
    if not report.strip():
        bot.send_message(chat_id, "⚠️ ទិន្នន័យបាត់! សូម /start ហើយបំពេញម្ដងទៀត",
                         reply_markup=main_menu())
        return
    user_data[chat_id]['report'] = report
    user_state.pop(chat_id, None)
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("发送至群组", callback_data="attn:send"),
        types.InlineKeyboardButton("重新填写",   callback_data="attn:retry"),
    )
    bot.send_message(chat_id, report,
                     parse_mode='Markdown', reply_markup=markup)

@bot.callback_query_handler(func=lambda c: c.data == "attn:send")
def attn_send(call):
    chat_id = call.message.chat.id
    report  = user_data.get(chat_id, {}).get('report', '')
    # Safety: regenerate if report is empty
    if not report.strip():
        d = user_data.get(chat_id, {})
        reporter = call.from_user.first_name or "QC"
        report = _build_attendance_report(d, reporter)
        user_data[chat_id]['report'] = report
    if not report.strip():
        bot.send_message(chat_id,
            "⚠️ *ទិន្នន័យបាត់!* សូម /start ហើយបំពេញម្ដងទៀត",
            parse_mode='Markdown', reply_markup=main_menu())
        bot.answer_callback_query(call.id)
        return
    send_report_to_group(chat_id, call, report, "attn:retry")
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda c: c.data == "attn:retry")
def attn_retry(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    call.message.text = '🗓️ សម្រង់វត្តមាន'
    start_attendance(call.message)
    bot.answer_callback_query(call.id)


# ════════════════════════════════════════════
#   📦 REPORT 1: 来料异常
# ════════════════════════════════════════════

@bot.message_handler(func=lambda m: m.text == '📦 来料异常报告')
def start_incoming(message):
    user_state[message.chat.id] = 'inc'
    user_data[message.chat.id] = {'type': 'incoming'}
    msg = bot.send_message(
        message.chat.id,
        "📦 *来料异常报告 — របាយការណ៍គ្រឿងចូល*\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        + step_header(1, 9, "🗄", "柜号 (Cabinet No.)", "ឧ. CAB-2024-001"),
        parse_mode='Markdown', reply_markup=cancel_markup()
    )
    bot.register_next_step_handler(msg, inc_step_guihao)

def inc_step_guihao(message):
    if message.text == '❌ បោះបង់': return cancel_action(message)
    user_data[message.chat.id]['guihao'] = message.text
    msg = bot.send_message(message.chat.id,
        f"✅ 柜号: *{message.text}*\n\n"
        + step_header(2, 9, "🏭", "厂商 (Supplier / ក្រុមហ៊ុន)"),
        parse_mode='Markdown', reply_markup=cancel_markup())
    bot.register_next_step_handler(msg, inc_step_supplier)

def inc_step_supplier(message):
    if message.text == '❌ បោះបង់': return cancel_action(message)
    user_data[message.chat.id]['supplier'] = message.text
    msg = bot.send_message(message.chat.id,
        f"✅ 厂商: *{message.text}*\n\n"
        + step_header(3, 9, "📋", "品名 (Product Name / ឈ្មោះផលិតផល)"),
        parse_mode='Markdown', reply_markup=cancel_markup())
    bot.register_next_step_handler(msg, inc_step_product)

def inc_step_product(message):
    if message.text == '❌ បោះបង់': return cancel_action(message)
    user_data[message.chat.id]['product'] = message.text
    msg = bot.send_message(message.chat.id,
        f"✅ 品名: *{message.text}*\n\n"
        + step_header(4, 9, "🔢", "订单号 (Order No.)", "ឧ. PO-20240315"),
        parse_mode='Markdown', reply_markup=cancel_markup())
    bot.register_next_step_handler(msg, inc_step_order)

def inc_step_order(message):
    if message.text == '❌ បោះបង់': return cancel_action(message)
    user_data[message.chat.id]['order'] = message.text
    msg = bot.send_message(message.chat.id,
        f"✅ 订单号: *{message.text}*\n\n"
        + step_header(5, 9, "🏷", "物料编码 (Material Code)", "ឧ. MAT-001-XDS"),
        parse_mode='Markdown', reply_markup=cancel_markup())
    bot.register_next_step_handler(msg, inc_step_matcode)

def inc_step_matcode(message):
    if message.text == '❌ បោះបង់': return cancel_action(message)
    user_data[message.chat.id]['matcode'] = message.text
    msg = bot.send_message(message.chat.id,
        f"✅ 物料编码: *{message.text}*\n\n"
        + step_header(6, 9, "📦", "数量 / Quantity (សរុប)", "ឧ. 500"),
        parse_mode='Markdown', reply_markup=cancel_markup())
    bot.register_next_step_handler(msg, inc_step_qty)

def inc_step_qty(message):
    if message.text == '❌ បោះបង់': return cancel_action(message)
    if not message.text.isdigit():
        msg = bot.reply_to(message, "⚠️ សូមបញ្ចូលតែ *លេខ* ប៉ុណ្ណោះ!", parse_mode='Markdown')
        bot.register_next_step_handler(msg, inc_step_qty); return
    user_data[message.chat.id]['qty'] = int(message.text)
    msg = bot.send_message(message.chat.id,
        f"✅ 数量: *{message.text}*\n\n"
        + step_header(7, 9, "🔍", "抽检数 / Inspected Qty", "ឧ. 80"),
        parse_mode='Markdown', reply_markup=cancel_markup())
    bot.register_next_step_handler(msg, inc_step_sample)

def inc_step_sample(message):
    if message.text == '❌ បោះបង់': return cancel_action(message)
    if not message.text.isdigit():
        msg = bot.reply_to(message, "⚠️ សូមបញ្ចូលតែ *លេខ* ប៉ុណ្ណោះ!", parse_mode='Markdown')
        bot.register_next_step_handler(msg, inc_step_sample); return
    user_data[message.chat.id]['sample'] = int(message.text)
    msg = bot.send_message(message.chat.id,
        f"✅ 抽检: *{message.text}*\n\n"
        + step_header(8, 9, "❌", "不良数 / NG Qty", "ឧ. 5"),
        parse_mode='Markdown', reply_markup=cancel_markup())
    bot.register_next_step_handler(msg, inc_step_ng)

def inc_step_ng(message):
    if message.text == '❌ បោះបង់': return cancel_action(message)
    if not message.text.isdigit():
        msg = bot.reply_to(message, "⚠️ សូមបញ្ចូលតែ *លេខ* ប៉ុណ្ណោះ!", parse_mode='Markdown')
        bot.register_next_step_handler(msg, inc_step_ng); return
    chat_id = message.chat.id
    ng = int(message.text)
    sample = user_data[chat_id]['sample']
    if ng > sample:
        msg = bot.reply_to(message, "⚠️ NG មិនអាចធំជាង 抽检数! បញ្ចូលម្តងទៀត:")
        bot.register_next_step_handler(msg, inc_step_ng); return
    user_data[chat_id]['ng'] = ng
    rate = (ng / sample * 100) if sample > 0 else 0
    user_data[chat_id]['rate'] = rate
    msg = bot.send_message(message.chat.id,
        f"✅ 不良数: *{ng}*  |  不良率: *{rate:.2f}%*\n\n"
        + step_header(9, 9, "📝", "不良描述 / ពិពណ៌នាពិការភាព",
                      "ឧ. 焊破 ×3，气泡 ×2"),
        parse_mode='Markdown', reply_markup=cancel_markup())
    bot.register_next_step_handler(msg, inc_step_desc)

def inc_step_desc(message):
    if message.text == '❌ បោះបង់': return cancel_action(message)
    chat_id = message.chat.id
    user_data[chat_id]['desc'] = message.text
    d = user_data[chat_id]
    sample = d['sample']; ng = d['ng']; rate = d['rate']
    status = rate_status(rate)
    report = (
        "━━━━━━━━━━━━━━━━━━━━━\n"
        "📦 *[XDS] 来料异常报告*\n"
        "   *Incoming Material Report*\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        f"🗄  *柜号:*     `{d['guihao']}`\n"
        f"🏭 *厂商:*     `{d['supplier']}`\n"
        f"📋 *品名:*     `{d['product']}`\n"
        f"🔢 *订单号:*   `{d['order']}`\n"
        f"🏷  *物料编码:* `{d['matcode']}`\n"
        f"📦 *数量:*     `{d['qty']}`\n"
        f"🔍 *抽检:*     `{sample}`\n"
        f"❌ *不良数:*   `{ng}`\n"
        f"📊 *不良率:*   `{rate:.2f}%`\n"
        f"📌 *Status:*   {status}\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        f"📝 *不良描述:*\n`{d['desc']}`\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 *汇报人:* {message.from_user.first_name}"
    )
    user_data[chat_id]['report'] = report
    user_state.pop(chat_id, None)
    bot.send_message(chat_id, "📋 *Preview — 来料异常报告:*\n\n" + report,
                     parse_mode='Markdown', reply_markup=preview_markup("inc:send","inc:retry"))

@bot.callback_query_handler(func=lambda c: c.data == "inc:send")
def inc_send(call):
    chat_id = call.message.chat.id
    report = user_data.get(chat_id, {}).get('report', '')
    if not report.strip():
        bot.send_message(chat_id, "⚠️ ទិន្នន័យបាត់! សូម /start ហើយបំពេញម្ដងទៀត", reply_markup=main_menu())
        bot.answer_callback_query(call.id); return
    send_report_to_group(chat_id, call, report, "inc:retry")
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda c: c.data == "inc:retry")
def inc_retry(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    call.message.text = '📦 来料异常报告'
    start_incoming(call.message)
    bot.answer_callback_query(call.id)

# ════════════════════════════════════════════
#   ⚙️ REPORT 2: 制程异常
# ════════════════════════════════════════════

@bot.message_handler(func=lambda m: m.text == '⚙️ 制程异常报告')
def start_process(message):
    user_state[message.chat.id] = 'proc'
    user_data[message.chat.id] = {'type': 'process'}
    msg = bot.send_message(
        message.chat.id,
        "⚙️ *制程异常报告 — របាយការណ៍ពិការភាពផ្ទៃក្នុង*\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        + step_header(1, 8, "👥", "客户 (Customer / អតិថិជន)", "ឧ. TREK / GIANT"),
        parse_mode='Markdown', reply_markup=cancel_markup()
    )
    bot.register_next_step_handler(msg, proc_step_customer)

def proc_step_customer(message):
    if message.text == '❌ បោះបង់': return cancel_action(message)
    user_data[message.chat.id]['customer'] = message.text
    msg = bot.send_message(message.chat.id,
        f"✅ 客户: *{message.text}*\n\n"
        + step_header(2, 8, "🔢", "订单号码 (Order No.)", "ឧ. PO-20240315"),
        parse_mode='Markdown', reply_markup=cancel_markup())
    bot.register_next_step_handler(msg, proc_step_order)

def proc_step_order(message):
    if message.text == '❌ បោះបង់': return cancel_action(message)
    user_data[message.chat.id]['order'] = message.text
    msg = bot.send_message(message.chat.id,
        f"✅ 订单号: *{message.text}*\n\n"
        + step_header(3, 8, "📐", "图号 (Drawing No.)", "ឧ. DWG-XDS-001"),
        parse_mode='Markdown', reply_markup=cancel_markup())
    bot.register_next_step_handler(msg, proc_step_drawing)

def proc_step_drawing(message):
    if message.text == '❌ បោះបង់': return cancel_action(message)
    user_data[message.chat.id]['drawing'] = message.text
    msg = bot.send_message(message.chat.id,
        f"✅ 图号: *{message.text}*\n\n"
        + step_header(4, 8, "📋", "品名 (Product Name / ឈ្មោះផលិតផល)"),
        parse_mode='Markdown', reply_markup=cancel_markup())
    bot.register_next_step_handler(msg, proc_step_product)

def proc_step_product(message):
    if message.text == '❌ បោះបង់': return cancel_action(message)
    user_data[message.chat.id]['product'] = message.text
    msg = bot.send_message(message.chat.id,
        f"✅ 品名: *{message.text}*\n\n"
        + step_header(5, 8, "📦", "订单数量 / Order Qty", "ឧ. 1000"),
        parse_mode='Markdown', reply_markup=cancel_markup())
    bot.register_next_step_handler(msg, proc_step_qty)

def proc_step_qty(message):
    if message.text == '❌ បោះបង់': return cancel_action(message)
    if not message.text.isdigit():
        msg = bot.reply_to(message, "⚠️ សូមបញ្ចូលតែ *លេខ* ប៉ុណ្ណោះ!", parse_mode='Markdown')
        bot.register_next_step_handler(msg, proc_step_qty); return
    user_data[message.chat.id]['qty'] = int(message.text)
    msg = bot.send_message(message.chat.id,
        f"✅ 订单数量: *{message.text}*\n\n"
        + step_header(6, 8, "🔍", "抽检数 / Inspected Qty", "ឧ. 100"),
        parse_mode='Markdown', reply_markup=cancel_markup())
    bot.register_next_step_handler(msg, proc_step_sample)

def proc_step_sample(message):
    if message.text == '❌ បោះបង់': return cancel_action(message)
    if not message.text.isdigit():
        msg = bot.reply_to(message, "⚠️ សូមបញ្ចូលតែ *លេខ* ប៉ុណ្ណោះ!", parse_mode='Markdown')
        bot.register_next_step_handler(msg, proc_step_sample); return
    user_data[message.chat.id]['sample'] = int(message.text)
    msg = bot.send_message(message.chat.id,
        f"✅ 抽检: *{message.text}*\n\n"
        + step_header(7, 8, "❌", "不良数 / NG Qty", "ឧ. 3"),
        parse_mode='Markdown', reply_markup=cancel_markup())
    bot.register_next_step_handler(msg, proc_step_ng)

def proc_step_ng(message):
    if message.text == '❌ បោះបង់': return cancel_action(message)
    if not message.text.isdigit():
        msg = bot.reply_to(message, "⚠️ សូមបញ្ចូលតែ *លេខ* ប៉ុណ្ណោះ!", parse_mode='Markdown')
        bot.register_next_step_handler(msg, proc_step_ng); return
    chat_id = message.chat.id
    ng = int(message.text)
    sample = user_data[chat_id]['sample']
    if ng > sample:
        msg = bot.reply_to(message, "⚠️ NG មិនអាចធំជាង 抽检数! បញ្ចូលម្តងទៀត:")
        bot.register_next_step_handler(msg, proc_step_ng); return
    user_data[chat_id]['ng'] = ng
    rate = (ng / sample * 100) if sample > 0 else 0
    user_data[chat_id]['rate'] = rate
    msg = bot.send_message(message.chat.id,
        f"✅ 不良数: *{ng}*  |  不良率: *{rate:.2f}%*\n\n"
        + step_header(8, 8, "📝", "不良描述 / ពិពណ៌នាពិការភាព",
                      "ឧ. 焊破 ×3，开裂 ×1"),
        parse_mode='Markdown', reply_markup=cancel_markup())
    bot.register_next_step_handler(msg, proc_step_desc)

def proc_step_desc(message):
    if message.text == '❌ បោះបង់': return cancel_action(message)
    chat_id = message.chat.id
    user_data[chat_id]['desc'] = message.text
    d = user_data[chat_id]
    sample = d['sample']; ng = d['ng']; rate = d['rate']
    status = rate_status(rate)
    report = (
        "━━━━━━━━━━━━━━━━━━━━━\n"
        "⚙️ *[XDS] 制程异常报告*\n"
        "   *Process Defect Report*\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        f"👥 *客户:*     `{d['customer']}`\n"
        f"🔢 *订单号:*   `{d['order']}`\n"
        f"📐 *图号:*     `{d['drawing']}`\n"
        f"📋 *品名:*     `{d['product']}`\n"
        f"📦 *订单数量:* `{d['qty']}`\n"
        f"🔍 *抽检:*     `{sample}`\n"
        f"❌ *不良数:*   `{ng}`\n"
        f"📊 *不良率:*   `{rate:.2f}%`\n"
        f"📌 *Status:*   {status}\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        f"📝 *不良描述:*\n`{d['desc']}`\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 *汇报人:* {message.from_user.first_name}"
    )
    user_data[chat_id]['report'] = report
    user_state.pop(chat_id, None)
    bot.send_message(chat_id, "📋 *Preview — 制程异常报告:*\n\n" + report,
                     parse_mode='Markdown', reply_markup=preview_markup("proc:send","proc:retry"))

@bot.callback_query_handler(func=lambda c: c.data == "proc:send")
def proc_send(call):
    chat_id = call.message.chat.id
    report = user_data.get(chat_id, {}).get('report', '')
    if not report.strip():
        bot.send_message(chat_id, "⚠️ ទិន្នន័យបាត់! សូម /start ហើយបំពេញម្ដងទៀត", reply_markup=main_menu())
        bot.answer_callback_query(call.id); return
    send_report_to_group(chat_id, call, report, "proc:retry")
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda c: c.data == "proc:retry")
def proc_retry(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    call.message.text = '⚙️ 制程异常报告'
    start_process(call.message)
    bot.answer_callback_query(call.id)

# ════════════════════════════════════════════
#   ប៊ូតុង: Links / Info
# ════════════════════════════════════════════

@bot.message_handler(func=lambda m: m.text == '📖 មេរៀនភាសាចិន')
def lesson(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📚 បើ Flashcards",
               url="https://cara868710-web.github.io/qc-flashcardfuxikecheng-system/"))
    bot.send_message(message.chat.id, "📚 *មេរៀនភាសាចិន — Flashcards*\nចុចប៊ូតុងខាងក្រោមដើម្បីបើ:",
                     parse_mode='Markdown', reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == '📊 តេស្តសមត្ថភាព')
def quiz(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🧪 ចូលធ្វើតេស្ត",
               url="https://cara868710-web.github.io/my-flashcards/quiz-app.html"))
    bot.send_message(message.chat.id, "📊 *Quiz — តេស្តសមត្ថភាព*\nចុចប៊ូតុងខាងក្រោម:",
                     parse_mode='Markdown', reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == '📅 កាលវិភាគ')
def schedule(message):
    bot.send_message(message.chat.id,
        "📅 *កាលវិភាគបណ្តុះបណ្តាល*\n\n"
        "🗓 រៀងរាល់ *ថ្ងៃសៅរ៍*\n"
        "⏰ ម៉ោង *០៥:០០ PM*\n"
        "📍 ការិយាល័យ QC\n\n"
        "💡 _កុំភ្លេចនាំមកថ្ងៃនោះ!_",
        parse_mode='Markdown')

@bot.message_handler(func=lambda m: m.text in ['ℹ️ ជំនួយ / Help', '/help'])
def help_msg(message):
    txt = (
        "ℹ️ *របៀបប្រើប្រាស់ Bot v3.0*\n\n"
        "🔍 *ស្វែងរកពាក្យ:*\n"
        "  • វាយ `焊破` → ខ្ញុំឆ្លើយ ខ្មែរ\n"
        "  • វាយ `ហ្វ្រាំង` → ខ្ញុំឆ្លើយ ចិន\n\n"
        "🗓️ *សម្រង់វត្តមាន (NEW!):*\n"
        "  • ផ្នែក / សម័យ / 应到 / 实到 / 请假\n"
        "  • 工号+ឈ្មោះ+ហេតុផល → ផ្ញើ Group\n\n"
        "📦 *来料异常:* 柜号/厂商/品名/订单 ...\n"
        "⚙️ *制程异常:* 客户/图号/品名/订单 ...\n\n"
        "🤖 *Commands:*\n"
        "  /start — ចាប់ផ្តើម\n"
        "  /getid — មើល Group ID\n"
        "  /help  — ជំនួយ"
    )
    bot.send_message(message.chat.id, txt, parse_mode='Markdown', reply_markup=main_menu())

# ════════════════════════════════════════════
#   Message Handler ចម្បង (ស្វែងរក)
# ════════════════════════════════════════════

@bot.message_handler(func=lambda message: True)
def handle_all(message):
    chat_id = message.chat.id
    text = message.text
    state = user_state.get(chat_id, '')
    if state == 'searching' or (state == '' and len(text) >= 1):
        do_search(message)

def do_search(message):
    chat_id = message.chat.id
    query = message.text.strip()
    user_state.pop(chat_id, None)
    results = fuzzy_search(query)
    if not results:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📂 មើលតាមប្រភេទ", callback_data="back:cats"))
        bot.reply_to(message,
            f"😕 ស្វែងរក *\"{query}\"* មិនឃើញ!\n\n💡 ព្យាយាម: `焊破`, `ហ្វ្រាំង`...",
            parse_mode='Markdown', reply_markup=markup)
        return
    if len(results) == 1:
        send_result(message, results[0])
    else:
        markup = types.InlineKeyboardMarkup(row_width=1)
        for item in results:
            label = f"🇨🇳 {item['cn']}  ↔  🇰🇭 {item['km']}"
            markup.add(types.InlineKeyboardButton(label, callback_data=f"pick:{item['cn']}"))
        markup.add(types.InlineKeyboardButton("❌ បិទ", callback_data="close:results"))
        bot.reply_to(message,
            f"🔍 រកឃើញ *{len(results)}* លទ្ធផល *\"{query}\"*:\n👇 ជ្រើសយក:",
            parse_mode='Markdown', reply_markup=markup)

def send_result(message_or_call, item, is_call=False):
    text = (
        f"✅ *លទ្ធផល*\n"
        f"━━━━━━━━━━━━━\n"
        f"🇨🇳 *ចិន:* `{item['cn']}`\n"
        f"🇰🇭 *ខ្មែរ:* `{item['km']}`\n"
        f"📂 *ប្រភេទ:* {item['cat']}\n"
        f"━━━━━━━━━━━━━"
    )
    markup = result_inline(item)
    chat_id = message_or_call.chat.id if not is_call else message_or_call.message.chat.id
    if os.path.exists(item['img']):
        with open(item['img'], 'rb') as photo:
            bot.send_photo(chat_id, photo, caption=text, parse_mode='Markdown', reply_markup=markup)
    else:
        bot.send_message(chat_id, text + "\n\n📷 _រូបភាពមិនទាន់មាន_",
                         parse_mode='Markdown', reply_markup=markup)

@bot.callback_query_handler(func=lambda c: c.data.startswith("pick:"))
def pick_result(call):
    cn = call.data[5:]
    item = next((d for d in qc_data if d['cn'] == cn), None)
    if item:
        send_result(call, item, is_call=True)
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda c: c.data == "close:results")
def close_results(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.answer_callback_query(call.id, "បិទ!")

# ════════════════════════════════════════════
#   Run
# ════════════════════════════════════════════
if __name__ == "__main__":
    if not os.path.exists('images'):
        os.makedirs('images')
        print("📁 Created 'images' folder.")
    print("🚀 XDS QC Assistant v3.0 is running...")
    print("📡 Listening for messages...")
    bot.infinity_polling(timeout=30, long_polling_timeout=20)
