import streamlit as st
import openai
import json
import os
import random
from newspaper import Article
from urllib.parse import urlparse
from PIL import Image

# Constants for the app
APP_NAME = "Trust In Media (TIM) IQ Playground Toolkit"

# Function to interact with GPT-4 API
def gpt4_interaction(prompt, max_tokens=1800):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an advanced text analysis and manipulation assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        st.error(f"Error interacting with OpenAI: {e}")
        return None

# Function to get text from input (either URL or plain text)
def get_text_from_input(input_text):
    if is_url(input_text):
        try:
            article = Article(input_text)
            article.download()
            article.parse()
            return article.text
        except Exception as e:
            st.error(f"Failed to fetch article from URL: {str(e)}")
            return None
    else:
        return input_text

# Function to check if input is a URL
def is_url(text):
    try:
        result = urlparse(text)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

# Function to handle API key input
def api_key_input():
    st.sidebar.header("API Key Configuration")
    api_key = st.sidebar.text_input("Enter your OpenAI API Key:", type="password")
    if api_key:
        st.session_state['api_key'] = api_key
        openai.api_key = api_key
        st.sidebar.success("API key set for this session!")
    return api_key

# Main application
st.title(APP_NAME)

# Load and display logo
logo_path = "./tim_logo.png"  # Update this path if your logo is located elsewhere
if os.path.exists(logo_path):
    logo_img = Image.open(logo_path)
    st.image(logo_img, width=200)
else:
    st.warning("Logo image not found.")

# Check for API key in session state
if 'api_key' not in st.session_state or not st.session_state['api_key']:
    st.warning("OpenAI API key not found. Please enter it in the sidebar.")
    api_key = api_key_input()
    if not api_key:
        st.stop()
else:
    openai.api_key = st.session_state['api_key']

# Define the tools
tools = [
    "What If? Scenario Analyzer",
    "Debate Counter-Argument Generator",
    "Article Neutralizer",
    "Emotion Amplifier/Reducer",
    "Narrative Perspective Changer",
    "Fact vs. Opinion Analyzer",
    "Information Complexity Mixer",
    "Rhetorical Device Highlighter",
    "Cross-Cultural Interpretation Tool",
    "Variable Adjustment"
]

# Sidebar for tool selection
selected_tool = st.sidebar.selectbox("Select a Tool", tools)

# Function definitions for each tool

def save_report_as_html(title, original_text, modified_text, analysis):
    html_content = f"""
    <html>
    <head>
    <title>{title}</title>
    <style>
    body {{font-family: Arial, sans-serif; padding: 20px; background-color: #F0F4F8; color: #2C3E50; line-height: 1.6;}}
    h1 {{color: #3498DB; text-align: center;}}
    h2 {{color: #2C3E50; margin-top: 40px;}}
    .container {{display: flex; justify-content: space-between; margin-top: 20px;}}
    .text-box {{width: 48%; padding: 15px; background-color: white; border: 1px solid #ddd; border-radius: 8px;}}
    pre {{font-size: 14px; white-space: pre-wrap; word-wrap: break-word;}}
    .original {{background-color: #eef4ff;}}
    .modified {{background-color: #eaf3e8;}}
    .analysis {{margin-top: 20px; padding: 15px; background-color: #fff3cd; border-radius: 8px; color: #856404;}}
    </style>
    </head>
    <body>
    <h1>{title}</h1>
    <div class="container">
        <div class="text-box original">
            <h2>Original Text</h2>
            <pre>{original_text}</pre>
        </div>
        <div class="text-box modified">
            <h2>Modified Text</h2>
            <pre>{modified_text}</pre>
        </div>
    </div>
    <div class="analysis">
        <h2>Analysis</h2>
        <pre>{analysis}</pre>
    </div>
    </body>
    </html>
    """

    # Create a download button
    st.download_button(
        label="Download Report as HTML",
        data=html_content,
        file_name=f"{title}.html",
        mime="text/html"
    )

