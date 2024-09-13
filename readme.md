
# Trust In Media (TIM) IQ Playground Toolkit

**TIM IQ Playground Toolkit** is an interactive Streamlit-based web application designed to analyze and manipulate text using advanced AI-driven tools. The toolkit offers a variety of functions such as scenario analysis, counter-argument generation, text neutralization, emotion amplification/reduction, and more. These tools help users better understand and modify information in meaningful ways.

## Features

- **What If? Scenario Analyzer**: Modify text based on sentiment, context, demographic, and socio-economic backgrounds.
- **Debate Counter-Argument Generator**: Generate counter-arguments for any text and analyze rhetorical techniques and logical fallacies.
- **Article Neutralizer**: Remove bias, emotional language, and subjective statements from any article or text.
- **Emotion Amplifier/Reducer**: Amplify or reduce the emotional intensity of the text.
- **Narrative Perspective Changer**: Rewrite text from different perspectives such as first-person, third-person, antagonist, or protagonist.
- **Fact vs. Opinion Analyzer**: Distinguish between factual statements and opinions within the text.
- **Information Complexity Mixer**: Simplify or complexify text for a different audience or depth of detail.
- **Rhetorical Device Highlighter**: Highlight rhetorical devices in a text and explain their impact.
- **Cross-Cultural Interpretation Tool**: Reinterpret text from the perspective of different cultural contexts.
- **Variable Adjustment Tool**: Adjust variables like accuracy, relevance, clarity, and more to rewrite and analyze text.

## Requirements

- Python 3.8 or higher
- Streamlit
- OpenAI Python client
- Newspaper3k
- PIL (Pillow)
- LXML

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/tim-iq-playground.git
   cd tim-iq-playground
   ```

2. **Install the required dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Add your OpenAI API key:**

   Open the application and enter your OpenAI API key when prompted, or provide it via the sidebar.

## Usage

1. **Run the application:**

   ```bash
   streamlit run streamlit_app.py
   ```

2. **Access the app:** Open a browser and navigate to the address shown in your terminal (e.g., `http://localhost:8501`).

3. **Select a tool:** Choose a tool from the sidebar, and input the text or URL you want to analyze or manipulate.

4. **Generate results:** Once you’ve selected the tool and provided the input, click the relevant button to generate and view results. You can download reports as HTML.

## Tools

- **What If? Scenario Analyzer**: Modify text based on various parameters such as sentiment and context.
- **Debate Counter-Argument Generator**: Generate strong counter-arguments and analyze rhetoric.
- **Article Neutralizer**: Neutralize biased language and present factual information.
- **Emotion Amplifier/Reducer**: Change the emotional intensity of a text.
- **Narrative Perspective Changer**: Rewrite text from a different narrative viewpoint.
- **Fact vs. Opinion Analyzer**: Differentiate between factual content and opinions.
- **Information Complexity Mixer**: Adjust the complexity of the text.
- **Rhetorical Device Highlighter**: Highlight rhetorical devices.
- **Cross-Cultural Interpretation Tool**: Analyze text from a cross-cultural perspective.
- **Variable Adjustment Tool**: Modify text based on specific variable adjustments (accuracy, clarity, etc.).

## API Key

This app requires an OpenAI API key. The user is prompted to enter their key upon opening the app, and it is used for that session only. The key is not saved after the session to ensure security.

## Contributing

Contributions are welcome! If you have suggestions for new features or improvements, feel free to fork the repository and submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
