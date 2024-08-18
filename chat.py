from telegram import Update
from telegram.ext import ContextTypes
import ollama


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"Hello {update.effective_user.first_name}")


async def ollama_hw(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_input = update.message.text.replace(
        "/ollama ", "", 1
    )  # Elimina el comando "/ollama" del mensaje
    response = ollama.chat(
        model="llama3.1",
        messages=[
            {
                "role": "user",
                "content": user_input,
            },
        ],
    )
    await update.message.reply_text(response["message"]["content"])