def what_if_scenario_analyzer():
    st.header("What If? Scenario Analyzer")
    input_text = st.text_area("Paste an article or URL here:")

    sentiment = st.selectbox("Sentiment:", ["positive", "neutral", "negative"])
    context = st.selectbox("Context:", ["current", "historical", "future", "economic boom", "economic downturn"])
    source = st.selectbox("Source:", ["neutral", "left-leaning", "right-leaning", "academic", "tabloid"])
    demographic = st.selectbox("Demographic:", ["general", "youth", "elderly", "urban", "rural"])
    socioeconomic = st.selectbox("Socio-Economic:", ["middle class", "upper class", "working class", "unemployed"])
    cultural = st.selectbox("Cultural Context:", ["mainstream", "conservative", "liberal", "traditional", "modern"])

    if st.button("Apply What If? Scenario"):
        if not input_text:
            st.warning("Please paste an article or URL into the text area.")
            return

        with st.spinner("Processing..."):
            original_text = get_text_from_input(input_text)
            if not original_text:
                return

            prompt = f"""Original Text: {original_text}

Modify the text based on the following parameters:
Sentiment: {sentiment}
Context: {context}
Source: {source}
Demographic: {demographic}
Socio-Economic Background: {socioeconomic}
Cultural Context: {cultural}

Provide the modified text below, and include a brief analysis of how the information has been manipulated. Separate the modified text and analysis with three dashes (---) on a new line."""

            response = gpt4_interaction(prompt)
            if response:
                parts = response.split("\n---\n")
                if len(parts) == 2:
                    modified_text, analysis = parts
                else:
                    modified_text = parts[0]
                    analysis = "No separate analysis provided."
                st.subheader("Modified Text")
                st.write(modified_text.strip())
                st.subheader("Analysis")
                st.write(analysis.strip())

                # Provide the download button immediately after displaying results
                save_report_as_html("What If? Scenario Analysis", original_text, modified_text.strip(), analysis.strip())
            else:
                st.error("There was an issue processing the text with the OpenAI API.")

def debate_counter_argument_generator():
    st.header("Debate Counter-Argument Generator")
    input_text = st.text_area("Paste an article or URL here:")

    if st.button("Generate Counter-Argument"):
        if not input_text:
            st.warning("Please paste an article or URL into the text area.")
            return

        with st.spinner("Processing..."):
            original_text = get_text_from_input(input_text)
            if not original_text:
                return

            prompt = f"""Assuming the role of a seasoned debater, create a comprehensive, logically sound, and persuasive counter-narrative to the following text:

{original_text}

Provide a well-structured counter-argument, and include an analysis of the rhetorical techniques and logical fallacies (if any) used in the original text. Separate the counter-argument and analysis with three dashes (---) on a new line."""

            response = gpt4_interaction(prompt)
            if response:
                parts = response.split("\n---\n")
                if len(parts) == 2:
                    counter_argument, analysis = parts
                else:
                    counter_argument = parts[0]
                    analysis = "No separate analysis provided."
                st.subheader("Counter-Argument")
                st.write(counter_argument.strip())
                st.subheader("Analysis")
                st.write(analysis.strip())

                # Provide the download button
                save_report_as_html("Debate Counter-Argument Report", original_text, counter_argument.strip(), analysis.strip())
            else:
                st.error("There was an issue processing the text with the OpenAI API.")

def article_neutralizer():
    st.header("Article Neutralizer")
    input_text = st.text_area("Paste an article or URL here:")

    if st.button("Neutralize Text"):
        if not input_text:
            st.warning("Please paste an article or URL into the text area.")
            return

        with st.spinner("Processing..."):
            original_text = get_text_from_input(input_text)
            if not original_text:
                return

            prompt = f"""Neutralize the following text by removing any bias, emotional language, or subjective statements. 
Present only factual information in a neutral tone. If claims are made without evidence, indicate that they are unverified.
Maintain the overall structure and length of the original text as much as possible.
After neutralizing the text, provide a brief analysis of what changes were made and why.

Original text:
{original_text}

Please provide the neutralized version of the text, followed by an analysis of the changes made. Separate the neutralized text and analysis with three dashes (---) on a new line."""

            response = gpt4_interaction(prompt)
            if response:
                parts = response.split("\n---\n")
                if len(parts) == 2:
                    neutralized_text, analysis = parts
                else:
                    neutralized_text = parts[0]
                    analysis = "No separate analysis provided."
                st.subheader("Neutralized Text")
                st.write(neutralized_text.strip())
                st.subheader("Analysis")
                st.write(analysis.strip())

                # Provide the download button
                save_report_as_html("Text Neutralization Report", original_text, neutralized_text.strip(), analysis.strip())
            else:
                st.error("There was an issue processing the text with the OpenAI API.")

