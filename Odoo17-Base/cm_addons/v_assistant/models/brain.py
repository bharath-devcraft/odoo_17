import pyttsx3
import datetime
import wikipedia
import pyjokes
import os
from odoo import models, fields, api
from . import users_neura as u_neura
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


def execute_linux_command(command):
    # Use os.system() to execute the Linux command
    exit_code = os.system(command)
    return exit_code


def set_voice(voice_id):
    engine = pyttsx3.init()
    engine.setProperty('voice', voice_id)

def list_available_voices():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for voice in voices:
        print(f"Voice: {voice.name}")
        print(f" - ID: {voice.id}")
        #print(f" - Languages: {voice.languages}")

def talk(text):
    # ~ try:
        # ~ print("Sssssss2343223423432432",text)
        # ~ # Initialize the text-to-speech engine
        # ~ engine = pyttsx3.init()
        # ~ # Set properties (optional)
        # ~ engine.setProperty('rate', 150)  # Speed of speech (words per minute)
        # ~ engine.setProperty('volume', 1.0)  # Volume level (0.0 to 1.0)
        # ~ # Say the given text
        # ~ engine.say(text)
        # ~ # Wait for the speech to complete
        # ~ engine.runAndWait()
    # ~ except:
        # ~ # Example usage:
        # ~ command_to_execute = 'espeak -ven+f3 -s150 "%s"'%(text)  # Replace this with your desired Linux command
        # ~ execute_linux_command(command_to_execute)
    return text

def take_command():
    try:
        with sr.Microphone() as source:
            print('listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'alexa' in command:
                command = command.replace('alexa', '')
                print(command)
    except:
        pass
    return command


def run_alexa(env, req):
    command = req.lower().strip()
    if 'play' in command:
        song = command.replace('play', '')
        return talk('playing ' + song)
        #pywhatkit.playonyt(song)
    elif 'hi' in command or 'hello' in command or 'hey' in command or 'giant' in command or 'hai' in command:
        v="Hello!! how can i help you! Ask something like,\n\
                    Time - current time. \n\
                    Date - current date. \n\
                    Joke - to say jokes. \n\
                    Users Count - To know application users count. \n\
                    Transaction Count - To know application Transaction count. \n\
                    Today Transaction - To know application Transaction count of today. \n\
                    unit price of the product 'Product name AAA' - This product current price is XXXX. \n\
                    "
        return talk(v)

    elif 'today transaction' in command or 'today approved' in command or 'today count' in command:
        trans_count = env['ct.transaction'].search([('status','=','approved'),('ap_rej_date', '>=', fields.Date.today())])
        count = 0
        net_amt= 0
        for trans in trans_count:
            count +=1
            net_amt += trans.net_amt
        return talk('Today approved transaction count is %s , with the value of : %s' % (str(count),str(round(net_amt,2))))
    
    elif 'transaction count' in command or 'transaction' in command:
        trans_count = env['ct.transaction'].search_count([])
        return talk('This application has %s transactions. would you like to know today approved count?' % str(trans_count))
    
    elif 'product ' in command or 'unit price' in command or 'price' in command:
        print("ssssssssssssssssssssssssssss")
        import re
        match = re.search(r"product\s+'(.+)'", command)
        product_name = match.group(1)
        product_name = product_name.upper()
        env.cr.execute(""" select id
        from product_template where upper(name ->> 'en_US') = '%s'""" %(str(product_name)))
        data = env.cr.dictfetchall()
        print("ssssssssssssssssssssssssssss",data)
        for pros in data:        
            pro = env['product.template'].search([('id','=',pros['id'])])
        
            return talk('This product current price is %s' % str(pro.list_price))
    

    elif 'time' in command:
        new_time = datetime.now() + timedelta(hours=5, minutes=30)
        time = new_time.strftime('%I:%M %p')
        return talk('Current time is ' + time)
    elif 'who the heck is' in command:
        person = command.replace('who the heck is', '')
        info = wikipedia.summary(person, 1)
        return talk(info)
    elif 'date' in command:
        current_date = (datetime.now() + timedelta(hours=5, minutes=30)).date().strftime('%d/%m/%y')
        print('ssssssssssssssssssss',current_date)
        return talk('The Today date is '+str(current_date))
    elif 'are you single' in command:
        return talk('I am in a relationship with wifi')
    elif 'joke' in command:
        return talk(pyjokes.get_joke())
    elif 'change your voice' in command:
        list_available_voices()
        return talk('choose the voice ID listed below')
    elif 'users ' in command:
        return talk(u_neura.users_details())
    elif 'Thanks' in command or 'Thank you' in command:
        return talk("Welcome, Happy to assist you!!")
    else:
        return talk("I'm unable to understand, please provide more details")


