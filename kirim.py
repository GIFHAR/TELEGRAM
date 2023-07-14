from multiprocessing import context
import firebase_admin
from firebase_admin import credentials
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from firebase_admin import db
from telegram import Bot
import schedule
import time
from multiprocessing import Process

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://angelica-c9620-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

# Telegram bot token
TOKEN = '5437326616:AAHqAczdPMH_6nP1frR46v6Oa-S3ZDsfpbs'
CHAT_ID = '1281100174'
bot = Bot(token=TOKEN)
updater = None
is_bot_running = False

previous_condition = None
message_sent = False

def start(update, context):
    global is_bot_running
    if is_bot_running:
        start_time = time.time()  
        time.sleep(0.10)
        elapsed_time = round((time.time() - start_time) * 1000, 2)  
        context.bot.send_message(chat_id=CHAT_ID, text=f"Bot masih dalam kondisi berjalan")
        context.bot.send_message(chat_id=CHAT_ID, text=f"Waktu respon: {elapsed_time}ms")
    else:
        is_bot_running = True
        start_time = time.time()  
        time.sleep(0.10)
        elapsed_time = round((time.time() - start_time) * 1000, 2)  
        context.bot.send_message(chat_id=CHAT_ID, text=f"Selamat Datang di Telkom Bot")
        send_battery_status()
        ac_voltdown()
        context.bot.send_message(chat_id=CHAT_ID, text=f"Waktu respon: {elapsed_time}ms")
        send_message_with_options(update, context)

def send_message_with_options(update, context):
    options = [[KeyboardButton("Cek Report Daily")],
              [KeyboardButton("Cek Kondisi Baterai")],
              [KeyboardButton("Cek Kondisi PLN")]]
    reply_markup = ReplyKeyboardMarkup(options, one_time_keyboard=True)
    context.bot.send_message(chat_id=CHAT_ID, text='Pilih opsi yang diinginkan :', reply_markup=reply_markup)

def handle_option(update, context):
    selected_option = update.message.text

    start_time = time.time()
    time.sleep(0.10)
    elapsed_time = round((time.time() - start_time) * 1000, 2)
    if selected_option == 'Cek Report Daily':
        data = cek_report_daily()  
        context.bot.send_message(chat_id=CHAT_ID, text=data)
        context.bot.send_message(chat_id=CHAT_ID, text=f"Waktu respon: {elapsed_time}ms")
        send_message_with_options(update, context)
    elif selected_option == 'Cek Kondisi Baterai':
        data = cek_kondisi_baterai()  
        context.bot.send_message(chat_id=CHAT_ID, text=data)
        context.bot.send_message(chat_id=CHAT_ID, text=f"Waktu respon: {elapsed_time}ms")
        send_message_with_options(update, context)
    elif selected_option == 'Cek Kondisi PLN':
        data = cek_kondisi_pln()  
        context.bot.send_message(chat_id=CHAT_ID, text=data)
        context.bot.send_message(chat_id=CHAT_ID, text=f"Waktu respon: {elapsed_time}ms")
        send_message_with_options(update, context)

