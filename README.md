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
</p>

</h2>

</p>

>[!IMPORTANT]
>このリポジトリのリリースノートやREADME、コミットメッセージの9割近くは[claude.ai](https://claude.ai/)や[ChatGPT4](https://chatgpt.com/)を活用した[AIRA](https://github.com/Sunwood-ai-labs/AIRA), [SourceSage](https://github.com/Sunwood-ai-labs/SourceSage), [Gaiah](https://github.com/Sunwood-ai-labs/Gaiah), [HarmonAI_II](https://github.com/Sunwood-ai-labs/HarmonAI_II), [IRIS](https://github.com/Sunwood-ai-labs/IRIS)で生成しています。

このStreamlitアプリは、PDFを音声ポッドキャスト、講義、要約などに変換します。テキスト生成と音声合成にはOpenAIのGPTモデルを使用しています。

https://github.com/user-attachments/assets/a94a33bf-8a01-4661-be25-21b0a83c43b8


## ✨ 主な機能

- 複数のPDFファイルをアップロード可能
- 異なる指示テンプレート（ポッドキャスト、講義、要約など）から選択可能
- テキスト生成と音声モデルをカスタマイズ可能
- 話者に異なる声を選択可能

## 🔧 使用方法

1. 1つまたは複数のPDFファイルをアップロード
2. 希望する指示テンプレートを選択
3. 必要に応じて指示をカスタマイズ
4. 「音声を生成」をクリックして音声コンテンツを作成


> [!WARNING]
> このアプリを使用するにはOpenAI APIキーが必要です。

## 🎧 Example

<audio controls>
  <source src="https://raw.githubusercontent.com/lamm-mit/PDF2Audio/main/SciAgents%20discovery%20summary%20-%20example.mp3" type="audio/mpeg">
  ⚠️ お使いのブラウザは音声要素をサポートしていません。 ⚠️
</audio>


## 🚀 デプロイメント手順

このアプリケーションをAWS ECRとEC2を使用してデプロイする手順は以下の通りです：

### 1. ECRリポジトリの作成

まず、Amazon Elastic Container Registry (ECR) にリポジトリを作成します：

```bash
aws ecr create-repository --repository-name pdf2audio-jp-streamlit-app --region ap-northeast-1
aws ecr describe-repositories --repository-names pdf2audio-jp-streamlit-app --region ap-northeast-1
```

これにより、新しいECRリポジトリが作成され、その詳細が表示されます。

### 2. ECRへのログイン

次に、ECRにログインします：

```bash
aws ecr get-login-password --region ap-northeast-1 | docker login --username AWS --password-stdin XXXXXX.dkr.ecr.ap-northeast-1.amazonaws.com
```

注意: `XXXXXX`の部分は、あなたのAWSアカウントIDに置き換えてください。

### 3. Dockerイメージのビルドとプッシュ

アプリケーションのDockerイメージをビルドし、ECRにプッシュします：

```bash
docker build -t pdf2audio-jp-streamlit-app .
docker tag pdf2audio-jp-streamlit-app:latest XXXXXX.dkr.ecr.ap-northeast-1.amazonaws.com/pdf2audio-jp-streamlit-app:latest
docker push XXXXXX.dkr.ecr.ap-northeast-1.amazonaws.com/pdf2audio-jp-streamlit-app:latest
```

これらのコマンドにより、ローカルでDockerイメージがビルドされ、ECRリポジトリにプッシュされます。

### 4. EC2インスタンスへの接続

アプリケーションをホストするEC2インスタンスに接続するには：

```bash
ssh -i "C:\Users\makim\.ssh\streamlit-terraform-keypair-tokyo-PEM2.pem" ubuntu@i-02c64da0e38c52135
```

注意: パスとインスタンスIDは、あなたの環境に合わせて適切に変更してください。

これらの手順により、アプリケーションをAWSクラウド環境にデプロイすることができます。EC2インスタンス上でDockerコンテナを実行し、アプリケーションを起動してください。



## 🙏 謝辞

このプロジェクトは、[https://github.com/knowsuchagency/pdf-to-podcast](https://github.com/knowsuchagency/pdf-to-podcast)と[https://github.com/knowsuchagency/promptic](https://github.com/knowsuchagency/promptic)で公開されているコードを参考にし、それに基づいています。

GitHubリポジトリ: [lamm-mit/PDF2Audio](https://github.com/lamm-mit/PDF2Audio)

## 📄 ライセンス

MIT License

## 🆕 最新情報

**バージョン: v0.1.0**

このバージョンでは、PDFを音声に変換するStreamlitアプリケーションが導入されました。また、様々なワークフローとスクリプトが追加され、GitHubとの連携が強化されました。詳細については、[v0.1.0リリースノート](https://github.com/Sunwood-ai-labs/pdf2audio-JP-st/releases/tag/v0.1.0) を参照してください。
