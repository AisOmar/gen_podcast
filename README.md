# Generate a Podcast

This repository is dedicated to the development of a podcast app that leverages the power of Large Language Models (LLM) to generate personalized and dynamic podcast content.

## Introduction

The `gen_podcast` project aims to redefine the podcasting experience by utilizing Large Language Models (LLM) to create podcasts. This innovative approach allows for the generation of content that is both highly personalized and infinitely versatile, catering to a wide range of interests and preferences. Targeting podcast enthusiasts, content creators, and anyone with a curiosity for niche topics, the project seeks to make information consumption more accessible, engaging, and tailored to individual tastes.

## Features

- **Customizable Content**: Generate podcasts based on specific interests, from historical discussions to the latest in technology.
- **Dynamic Interactivity**: Engage with podcasts that adapt to listener feedback and preferences.
- **Accessibility**: Make information available in a format that's easy to consume for people who prefer audio or have visual impairments.
- **Diverse Voices**: Choose from a variety of narrators to find the voice that suits your style or mood.
- **Educational and Entertaining**: Mix educational content with entertainment to enjoy learning in a relaxed format.

## Getting Started

1. **Prerequisites**: Ensure you have the necessary software and tools installed, including Python, relevant libraries, and access to OpenAI APIs.
2. **Setup**: Clone the repository and install dependencies as detailed in the provided documentation.
3. **First Run**: Follow the instructions to generate your first podcast episode, including selecting a topic and customizing the narration style.

## Deploying Your Application on Hugging Face Spaces

Take your Gradio app from a temporary live notebook to a permanent fixture on the web by deploying it to Hugging Face Spaces. Here's how to make your application accessible to users on Hugging Face:

1. **Sign Up or Log In**:
   - If you don't have a Hugging Face account, sign up at [Hugging Face](https://huggingface.co/).
   - If you already have an account, simply log in.

2. **Create a New Space**:
   - Go to the Spaces section by clicking on "Spaces" in the navigation bar.
   - Initiate the creation process by selecting "Create New Space".

3. **Configure Your Space**:
   - Enter a name for your app in the provided field.
   - Choose 'Gradio' as the SDK you'd like to use for your Space.
   - Decide on the visibility of your app by selecting either Private or Public.

4. **Set Up Your App**:
   - In the new Space, you'll have an option to create an `app.py` file right in the web editor.
   - Copy and paste the code from your Gradio app's last two cells into the `app.py` file within this editor.

5. **Deploy**:
   - Commit your changes. This triggers the build process.
   - Once the build completes, your app will be live and shareable with the world!

If you're comfortable with Git, you can manage your Space using the command line:

```bash
git clone https://huggingface.co/spaces/{username}/gen_podcast
cd gen_podcast
# Add your files
git add app.py
git add requirements.txt
# Commit your changes
git commit -m "Add application file and dependencies"
# Push to deploy
git push origin main
```

Remember to replace `{username}` with your Hugging Face username. After pushing your changes, Hugging Face automatically builds and deploys your Space, making it available for public or private use based on your settings.

## Tutorial 

Step 1: Generate a podcast 
  - [Video](https://youtu.be/jOatry2TYTo)
  - [Colab Notebook](https://colab.research.google.com/drive/1syStcIw-_jBkIv1UrqRuZ0zxTa3auWwr?usp=sharing)

Step 2: Deploy as an app [Will be added soon]