def cek_report_daily():
    if is_bot_running == True:
        ref = db.reference('/test')
        data = ref.get()

        daya_pln = data.get('Daya PLN')
        daya_discharging = data.get('Daya Discharge')
        daya_charging1 = data.get('Daya Charge Batt 1')
        daya_charging2 = data.get('Daya Charge Batt 2')
        daya_charging3 = data.get('Daya Charge Batt 3')
        daya_charging4 = data.get('Daya Charge Batt 4')
        soc1 = data.get('SOC Batt 1')
        soc2 = data.get('SOC Batt 2')
        soc3 = data.get('SOC Batt 3')
        soc4 = data.get('SOC Batt 4')
        soh1 = data.get('SOH Batt 1')
        soh2 = data.get('SOH Batt 2')
        soh3 = data.get('SOH Batt 3')
        soh4 = data.get('SOH Batt 4')
        cc1 = data.get('Cycle Count Batt 1')
        cc2 = data.get('Cycle Count Batt 2')
        cc3 = data.get('Cycle Count Batt 3')
        cc4 = data.get('Cycle Count Batt 4')

        report1 = f"Report Daily:\nDaya PLN: {daya_pln}\nDaya Discharge: {daya_discharging}\nDaya Charge Batt 1: {daya_charging1}\nDaya Charge Batt 2: {daya_charging2}\nDaya Charge Batt 3: {daya_charging3}\nDaya Charge Batt 4: {daya_charging4}\nSOC Batt 1: {soc1}\nSOC Batt 2: {soc2}\nSOC Batt 3: {soc3}\nSOC Batt 4: {soc4}\nSOH Batt 1: {soh1}\nSOH Batt 2: {soh2}\nSOH Batt 3: {soh3}\nSOH Batt 4: {soh4}\nCycle Count Batt 1: {cc1}\nCycle Count Batt 2: {cc2}\nCycle Count Batt 3: {cc3}\nCycle Count Batt 4: {cc4}"
        return report1

def cek_kondisi_baterai():
    if is_bot_running == True:
        ref = db.reference('/test')
        data = ref.get()

        arus_batt1 = data.get('Arus Batt 1')
        arus_batt2 = data.get('Arus Batt 2')
        arus_batt3 = data.get('Arus Batt 3')
        arus_batt4 = data.get('Arus Batt 4')
        tegangan_batt1 = data.get('Tegangan Batt 1')
        tegangan_batt2 = data.get('Tegangan Batt 2')
        tegangan_batt3 = data.get('Tegangan Batt 3')
        tegangan_batt4 = data.get('Tegangan Batt 4')
        daya_charging1 = data.get('Daya Charge Batt 1')
        daya_charging2 = data.get('Daya Charge Batt 2')
        daya_charging3 = data.get('Daya Charge Batt 3')
        daya_charging4 = data.get('Daya Charge Batt 4')
        soc1 = data.get('SOC Batt 1')
        soc2 = data.get('SOC Batt 2')
        soc3 = data.get('SOC Batt 3')
        soc4 = data.get('SOC Batt 4')
        soh1 = data.get('SOH Batt 1')
        soh2 = data.get('SOH Batt 2')
        soh3 = data.get('SOH Batt 3')
        soh4 = data.get('SOH Batt 4')
        cc1 = data.get('Cycle Count Batt 1')
        cc2 = data.get('Cycle Count Batt 2')
        cc3 = data.get('Cycle Count Batt 3')
        cc4 = data.get('Cycle Count Batt 4')
        kondisi_batt1 = data.get('Kondisi Batt 1')
        kondisi_batt2 = data.get('Kondisi Batt 2')
        kondisi_batt3 = data.get('Kondisi Batt 3')
        kondisi_batt4 = data.get('Kondisi Batt 4')
        
        report2 = f"Cek Kondisi Baterai:\nArus Batt 1: {arus_batt1}\nArus Batt 2: {arus_batt2}\nArus Batt 3: {arus_batt3}\nArus Batt 4: {arus_batt4}\nTegangan Batt 1: {tegangan_batt1}\nTegangan Batt 2: {tegangan_batt2}\nTegangan Batt 3: {tegangan_batt3}\nTegangan Batt 4: {tegangan_batt4}\nDaya Charge Batt 1: {daya_charging1}\nDaya Charge Batt 2: {daya_charging2}\nDaya Charge Batt 3: {daya_charging3}\nDaya Charge Batt 4: {daya_charging4}\nSOC Batt 1: {soc1}\nSOC Batt 2: {soc2}\nSOC Batt 3: {soc3}\nSOC Batt 4: {soc4}\nSOH Batt 1: {soh1}\nSOH Batt 2: {soh2}\nSOH Batt 3: {soh3}\nSOH Batt 4: {soh4}\nCycle Count Batt 1: {cc1}\nCycle Count Batt 2: {cc2}\nCycle Count Batt 3: {cc3}\nCycle Count Batt 4: {cc4}\nKondisi Batt 1: {kondisi_batt1}\nKondisi Batt 2: {kondisi_batt2}\nKondisi Batt 3: {kondisi_batt3}\nKondisi Batt 4: {kondisi_batt4}"
        return report2   