def emotion_amplifier_reducer():
    st.header("Emotion Amplifier/Reducer")
    input_text = st.text_area("Paste an article or URL here:")
    emotion_intensity = st.selectbox("Emotion Intensity:", ["amplify", "reduce"])

    if st.button("Apply Emotion Change"):
        if not input_text:
            st.warning("Please paste an article or URL into the text area.")
            return

        with st.spinner("Processing..."):
            original_text = get_text_from_input(input_text)
            if not original_text:
                return

            prompt = f"""Original Text: {original_text}

Please rewrite the text with a focus on {emotion_intensity} the emotional intensity. If the text is neutral, make it more emotionally charged, or tone it down to be more analytical. Include a brief analysis of the changes made. Separate the modified text and analysis with three dashes (---) on a new line."""

            response = gpt4_interaction(prompt)
            if response:
                parts = response.split("\n---\n")
                if len(parts) == 2:
                    modified_text, analysis = parts
                else:
                    modified_text = parts[0]
                    analysis = "No separate analysis provided."
                st.subheader("Modified Text")
                st.write(modified_text.strip())
                st.subheader("Analysis")
                st.write(analysis.strip())

                # Provide the download button
                save_report_as_html("Emotion Amplifier/Reducer Report", original_text, modified_text.strip(), analysis.strip())
            else:
                st.error("There was an issue processing the text with the OpenAI API.")

def narrative_perspective_changer():
    st.header("Narrative Perspective Changer")
    input_text = st.text_area("Paste an article or URL here:")
    perspective = st.selectbox("New Perspective:", ["first-person", "third-person", "antagonist", "protagonist"])

    if st.button("Change Perspective"):
        if not input_text:
            st.warning("Please paste an article or URL into the text area.")
            return

        with st.spinner("Processing..."):
            original_text = get_text_from_input(input_text)
            if not original_text:
                return

            prompt = f"""Original Text: {original_text}

Please rewrite the text from a {perspective} perspective. Change pronouns, restructure sentences, and adjust the tone to match the new perspective. Include a brief analysis of the changes made. Separate the modified text and analysis with three dashes (---) on a new line."""

            response = gpt4_interaction(prompt)
            if response:
                parts = response.split("\n---\n")
                if len(parts) == 2:
                    modified_text, analysis = parts
                else:
                    modified_text = parts[0]
                    analysis = "No separate analysis provided."
                st.subheader("Modified Text")
                st.write(modified_text.strip())
                st.subheader("Analysis")
                st.write(analysis.strip())

                # Provide the download button
                save_report_as_html("Narrative Perspective Changer Report", original_text, modified_text.strip(), analysis.strip())
            else:
                st.error("There was an issue processing the text with the OpenAI API.")

def fact_vs_opinion_analyzer():
    st.header("Fact vs. Opinion Analyzer")
    input_text = st.text_area("Paste an article or URL here:")

    if st.button("Analyze Fact vs. Opinion"):
        if not input_text:
            st.warning("Please paste an article or URL into the text area.")
            return

        with st.spinner("Processing..."):
            original_text = get_text_from_input(input_text)
            if not original_text:
                return

            prompt = f"""Analyze the following text and distinguish between factual statements and opinions. Highlight factual statements in one color and opinions in another. Provide explanations for the categorization.

Original text:
{original_text}

Please provide the analyzed text with explanations. Separate the analyzed text and explanations with three dashes (---) on a new line."""

            response = gpt4_interaction(prompt)
            if response:
                parts = response.split("\n---\n")
                if len(parts) == 2:
                    analyzed_text, explanations = parts
                else:
                    analyzed_text = parts[0]
                    explanations = "No separate explanations provided."
                st.subheader("Analyzed Text")
                st.write(analyzed_text.strip())
                st.subheader("Explanations")
                st.write(explanations.strip())

                # Provide the download button
                save_report_as_html("Fact vs. Opinion Analyzer Report", original_text, analyzed_text.strip(), explanations.strip())
            else:
                st.error("There was an issue processing the text with the OpenAI API.")

