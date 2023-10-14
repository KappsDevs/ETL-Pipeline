import pandas as pd
import requests
import json
import openai
import win32com.client as win32

""" --------------------------------------------------  Prepare  -------------------------------------------------- """

link_api = 'https://sdw-2023-prd.up.railway.app'

df = pd.read_csv('SDW.csv')      #read

user_ids = df["UserID"].tolist()

print(user_ids)                  #Testing

open_api_key = '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'

openai.api_key = open_api_key


""" --------------------------------------------------  Extract  -------------------------------------------------- """

# to get the user id 
def get_user(id):

    response = requests.get(f'{link_api}/users/{id}')  

    if response.status_code == 200:                  # successful request
        return response.json()
    else:
        return None

#to read each id and atribute to user if not none
users = [user for id in user_ids if (user :=  get_user(id)) is not None] 
print(json.dumps(users, indent=2))


""" -------------------------------------------------- Transform -------------------------------------------------- """

def generate_news(user):

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[                        

            {"role": "system",
            "content": "You are a great motivational mentor."},  # how do we want chatgpt to behave

            {"role": "user",                                        # what do we want the chatgpt to do
            "content": f"Create a message for the {user['name']} to motivate and inspire (maximum of 100 characters)"}
        ]
    )

    return completion.choices[0].message.content.strip('\"')


for user in users:
    news = generate_news(user)
    print(news)
    user['news'].append({                                   #to add the news to its users
        "icon": "https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/credit.svg",
        "description": news
    })


""" --------------------------------------------------  Load  -------------------------------------------------- """

def update_user(user): 

    response =  requests.put(f"{link_api}/users/{user['id']}",json=user) # to "put" back updated


    if response.status_code == 200:              
        return True
    else:
        return False

for user in users:                                         # only to check if was a sucess
    success = update_user(user)
    print(f"User {user['name']} updated? {success} ")



