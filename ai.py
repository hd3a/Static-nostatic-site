import os
import requests

HF_API_TOKEN = os.environ["HF_API_TOKEN"]
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
REPO = os.environ["REPO"]
ISSUE_NUMBER = os.environ["ISSUE_NUMBER"]
CONTENT = os.environ.get("COMMENT_BODY") or os.environ.get("ISSUE_BODY", "")

# AI生成
hf_headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
hf_data = {"inputs": f"以下の質問に丁寧に返信してください:\n{CONTENT}"}

response = requests.post(
    "https://api-inference.huggingface.co/models/TheBloke/guanaco-7B-GGML",
    headers=hf_headers,
    json=hf_data
)

reply_text = response.json()[0]["generated_text"]

# GitHubにコメント投稿
gh_headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}
url = f"https://api.github.com/repos/{REPO}/issues/{ISSUE_NUMBER}/comments"
resp = requests.post(url, headers=gh_headers, json={"body": reply_text})

if resp.status_code == 201:
    print("✅ コメント返信成功")
else:
    print("❌ コメント返信失敗", resp.text)
