---
title: Pdf2audio JP St
emoji: 🏆
colorFrom: red
colorTo: gray
sdk: streamlit
sdk_version: 1.38.0
app_file: app.py
pinned: false
---

<p align="center">
<img src="https://huggingface.co/datasets/MakiAi/IconAssets/resolve/main/pdf2audio-JP-ST.png" width="50%">
<br>
<h1 align="center">PDF to Audio Converter JP・ST</h1>
<h2 align="center">
  ～ Building Cloud Infrastructures, Block by Block ～
<br>
  <img alt="GitHub Last Commit" src="https://img.shields.io/github/last-commit/Sunwood-ai-labs/pdf2audio-JP-st">
  <img alt="GitHub Top Language" src="https://img.shields.io/github/languages/top/Sunwood-ai-labs/pdf2audio-JP-st">
  <img alt="License" src="https://img.shields.io/github/license/Sunwood-ai-labs/pdf2audio-JP-st">
  <br>
  <a href="https://github.com/Sunwood-ai-labs/pdf2audio-JP-st" title="Go to GitHub repo"><img src="https://img.shields.io/static/v1?label=Sunwood-ai-labs&message=pdf2audio-JP-st&color=blue&logo=github"></a>
  <img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/Sunwood-ai-labs/pdf2audio-JP-st?style=social">
  <a href="https://github.com/Sunwood-ai-labs/pdf2audio-JP-st"><img alt="GitHub forks" src="https://img.shields.io/github/forks/Sunwood-ai-labs/pdf2audio-JP-st?style=social"></a>
<br>
<p align="center">
  <a href="https://hamaruki.com/"><b>[🌐 Website]</b></a> •
  <a href="https://github.com/Sunwood-ai-labs"><b>[🐱 GitHub]</b></a> •
  <a href="https://x.com/hAru_mAki_ch"><b>[🐦 Twitter]</b></a> •
  <a href="https://hamaruki.com/"><b>[🍀 Official Blog]</b></a>
   <br>

   <a href="https://github.com/Sunwood-ai-labs/pdf2audio-JP-st/blob/main/README.md"><img src="https://img.shields.io/badge/ドキュメント-日本語-white.svg" alt="JA doc"/></a>
   <a href="https://github.com/Sunwood-ai-labs/pdf2audio-JP-st/blob/main/docs/README.en.md"><img src="https://img.shields.io/badge/english-document-white.svg" alt="EN doc"></a>

   [![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/MakiAi/pdf2audio-JP-st)
</p>

</h2>

</p>

>[!IMPORTANT]
>Nearly 90% of the release notes, README, and commit messages in this repository are generated using [claude.ai](https://claude.ai/) and [ChatGPT4](https://chatgpt.com/) through [AIRA](https://github.com/Sunwood-ai-labs/AIRA), [SourceSage](https://github.com/Sunwood-ai-labs/SourceSage), [Gaiah](https://github.com/Sunwood-ai-labs/Gaiah), [HarmonAI_II](https://github.com/Sunwood-ai-labs/HarmonAI_II), and [IRIS](https://github.com/Sunwood-ai-labs/IRIS).

This Streamlit app converts PDFs into audio content like podcasts, lectures, and summaries. It utilizes OpenAI's GPT models for text generation and speech synthesis.


## 🚀 Project Overview

This project provides a Streamlit application that allows users to upload PDF files and generate audio content (podcasts, lectures, summaries, etc.) using OpenAI's GPT models. Users can upload multiple PDF files and control the generated audio content by selecting from various instruction templates or by customizing instructions.


## ✨ Key Features

- Ability to upload multiple PDF files
- Selection from different instruction templates (podcast, lecture, summary, etc.)
- Customizable text generation and voice models
- Different voice options for the speaker
- Deployment using AWS ECR and EC2


## 🔧 How to Use

1. Upload one or more PDF files.
2. Select the desired instruction template.
3. Customize the instructions if needed.
4. Click "Generate Audio" to create the audio content.


> [!WARNING]
> You need an OpenAI API key to use this app.


## 🎧 Example

<audio controls>
  <source src="https://github.com/Sunwood-ai-labs/pdf2audio-JP-st/raw/595e0375167c78d5014cfae3174cdba33cd544b6/docs/Paper-commentary-podcast_audio.mp3" type="audio/mpeg">
  ⚠️ Your browser does not support the audio element. Please visit "https://huggingface.co/spaces/MakiAi/pdf2audio-JP-st" ⚠️
</audio>


## 📦 Installation Instructions

This application is designed to be deployed using Docker.

1. Clone the repository.
2. Install the necessary Python packages using the `requirements.txt` file.
3. Copy the `terraform.example.tfvars` file and rename it to `terraform.tfvars`. Enter your AWS credentials and settings.
4. Deploy the AWS infrastructure using Terraform.
5. Launch the application.


## 🚀 Deployment Instructions

Here are the steps to deploy this application using AWS ECR and EC2:

### 1. Create an ECR Repository

First, create a repository in Amazon Elastic Container Registry (ECR):

```bash
aws ecr create-repository --repository-name pdf2audio-jp-streamlit-app --region ap-northeast-1
aws ecr describe-repositories --repository-names pdf2audio-jp-streamlit-app --region ap-northeast-1
```

This will create a new ECR repository and display its details.

### 2. Log in to ECR

Next, log in to ECR:

```bash
aws ecr get-login-password --region ap-northeast-1 | docker login --username AWS --password-stdin XXXXXX.dkr.ecr.ap-northeast-1.amazonaws.com
```

Note: Replace `XXXXXX` with your AWS account ID.

### 3. Build and Push the Docker Image

Build the Docker image of the application and push it to ECR:

```bash
docker build -t pdf2audio-jp-streamlit-app .
docker tag pdf2audio-jp-streamlit-app:latest XXXXXX.dkr.ecr.ap-northeast-1.amazonaws.com/pdf2audio-jp-streamlit-app:latest
docker push XXXXXX.dkr.ecr.ap-northeast-1.amazonaws.com/pdf2audio-jp-streamlit-app:latest
```

These commands will build the Docker image locally and push it to the ECR repository.

### 4. Connect to the EC2 Instance

To connect to the EC2 instance that will host the application:

```bash
ssh -i "C:\Users\makim\.ssh\streamlit-terraform-keypair-tokyo-PEM2.pem" ubuntu@i-02c64da0e38c52135
```

Note: Adjust the path and instance ID appropriately for your environment.

These steps will allow you to deploy the application to the AWS cloud environment. Run the Docker container on the EC2 instance and launch the application.


## 🙏 Acknowledgments

This project refers to and is based on the code published in [https://github.com/knowsuchagency/pdf-to-podcast](https://github.com/knowsuchagency/pdf-to-podcast) and [https://github.com/knowsuchagency/promptic](https://github.com/knowsuchagency/promptic).

GitHub repository: [lamm-mit/PDF2Audio](https://github.com/lamm-mit/PDF2Audio)


## 📄 License

MIT License


## 🆕 What's New

**Version: v0.2.2**

This release mainly focuses on updating the README file and modifying the release note generation settings. It also includes changes to improve usability, such as removing unnecessary font files and adding a link to the demo page on Hugging Face Spaces.