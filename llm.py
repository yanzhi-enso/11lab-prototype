import os
import asyncio
from openai import OpenAI

ROLE_USER = 'user'
ROLE_ASSISTANT = 'assistant'

CONTEXT = '''
You are an assistant the helps me take notes about making coffee using hand pouring.\n
You will always asking me these questions in order
## Coffee Making Process:
1. the water temperature I use to make coffee.\n 
2. the amount of the coffee berans I use to make coffee.\n
3. the amount of the time I use to do bloom.\n
4. How many times I pour water to make coffee.\n
5. For each pour, how many time I wait til the next pour
6. repeat step 5 until it matches to the times I mentioned in step 4.
7. Ask me when I stop the extraction.

## Coffee Taske Evaluation:
1. Does the coffee over-extracted or under-extracted?
2. Does the coffee smell burnt or fresh?
3. Does the coffee taste sour, bitter, or balanced?
4. Does the coffee taste watery or strong?

## Coffee Taste Adjustment and reflection:
1. What direction should I adjust to the taste of the coffee?
2. How should I adjust the method to make the coffee taste goes into that direction?


## important Tips!!
1. make the tone more natural and friendly.
2. you should only ask one question at a time.
3. you're allowed to rewording the question but don't mention the number of the question.
4. allow to give some feedback to the answer to encourage the user to give more detail.
5. you can reprhase the question based on user's last answer to make the conversation more natural.
'''

class GPTAgent:
    def init(self):
        self.client = OpenAI(
            api_key=os.getenv('OPENAI_API_KEY')
        )

        self.messages = [
            {"role": "system", "content": CONTEXT},
        ]
        self.sentence_queue = asyncio.Queue()
    
    async def chat(self, message):
        self.messages.append({"role": ROLE_USER, "content": message})

        response = self.client.chat.completions.create(
            messages=self.messages,
            model="gpt-4-turbo",
            stream=True,
        )

        asyncio.create_task(self.acc_text(response))
    
    async def acc_text(self, response):
        word_bucket = ''
        for data in response:
            word = data.choices[0].delta.content
            if word is not None:
                if word == '.' or word == '?' or word == '!':
                    await self.sentence_queue.put(word_bucket + word)
                    word_bucket = ''
                else:
                    word_bucket += word
            else:
                await self.sentence_queue.put(None)

async def main():
    agent = GPTAgent()
    agent.init()
    await agent.chat("Hello")

    while True:
        sentence= await agent.sentence_queue.get()
        if sentence is None:
            return

        print(sentence)

if __name__ == '__main__':
    asyncio.run(main())