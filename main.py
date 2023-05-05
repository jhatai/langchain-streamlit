import streamlit as st
from langchain import PromptTemplate
from langchain.llms import OpenAI

template = """
    
    Your goal is to:
    - Based on the topic and  a specified tone to create a {blog_length}-word blog
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
    input_variables=["tone", "dialect", "topic","blog_length"],
    template=template,
)


def load_LLM(openai_api_key):
    """Logic for loading the chain you want to use should go here."""
    # Make sure your openai_api_key is set as an environment variable
    llm = OpenAI(temperature=.7, openai_api_key=openai_api_key)
    return llm


st.set_page_config(page_title="Globalize Email", page_icon=":robot:")
st.header("AI writer for blogs")

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

col1, col2 = st.columns(2)
with col1:
    option_tone = st.selectbox(
        'Which tone would you like your blog to have?',
        ('Formal', 'Informal'))

with col2:
    option_dialect = st.selectbox(
        'Which English Dialect would you like?',
        ('American', 'British'))

col1, col2 = st.columns(2)
with col1:
    test_p = st.number_input(
        'Blog length')

with col2:
    length_input = st.number_input(
        'Blog length')


def get_text():
    input_text = st.text_area(label="Topic Input", label_visibility='collapsed',
                              placeholder="Your Topic...", key="topic_input")
    return input_text


topic_input = get_text()

if len(topic_input.split(" ")) > 700:
    st.write("Please enter a shorter topic. The maximum length is 700 words.")
    st.stop()


def update_text_with_example():
    print("in updated")
    st.session_state.topic_input = f"Generating a blog for topic -- {topic_input}"


st.button("*See An Example*", type='secondary',
          help="Click to see an example of the email you will be converting.", on_click=update_text_with_example)

st.markdown("### Your Converted Blog:")

if topic_input:
    if not openai_api_key:
        st.warning(
            'Please insert OpenAI API Key. Instructions [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)', icon="⚠️")
        st.stop()

    llm = load_LLM(openai_api_key=openai_api_key)

    prompt_with_topic = prompt.format(blog_length=length_input,
                                      tone=option_tone, dialect=option_dialect, topic=topic_input)

    formatted_blog = llm(prompt_with_topic)

    st.write(formatted_blog)
