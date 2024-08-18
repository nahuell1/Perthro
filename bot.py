from telegram.ext import ApplicationBuilder, MessageHandler, filters, CommandHandler
from weather import tiempo
from chat import hello, ollama_hw
from document_processing import handle_pdf
import os
from dotenv import load_dotenv

load_dotenv()


app = ApplicationBuilder().token(os.getenv("TELEGRAM_API_KEY")).build()

app.add_handler(CommandHandler("ollama", ollama_hw))
app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("tiempo", tiempo))
app.add_handler(MessageHandler(filters.Document.ALL, handle_pdf))

app.run_polling()
