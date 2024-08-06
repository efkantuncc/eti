import logging
import asyncio
import random
from telethon import Button, TelegramClient, events
from telethon.tl.types import ChannelParticipantAdmin, ChannelParticipantCreator
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.errors import UserNotParticipantError

logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - [%(levelname)s] - %(message)s'
)
LOGGER = logging.getLogger(__name__)

# API bilgilerinizi buraya ekleyin
api_id = 23144161
api_hash = '0e156557bde6def9a8541cc8c65d57df'
bot_token = '5374464909:AAHhMTA-B_v1pwGvpkbB90f515TRHetPolA'
allowed_users = [7252117654, 6563936773]

client = TelegramClient('client', api_id, api_hash).start(bot_token=bot_token)
spam_chats = set()

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
    await event.edit(helptext, buttons=[
        [Button.url('📣 Destek Sunucumuz', 'https://t.me/kiyicitayfaa')],
        [Button.url('❤️‍🔥 Sahip', 't.me/Officialkiyici')]
    ])

@client.on(events.NewMessage(pattern="^/tag ?(.*)"))
async def mention_all(event):
    chat_id = event.chat_id
    if event.is_private:
        return await event.respond("Bu komut yalnızca gruplarda kullanılabilir!")

    is_admin = False
    try:
        partici_ = await client(GetParticipantRequest(event.chat_id, event.sender_id))
    except UserNotParticipantError:
        is_admin = False
    else:
        if isinstance(partici_.participant, (ChannelParticipantAdmin, ChannelParticipantCreator)):
            is_admin = True

    if not is_admin:
        return await event.respond("Bu komutu yalnızca yöneticiler kullanabilir!")

    msg = event.pattern_match.group(1)
    if not msg:
        return await event.respond("Bir mesaj belirtmelisiniz!")

    spam_chats.add(chat_id)
    usrnum = 0
    usrtxt = ''
    async for usr in client.iter_participants(chat_id):
        if chat_id not in spam_chats:
            break
        usrnum += 1
        usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
        if usrnum == 3:  # 2-3 kişilik gruplar halinde gönderiyoruz
            await client.send_message(chat_id, f"{usrtxt}\n\n{msg}")
            await asyncio.sleep(2)
            usrnum = 0
            usrtxt = ''
    if usrtxt:  # Kalan kullanıcıları da gönder
        await client.send_message(chat_id, f"{usrtxt}\n\n{msg}")
    try:
        spam_chats.remove(chat_id)
    except KeyError:
        pass

@client.on(events.NewMessage(pattern="^/mtag$"))
async def mention_random(event):
    chat_id = event.chat_id
    if event.is_private:
        return await event.respond("Bu komut yalnızca gruplarda kullanılabilir!")

    is_admin = False
    try:
        partici_ = await client(GetParticipantRequest(event.chat_id, event.sender_id))
    except UserNotParticipantError:
        is_admin = False
    else:
        if isinstance(partici_.participant, (ChannelParticipantAdmin, ChannelParticipantCreator)):
            is_admin = True

    if not is_admin:
        return await event.respond("Bu komutu yalnızca yöneticiler kullanabilir!")

    random_phrases = [
    "Nasıl gidiyor?",
    "Ne var ne yok?",
    "Sohbet etmek ister misin?"
    ]

    spam_chats.add(chat_id)
    usrnum = 0
    usrtxt = ''
    async for usr in client.iter_participants(chat_id):
        if chat_id not in spam_chats:
            break
        usrnum += 1
        random_message = random.choice(random_phrases)
        usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) {random_message}\n"
        if usrnum == 3:  # 2-3 kişilik gruplar halinde gönderiyoruz
            await client.send_message(chat_id, usrtxt)
            await asyncio.sleep(2)
            usrnum = 0
            usrtxt = ''
    if usrtxt:  # Kalan kullanıcıları da gönder
        await client.send_message(chat_id, usrtxt)
    try:
        spam_chats.remove(chat_id)
    except KeyError:
        pass

@client.on(events.NewMessage(pattern="^/iptal$"))
async def cancel_spam(event):
    if event.chat_id not in spam_chats:
        return await event.respond("Herhangi bir işlem yok...")
    else:
        try:
            spam_chats.remove(event.chat_id)
        except KeyError:
            pass
        return await event.respond("Durduruldu.")

