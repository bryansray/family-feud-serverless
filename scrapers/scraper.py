from bs4 import BeautifulSoup
# from urllib.request import urlopen
import requests
import json
import boto3
import random, string

class Question:
    def __init__(self, text):
        self.id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        self.text = text
        self.answers = []

    def add_answer(self, text, responses):
        answer = Answer(text, responses)
        self.answers.append(answer)

    def __str__(self):
        return f'Question: {self.text} : {len(self.answers)}'

class Answer:
    def __init__(self, text, responses):
        self.text = text
        self.responses = responses

    def __str__(self):
        return f'\tAnswer: {self.text} : {self.responses}\n'

class QuestionEncoder(json.JSONEncoder):
    def default(self, obj):
        return obj.__dict__

class Scraper:
    def __init__(self, url):
        page = requests.get(url)
        html = page.content #.read().decode("utf-8")
        self.soup = BeautifulSoup(html, "html.parser")

    def process(self):
        question_elements = self.__get_questions()
        questions = []

        for question_element in question_elements:
            table = question_element.findNext("table")
            if table is None:
                continue

            question = Question(question_element.get_text())
            
            answer_elements = table.find_all("tr")

            for answer_element in answer_elements:
                text = answer_element.findNext("td")
                responses = text.findNext("td")

                question.add_answer(text.get_text(), responses.get_text())

            questions.append(question)
        
        return questions

    def __get_questions(self):
        return self.soup.find_all("h2")[2::]


class Program:
    def run(self):
        scraper = Scraper("https://hobbylark.com/party-games/list-of-family-feud-questions")
        questions = scraper.process()

        question = questions

        dynamodb = boto3.resource('dynamodb')

        poll_table = dynamodb.Table('questions')

        with poll_table.batch_writer() as batch:
            for question in questions:
                batch.put_item(Item = {
                    'id': question.id,
                    'text': question.text,
                    'answers': [
                        
                    ]
                })

        # data = json.dumps(question, indent = 4, cls = QuestionEncoder)
        # print(data)
        # requests.post("https://rj4ll3zbyj.execute-api.us-west-2.amazonaws.com/dev/v1/questions", data = data)


program = Program()
program.run()
