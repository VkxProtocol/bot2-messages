import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CallbackContext

# Configuração de logs
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Token do bot e ID do grupo
TOKEN = '[REDACTED_SECRET]'
GROUP_CHAT_ID = '-1002405955713'

# Lista de mensagens a serem enviadas
messages = [
    {"text": "🌟 VKINHA Update: Stay informed about our project! Visit our official website: https://www.vkinha.com.br 🌟", "keyboard": None},
    {"text": "🌟 VKINHA Update: Did you know the pre-sale on DxSale is set up?", "keyboard": [[InlineKeyboardButton("Click here!", url="https://www.dx.app/dxsale/view?address=0x0597Ce945ED83C81AdC47c97139B5602ddb03c69&chain=56")]]},
    {"text": "Did you know we are partnering with:", "keyboard": [
        [InlineKeyboardButton("Azbit", url="https://azbit.com"), InlineKeyboardButton("Bifinance", url="https://bifinance.com")],
        [InlineKeyboardButton("CertiK", url="https://www.certik.com"), InlineKeyboardButton("Gate.io", url="https://www.gate.io")],
        [InlineKeyboardButton("Cryptopix", url="https://cryptopix.com")]
    ]},
    {"text": "Follow us on Instagram:", "keyboard": [[InlineKeyboardButton("Instagram", url="https://www.instagram.com/vkinhacoin/")]]},
    {"text": "Do you know our X (Twitter) profile?", "keyboard": [[InlineKeyboardButton("Twitter", url="https://x.com/vkinhacoin")]]},
    {"text": "Have you seen our CODE? Check it out, it’s verified and audited:", "keyboard": [[InlineKeyboardButton("BSCScan", url="https://bscscan.com/address/0x7Bd2024cAd405ccA960fE9989334A70153c41682#code")]]},
    {"text": "Support our community! Drop a 🔥 on the DX site to boost our token!", "keyboard": None},
    {"text": "Thank you for supporting VKINHA.", "keyboard": None},
    {"text": "Did you know we will support projects that help lives?", "keyboard": None},
    {"text": "Check out our Roadmap:", "keyboard": [[InlineKeyboardButton("Roadmap Link", url="https://vkinha.com/roadmap.html")]]}
]

# Função para enviar mensagens periódicas
async def send_periodic_messages(context: CallbackContext):
    # Inicializa o índice se não existir
    if "current_message_index" not in context.bot_data:
        context.bot_data["current_message_index"] = 0

    index = context.bot_data["current_message_index"]
    message_data = messages[index]

    try:
        await context.bot.send_message(
            chat_id=GROUP_CHAT_ID,
            text=message_data["text"],
            reply_markup=InlineKeyboardMarkup(message_data["keyboard"]) if message_data["keyboard"] else None
        )
        logger.info(f"Mensagem enviada: {message_data['text']}")
    except Exception as e:
        logger.error(f"Erro ao enviar mensagem: {e}")

    # Atualiza o índice para a próxima mensagem
    context.bot_data["current_message_index"] = (index + 1) % len(messages)

# Função principal
def main():
    # Inicializa o bot
    application = Application.builder().token(TOKEN).build()

    # Configura o JobQueue para enviar mensagens a cada 15 minutos
    job_queue = application.job_queue
    job_queue.run_repeating(
        callback=send_periodic_messages,
        interval=900,  # 15 minutos em segundos (15 * 60)
        first=10       # Primeira mensagem após 10 segundos
    )

    # Inicia o bot com polling
    application.run_polling()

if __name__ == '__main__':
    main()