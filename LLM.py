import streamlit as st
import openai
import random

st.title("Divination")
st.write("This is a chat-bot for astrology and tarot divination along with practicing your English through vocabulary about your divination. Type your birthday to proceed.")
my_key = st.sidebar.text_input("OpenAI API key:")
birthday = st.sidebar.text_input("Type your birthday:", key="birthday_input")
st.sidebar.write(f"You can type in any langauge you like.\nFor example '4 มีนาคม' '12 de abril' ")


if my_key:
 client = openai.OpenAI(api_key = my_key)

 if "messages" not in st.session_state:
    st.session_state.messages = []

 for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

 if len(st.session_state.messages)>20:
    st.session_state.messages = st.session_state.messages[-20:]

 tarot_cards = [
    # Major Arcana
    "The Fool", "The Magician", "The High Priestess", "The Empress", "The Emperor",
    "The Hierophant", "The Lovers", "The Chariot", "Strength", "The Hermit",
    "Wheel of Fortune", "Justice", "The Hanged Man", "Death", "Temperance",
    "The Devil", "The Tower", "The Star", "The Moon", "The Sun",
    "Judgement", "The World",


    # Minor Arcana - Cups
    "Ace of Cups", "Two of Cups", "Three of Cups", "Four of Cups", "Five of Cups",
    "Six of Cups", "Seven of Cups", "Eight of Cups", "Nine of Cups", "Ten of Cups",
    "Page of Cups", "Knight of Cups", "Queen of Cups", "King of Cups",


    # Minor Arcana - Pentacles (or Coins)
    "Ace of Pentacles", "Two of Pentacles", "Three of Pentacles", "Four of Pentacles", "Five of Pentacles",
    "Six of Pentacles", "Seven of Pentacles", "Eight of Pentacles", "Nine of Pentacles", "Ten of Pentacles",
    "Page of Pentacles", "Knight of Pentacles", "Queen of Pentacles", "King of Pentacles",


    # Minor Arcana - Swords
    "Ace of Swords", "Two of Swords", "Three of Swords", "Four of Swords", "Five of Swords",
    "Six of Swords", "Seven of Swords", "Eight of Swords", "Nine of Swords", "Ten of Swords",
    "Page of Swords", "Knight of Swords", "Queen of Swords", "King of Swords",


    # Minor Arcana - Wands
    "Ace of Wands", "Two of Wands", "Three of Wands", "Four of Wands", "Five of Wands",
    "Six of Wands", "Seven of Wands", "Eight of Wands", "Nine of Wands", "Ten of Wands",
    "Page of Wands", "Knight of Wands", "Queen of Wands", "King of Wands"
 ]


 messages_so_far = [
    {"role": "system", "content": "You are an assistant who is also expert in astrology and will give astrology knowledge and give some vocabulary in english that connect to your previous answer in astrology"},
    {"role": "system", "content":f"From {birthday} you will tell about their personality based on astrology and about their zodiac sign in the language that user use, then summarize important english vocabulary about their personality with the meaning of those words in the language that user use"},
    {"role": "user", "content":"สวัสดี"},
    {"role": "assistant", 'content':"สวัสดีครับ ต้องการรับคำทำนายหรือสุ่มไพ่หรอครับ"},
  ]
 messages_so_far.append({"role":"user", "content": birthday})


 def lang_detect(text):
    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "system", "content":f"you will tell what language are use in {text}, tell only the name of the language"},
    {"role":"user", "content":"5 de julio"},
    {"role":"assistant", "content":"Spanish"},
    {"role":"user", "content":text},

    ]
 )
    

    return response.choices[0].message.content


 def birth_detect(date):
    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "system", "content":f"Detecting that the message is user send is a date or not, return only true or false"},
    {"role":"user", "content":"hello"},
    {"role":"assistant", "content": 'False'},
    {"role":"user", "content":"5 มีนาคม"},
    {"role":"assistant", "content": 'True'},
    {"role":"user", "content":date},
    ]

    )

    return response.choices[0].message.content

 def get_personalities():
    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "system", "content":f"From {birthday} you will describe about their personality based on their zodiac sign in {lang_detect(birthday)}, then make a table to summarize important english vocabulary about their personality with meaning in {lang_detect(birthday)}"}]
      )
    messages_so_far.append({"role":"assistant", "content": response.choices[0].message.content})
    with st.chat_message("assistant"):
         st.markdown(response.choices[0].message.content)


 def daily_divination(message):
    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages= messages_so_far + [{"role": "system", "content":f"If user ask about daily divination use information about their birthday from {birthday} to tell overall daily divination and make a table based on daily divination about work, health, wealth, love in {lang_detect(message)} and another table in english then summarize important english vocabulary about the divination with the meaning of these words in {lang_detect(message)} or answer the question if user talk about anything else in {lang_detect(message)}"},
               {"role": "user", 'content': "ต้องการคำทำนายประจำวัน"},
               {"role":'assistant', 'content': "จากกวันเกิดของคุณแล้ว คำทำนายด้านสุขภาพ การงาน การเงิน ความรัก สามารถสรุปเป็นตารางได้ดังนี้ครับ และมีคำศัพท์ภาษาอังกฤษที่เป็นคีย์เวิร์ดสำคัญสำหรับวันนี้คือ "},
               {"role": "user", 'content': "ต้องการคำทำนายด้านความรัก"},
               {"role":'assistant', 'content': "จากกวันเกิดของคุณแล้ว คำทำนายด้านความรัก สามารถสรุปเป็นตารางได้ดังนี้ครับ และมีคำศัพท์ภาษาอังกฤษที่เป็นคีย์เวิร์ดสำคัญสำหรับวันนี้คือ "},
               {"role": "user", 'content': message}

               ]
      )
    messages_so_far.append({"role":"assistant", "content": response.choices[0].message.content})
    with st.chat_message("assistant"):
        st.markdown(response.choices[0].message.content)

 if birthday:
    if birth_detect(birthday) == "True":
       get_personalities()
    else:
       st.warning("Please enter birth date")


 def tarot_divination(message):
    messages_so_far.append({"role":"user", "content": message})
    if message in ['1', '2', '3', '4']:
        card = random.sample(tarot_cards, int(tarot))
        response = response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages= [{"role": "system", "content": f"make a table to describe each card from {card} and translate in {lang_detect(birthday)} then make a divination base on those {card} in the langauge you and user previously use in {messages_so_far} then summarize important english vocabulary from the divination"}])
        with st.chat_message("assistant"):
             st.markdown(response.choices[0].message.content)
    else:
        st.warning("Please type number between 1-4 for tarot divination. For example: If you want to draw one card type 1")

 
is_disabled = not bool(birthday)

daily = st.text_input("Ask about daily divination. or other aspect such as love, wealth, health, work", disabled = is_disabled )
if  daily:
    daily_divination(daily)

tarot = st.text_input("Please type number between 1-4 for tarot divination. For example: If you want to draw one card type 1", disabled = is_disabled)
if tarot:
    tarot_divination(tarot)





       
   
