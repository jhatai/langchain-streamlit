import streamlit as st
from langchain import PromptTemplate
from langchain.llms import OpenAI
import openai

template = """
    
    Your goal is to:
    - Use {tone} voice and tone. Based on the topic and  a specified tone to create a {blog_length}-word blog
    - Convert the blog to a specified dialect

    Here are some examples different Tones:
    - Formal: We went to Barcelona for the weekend. We have a lot of things to tell you.
    - Informal: Went to Barcelona for the weekend. Lots to tell you.  

    Here are some examples of words in different dialects:
    - American: French Fries, cotton candy, apartment, garbage, cookie, green thumb, parking lot, pants, windshield
    - British: chips, candyfloss, flag, rubbish, biscuit, green fingers, car park, trousers, windscreen

    Example Sentences from each dialect:
    - American: I headed straight for the produce section to grab some fresh vegetables, like bell peppers and zucchini. After that, I made my way to the meat department to pick up some chicken breasts.
    - British: Well, I popped down to the local shop just the other day to pick up a few bits and bobs. As I was perusing the aisles, I noticed that they were fresh out of biscuits, which was a bit of a disappointment, as I do love a good cuppa with a biscuit or two.

        
    Below is the topic, tone, and dialect:
    TONE: {tone}
    DIALECT: {dialect}
    Topic: {topic}
    
    YOUR {dialect} RESPONSE:
"""

prompt = PromptTemplate(
    input_variables=["tone", "dialect", "topic", "blog_length"],
    template=template,
)


def load_LLM(openai_api_key):
    """Logic for loading the chain you want to use should go here."""
    # Make sure your openai_api_key is set as an environment variable
    llm = OpenAI(temperature=.7, openai_api_key=openai_api_key )
    return llm


st.set_page_config(page_title="Globalize Email", page_icon=":robot:")
st.header("AI writer for blogs")
img_url = "https://media.discordapp.net/attachments/941971306004504638/1104201199181373550/HHT_style_close-up_shot__genre_gourmet__emotion_tempting__scene_255a9415-94e4-40e6-b92e-2c5f021c69b1.png?width=891&height=593"
st.image(image=img_url, use_column_width='auto')

# col1, col2 = st.columns(2)

# with col1:
#     st.markdown("Often professionals would like to improve their emails, but don't have the skills to do so. \n\n This tool \
#                 will help you improve your email skills by converting your emails into a more professional format. This tool \
#                 is powered by [LangChain](https://langchain.com/) and [OpenAI](https://openai.com) and made by \
#                 [@GregKamradt](https://twitter.com/GregKamradt). \n\n View Source Code on [Github](https://github.com/gkamradt/globalize-text-streamlit/blob/main/main.py)")

# with col2:
#     st.image(image='TweetScreenshot.png', width=500, caption='https://twitter.com/DannyRichman/status/1598254671591723008')

st.markdown("## Enter configs to write a blog")


def get_api_key():
    input_text = st.text_input(
        label="OpenAI API Key ",  placeholder="Ex: sk-2twmA8tfCb8un4...", key="openai_api_key_input")
    return input_text


openai_api_key = get_api_key()

col1, col2, col3 = st.columns(3)
with col1:
    option_tone = st.selectbox(
        'Which tone ?',
        ('professional', 'conversational','humorous','empathic','academic','casual','creative'))

with col2:
    option_dialect = st.selectbox(
        'Which English Dialect?',
        ('American', 'British'))

# col1, col2 = st.columns(2)
# with col1:
#     test_p = st.number_input(
#         'test col')

with col3:
    length_input = st.number_input(
        'Blog length', min_value=100, max_value=1000, value=100, step=1)


def get_text():
    input_text = st.text_area(label="Topic Input", label_visibility='collapsed',
                              placeholder="Your Topic...", key="topic_input")
    return input_text

st.text('Tell me the topic you are interested in...')
topic_input = get_text()

if len(topic_input.split(" ")) > 700:
    st.write("Please enter a shorter topic. The maximum length is 700 words.")
    st.stop()


def update_text_with_example():
    print("in updated")
    st.session_state.topic_input = f"Generating a blog for topic -- {topic_input}"


st.button("*Execute..*", type='secondary',
          help="Click to see an example of the email you will be converting.", on_click=update_text_with_example)

st.markdown("### Suggestion from AI writer:")

def generate_response(prompt):
    completions = openai.Completion.create(
        engine = "text-davinci-003",
        prompt = prompt,
        max_tokens = 1024,
        n = 1,
        stop = None,
        temperature=0.5,
    )
    message = completions.choices[0].text
    return message 

if topic_input:
    if not openai_api_key:
        st.warning(
            'Please insert OpenAI API Key. Instructions [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)', icon="⚠️")
        st.stop()

    # llm = load_LLM(openai_api_key=openai_api_key)

    prompt_with_topic = prompt.format(blog_length=length_input,
                                      tone=option_tone, dialect=option_dialect, topic=topic_input)

    # formatted_blog = llm(prompt_with_topic)

    # st.write(formatted_blog)
    st.code(generate_response(prompt_with_topic))

    

# todo 1. write page title and description 2. Add options applied
