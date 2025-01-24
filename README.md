# 100try11_SNStextgenerater
# SNSキャプション生成アプリ

📸 商品画像からInstagram向けの魅力的なキャプションを自動生成するAIアプリ

![Demo](demo.gif) <!-- スクリーンショットやデモ動画を追加 -->

## ✨ 特徴

- **画像認識AI連携**：Google Gemini Pro Visionを活用した高度な画像解析
- **ワンクリック生成**：3種類のキャプションパターンを自動提案
- **履歴管理**：過去の生成結果をサイドバーで確認可能
- **レスポンシブデザイン**：スマートフォン・タブレット・PCに対応
- **多機能UI**：
  - クリップボードコピー機能
  - 再生成＆リセット機能
  - アニメーション付きインターフェース

## 🛠 技術スタック

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-FF4B4B?logo=streamlit)
![Gemini](https://img.shields.io/badge/Gemini_API-1.5_Flash-4285F4?logo=google)

| カテゴリ       | 技術要素                     |
|----------------|-----------------------------|
| フロントエンド | Streamlit                   |
| AI処理         | Google Gemini Pro Vision    |
| 画像処理       | Pillow                      |
| 設定管理       | python-dotenv 