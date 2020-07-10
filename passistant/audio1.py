import speech_recognition as speech
import webbrowser
import pyttsx3
import pyjokes as jokes
import smtplib
from email.message import EmailMessage
import sys
from PIL import ImageTk, Image
from tkinter import font

import tkinter as gui
root=gui.Tk()
root.minsize(height=root.winfo_screenheight(),width=root.winfo_screenwidth())
root.configure(background='#1f1f1f')
root.title('Assistant-created by Starki')
im = ImageTk.PhotoImage(Image.open("green.png"))
im2 = ImageTk.PhotoImage(Image.open("red.png"))
heading=font.Font(family='Roboto Condensed',size=40,weight='bold')
subhead=font.Font(family='Roboto Condensed',size=20,weight='bold')
content=font.Font(family='Roboto Condensed',size=15,weight='bold')
content2=font.Font(family='Roboto Condensed',size=10,weight='bold')

engine = pyttsx3.init()
samplerate=48000
chunksize=32
#function to take out numbers from a string



def convert(s):
        
    
    i=0
    
    num=[]
    while i<len(s):
    
        try:
            x=''
            while i<len(s) and s[i].isspace()==False :
                
                if i<len(s):
                    if s[i].isdigit()==True:
                        x+=s[i]    
                        i+=1
                    else:
                        i+=1 
            #print(x) 
            else:
                i+=1
            if len(x)>0:
                num.append(int(x))        
    
        except IndexError:
            pass
        
    return num     
#end of function convert

def outres(s):
    gui.Label(root,font=content2,anchor='w',bg='BLACK',fg='white',text=s).place(width=1000,relx=0,rely=0.68)
        
    root.update() 
    
def outcomma(s):
    gui.Label(root,text=s,font=content2,bg='BLACK',fg='white',anchor='w').place(width=1000,relx=0,rely=0.5)
        
def outunder(s):
    gui.Label(root,font=content2,bg='BLACK',fg='white',text=s,anchor='w').place(width=1000,relx=0,rely=0.6)

#function to record audio
def record():
    
    s=speech.Recognizer()
    with speech.Microphone(sample_rate=samplerate,chunk_size=chunksize) as source:
        s.adjust_for_ambient_noise(source)
        #print("say something")
        gui.Label(root,text="say something",bg="#1f1f1f",fg='green',font=subhead).place(relx=0.1,rely=0.3)   
        gui.Label(root,image=im,bg='#1f1f1f').place(relx=0.14,rely=0.2)
       
        root.update()
        audio=s.listen(source)     
        t = s.recognize_google(audio) 
        t.lower()
        #gui.Label(root,text=t,bg='red').place(relx=0.5,rely=0.5)
        if t.__contains__('exit'):
            engine.say("ok sir")
            engine.runAndWait()
            sys.exit()
        gui.Label(root,text="not listening",bg='#1f1f1f',fg="red",font=subhead,anchor='w').place(width=300,relx=0.1,rely=0.3)   
        gui.Label(root,image=im2,bg='#1f1f1f').place(relx=0.14,rely=0.2)
        gui.Label(root,text=t,font=content2,bg='black',fg='white').place(relx=0,rely=0.5)
        outcomma(t)
        outunder(t)   
        root.update()
        #outres(t)   
    
        return t
