# Imports
from openai import OpenAI
import gradio as gr

# Setting up ollama
ollama_url = "http://localhost:11434/v1"
ollama = OpenAI(api_key="ollama", base_url=ollama_url)

models = [
    "Yi-Coder",
    "StarCoder"
]

clients = {
    "yi-coder": ollama,
    "starcoder": ollama
}

# Code system prompt - decides the tone and response of the model
system_prompt = """
You are a helpful coding assistant who generates very efficient code in the language they want.
The only objectives are to make it as fast as possible using ANY methods possible, make it have no errors, and to give the generated output.
Do not provide any explanation at all, assuming the user knows how to code. Also, do not put the coding language at line 1. Just respond with the code.
"""

# Creates user prompt
def user_prompt_for(code_type, prompt):
    return f"""
Generate code about {prompt} to {code_type} with the fastest possible implementation that produces identical output in the least time.
Respond only with {code_type} code. Do NOT provide ANY explanation..
Prompt:
{prompt}
"""
# Creates the format that OpenAI recieves
def messages_for(prompt, code_type):
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt_for(code_type, prompt)}
    ]

# Runs the main model
def port(model, prompt, code_type):
    client = clients[model.lower()]
    stream = client.chat.completions.create(model = model, messages=messages_for(prompt, code_type), stream = True)
    response = ""
    for chunk in stream:
        response += chunk.choices[0].delta.content or ''
        yield response


coding_language = [
    "HTML: Front-end, simple, website-used programming",
    "CSS: Front and back-end stylist programming",
    "Python: Simple, object oriented programming",
    "Java: High-level, object-oriented programming",
    "C++: High-performance, compiled programming",
    "C#: Modern, general-purpose, object-oriented programming",
    "PHP: Widely-used, open-source, server-side scripting programming",
    "Rust: Modern, high-performance systems programming"
]


# Setting the theme using gradio
theme = gr.themes.Default(font=[gr.themes.GoogleFont("Source Code Pro")], primary_hue=gr.themes.colors.teal, secondary_hue=gr.themes.colors.sky).set(loader_color ="#FF0000")

# UI using gradio

with gr.Blocks(theme=theme, title="CODER-AI") as ui:
    with gr.Row():
        model = gr.Dropdown(models, label="Select Model", value="Yi-Coder")
        code_type = gr.Dropdown(coding_language, label="Select Coding Language", value=coding_language[0])
    with gr.Row():
        prompt = gr.Textbox(label="Prompt the code you want our AI assistant to generate!", lines = 14, value = "Generate a code snippet calculating the logarithm of any number.")
        code = gr.Code(label="Code", interactive=True, lines=14)
    with gr.Row():
        generate = gr.Button("Generate Code", variant="primary")

    generate.click(port, inputs = [model, prompt, code_type], outputs=[code])

# Launches the User Interface
if __name__ == "__main__":
    ui.launch(inbrowser=True, share=True)
