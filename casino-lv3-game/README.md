# Royal Table Ultimate - 使い方

ローカル専用のカジノゲームです。  
実マネー機能はありません（遊戯用チップのみ）。

## 1. 起動方法

```powershell
cd C:\uep-v5-ultimate-enterprise-platform\casino-lv3-game
npm install
npm run dev
```

ブラウザで `http://127.0.0.1:30080` を開きます。  
終了はターミナルで `Ctrl + C`。

## 2. 画面の基本操作

- `mode` でゲームモード切替
  - `Blackjack+`
  - `5 Card Poker`
  - `Texas Hold'em`
- `theme` で見た目切替（Classic / Neon / VIP）
- `CPU` でCPU難易度切替（Hold'em向け）
- `BGM ON/OFF` でBGM切替
- `SFX/BGM/Effects/Init Chips` で設定を変更し、`設定適用`で保存

## 3. 各モードの遊び方

### Blackjack+

- `配札` で開始
- `Hit` で1枚引く
- `Stand` で確定
- `Double` で賭け金2倍 + 1枚引いて強制Stand
- `Split` は最初の2枚が同ランクのとき有効
- `Insurance` はDealer公開カードがAのとき有効

### 5 Card Poker

- `配札` で5枚ずつ自動配布
- 自動で役判定し、キッカー比較まで行って勝敗を決定

### Texas Hold'em

- `配札` で開始（SB/BBを徴収して開始）
- アクション順は固定
  - `Preflop`: プレイヤー先攻
  - `Flop / Turn / River`: AI先攻
- 各ストリートで、プレイヤーが手動アクションを選択
  - `Fold / Check / Call / Bet / Raise / All-in`
- レイズ額はスライダーで指定
- `Pot / P Stack / AI Stack` を見ながら進行
- オールイン時はサイドポット精算（ヘッズアップ簡易版）に対応
- CPUは `Normal / Hard` でレンジ/ブラフ頻度が変化

#### 5bet / 再再応答フロー

- プレイヤーが `Raise` し、AIが `re-raise` を返した場合、再選択UIが出ます
  - `Fold / Call / Raise(4bet) / All-in`
- プレイヤーが `4bet` した後、AIは `fold / call / five-bet` を選択
- AIが `five-bet` を選んだ場合、プレイヤーはもう一度選択します
  - `Fold / Call / All-in`
- すべてのアクションは金額付きで `AI対戦ログ` と `リプレイ` に保存されます
- 同点時はポットを分割し、奇数端数はプレイヤー側に1チップ配分されます

## 4. リプレイと保存

- `リプレイ再生` で手番ごとの再描画再生
- `リプレイ保存` で現在のリプレイをローカル保存
- `保存リプレイ読込` で保存済みリプレイを再利用

## 5. 戦績ダッシュボード

以下を画面上部で確認できます。

- Chips
- Wins / Losses
- Games
- WinStreak / MaxStreak
- AI Win / AI Loss
- Pot / P Stack / AI Stack（対戦中）

さらに、右下パネルに以下が表示されます。

- 役や結果の出現回数
- AI対戦ログ（ストリートごとの行動）

## 6. トラブル時

- 反映されない: ブラウザを再読み込み
- まだ反映されない: `Ctrl + C` 後に `npm run dev` を再実行
- 音が鳴らない: ブラウザタブを一度クリックしてから再操作（ブラウザの自動再生制限対策）
- 設定が戻る: `設定適用`を押した後にプレイ開始
