import torch
from transformers import pipeline
import ollama
from pydantic import BaseModel, Field
import gradio as gr
import os
import pandas as pd
import io  # Add this import at the top of your file


def create_file(filename, content):
    with open(filename, 'w') as file:
        file.write(content)
    print(f"File '{filename}' created with content: {content}")

def read_file(filename):
    try:
        with open(filename, 'r') as file:
            content = file.read()
        print(f"Content of '{filename}': {content}")
        return content
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        return None

def delete_file(filename):
    try:
        os.remove(filename)
        print(f"File '{filename}' deleted.")
    except FileNotFoundError:
        print(f"File '{filename}' not found.")

def get_response(prompt):
    tools = [
        {
            'type': 'function',
            'function': {
                'name': 'create_file',
                'description': 'Create a new file with given content',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'filename': {
                            'type': 'string',
                            'description': 'The name of the file to create',
                        },
                        'content': {
                            'type': 'string',
                            'description': 'The content to write to the file',
                        },
                    },
                    'required': ['filename', 'content'],
                },
            },
        },
        {
            'type': 'function',
            'function': {
                'name': 'read_file',
                'description': 'Read the content of a file',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'filename': {
                            'type': 'string',
                            'description': 'The name of the file to read',
                        },
                    },
                    'required': ['filename'],
                },
            },
        },
        {
            'type': 'function',
            'function': {
                'name': 'delete_file',
                'description': 'Delete a file',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'filename': {
                            'type': 'string',
                            'description': 'The name of the file to delete',
                        },
                    },
                    'required': ['filename'],
                },
            },
        },
        {
            'type': 'function',
            'function': {
                'name': 'create_task_table',
                'description': 'Create a task manager table',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'tasks': {
                            'type': 'string',
                            'description': 'Comma-separated list of tasks',
                        },
                        'statuses': {
                            'type': 'string',
                            'description': 'Comma-separated list of task statuses',
                        },
                        'priorities': {
                            'type': 'string',
                            'description': 'Comma-separated list of task priorities',
                        },
                    },
                    'required': ['tasks', 'statuses', 'priorities'],
                },
            },
        },
        {
            'type': 'function',
            'function': {
                'name': 'manage_tasks',
                'description': 'Manage tasks in the task table',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'action': {
                            'type': 'string',
                            'description': 'Action to perform (execute or delete)',
                        },
                        'task_index': {
                            'type': 'integer',
                            'description': 'Index of the task to manage',
                        },
                    },
                    'required': ['action', 'task_index'],
                },
            },
        },
    ]

    response = ollama.chat(
        model='llama3.2',
        messages=[{'role': 'user', 'content': prompt}],
        tools=tools,
    )

    tool_calls = response['message']['tool_calls']
    
    results = []
    task_table = None
    for tool_call in tool_calls:
        function_name = tool_call['function']['name']
        arguments = tool_call['function']['arguments']
        
        if function_name == 'create_file':
            create_file(arguments['filename'], arguments['content'])
            results.append(f"Created file: {arguments['filename']}")
        elif function_name == 'read_file':
            content = read_file(arguments['filename'])
            results.append(f"Read file: {arguments['filename']}, Content: {content}")
        elif function_name == 'delete_file':
            delete_file(arguments['filename'])
            results.append(f"Deleted file: {arguments['filename']}")
        elif function_name == 'create_task_table':
            task_table = create_task_table(arguments['tasks'], arguments['statuses'], arguments['priorities'])
            results.append(f"Created task table:\n{task_table.to_string()}")
        elif function_name == 'manage_tasks':
            if task_table is not None:
                task_table, result = manage_tasks(task_table, arguments['action'], arguments['task_index'])
                results.append(f"Task management result: {result}")
                results.append(f"Updated task table:\n{task_table.to_string()}")
            else:
                results.append("Error: Task table not created yet.")

    return results, task_table


pipe = pipeline("automatic-speech-recognition",
                "openai/whisper-large-v3-turbo",
                torch_dtype=torch.float16,
                device="mps")



def transcribe_and_respond(audio_input):
    if audio_input is None:
        raise gr.Error("No audio file")
    
    # Transcribe the audio
    transcription = pipe(audio_input, generate_kwargs={"task": "transcribe"}, return_timestamps=True)["text"]
    
    # Get response based on the transcription
    response, task_table = get_response(transcription)
    
    return transcription, "\n".join(response), task_table

def create_task_table(tasks, statuses, priorities):
    data = {
        'Task': tasks.split(','),
        'Status': statuses.split(','),
        'Priority': priorities.split(',')
    }
    df = pd.DataFrame(data)
    return df

demo = gr.Interface(
    fn=transcribe_and_respond,
    inputs=[gr.Audio(sources=["microphone", "upload"], type="filepath")],
    outputs=[
        gr.Textbox(label="Transcription"),
        gr.Textbox(label="AI Response"),
        gr.Dataframe(label="Table Output")
    ],
    title="Whisper Large V3 Turbo: Transcribe Audio and Get AI Response",
    description="Transcribe audio inputs and get AI responses. Thanks to HuggingFace and Ollama.",
    allow_flagging="never",
)

demo.launch()