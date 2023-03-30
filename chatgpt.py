import openai


class ChatGpt:
    def __init__(self, model="gpt-3.5-turbo", max_tokens=3800, stop=None, temperature=0.7):
        self.model = model
        self.max_tokens = max_tokens
        self.stop = stop
        self.temperature = temperature

    def question(self, prompt=any):
        message = ""
        try:
            openai.api_key = "YOUR_API_KEY"
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0301",
                max_tokens=3800,
                stop=None,
                temperature=0.7,
                messages=[{"role": "user", "content": prompt}]
            )
            message = response['choices'][0]['message']['content']
            return message
        except:
            message = "error"
            return message
