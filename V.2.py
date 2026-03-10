import telebot
from telebot import types
import os
import difflib
import re
import unicodedata

# ════════════════════════════════════════════
#   XDS Smart QC Assistant Bot — Version 2.0
# ════════════════════════════════════════════

API_TOKEN = '8629154594:AAGLk72HQU73UbDOxAq_5BL3Sg6mwc9n6jY'
TARGET_GROUP_ID = '-5104865599'

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
    """សម្រួលអក្សរ: lowercase + strip"""
    return text.lower().strip().replace(" ", "")

def fuzzy_search(query, threshold=0.45):
    """ស្វែងរកពាក្យដោយប្រើ fuzzy matching"""
    q = normalize(query)
    results = []

    for item in qc_data:
        cn = normalize(item['cn'])
        km = normalize(item['km'])

        score = 0.0

        # 1️⃣ ត្រូវបានត្រឹមត្រូវ 100%
        if q == cn or q == km:
            score = 1.0
        # 2️⃣ ផ្ទុកក្នុង string
        elif q in cn or q in km:
            score = 0.9
        # 3️⃣ ពាក្យរបស់ km/cn ផ្ទុក query
        elif cn in q or km in q:
            score = 0.75
        else:
            # 4️⃣ Fuzzy ratio (difflib)
            r1 = difflib.SequenceMatcher(None, q, cn).ratio()
            r2 = difflib.SequenceMatcher(None, q, km).ratio()
            score = max(r1, r2)

            # 5️⃣ ស្វែងរករៀងរៀង character
            if len(q) >= 2:
                for i in range(len(q) - 1):
                    bigram = q[i:i+2]
                    if bigram in cn or bigram in km:
                        score = max(score, 0.55)
                        break

        if score >= threshold:
            results.append((score, item))

    # Sort by score ចុះក្រោម
    results.sort(key=lambda x: -x[0])
    return [item for _, item in results[:5]]  # Max 5 results

# ════════════════════════════════════════════
#   Keyboards (Menus)
# ════════════════════════════════════════════

def main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.row('🔍 ស្វែងរកពាក្យ', '📚 មើលតាមប្រភេទ')
    markup.row('📦 来料异常报告', '⚙️ 制程异常报告')
    markup.row('📖 មេរៀនភាសាចិន', '📊 តេស្តសមត្ថភាព')
    markup.row('📅 កាលវិភាគ', 'ℹ️ ជំនួយ / Help')
    return markup

def category_menu():
    """Inline keyboard សម្រាប់ប្រភេទ"""
    cats = sorted(set(d['cat'] for d in qc_data))
    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = [types.InlineKeyboardButton(c, callback_data=f"cat:{c}") for c in cats]
    markup.add(*buttons)
    markup.add(types.InlineKeyboardButton("🔙 ត្រឡប់ក្រោយ", callback_data="back:main"))
    return markup

def result_inline(item):
    """Inline keyboard ក្រោយលទ្ធផល"""
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
user_state = {}   # chat_id → state string
user_data  = {}   # chat_id → dict (DPU form)

# ════════════════════════════════════════════
#   /start & /help
# ════════════════════════════════════════════

@bot.message_handler(commands=['start'])
def send_welcome(message):
    name = message.from_user.first_name or "បង"
    txt = (
        f"🙏 សួស្តី **{name}**!\n\n"
        "ខ្ញុំជា **XDS QC Assistant** — ជំនួយការ QC ឆ្លាតវៃ 🤖\n\n"
        "💡 *អ្វីដែលខ្ញុំធ្វើបាន:*\n"
        "• 🔍 ស្វែងរកពាក្យចិន↔ខ្មែរ (វាយពាក្យស្រដៀងក៏បាន!)\n"
        "• 📸 មើលរូបភាពពិការភាព\n"
        "• 📝 ធ្វើរបាយការណ៍ DPU ផ្ញើ Group ស្វ័យប្រវត្តិ\n"
        "• 📚 មើលពាក្យតាមប្រភេទ\n\n"
        "👇 ចុចប៊ូតុងខាងក្រោម ឬ **វាយពាក្យណាមួយ** ដើម្បីស្វែងរក!"
    )
    bot.send_message(message.chat.id, txt, parse_mode='Markdown', reply_markup=main_menu())

@bot.message_handler(commands=['getid'])
def get_id(message):
    bot.reply_to(message, f"🆔 Group ID: `{message.chat.id}`", parse_mode='Markdown')

# ════════════════════════════════════════════
#   ប៊ូតុង: ស្វែងរក
# ════════════════════════════════════════════

@bot.message_handler(func=lambda m: m.text == '🔍 ស្វែងរកពាក្យ')
def ask_search(message):
    user_state[message.chat.id] = 'searching'
    msg = bot.send_message(
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

    bot.edit_message_text(
        text, call.message.chat.id, call.message.message_id,
        parse_mode='Markdown', reply_markup=markup
    )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda c: c.data == "back:cats")