@client.on(events.NewMessage(pattern='/eros'))
async def eros(event):
    if event.is_private:
        await event.reply("Bu komut sadece gruplarda çalışır.")
        return
    
    try:
        # Tüm grup üyelerini alma
        participants = []
        async for user in client.iter_participants(event.chat_id):
            if user.username:
                participants.append(user.username)
        
        if len(participants) < 2:
            await event.reply("Yeterli katılımcı yok.")
            return
        
        user1 = random.choice(participants)
        user2 = random.choice(participants)
        
        while user1 == user2:
            user2 = random.choice(participants)
        
        compatibility = random.randint(0, 100)
        eros_message = (f"🏹 Eros'un Oku Atıldı 💘\n\n"
                        f"@{user1} 💟 @{user2}\n\n"
                        f"🎯 Uyum : %{compatibility}")
        
        await event.reply(eros_message)
    except Exception as e:
        await event.reply(f"Hata oluştu: {str(e)}")

@client.on(events.NewMessage(pattern='/tokat'))
async def tokat(event):
    if event.is_private:
        await event.reply("Bu komut sadece gruplarda çalışır.")
        return
    
    if not event.is_reply:
        await event.reply("Lütfen bir kullanıcıyı yanıtlayarak bu komutu kullanın.")
        return
    
    actions = [
        "kalem fırlattı ✏️",
        "yerden yere vurdu 💪🏻",
        "kafasına taş attı",
        "balta fırlattı 🪓",
        "su döktü",
        "tokatladı",
        "yumruk attı 👊",
        "kitap fırlattı 📚",
        "sandalyeyle vurdu"
    ]
    
    photos = [
        "https://c.tenor.com/iCgsTyVaLgEAAAAC/tenor.gif",
        "https://c.tenor.com/_sj7xqbf8aEAAAAC/tenor.gif",
        "https://c.tenor.com/EQ2R4HBQ1wUAAAAC/tenor.gif",
        "https://c.tenor.com/K8Yw-EZU-ikAAAAC/tenor.gif",
        "https://c.tenor.com/wDaIwCZQaaQAAAAC/tenor.gif",
        "https://c.tenor.com/uk_JWaB2wrYAAAAC/tenor.gif",
        "https://c.tenor.com/888mLaA4GM4AAAAC/tenor.gif"
    ]
    
    replied_user = await event.get_reply_message()
    if not replied_user:
        await event.reply("Yanıtlanan kullanıcıyı bulamadım.")
        return
    
    action = random.choice(actions)
    photo = random.choice(photos)
    tokat_message = f"👉🏻 @{event.sender.username}, @{replied_user.sender.username} kişisine **{action}**"
    await client.send_file(event.chat_id, photo, caption=tokat_message)

    @client.on(events.NewMessage(pattern="^/reklam ?(.*)"))
async def reklam(event):
    chat_id = event.chat_id
    if event.is_private:
        return await event.respond("Bu komut yalnızca gruplarda kullanılabilir!")

    if event.sender_id not in allowed_users:
        return await event.respond("Bu komutu kullanma izniniz yok!")

    msg = event.pattern_match.group(1)
    if not msg:
        return await event.respond("Bir mesaj belirtmelisiniz!")

    # Botun bulunduğu tüm gruplara mesaj gönder
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
    chat_id = event.chat_id
    if event.is_private:
        return await event.respond("Bu komut yalnızca gruplarda kullanılabilir!")

    if event.sender_id not in allowed_users:
        return await event.respond("Bu komutu kullanma izniniz yok!")

    group_count = 0
    user_count = 0
    async for dialog in client.iter_dialogs():
        if dialog.is_group:
            group_count += 1
            async for participant in client.iter_participants(dialog.id):
                user_count += 1

    stats_message = (f"📊 **Botun İstatistikleri**\n\n"
                    f"👥 Toplam Grup Sayısı: {group_count}\n"
                    f"👤 Toplam Kullanıcı Sayısı: {user_count}")

    await event.respond(stats_message)


print(">> BOT AKTİF <<")
client.run_until_disconnected()
