from telegram import Update, Document
from telegram.ext import ContextTypes
import PyPDF2
import os


async def pdf_to_text(document):
    file = await document.get_file()
    file_path = f"{document.file_id}.pdf"
    await file.download_to_drive(file_path)
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    # Eliminar el archivo PDF después de procesarlo
    os.remove(file_path)
    return text


# Función para manejar archivos PDF
async def handle_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    document: Document = update.message.document

    if document.mime_type == "application/pdf":
        await update.message.reply_text("Gracias por enviar un archivo PDF.")
        text = await pdf_to_text(document)
        if text:
            await update.message.reply_text(
                f"Contenido del PDF:\n{text[:4000]}"
            )  # Telegram tiene un límite de 4096 caracteres por mensaje
        else:
            await update.message.reply_text("No se pudo extraer texto del PDF.")

    else:
        await update.message.reply_text(
            "Solo acepto archivos PDF. Por favor, envía un archivo PDF."
        )