def cek_kondisi_pln():
    if is_bot_running == True:
        ref = db.reference('/test')
        data = ref.get()
        
        daya_pln = data.get('Daya PLN')
        arus_pln = data.get('Arus DC')
        tegangan_pln = data.get('Tegangan AC')
        kondisi_pln = data.get('Kondisi')

        report3 = f"Cek Kondisi PLN:\nDaya PLN: {daya_pln}\nArus PLN: {arus_pln}\nTegangan PLN: {tegangan_pln}\nKondisi PLN: {kondisi_pln}"
        return report3

def send_battery_status():
    
    global previous_condition
    global message_sent
    
    ref = db.reference('/test')
    data = ref.get()

    kondisi_batt1 = data.get('Kondisi Batt 1')
    kondisi_batt2 = data.get('Kondisi Batt 2')
    kondisi_batt3 = data.get('Kondisi Batt 3')
    kondisi_batt4 = data.get('Kondisi Batt 4')
    
    if previous_condition is None:
        previous_condition = [None, None, None, None, None, None]
        
    if kondisi_batt1 != previous_condition[0]:  # Check if the condition has changed
        
        if kondisi_batt1 == 'Charging':
            bot.send_message(chat_id=CHAT_ID, text="Batterai 1 dalan kondisi Charging")
    
            daya_charging1 = data.get('Daya Charge Batt 1')
            soc1 = data.get('SOC Batt 1')


            report_message = f"Report Baterai 1 :\nSOC Batt 1: {soc1}\nDaya Charge Batt 1: {daya_charging1}\n"
            bot.send_message(chat_id=CHAT_ID, text=report_message)
            start_time = time.time()
            time.sleep(0.10)
            elapsed_time = round((time.time() - start_time) * 1000, 2)
            bot.send_message(chat_id=CHAT_ID, text=f"Waktu respon: {elapsed_time}ms")
        previous_condition[0] = kondisi_batt1
            # message_sent = True

    if kondisi_batt2 != previous_condition[1]:  # Check if the condition has changed
        
        if kondisi_batt2 == 'Charging':
            bot.send_message(chat_id=CHAT_ID, text="Batterai 2 dalan kondisi Charging")

            daya_charging2 = data.get('Daya Charge Batt 2')
            soc2 = data.get('SOC Batt 2')


            report_message = f"Report Baterai 2 :\nSOC Batt 2: {soc2}\nDaya Charge Batt 2: {daya_charging2}\n"
            bot.send_message(chat_id=CHAT_ID, text=report_message)
            start_time = time.time()
            time.sleep(0.10)
            elapsed_time = round((time.time() - start_time) * 1000, 2)
            bot.send_message(chat_id=CHAT_ID, text=f"Waktu respon: {elapsed_time}ms")
        previous_condition[1] = kondisi_batt2
            # message_sent = True

    if kondisi_batt3 != previous_condition[2]:  # Check if the condition has changed
        
        if kondisi_batt3 == 'Charging':
            bot.send_message(chat_id=CHAT_ID, text="Batterai 3 dalan kondisi Charging")

            daya_charging3 = data.get('Daya Charge Batt 3')
            soc3 = data.get('SOC Batt 3')


            report_message = f"Report Baterai 3 :\nSOC Batt 3: {soc3}\nDaya Charge Batt 3: {daya_charging3}\n"
            bot.send_message(chat_id=CHAT_ID, text=report_message)
            start_time = time.time()
            time.sleep(0.10)
            elapsed_time = round((time.time() - start_time) * 1000, 2)
            bot.send_message(chat_id=CHAT_ID, text=f"Waktu respon: {elapsed_time}ms")
        previous_condition[2] = kondisi_batt3
            # message_sent = True
              
    if kondisi_batt4 != previous_condition[3]:  # Check if the condition has changed
        
        if kondisi_batt4 == 'Charging':
            bot.send_message(chat_id=CHAT_ID, text="Batterai 4 dalan kondisi Charging")

            daya_charging4 = data.get('Daya Charge Batt 4')
            soc4 = data.get('SOC Batt 4')


            report_message = f"Report Baterai 4 :\nSOC Batt 4: {soc4}\nDaya Charge Batt 4: {daya_charging4}\n"
            bot.send_message(chat_id=CHAT_ID, text=report_message)
            start_time = time.time()
            time.sleep(0.10)
            elapsed_time = round((time.time() - start_time) * 1000, 2)
            bot.send_message(chat_id=CHAT_ID, text=f"Waktu respon: {elapsed_time}ms")
        previous_condition[3] = kondisi_batt4
            # message_sent = True 
    
    if [kondisi_batt1, kondisi_batt2, kondisi_batt3, kondisi_batt4] != previous_condition[4]: 
        if all(status == 'Charging' for status in [kondisi_batt1, kondisi_batt2, kondisi_batt3, kondisi_batt4]):
            bot.send_message(chat_id=CHAT_ID, text='Kondisi Semua Baterai Charging')
            start_time = time.time()
            time.sleep(0.10)
            elapsed_time = round((time.time() - start_time) * 1000, 2)
            bot.send_message(chat_id=CHAT_ID, text=f"Waktu respon: {elapsed_time}ms")
            previous_condition[4] = [kondisi_batt1, kondisi_batt2, kondisi_batt3, kondisi_batt4]   
            # message_sent = True 
        
    if [kondisi_batt1, kondisi_batt2, kondisi_batt3, kondisi_batt4] != previous_condition[5]:  # Check if the condition has changed
        if any(status == 'Discharging' for status in [kondisi_batt1, kondisi_batt2, kondisi_batt3, kondisi_batt4]):
            daya_charging1 = data.get('Daya Charge Batt 1')
            daya_charging2 = data.get('Daya Charge Batt 2')
            daya_charging3 = data.get('Daya Charge Batt 3')
            daya_charging4 = data.get('Daya Charge Batt 4')
            soc1 = data.get('SOC Batt 1')
            soc2 = data.get('SOC Batt 2')
            soc3 = data.get('SOC Batt 3')
            soc4 = data.get('SOC Batt 4')

            report_message = f"Kondisi Baterai Discharging :\nSOC Batt 1: {soc1}\nDaya Charge Batt 1: {daya_charging1}\n"
            report_message += f"SOC Batt 2: {soc2}\nDaya Charge Batt 2: {daya_charging2}\n"
            report_message += f"SOC Batt 3: {soc3}\nDaya Charge Batt 3: {daya_charging3}\n"
            report_message += f"SOC Batt 4: {soc4}\nDaya Charge Batt 4: {daya_charging4}\n"
            bot.send_message(chat_id=CHAT_ID, text=report_message)
            start_time = time.time()
            time.sleep(0.10)
            elapsed_time = round((time.time() - start_time) * 1000, 2)
            bot.send_message(chat_id=CHAT_ID, text=f"Waktu respon: {elapsed_time}ms")
            previous_condition[5] = [kondisi_batt1, kondisi_batt2, kondisi_batt3, kondisi_batt4]   
            # message_sent = True
        if all(status == 'Normal' for status in [kondisi_batt1, kondisi_batt2, kondisi_batt3, kondisi_batt4]):
            bot.send_message(chat_id=CHAT_ID, text='Kondisi Semua Baterai Normal')
            start_time = time.time()
            time.sleep(0.10)
            elapsed_time = round((time.time() - start_time) * 1000, 2)
            bot.send_message(chat_id=CHAT_ID, text=f"Waktu respon: {elapsed_time}ms")
            previous_condition[5] = [kondisi_batt1, kondisi_batt2, kondisi_batt3, kondisi_batt4]   
            # message_sent = True
            
       

