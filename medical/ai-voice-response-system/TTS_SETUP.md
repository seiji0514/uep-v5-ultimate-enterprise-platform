# TTS（音声合成）セットアップガイド

## 問題: TTSライブラリが利用できません

サーバー起動時に「TTSライブラリが利用できません」という警告が表示される場合、音声合成機能が動作しません。

## 解決方法

### 方法1: pyttsx3をインストール（推奨・簡単）

```bash
pip install pyttsx3
```

**Windowsの場合**: 追加の設定は不要です（SAPI5が標準で利用可能）

**Linuxの場合**: 以下のいずれかをインストールしてください：
```bash
# Ubuntu/Debian
sudo apt-get install espeak

# または
sudo apt-get install festival
```

**Macの場合**:
```bash
brew install espeak
```

### 方法2: transformers TTSをインストール（高品質・重い）

```bash
pip install torch transformers librosa soundfile
```

**注意**: 初回起動時にモデルのダウンロードに時間がかかります（数GB）

## 動作確認

サーバーを再起動して、以下のメッセージが表示されることを確認してください：

```
INFO - pyttsx3エンジンを初期化しました
```

または

```
INFO - transformers TTSパイプラインを初期化しました
```

## トラブルシューティング

### pyttsx3がインストールできない

```bash
# pipをアップグレード
python -m pip install --upgrade pip

# 再度インストール
pip install pyttsx3
```

### Windowsでpyttsx3が動作しない

1. Windowsの音声設定を確認
2. 管理者権限で実行してみる
3. 別のTTSエンジン（transformers）を試す

### Linuxでespeakが動作しない

```bash
# espeakのバージョン確認
espeak --version

# 日本語サポートの確認
espeak --voices | grep jp
```

## 推奨設定

**ローカル・無料・軽量**: `pyttsx3`（推奨）
- インストールが簡単
- リソース使用量が少ない
- オフラインで動作

**高品質・多機能**: `transformers TTS`
- より自然な音声
- カスタマイズ可能
- リソース使用量が多い
