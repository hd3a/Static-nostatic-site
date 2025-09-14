# ⏰ 自動更新される time.json

このリポジトリは、GitHub Actions を使って **10分ごとに現在時刻（UST）を含む JSON ファイル（time.json）を生成し、自動で GitHub Pages に反映** する仕組みを持っています。
<p align="center"> <a href=" https://hd3a.github.io/Static-nostatic-site/time.json" target="_blank"> <img src="https://img.shields.io/badge/Open-time.json-blue?style=for-the-badge" alt="Open time.json"> </a> </p>
---

## 🔧 機能概要

- **10分おき**に GitHub Actions が起動
- `docs/time.json` に UST の現在時刻を書き込む
- `git commit & push` によって自動で反映
- GitHub Pages から `time.json` を誰でも取得可能

---

## 📄 time.json の内容(例)

```json
{
  "time": "2025-09-15T22:30:00+09:00"
}

--