def send_report_daily(context):
    data = cek_report_daily()
    bot.send_message(chat_id=CHAT_ID, text=data)
    start_time = time.time()
    time.sleep(0.10)
    elapsed_time = round((time.time() - start_time) * 1000, 2)
    context.bot.send_message(chat_id=CHAT_ID, text=f"Waktu respon: {elapsed_time}ms")

def schedule_report_daily(context):
    schedule.every().day.at("08:00").do(send_report_daily)
    start_time = time.time()
    time.sleep(0.10)
    elapsed_time = round((time.time() - start_time) * 1000, 2)
    context.bot.send_message(chat_id=CHAT_ID, text=f"Waktu respon: {elapsed_time}ms")

def stop_bot(update, context):
    ref = db.reference('/test')
    data = ref.get()
    kondisi = data.get('Kondisi')
    start_time = time.time()
    time.sleep(0.10)
    elapsed_time = round((time.time() - start_time) * 1000, 2)

    global is_bot_running
    if is_bot_running == True:
        if kondisi == 'AC Voltdown':
            ref.update({'Kondisi': 'AC Voltdown'})
            context.bot.send_message(chat_id=CHAT_ID, text="Kondisi PLN belum normal")
        else:
            context.bot.send_message(chat_id=CHAT_ID, text="Kondisi PLN sudah dalam keadaan normal")
        context.bot.send_message(chat_id=CHAT_ID, text="Bot telah berhenti")
        context.bot.send_message(chat_id=CHAT_ID, text=f"Waktu respon: {elapsed_time}ms")
        is_bot_running = False  
    else:
        context.bot.send_message(chat_id=CHAT_ID, text="Bot tidak dalam kondisi berjalan")
        context.bot.send_message(chat_id=CHAT_ID, text=f"Waktu respon: {elapsed_time}ms")

