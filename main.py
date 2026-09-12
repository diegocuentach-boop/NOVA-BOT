import json, os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

TOKEN = os.environ.get("BOT_TOKEN")
PIDIENDO_USUARIO = 1
DB_FILE = "usuarios.json"

def cargar_db():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as f:
        return json.load(f)

def guardar_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = cargar_db()
    user_id = str(update.effective_user.id)
    if user_id in db:
        usuario = db[user_id]
        await update.message.reply_text(f"Bienvenido de nuevo {usuario} 👑")
        return ConversationHandler.END
    else:
        await update.message.reply_text("Dime un usuario 👇\nEjemplo: 1mcog")
        return PIDIENDO_USUARIO

async def recibir_usuario(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = cargar_db()
    user_id = str(update.effective_user.id)
    usuario_elegido = update.message.text
    db[user_id] = usuario_elegido
    guardar_db(db)
    teclado = [["🛒 Comprar", "💳 Recargar saldo"],["📦 Mis compras", "📜 Historial"],["👤 Mi cuenta", "🚪 Cerrar sesion"]]
    markup = ReplyKeyboardMarkup(teclado, resize_keyboard=True)
    await update.message.reply_text(f"Usuario {usuario_elegido} guardado para siempre ✅", reply_markup=markup)
    return ConversationHandler.END

app = Application.builder().token(TOKEN).build()
conv = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={PIDIENDO_USUARIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_usuario)]},
    fallbacks=[]
)
app.add_handler(conv)
app.run_polling()
