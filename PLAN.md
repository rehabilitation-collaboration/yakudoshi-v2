# PLAN: Yakudoshi v2 — 厄年と死亡率の疫学的検証（フルスクラッチ）

## Background（なぜ必要か）
厄年論文v1（~/claude/analysis/yakudoshi-paper/）をワークフロー通りにゼロから再走する。
データ選定・分析設計・執筆まで全て独自に行う。v1の成果物は参照しない。

## Goals（成功の定義）
- 厄年が日本人の死亡率に影響するかを統計的に検証した査読可能な論文を完成させる
- writing-guide.md に沿って執筆し、阿修羅・文殊レビューをパスする
- medRxivに投稿可能な状態にする

## Non-Goals（やらないこと）
- v1の分析コード・manuscript.mdの参照・流用
- 死因別分析（全死因のみ）
- 都道府県別分析

## Test Strategy（検証方法）
- 分析コード: pytest（数値整合性・変換ロジック）
- 論文: 阿修羅・文殊レビュー（/asura-monju）
- 書誌: CrossRef照合（verify_references.py相当）

---

## 研究デザイン

### データ
- JMD Deaths_1x1.txt + Exposures_1x1.txt（1947-2024, 78年間）
- 年齢: 1歳刻み、男女別
- アウトカム: 年齢別・性別・暦年別の死亡数 / 曝露人口

### 厄年の定義
- 男性本厄: 25, 42, 61歳（数え年）
- 女性本厄: 19, 33, 37, 61歳（数え年）
- 数え年→満年齢: -1（大半の場合）、感度分析で-2も検証
- 前厄・後厄: 感度分析で検証

### 分析手法（v1との差別化ポイント）

**主分析: ノンパラメトリック・局所比較アプローチ**
- 厄年年齢の死亡率を、近傍年齢（±k歳、k=2,3,5）の死亡率と比較
- 帰無仮説: 厄年年齢の死亡率は近傍年齢の補間値と等しい
- 検定: 各暦年×性別のペアでratioを計算 → 全年にわたるratioの分布を検定
- モデルフリーな手法でスプライン仕様依存を回避

**補助分析: Poisson回帰（シンプルなモデルベース確認）**
- log(Deaths) = log(Exposure) + poly(Age) + Yakudoshi + Year調整
- v1のNB回帰より単純なモデルで、主分析の裏付けとして使う

**感度分析**
1. 数え年変換（-1 vs -2）
2. 前厄・後厄の包含
3. 近傍ウィンドウ幅（±2, ±3, ±5）
4. 時代区分別（1947-1970, 1971-2000, 2001-2024）
5. 年齢範囲制限（20-70歳）

---

### Phase 1: データ準備 + 探索的分析 ✅
- 変更対象: `data_loader.py`, `exploratory.py`（新規）
- [x] JMDデータの読み込み・パース関数を実装
- [x] 数え年→満年齢変換の定義を実装（definitions.py）
- [x] 年齢×死亡率の基本プロット（男女別、複数年重ね描き）を生成
- [x] 厄年年齢をハイライトしたプロットで視覚的に確認
- [x] pytest: 22テスト全パス

### Phase 2: 主分析（局所比較法） ✅
- 変更対象: `analysis.py`（新規）
- [x] 局所比較ratio計算の実装（各年・各性別・各厄年年齢）
- [x] ratio分布の統計検定（Wilcoxon signed-rank, permutation test）
- [x] 効果量（Cohen's d）の計算
- [x] 結果テーブルの出力（年齢別・性別・ratio中央値・95%CI・p値）

### Phase 3: 補助分析 + 感度分析 ✅
- 変更対象: `sensitivity.py`（新規）
- [x] Poisson回帰の実装（主分析の裏付け）
- [x] 感度分析5項目の実装と実行
- [x] 全結果をresults_summary.txtに出力

### Phase 4: 図表作成 ✅
- 変更対象: `plots.py`（新規）
- [x] Figure 1: 年齢別死亡率曲線（厄年年齢マーク付き）
- [x] Figure 2: 局所比較ratioのフォレストプロット（男女×厄年年齢）
- [x] Figure 3: 感度分析の結果比較プロット
- [x] 全図300 DPI、PNG + PDF出力

### Phase 5: 論文執筆 ✅
- 変更対象: `manuscript.md`（新規）
- [x] writing-guide.md参照しながら執筆
- [x] 全セクション（Title/Abstract/Intro/Methods/Results/Discussion/References）
- [ ] 参考文献はCrossRef/PubMedで全件検証 → Phase 6で実施
- [x] STROBE準拠を意識して執筆

### Phase 6: レビュー + 修正 ✅
- [x] CrossRef照合スクリプト実装・実行（12本中PASS 10, MANUAL 1, FAIL 0）
- [x] /asura-monju 実行（P1:0, P2:5, P3:15）
- [x] P1/P2指摘を修正（全5件対応済み）
- [x] PDF生成（output/manuscript.pdf）
- [x] Git init + push（rehabilitation-collaboration/yakudoshi-v2）

## リスク / Trade-offs
- 局所比較法はモデルフリーで頑健だが、交絡調整の柔軟性は低い → Poisson回帰で補完
- 数え年変換の不確実性（-1 or -2）→ 感度分析でカバー
- JMDは集計データのため個人レベルの交絡調整は不可能 → Limitationsで議論