def back_to_cats(call):
    bot.edit_message_text(
        "📂 *ជ្រើសរើសប្រភេទ:*",
        call.message.chat.id, call.message.message_id,
        parse_mode='Markdown', reply_markup=category_menu()
    )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda c: c.data == "back:main")
def back_to_main(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.send_message(call.message.chat.id, "🏠 Menu ចម្បង:", reply_markup=main_menu())
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda c: c.data == "search:again")
def search_again(call):
    user_state[call.message.chat.id] = 'searching'
    bot.send_message(
        call.message.chat.id,
        "🔍 វាយពាក្យចង់ស្វែងរក:",
        reply_markup=cancel_markup()
    )
    bot.answer_callback_query(call.id)

# ════════════════════════════════════════════
#   HELPER: Rate Status + Send Report
# ════════════════════════════════════════════

def rate_status(rate):
    if rate == 0:    return "🟢 ល្អឥតខ្ចោះ"
    elif rate <= 1:  return "🟡 ល្អ"
    elif rate <= 5:  return "🟠 ត្រូវប្រយ័ត្ន"
    else:            return "🔴 ចាំបាច់ធ្វើ Action"

def validate_number(message, next_step, label="លេខ"):
    if not message.text.isdigit():
        msg = bot.reply_to(message, f"⚠️ សូមបញ្ចូលតែ *{label}* ប៉ុណ្ណោះ!", parse_mode='Markdown')
        bot.register_next_step_handler(msg, next_step)
        return False
    return True

def send_report_to_group(chat_id, call, report, retry_cb):
    try:
        bot.send_message(TARGET_GROUP_ID, report, parse_mode='Markdown')
        bot.edit_message_reply_markup(chat_id, call.message.message_id, reply_markup=None)
        bot.send_message(chat_id, "✅ *ផ្ញើចូល Group រួចរាល់ហើយ!* 🎉", parse_mode='Markdown', reply_markup=main_menu())
    except Exception as e:
        bot.send_message(chat_id, f"⚠️ ផ្ញើ Group មិនបានទេ!\nError: `{e}`", parse_mode='Markdown', reply_markup=main_menu())

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

# ════════════════════════════════════════════
#   📦 REPORT 1: 来料异常 (Incoming Material)
#   Fields: 柜号/厂商/品名/订单号/物料编码/数量/抽检/不良率
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
        parse_mode='Markdown',
        reply_markup=cancel_markup()
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
                      "ឧ. 焊破 ×3，气泡 ×2 — វាយពណ៌នាបញ្ហាលម្អិត"),
        parse_mode='Markdown', reply_markup=cancel_markup())
    bot.register_next_step_handler(msg, inc_step_desc)

def inc_step_desc(message):
    if message.text == '❌ បោះបង់': return cancel_action(message)
    chat_id = message.chat.id
    user_data[chat_id]['desc'] = message.text
    d = user_data[chat_id]
    sample = d['sample']
    ng     = d['ng']
    rate   = d['rate']
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

    bot.send_message(chat_id,
        "📋 *Preview — 来料异常报告:*\n\n" + report,
        parse_mode='Markdown',
        reply_markup=preview_markup("inc:send", "inc:retry")
    )

@bot.callback_query_handler(func=lambda c: c.data == "inc:send")
def inc_send(call):
    chat_id = call.message.chat.id
    report = user_data.get(chat_id, {}).get('report', '')
    send_report_to_group(chat_id, call, report, "inc:retry")
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda c: c.data == "inc:retry")
def inc_retry(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    call.message.text = '📦 来料异常报告'
    start_incoming(call.message)
    bot.answer_callback_query(call.id)

# ════════════════════════════════════════════
#   ⚙️ REPORT 2: 制程异常 (Process Defect)
#   Fields: 客户/订单号码/图号/品名/订单数量/抽检/不良率
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
        parse_mode='Markdown',
        reply_markup=cancel_markup()
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
                      "ឧ. 焊破 ×3，开裂 ×1 — វាយពណ៌នាបញ្ហាលម្អិត"),
        parse_mode='Markdown', reply_markup=cancel_markup())
    bot.register_next_step_handler(msg, proc_step_desc)

def proc_step_desc(message):
    if message.text == '❌ បោះបង់': return cancel_action(message)
    chat_id = message.chat.id
    user_data[chat_id]['desc'] = message.text
    d = user_data[chat_id]
    sample = d['sample']
    ng     = d['ng']
    rate   = d['rate']
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

    bot.send_message(chat_id,
        "📋 *Preview — 制程异常报告:*\n\n" + report,
        parse_mode='Markdown',
        reply_markup=preview_markup("proc:send", "proc:retry")
    )

