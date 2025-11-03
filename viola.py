from customtkinter import *
from PIL import Image
from google import genai

API_KEY = "AIzaSyBdrmfptKVrylajFmTlnnZqT-eKv9jIwCE"
chathistory = "You are Viola - The most friendly AI Assistant. Give brief and concise responses, not detailed ones. Provide detailed responses only when asked. And don't put 'Viola:' before response."
client = genai.Client(api_key=API_KEY)

set_appearance_mode("light")
set_default_color_theme("blue")

root = CTk()
root.geometry("350x650")
root.title("Viola Chatbot")

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=0)
root.grid_columnconfigure(0, weight=1)

chat_frame = CTkScrollableFrame(master=root, fg_color="white", corner_radius=0)
chat_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

def add_message(text, sender="user"):
    if sender == "user":
        msg = CTkLabel(chat_frame, text=text, anchor="e",
                       justify="left", fg_color="white",
                       text_color="black", corner_radius=10,
                       font=("Arial", 13), wraplength=250, padx=10, pady=6)
        msg.pack(anchor="e", pady=4, padx=8)
    else:
        msg = CTkLabel(chat_frame, text=text, anchor="w",
                       justify="left", fg_color="#E3F2FD",
                       text_color="black", corner_radius=10,
                       font=("Arial", 13), wraplength=250, padx=10, pady=6)
        msg.pack(anchor="w", pady=4, padx=8)
    chat_frame.update_idletasks()
    chat_frame._parent_canvas.yview_moveto(1)

def send_to_gemini():
    global chathistory
    user_text = userinput.get("0.0", "end").strip()
    if user_text == "":
        return
    add_message(user_text, "user")
    userinput.delete("0.0", "end")
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=chathistory + "\nUser: " + user_text
        )
        bot_reply = response.text.strip()
    except Exception as e:
        bot_reply = "Sorry, something went wrong."
    add_message(bot_reply, "bot")
    chathistory += f"\nUser: {user_text}\nSapna: {bot_reply}"

input_frame = CTkFrame(master=root, fg_color="white")
input_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
input_frame.grid_columnconfigure(0, weight=1)
input_frame.grid_columnconfigure(1, weight=0)

userinput = CTkTextbox(master=input_frame,
                       corner_radius=20,
                       border_color="#90CAF9",
                       border_width=2,
                       height=60,
                       fg_color="white",
                       text_color="black")
userinput.grid(row=0, column=0, sticky="ew", padx=(0, 10))

sendbtn = CTkButton(master=input_frame,
                    text="Send",
                    corner_radius=20,
                    fg_color="#2196F3",
                    hover_color="#1976D2",
                    border_width=0,
                    width=60,
                    command=send_to_gemini)
sendbtn.grid(row=0, column=1)

add_message("Hello! How can I assist you today?", "bot")

root.mainloop()