def information_complexity_mixer():
    st.header("Information Complexity Mixer")
    input_text = st.text_area("Paste an article or URL here:")
    complexity_level = st.selectbox("Complexity Level:", ["simplified", "complexified"])

    if st.button("Apply Complexity Change"):
        if not input_text:
            st.warning("Please paste an article or URL into the text area.")
            return

        with st.spinner("Processing..."):
            original_text = get_text_from_input(input_text)
            if not original_text:
                return

            prompt = f"""Original Text: {original_text}

Please rewrite the text to make it {complexity_level}. Either simplify the content for a general audience or add more complexity and detail. Include a brief analysis of the changes made. Separate the modified text and analysis with three dashes (---) on a new line."""

            response = gpt4_interaction(prompt)
            if response:
                parts = response.split("\n---\n")
                if len(parts) == 2:
                    modified_text, analysis = parts
                else:
                    modified_text = parts[0]
                    analysis = "No separate analysis provided."
                st.subheader("Modified Text")
                st.write(modified_text.strip())
                st.subheader("Analysis")
                st.write(analysis.strip())

                # Provide the download button
                save_report_as_html("Information Complexity Mixer Report", original_text, modified_text.strip(), analysis.strip())
            else:
                st.error("There was an issue processing the text with the OpenAI API.")

def rhetorical_device_highlighter():
    st.header("Rhetorical Device Highlighter")
    input_text = st.text_area("Paste an article or URL here:")

    if st.button("Highlight Rhetorical Devices"):
        if not input_text:
            st.warning("Please paste an article or URL into the text area.")
            return

        with st.spinner("Processing..."):
            original_text = get_text_from_input(input_text)
            if not original_text:
                return

            prompt = f"""Analyze the following text for rhetorical devices. Highlight devices like metaphors, similes, hyperbole, etc., and provide explanations on how they impact the reader.

Original text:
{original_text}

Please provide the highlighted text with explanations. Separate the highlighted text and explanations with three dashes (---) on a new line."""

            response = gpt4_interaction(prompt)
            if response:
                parts = response.split("\n---\n")
                if len(parts) == 2:
                    highlighted_text, explanations = parts
                else:
                    highlighted_text = parts[0]
                    explanations = "No separate explanations provided."
                st.subheader("Highlighted Text")
                st.write(highlighted_text.strip())
                st.subheader("Explanations")
                st.write(explanations.strip())

                # Provide the download button
                save_report_as_html("Rhetorical Device Highlighter Report", original_text, highlighted_text.strip(), explanations.strip())
            else:
                st.error("There was an issue processing the text with the OpenAI API.")

def cross_cultural_interpretation_tool():
    st.header("Cross-Cultural Interpretation Tool")
    input_text = st.text_area("Paste an article or URL here:")
    culture = st.selectbox("Culture:", ["Western", "Eastern", "Middle Eastern", "African", "South American"])

    if st.button("Apply Cultural Interpretation"):
        if not input_text:
            st.warning("Please paste an article or URL into the text area.")
            return

        with st.spinner("Processing..."):
            original_text = get_text_from_input(input_text)
            if not original_text:
                return

            prompt = f"""Original Text: {original_text}

Please reinterpret the text from the perspective of {culture} culture. Adjust language, idioms, and cultural references to simulate how the text might be perceived in that cultural context. Include a brief analysis of the changes made. Separate the modified text and analysis with three dashes (---) on a new line."""

            response = gpt4_interaction(prompt)
            if response:
                parts = response.split("\n---\n")
                if len(parts) == 2:
                    modified_text, analysis = parts
                else:
                    modified_text = parts[0]
                    analysis = "No separate analysis provided."
                st.subheader("Modified Text")
                st.write(modified_text.strip())
                st.subheader("Analysis")
                st.write(analysis.strip())

                # Provide the download button
                save_report_as_html("Cross-Cultural Interpretation Report", original_text, modified_text.strip(), analysis.strip())
            else:
                st.error("There was an issue processing the text with the OpenAI API.")