def ac_voltdown():
    
    global previous_condition
    global message_sent
    
    ref = db.reference('/test')
    data = ref.get()
    kondisi = data.get('Kondisi')
    
    if kondisi != previous_condition:  # Check if the condition has changed
        previous_condition = kondisi
    
        if kondisi == 'AC Voltdown':
            daya_discharging = data.get('Daya Discharge')
            soc1 = data.get('SOC Batt 1')
            soc2 = data.get('SOC Batt 2')
            soc3 = data.get('SOC Batt 3')
            soc4 = data.get('SOC Batt 4')
            report4 = f"Report PLN AC Voltdown:\nKondisi: {kondisi}\nDaya Discharge: {daya_discharging}\nSOC Batt 1: {soc1}\nSOC Batt 2: {soc2}\nSOC Batt 3: {soc3}\nSOC Batt 4: {soc4}"
            bot.send_message(chat_id=CHAT_ID, text=report4)
            start_time = time.time()
            time.sleep(0.10)
            elapsed_time = round((time.time() - start_time) * 1000, 2)
            bot.send_message(chat_id=CHAT_ID, text=f"Waktu respon: {elapsed_time}ms")
            message_sent = True

        elif kondisi == 'Normal':
            bot.send_message(chat_id=CHAT_ID, text='Kondisi PLN dalam keadaan Normal')
            start_time = time.time()
            time.sleep(0.10)
            elapsed_time = round((time.time() - start_time) * 1000, 2)
            bot.send_message(chat_id=CHAT_ID, text=f"Waktu respon: {elapsed_time}ms")  
            message_sent = True
    else:
        message_sent = False

def jobpln():
    while True:
        ac_voltdown()
        time.sleep(1)

def jobbaterai():
    while True:
        send_battery_status()
        time.sleep(1)
    
def main():
    global updater
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('stop', stop_bot))
    dispatcher.add_handler(CommandHandler('send_options', send_message_with_options))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_option))

    # Start the bot
    updater.start_polling()
    
    process1 = Process(target=jobpln)
    process2 = Process(target=jobbaterai)

    process1.start()
    process2.start()
    
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    main()
    
