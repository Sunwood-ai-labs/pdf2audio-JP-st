## PDF to Audio Converter JP・ST

～ Building Cloud Infrastructures, Block by Block ～

[![GitHub Last Commit](https://img.shields.io/github/last-commit/Sunwood-ai-labs/pdf2audio-JP-st)](https://github.com/Sunwood-ai-labs/pdf2audio-JP-st)
[![GitHub Top Language](https://img.shields.io/github/languages/top/Sunwood-ai-labs/pdf2audio-JP-st)](https://github.com/Sunwood-ai-labs/pdf2audio-JP-st)
[![License](https://img.shields.io/github/license/Sunwood-ai-labs/pdf2audio-JP-st)](https://github.com/Sunwood-ai-labs/pdf2audio-JP-st)
[![Sunwood-ai-labs](https://img.shields.io/static/v1?label=Sunwood-ai-labs&message=pdf2audio-JP-st&color=blue&logo=github)](https://github.com/Sunwood-ai-labs/pdf2audio-JP-st)
[![GitHub Repo stars](https://img.shields.io/github/stars/Sunwood-ai-labs/pdf2audio-JP-st?style=social)](https://github.com/Sunwood-ai-labs/pdf2audio-JP-st)
[![GitHub forks](https://img.shields.io/github/forks/Sunwood-ai-labs/pdf2audio-JP-st?style=social)](https://github.com/Sunwood-ai-labs/pdf2audio-JP-st)


[**🌐 Website**](https://hamaruki.com/) •
[**🐱 GitHub**](https://github.com/Sunwood-ai-labs) •
[**🐦 Twitter**](https://x.com/hAru_mAki_ch) •
[**🍀 Official Blog**](https://hamaruki.com/)


[![JA doc](https://img.shields.io/badge/ドキュメント-日本語-white.svg)](https://github.com/Sunwood-ai-labs/pdf2audio-JP-st/blob/main/README.md)
[![EN doc](https://img.shields.io/badge/english-document-white.svg)](https://github.com/Sunwood-ai-labs/pdf2audio-JP-st/blob/main/docs/README.en.md)


>[!IMPORTANT]
>Nearly 90% of the release notes, README, and commit messages in this repository are generated using [claude.ai](https://claude.ai/) and [ChatGPT4](https://chatgpt.com/) through [AIRA](https://github.com/Sunwood-ai-labs/AIRA), [SourceSage](https://github.com/Sunwood-ai-labs/SourceSage), [Gaiah](https://github.com/Sunwood-ai-labs/Gaiah), [HarmonAI_II](https://github.com/Sunwood-ai-labs/HarmonAI_II), and [IRIS](https://github.com/Sunwood-ai-labs/IRIS).

This Streamlit app converts PDFs into audio podcasts, lectures, summaries, etc. It uses OpenAI's GPT model for text generation and speech synthesis.


## 🌟 Features

- Upload multiple PDF files
- Choose from different instruction templates (podcast, lecture, summary, etc.)
- Customize text generation and voice model
- Select different voices for the speaker

## 🔧 How to Use

1. Upload one or more PDF files
2. Select the desired instruction template
3. Customize the instructions as needed
4. Click "Generate Audio" to create the audio content

## 🎧 Example

<audio controls>
  <source src="https://raw.githubusercontent.com/lamm-mit/PDF2Audio/main/SciAgents%20discovery%20summary%20-%20example.mp3" type="audio/mpeg">
  Your browser does not support the audio element.
</audio>

## ⚠️ Note

You will need an OpenAI API key to use this app.


## 🚀 Deployment Steps

Here are the steps to deploy this application using AWS ECR and EC2:

### 1. Create an ECR repository

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

### 3. Build and push the Docker image

Build the Docker image for the application and push it to ECR:

```bash
docker build -t pdf2audio-jp-streamlit-app .
docker tag pdf2audio-jp-streamlit-app:latest XXXXXX.dkr.ecr.ap-northeast-1.amazonaws.com/pdf2audio-jp-streamlit-app:latest
docker push XXXXXX.dkr.ecr.ap-northeast-1.amazonaws.com/pdf2audio-jp-streamlit-app:latest
```

These commands will build the Docker image locally and push it to the ECR repository.

### 4. Connect to the EC2 instance

To connect to the EC2 instance that will host the application:

```bash
ssh -i "C:\Users\makim\.ssh\streamlit-terraform-keypair-tokyo-PEM2.pem" ubuntu@i-02c64da0e38c52135
```

Note: Adjust the path and instance ID appropriately for your environment.

These steps will allow you to deploy the application to the AWS cloud environment. Run the Docker container on the EC2 instance and launch the application.


## 🙏 Credits

This project is inspired by and based on code published in [https://github.com/knowsuchagency/pdf-to-podcast](https://github.com/knowsuchagency/pdf-to-podcast) and [https://github.com/knowsuchagency/promptic](https://github.com/knowsuchagency/promptic).

GitHub repository: [lamm-mit/PDF2Audio](https://github.com/lamm-mit/PDF2Audio)

## 📄 Citations

```bibtex
@article{ghafarollahi2024sciagentsautomatingscientificdiscovery,
    title={SciAgents: Automating Scientific Discovery with Multi-Agent Intelligent Graph Reasoning}, 
    author={Alireza Ghafarollahi and Markus J. Buehler},
    year={2024},
    eprint={2409.05556},
    archivePrefix={arXiv},
    primaryClass={cs.AI},
    url={https://arxiv.org/abs/2409.05556}, 
}
@article{buehler2024graphreasoning,
    title={Accelerating scientific discovery through generative knowledge extraction, graph-based representations, and multimodal intelligent graph reasoning},
    author={Markus J. Buehler},
    journal={Machine Learning: Science and Technology},
    year={2024},
    url={http://iopscience.iop.org/article/10.1088/2632-2153/ad7228},
}
```