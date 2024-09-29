import os
import sys
from github import Github

def add_collaborator_to_repo(repo_name, collaborator):
    # GitHubのPersonal Access Tokenを環境変数から取得
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        print("Error: GITHUB_TOKEN environment variable not set.")
        sys.exit(1)

    # GitHubクライアントを初期化
    g = Github(token)

    try:
        # 認証されたユーザーを取得
        user = g.get_user()

        # 既存のリポジトリを取得
        repo = user.get_repo(repo_name)

        # コラボレーターを追加
        repo.add_to_collaborators(collaborator)
        print(f"Added {collaborator} as a collaborator to {repo_name}.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <repo_name> <collaborator>")
        sys.exit(1)

    repo_name = sys.argv[1]
    collaborator = sys.argv[2]
    add_collaborator_to_repo(repo_name, collaborator)

# python github_add_collaborator.py pdf2audio-JP-st iris-s-coon
