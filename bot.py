import logging
from dotenv import load_dotenv
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from database import init_db, add_expense, get_stats
import datetime

# tokens in .env
load_dotenv()
token = os.getenv("TELEGRAM_TOKEN")

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Initialize database
init_db()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💸 *Expense Tracker Bot*\n\n"
        "Available commands:\n"
        "/add <amount> <category> - Add new expense\n"
        "/stats - Show monthly statistics\n"
        "/export - Get data as CSV\n\n"
        "Example: `/add 15.50 coffee`",
        parse_mode="Markdown"
    )

async def add_expense_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        amount = float(context.args[0])
        category = ' '.join(context.args[1:])
        
        add_expense(amount, category)
        await update.message.reply_text(f"✅ Added: ${amount:.2f} ({category})")
    except:
        await update.message.reply_text("❌ Format: `/add 15.50 coffee`", parse_mode="Markdown")

async def show_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    stats = get_stats(datetime.datetime.now().month)
    response = "📊 *Monthly Stats*\n\n"
    
    for category, total in stats.items():
        response += f"{category}: ${total:.2f}\n"
    
    await update.message.reply_text(response, parse_mode="Markdown")

if __name__ == '__main__':
    app = ApplicationBuilder().token(token).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add", add_expense_cmd))
    app.add_handler(CommandHandler("stats", show_stats))
    
    app.run_polling()