#end of audio record function            


    
#mailing section
def emailfun():
    try:
        try:
            email=''
            engine.say("sir i need the mailing address")
            engine.runAndWait()
            email=record()
            
            email=email.replace(" ","")
            outres(email)
        
        except speech.UnknownValueError:
           
            pass
        
        while True:
            try:
                
                    
                engine.say("sir is the mailing address correct.")
                #print(email)
                engine.say(email)
                engine.runAndWait()
                response=record()
                
                if response.__contains__("yes"):
                    break
                elif response.__contains__("no"):
                    engine.say("sir please repeate the email ")
                    engine.runAndWait()
                    email=record()
                    email=email.replace(" ","")
                    outres(email)
            except speech.UnknownValueError:
                continue
        
        
        #subject       
        try:
            sub=''
            engine.say("sir what will be the subject")
            engine.runAndWait()
            sub=record()
            outres(sub)
        except speech.UnknownValueError:
            
            pass
        except UnboundLocalError:
            sub="no subject given"
            
        if sub.__contains__("no"):
            pass
        else:
            while True:
                try:
                    engine.say("sir is the subject correct")
                    engine.runAndWait()
                    #print(sub)
                    response=record()
                    if response.__contains__("no"):
                        engine.say("sir please repeate the subject.")
                        engine.runAndWait()
                        sub=record()
                        outres(sub)
                    else:
                        break
                except speech.UnknownValueError:
                    continue
        
        
        #message
        try:
            message=''
            engine.say("sir what is the message")
            engine.runAndWait()
            message=record()
            outres(message)
        except speech.UnknownValueError:
            pass
        except UnboundLocalError:
            pass
        
        while True:
            try:
                #print(message)
                engine.say("sir is the message correct")
                engine.say(message)
                engine.runAndWait()
                response=record()
                
                if response.__contains__("yes"):
                    break
                elif response.__contains__("no"):
                    engine.say("sir please repeate the message")
                    engine.runAndWait()
                    message=record()
                    outres(message)
            except speech.UnknownValueError:
                continue
        
        
        mail=EmailMessage()
        mail["from"]="starki"
        mail["to"]=email
        mail["subject"]=sub
        mail.set_content(message)
        
        with smtplib.SMTP(host='smtp.gmail.com',port=587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login('email addres of the account from which to send the mail','password of thata account')
            smtp.send_message(mail)        
        engine.say("mail sent")
        outres('mail sent')
        engine.runAndWait()
    except ConnectionError:
        emailfun()        
#end of mailing section

#filter text function
def filtertext(text):
    t=''
    if text.__contains__('what do you mean by'):
        t=text.replace("what do you mean by","")
    elif text.__contains__("Google"):
        t=text.replace("Google","")
    #print(text)    
    return t        
#end of filter text function


#copyfunction
def copyfun(text):
    try:
        engine.say("tell me the location")
        engine.runAndWait()
        location=record()
    except speech.UnknownValueError:
        copyfun(text)    
    #end of copy function
def main():
    #start of main section
    while True:
        
        try:
            gui.Label(root,text="Assistant",font=heading,bg="#1f1f1f",fg='#8DA05E').place(height=90,relx=0.1,rely=0)
            gui.Label(root,bg='#1f1f1f',fg="#8DA05E",text="your commands").place(relx=0,rely=0.45)
            #gui.Label(root,text='',font=content2,bg='BLACK',fg='white').place(width=1000,relx=0,rely=0.5)
            outcomma('')
            
            gui.Label(root,bg='#1f1f1f',fg="#8DA05E",text="what i understood").place(relx=0,rely=0.55)
            # gui.Label(root,font=content2,bg='BLACK',fg='white',text='').place(width=1000,relx=0,rely=0.6)
            outunder('')
            gui.Label(root,font=content2,bg='#1f1f1f',fg='#8DA05E',text='result',anchor='w').place(width=680,relx=0,rely=0.64)
            
            #list of commands
            gui.Label(root,font=subhead,bg="#1f1f1f", fg="#8DA05E",text="LIST OF COMMANDS").place(relx=0.5,rely=0.1)
            #gui.Label(root,font=content,bg="#1f1f1f", fg="#8DA05E",text=commands,anchor='e').place(width=700,relx=0.5,rely=0.2)
            gui.Label(root,font=content2,bg="#1f1f1f", fg="#8DA05E",text="1)exit:for closing the application",anchor='w').place(width=700,relx=0.5,rely=0.2)
            gui.Label(root,font=content2,bg="#1f1f1f", fg="#8DA05E",text="2)what you can do or tell me about yourself:introduction of application",anchor='w').place(width=700,relx=0.5,rely=0.23)
            gui.Label(root,font=content2,bg="#1f1f1f", fg="#8DA05E",text="3)tell me a joke",anchor='w').place(width=700,relx=0.5,rely=0.26)
            gui.Label(root,font=content2,bg="#1f1f1f", fg="#8DA05E",text="4)google (what you want to google):for searchin the internet",anchor='w').place(width=700,relx=0.5,rely=0.29)
            gui.Label(root,font=content2,bg="#1f1f1f", fg="#8DA05E",text="5)any statement that contains add,multiply,product,division can be used for performing mathematcal ",anchor='w').place(width=900,relx=0.5,rely=0.32) 
            #gui.Label(root,font=content2,bg="#1f1f1f", fg="#8DA05E",text="",anchor='w').place(width=700,relx=0.5,rely=0.50) 
            gui.Label(root,font=content2,bg="#1f1f1f", fg="#8DA05E",text="operation between two numbers like: add 2 and 3 or find me the product of 2 nd 3 ",anchor='w').place(width=900,relx=0.5,rely=0.35)
            gui.Label(root,font=content2,bg="#1f1f1f", fg="#8DA05E",text="6)can send mail by using words like email or mail example:send a mail for me",anchor='w').place(width=700,relx=0.5,rely=0.38)
            gui.Label(root,font=content,anchor='w',bg="#1f1f1f" ,fg="orange",text="if not working ,try to speak when mike symbol is displayed on the right corner of your task-bar").place(relx=0.1,rely=0.8)
            root.update()
            outres('')
            text=record()
            outunder(text)
            #gui.Label(root,font=content2,text=text,bg='BLACK',fg='white').place(relx=0,rely=0.6)
            root.update()
            
            
            #print ("you said: " + text) 
            #exit command    
            if text=="exit" or text.__contains__('exit') or text=="ok exit" or text=="go to sleep":
                engine.say("ok sir")
                engine.runAndWait()
                break
            else:
                
                if text=="tell me about my friends":
                    #engine.setProperty('rate', 140)
                    engine.say("your roomate is aiman")
                    engine.say("and he is chutiiya")
                    engine.say(" and your neighbours are rishabh and manish and both of them are gaandu")
                    engine.setProperty('rate', 200)
                    # rate = engine.getProperty('rate')   # getting details of current speaking rate
                    # print (rate) 
                    engine.runAndWait()
                
                #about assisitant
                elif text.__contains__('you can do') or text.__contains__('you do') or text.__contains__('yourself'):
                    engine.say("sir i am you assistant and i am here to help you.")
                    engine.say("i can do basic calculation like addition,subtraction,multiplication and divison")
                    engine.say("sir i can also send mails for you.")
                    engine.runAndWait()
                    
                #what to say on thank u       
                elif text=="thank you" or text.__contains__('thank'):
                    engine.say("no problem sir")   
                    engine.runAndWait()
                
                #conversation
                elif text.__contains__('hello') or text.__contains__('hii'):
                    engine.say('hello sir')
                    engine.runAndWait()
                
                elif  (text.__contains__('are') and text.__contains__('you')):
                    engine.say("sir i am your assistant.")
                    engine.say('i can do calculation,can send mail,can google stuffs and crack some jokes for you')
                    engine.runAndWait()     
                #joking section    
                elif text.__contains__("joke") or text.__contains__("humour"):
                    engine.setProperty("rate",180)
                    s=jokes.get_joke()
                    engine.say(s)
                    outres(s)
                    engine.runAndWait()    
                    
                    engine.setProperty("rate",200)
                
                #addition section
                elif text.__contains__('add') or text.__contains__('some') or text.__contains__('Add') or text.__contains__('sum') or text.__contains__('plus') or text.__contains__('+') :
                    x=convert(text)
                    
                    engine.say(sum(x)) 
            
                    outres(str(sum(x))) 
                     
                    engine.runAndWait()
                    
                #subtraction section    
                elif text.__contains__('minus') or text.__contains__('subtract') or  text.__contains__('-') :
                    x=convert(text)
                    
                    engine.say(x[0]-x[1])   
                    outres(str(x[0]-x[1]))
                    engine.runAndWait()
                    
                #multiplication section      
                elif text.__contains__('product') or text.__contains__('multiply') or  text.__contains__('*')or  text.__contains__('times') :
                    x=convert(text)
                    pro=1
                    for i in x:
                        pro*=i
                    engine.say(pro)   
                    outres(str(pro))
                    engine.runAndWait()
                    
                #division section       
                elif text.__contains__('divide') or text.__contains__('divided') or  text.__contains__('/') :
                    x=convert(text)
                    
                    engine.say(x[0]/x[1])
                    outres(str(x[0]/x[1]))   
                    engine.runAndWait()
                
                #mail section see function emailfun for implementation.    
                elif text.__contains__('email') or text.__contains__('mail'):
                    emailfun()     
                    
                #search internet
                elif text.__contains__('Google'):
                    
                    text2=filtertext(text)
                    #print(text2)
                    webbrowser.open_new("https://www.google.com/search?q="+text2)
                elif text.__contains__("Abhishek"):
                    engine.say("nooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo")
                    engine.runAndWait()   
                      
                else:
                    engine.say("am i getting it right")
                    engine.say("you said")
                    engine.say(text)
                    outres(text)
                    engine.runAndWait()
            
                return text   
             
        #error occurs when google could not understand what was said 
        
        except speech.UnknownValueError: 
            #print("Google Speech Recognition could not understand audio") 
            gui.Label(root,text="not listening",bg='#1f1f1f',fg="red",font=subhead,anchor='w').place(width=300,relx=0.1,rely=0.3)   
            gui.Label(root,image=im2,bg='#1f1f1f').place(relx=0.14,rely=0.2)
            root.update()
        except speech.RequestError as e: 
            pass
            #print("Could not request results from Google  Speech Recognition service; {0}".format(e)) 
         
if __name__=='__main__':        
    while True:
        main()
     