@bot.callback_query_handler(func=lambda c: c.data == "proc:send")
def proc_send(call):
    chat_id = call.message.chat.id
    report = user_data.get(chat_id, {}).get('report', '')
    send_report_to_group(chat_id, call, report, "proc:retry")
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda c: c.data == "proc:retry")
def proc_retry(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    call.message.text = '⚙️ 制程异常报告'
    start_process(call.message)
    bot.answer_callback_query(call.id)

# ════════════════════════════════════════════
#   ប៊ូតុង: Links
# ════════════════════════════════════════════

@bot.message_handler(func=lambda m: m.text == '📖 មេរៀនភាសាចិន')
def lesson(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📚 បើ Flashcards", url="https://cara868710-web.github.io/qc-flashcardfuxikecheng-system/"))
    bot.send_message(message.chat.id, "📚 *មេរៀនភាសាចិន — Flashcards*\nចុចប៊ូតុងខាងក្រោមដើម្បីបើ:", parse_mode='Markdown', reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == '📊 តេស្តសមត្ថភាព')
def quiz(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🧪 ចូលធ្វើតេស្ត", url="https://cara868710-web.github.io/my-flashcards/quiz-app.html"))
    bot.send_message(message.chat.id, "📊 *Quiz — តេស្តសមត្ថភាព*\nចុចប៊ូតុងខាងក្រោមដើម្បីចូល:", parse_mode='Markdown', reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == '📅 កាលវិភាគ')
def schedule(message):
    txt = (
        "📅 *កាលវិភាគបណ្តុះបណ្តាល*\n\n"
        "🗓 រៀងរាល់ *ថ្ងៃសៅរ៍*\n"
        "⏰ ម៉ោង *០៥:០០ PM*\n"
        "📍 ការិយាល័យ QC\n\n"
        "💡 _កុំភ្លេចនាំមកថ្ងៃនោះ!_"
    )
    bot.send_message(message.chat.id, txt, parse_mode='Markdown')

@bot.message_handler(func=lambda m: m.text in ['ℹ️ ជំនួយ / Help', '/help'])
def help_msg(message):
    txt = (
        "ℹ️ *របៀបប្រើប្រាស់ Bot*\n\n"
        "🔍 *ស្វែងរកពាក្យ:*\n"
        "  • វាយពាក្យចិន: `焊破` → ខ្ញុំឆ្លើយ ខ្មែរ\n"
        "  • វាយពាក្យខ្មែរ: `ហ្វ្រាំង` → ខ្ញុំឆ្លើយ ចិន\n"
        "  • វាយពាក្យ*ស្រដៀង*ក៏ស្វែងរកបានដែរ!\n\n"
        "📦 *来料异常报告:*\n"
        "  • 柜号 / 厂商 / 品名 / 订单号\n"
        "  • 物料编码 / 数量 / 抽检 / 不良率 / 不良描述\n\n"
        "⚙️ *制程异常报告:*\n"
        "  • 客户 / 订单号码 / 图号 / 品名\n"
        "  • 订单数量 / 抽检 / 不良率 / 不良描述\n\n"
        "📂 *មើលតាមប្រភេទ:*\n"
        "  • ចុច 📚 → ជ្រើសប្រភេទ\n\n"
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
    print(f"💬 Chat ID: {chat_id} | User: {message.from_user.username}")  # ← ត្រូវមាន 4 Space

    # ── ប្រសិនជានៅក្នុង state searching ──
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
        bot.reply_to(
            message,
            f"😕 ស្វែងរក *\"{query}\"* មិនឃើញ!\n\n💡 ព្យាយាម:\n• `焊破`, `ផ្សារ`, `ហ្វ្រាំង`...",
            parse_mode='Markdown',
            reply_markup=markup
        )
        return

    if len(results) == 1:
        # លទ្ធផលតែ ១ → បង្ហាញភ្លាម + រូបភាព
        send_result(message, results[0])
    else:
        # លទ្ធផលច្រើន → Inline buttons ជ្រើស
        markup = types.InlineKeyboardMarkup(row_width=1)
        for item in results:
            label = f"🇨🇳 {item['cn']}  ↔  🇰🇭 {item['km']}"
            markup.add(types.InlineKeyboardButton(label, callback_data=f"pick:{item['cn']}"))
        markup.add(types.InlineKeyboardButton("❌ បិទ", callback_data="close:results"))

        bot.reply_to(
            message,
            f"🔍 រកឃើញ *{len(results)}* លទ្ធផលស្រដៀង *\"{query}\"*:\n👇 ជ្រើសយក:",
            parse_mode='Markdown',
            reply_markup=markup
        )

def send_result(message_or_call, item, is_call=False):
    """ផ្ញើ result (ជាមួយ / ឬគ្មានរូបភាព)"""
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
        bot.send_message(chat_id, text + "\n\n📷 _រូបភាពមិនទាន់មាន_", parse_mode='Markdown', reply_markup=markup)

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

    print("🚀 XDS QC Assistant v2.0 is running...")
    print(f"📡 Listening for messages...")
    bot.infinity_polling(
    timeout=60,
    long_polling_timeout=30,
    none_stop=True,
    interval=3
)