def variable_adjustment():
    st.header("Variable Adjustment Analysis")
    input_text = st.text_area("Paste an article or URL here:")

    # Sliders for each variable
    accuracy = st.slider("Accuracy", 0, 100, 50)
    completeness = st.slider("Completeness", 0, 100, 50)
    relevance = st.slider("Relevance", 0, 100, 50)
    timeliness = st.slider("Timeliness", 0, 100, 50)
    consistency = st.slider("Consistency", 0, 100, 50)
    objectivity = st.slider("Objectivity", 0, 100, 50)
    credibility = st.slider("Credibility", 0, 100, 50)
    clarity = st.slider("Clarity", 0, 100, 50)
    accessibility = st.slider("Accessibility", 0, 100, 50)
    value = st.slider("Value", 0, 100, 50)

    if st.button("Analyze with Variables"):
        if not input_text:
            st.warning("Please paste an article or URL into the text area.")
            return

        with st.spinner("Processing..."):
            original_text = get_text_from_input(input_text)
            if not original_text:
                return

            prompt = f"""Original Text: {original_text}

Please rewrite the text based on the following criteria adjustments:
Accuracy: {accuracy}%
Completeness: {completeness}%
Relevance: {relevance}%
Timeliness: {timeliness}%
Consistency: {consistency}%
Objectivity: {objectivity}%
Credibility: {credibility}%
Clarity: {clarity}%
Accessibility: {accessibility}%
Value: {value}%

Modify the text to reflect these adjustments. For example, if accuracy is set to a low percentage, introduce some inaccuracies. If clarity is high, make the text more straightforward and easy to understand.

After rewriting the text, provide a brief analysis of the changes made and how they reflect the adjusted variables.

Separate the rewritten text and the analysis with three dashes (---) on a new line."""

            response = gpt4_interaction(prompt)
            if response:
                parts = response.split("\n---\n")
                if len(parts) == 2:
                    rewritten_text, analysis = parts
                else:
                    rewritten_text = parts[0]
                    analysis = "No separate analysis provided."
                st.subheader("Rewritten Text")
                st.write(rewritten_text.strip())
                st.subheader("Analysis")
                st.write(analysis.strip())

                # Provide the download button
                save_report_as_html("Variable Adjustment Analysis Report", original_text, rewritten_text.strip(), analysis.strip())
            else:
                st.error("There was an issue processing the text with the OpenAI API.")

# Clear all inputs
def clear_all():
    # Clear session state except for the API key
    api_key = st.session_state.get('api_key')
    st.session_state.clear()
    if api_key:
        st.session_state['api_key'] = api_key
    st.experimental_rerun()

# Fun Fact Function
def show_fun_fact():
    facts = [
        "Did you know? The way information is presented can significantly alter your perception of it.",
        "Fun fact: Your brain processes negatively framed information differently than positive information.",
        "Interesting tidbit: The order in which facts are presented can change their perceived importance.",
        "Did you know? The same statistic can support opposite arguments depending on how it's framed.",
        "Fun fact: Your current emotional state can affect how you interpret neutral information.",
        "Interesting tidbit: The use of certain words can subtly influence your opinion without you noticing.",
        "Did you know? Information overload can lead to poorer decision-making, not better.",
        "Fun fact: Your pre-existing beliefs can cause you to interpret neutral information as supporting your view.",
        "Interesting tidbit: The context in which information is presented can completely change its meaning.",
        "Did you know? The source of information often matters more to people than the actual content."
    ]
    st.info(random.choice(facts))

# Tool selection logic
if selected_tool == "What If? Scenario Analyzer":
    what_if_scenario_analyzer()
elif selected_tool == "Debate Counter-Argument Generator":
    debate_counter_argument_generator()
elif selected_tool == "Article Neutralizer":
    article_neutralizer()
elif selected_tool == "Emotion Amplifier/Reducer":
    emotion_amplifier_reducer()
elif selected_tool == "Narrative Perspective Changer":
    narrative_perspective_changer()
elif selected_tool == "Fact vs. Opinion Analyzer":
    fact_vs_opinion_analyzer()
elif selected_tool == "Information Complexity Mixer":
    information_complexity_mixer()
elif selected_tool == "Rhetorical Device Highlighter":
    rhetorical_device_highlighter()
elif selected_tool == "Cross-Cultural Interpretation Tool":
    cross_cultural_interpretation_tool()
elif selected_tool == "Variable Adjustment":
    variable_adjustment()

# Add Clear All and Fun Fact buttons
st.sidebar.button("Clear All", on_click=clear_all)
st.sidebar.button("Show Fun Fact", on_click=show_fun_fact)