import logging
import asyncio
from telethon import Button, TelegramClient, events
from telethon.errors import UserNotParticipantError
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.types import ChannelParticipantAdmin, ChannelParticipantCreator

# Ayarlar
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

# API bilgileri
api_id = 23144161
api_hash = '0e156557bde6def9a8541cc8c65d57df'
bot_token = '5374464909:AAHhMTA-B_v1pwGvpkbB90f515TRHetPolA'
allowed_users = [7252117654, 6563936773]

client = TelegramClient('client', api_id, api_hash).start(bot_token=bot_token)

@client.on(events.NewMessage(pattern="^/start$"))
async def start(event):
    photo_url = 'https://i.hizliresim.com/4fw6vm3.jpg'
    welcome_text = ("Merhaba Ben Etiket Botuyum,\n\n"
                    "Sizin için etiketleme işlemi yaparım ayrıca özel mesajlar ile :)")
    buttons = [
        [Button.url('📣 Destek Sunucumuz', 'https://t.me/kiyicitayfaa'), 
         Button.url('❤️‍🔥 Sahip', 'https://t.me/Officialkiyici')],
        [Button.inline('❔ Komutlar', b'commands')]
    ]
    await client.send_file(event.chat_id, photo_url, caption=welcome_text, buttons=buttons)

@client.on(events.CallbackQuery(data=b'commands'))
async def commands(event):
    helptext = "**Komutlar**\n\n" \
               "/tag <mesaj> - Sunucudaki herkesi etiketleyerek belirtilen mesajı gönderir.\n" \
               "/mtag - Sunucudaki herkesi etiketleyerek rastgele cümleler gönderir.\n" \
               "/iptal - Devam eden etiketleme işlemini durdurur.\n" \
               "/eros - Eros oyununu başlatır ve rastgele kişileri eşleştirir\n" \
               "/tokat - Rastgele eğlenceli eylemler gerçekleştirir"
    await event.edit(helptext)

@client.on(events.NewMessage(pattern="^/reklam ?(.*)"))
async def reklam(event):
    if event.sender_id not in allowed_users:
        return await event.respond("Bu komutu kullanma izniniz yok!")

    msg = event.pattern_match.group(1)
    if not msg:
        return await event.respond("Bir mesaj belirtmelisiniz!")

    async for dialog in client.iter_dialogs():
        if dialog.is_group:
            try:
                await client.send_message(dialog.id, msg)
                await asyncio.sleep(1)  # Her grup arasında kısa bir bekleme süresi
            except Exception as e:
                LOGGER.error(f"Mesaj gönderilirken hata oluştu: {str(e)}")

    await event.respond("Reklam mesajı tüm gruplara gönderildi.")

@client.on(events.NewMessage(pattern="^/stats$"))
async def stats(event):
    if event.sender_id not in allowed_users:
        return await event.respond("Bu komutu kullanma izniniz yok!")

    group_count = 0
    user_count = 0

    async for dialog in client.iter_dialogs():
        if dialog.is_group:
            group_count += 1
            try:
                async for participant in client.iter_participants(dialog.id):
                    user_count += 1
            except Exception as e:
                LOGGER.error(f"Grup üyeleri alınırken hata oluştu: {str(e)}")

    stats_message = (f"📊 **Botun İstatistikleri**\n\n"
                    f"👥 Toplam Grup Sayısı: {group_count}\n"
                    f"👤 Toplam Kullanıcı Sayısı: {user_count}")

    await event.respond(stats_message)

print(">> BOT AKTİF <<")
client.run_until_disconnected()
