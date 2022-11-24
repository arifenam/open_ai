import random
import base64
import os
from dotenv import load_dotenv

load_dotenv()
import requests

import openai

openai.api_key = os.getenv('OPEN_AI_API')


def open_ai_prompt(what_to_write):
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=what_to_write,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    data = response.get('choices')[0].get('text')
    return data


user = os.getenv('USER')
pas = os.getenv('PASS')
credentials = f'{user}:{pas}'
token = base64.b64encode(credentials.encode('utf-8'))
header = {'Authorization': 'Basic ' + token.decode()}


def wp_h2(text):
    code = f'<!-- wp:heading {{"textAlign":"center"}} --><h2 class="has-text-align-center">{text}</h2><!-- /wp:heading -->'
    return code


def wp_paragraph(text):
    code = f'<!-- wp:paragraph --><p>{text}</p><!-- /wp:paragraph -->'
    return code


def slugify(kw):
    while ' ' in kw:
        code = kw.replace(' ', '-')
        return code


post_end_url_api = "https://localhost/project/python_project_website/wp-json/wp/v2/posts"
content = ''

kw_file = open('keyword.txt')
keywords = kw_file.readlines()
kw_file.close()

for kw in keywords:
    kw = kw.strip().replace('best ', '').replace('\n', '')

    # Buying Guide Instruction:

    intro_prompt = f'write a 200 words introduction about {kw}'
    why_prompt = f'Write Why {kw} Is Important'
    how_prompt = f'Write how to choose best {kw}'
    consider_prompt = f'Write what feature to consider to buy {kw}'
    conc_prompt = f'Write a details conclusion About the importance of {kw}'

    # Heading

    intro = f'A Short Overview Of {kw}'.title()
    why = f'Why {kw} Is Important'.title()
    how = f'How To Choose The Best {kw}'.title()
    consider = f'What Feature Should be considered while buying {kw}'.title()
    conc = f'conclusion'.title()

    # Wp_Heading

    intro_head = wp_h2(intro)
    why_head = wp_h2(why)
    how_head = wp_h2(how)
    consider_head = wp_h2(consider)
    conc_head = wp_h2(conc)

    # Wp paragraph with open ai answer

    intro_ai = wp_paragraph(open_ai_prompt(intro_prompt))
    why_ai = wp_paragraph(open_ai_prompt(why_prompt))
    how_ai = wp_paragraph(open_ai_prompt(how_prompt))
    consideration_ai = wp_paragraph(open_ai_prompt(consider_prompt))
    conclu_ai = wp_paragraph(open_ai_prompt(conc_prompt))
    slug = slugify(kw)
    content = f'{intro_head}{intro_ai}{why_head}{why_ai}{how_head}{how_ai}'\
              f'{consider_head}{consideration_ai}{conc_head}{conclu_ai}'

    # Title Idea using Choices

    title_idea = f'best {kw}: Reviews and Buying Guide', f'Top Rated Best {kw}: 2023 Reviews'
    title = random.choice(title_idea).title()


    def wp_posting(title, slug, content):
        post_end_url_api = "https://localhost/project/python_project_website/wp-json/wp/v2/posts"
        data = {
            'title': title,
            'content': content,
            'slug': slug,
        }

        response = requests.post(post_end_url_api, data=data, headers=header, verify=False)
        print(response.status_code)


    wp_posting(title, slug, content)
