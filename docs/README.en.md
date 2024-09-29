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
>Nearly 90% of the release notes, README, and commit messages in this repository are generated using [claude.ai](https://claude.ai/) and [ChatGPT4](https://chatgpt.com/) with the help of [AIRA](https://github.com/Sunwood-ai-labs/AIRA), [SourceSage](https://github.com/Sunwood-ai-labs/SourceSage), [Gaiah](https://github.com/Sunwood-ai-labs/Gaiah), [HarmonAI_II](https://github.com/Sunwood-ai-labs/HarmonAI_II), and [IRIS](https://github.com/Sunwood-ai-labs/IRIS).

This Streamlit app converts PDFs into audio podcasts, lectures, summaries, and more. It utilizes OpenAI's GPT model for text generation and speech synthesis.

https://github.com/user-attachments/assets/a94a33bf-8a01-4661-be25-21b0a83c43b8


## ✨ Main Features

- Upload multiple PDF files
- Choose from different instruction templates (podcast, lecture, summary, etc.)
- Customize text generation and voice models
- Select different voices for speakers

## 🔧 How to Use

1. Upload one or more PDF files
2. Choose your desired instruction template
3. Customize instructions as needed
4. Click "Generate Audio" to create audio content


> [!WARNING]
> You will need an OpenAI API key to use this app.

## 🎧 Example

<audio controls>
  <source src="https://github.com/Sunwood-ai-labs/pdf2audio-JP-st/raw/595e0375167c78d5014cfae3174cdba33cd544b6/docs/Paper-commentary-podcast_audio.mp3" type="audio/mpeg">
  ⚠️ Your browser does not support the audio element. Please visit "https://huggingface.co/spaces/MakiAi/pdf2audio-JP-st" ⚠️
</audio>


## 🚀 Deployment Steps

Here are the steps to deploy this application using AWS ECR and EC2:

### 1. Create an ECR Repository

First, create a repository in Amazon Elastic Container Registry (ECR):

```bash
aws ecr create-repository --repository-name pdf2audio-jp-streamlit-app --region ap-northeast-1
aws ecr describe-repositories --repository-names pdf2audio-jp-streamlit-app --region ap-northeast-1
```

This will create a new ECR repository and display its details.

### 2. Login to ECR

Next, log in to ECR:

```bash
aws ecr get-login-password --region ap-northeast-1 | docker login --username AWS --password-stdin XXXXXX.dkr.ecr.ap-northeast-1.amazonaws.com
```

Note: Replace `XXXXXX` with your AWS account ID.

### 3. Build and Push the Docker Image

Build the Docker image of your application and push it to ECR:

```bash
docker build -t pdf2audio-jp-streamlit-app .
docker tag pdf2audio-jp-streamlit-app:latest XXXXXX.dkr.ecr.ap-northeast-1.amazonaws.com/pdf2audio-jp-streamlit-app:latest
docker push XXXXXX.dkr.ecr.ap-northeast-1.amazonaws.com/pdf2audio-jp-streamlit-app:latest
```

These commands will build the Docker image locally and push it to the ECR repository.

### 4. Connect to the EC2 Instance

To connect to the EC2 instance that will host your application:

```bash
ssh -i "C:\Users\makim\.ssh\streamlit-terraform-keypair-tokyo-PEM2.pem" ubuntu@i-02c64da0e38c52135
```

Note: Change the path and instance ID accordingly to your environment.

These steps will allow you to deploy the application to the AWS cloud environment. Run the Docker container on the EC2 instance and start the application.



## 🙏 Acknowledgments

This project was inspired by and based on the code published in [https://github.com/knowsuchagency/pdf-to-podcast](https://github.com/knowsuchagency/pdf-to-podcast) and [https://github.com/knowsuchagency/promptic](https://github.com/knowsuchagency/promptic).

GitHub repository: [lamm-mit/PDF2Audio](https://github.com/lamm-mit/PDF2Audio)

## 📄 License

MIT License

## 🆕 What's New

**Version: v0.1.0**

This version introduced the Streamlit application for converting PDFs to audio. It also added various workflows and scripts and enhanced GitHub integration. For more details, see the [v0.1.0 release notes](https://github.com/Sunwood-ai-labs/pdf2audio-JP-st/releases/tag/v0.1.0). 
```