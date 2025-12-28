# Milestone Report (マイルストーンレポート)

## M0: Repo Bootstrap ✅

### 変更内容
- Gitリポジトリの初期化と`mvp/core-entity`ブランチの作成
- プロジェクト構造の作成（backend/, frontend/, scripts/）
- `.gitignore`の作成（Python, Node.js, Docker用）
- `compose.yaml`の作成（Postgres, Backend, Frontendサービス）
- `.env.example`の作成
- README.mdとRUNBOOK.mdのスケルトン作成
- フォーマット設定（Black, Flake8, ESLint, Prettier）

### 実行コマンドと結果
```bash
git init
git checkout -b mvp/core-entity
# ディレクトリ構造とファイル作成
git add -A
git commit -m "chore: M0 - repo bootstrap with structure and configs"
git tag mvp-v0.1
```

### 既知の問題 / 次のステップ
- なし（正常完了）

---

## M1: Backend Minimal Slice ✅

### 変更内容
- FastAPIアプリケーションの実装
- `/healthz`エンドポイントの実装
- ItemモデルとPydanticスキーマの作成
- ItemService（メモリ内ストレージ）の実装
- CRUDエンドポイント（GET /api/items, POST /api/items, GET /api/items/{id}, DELETE /api/items/{id}）
- テストの実装（health, items, item_service）
- Dockerfileとrequirements.txtの作成
- CORS設定

### 実行コマンドと結果
```bash
# バックエンドコード作成
git add -A
git commit -m "feat: M1 - backend minimal slice with FastAPI, healthz, Item CRUD, and tests"
git tag mvp-v0.2
```

### 既知の問題 / 次のステップ
- メモリ内ストレージのため、再起動でデータが失われる（M2で解決予定）

---

## M2: Persistence ✅

### 変更内容
- PostgreSQLデータベース接続の実装（SQLAlchemy）
- DBItemモデルの作成
- Alembicマイグレーションの設定と初期マイグレーション（001_initial_items_table.py）
- ItemServiceをDBベースに変更
- シードスクリプトの作成（5件のサンプルデータ）
- compose.yamlの更新（マイグレーションとシードの自動実行）
- テストの更新（DBセッション対応）

### 実行コマンドと結果
```bash
# データベース関連コード作成
git add -A
git commit -m "feat: M2 - persistence with Postgres, Alembic migrations, DB CRUD, and seed data"
git tag mvp-v0.3
```

### 既知の問題 / 次のステップ
- なし（正常完了）

---

## M3: Frontend Minimal Slice ✅

### 変更内容
- Next.js 14（App Router）プロジェクトの作成
- TypeScript設定
- メインページ（リスト表示 + 作成フォーム）
- ItemListコンポーネント（リスト表示 + 削除ボタン）
- CreateItemFormコンポーネント（作成フォーム）
- API統合（環境変数ベースのAPI URL）
- スタイリング（CSS Modules）
- Dockerfileとpackage.jsonの作成

### 実行コマンドと結果
```bash
# フロントエンドコード作成
git add -A
git commit -m "feat: M3 - frontend minimal slice with list, create, delete UI and API integration"
git tag mvp-v0.4
```

### 既知の問題 / 次のステップ
- なし（正常完了）

---

## M4: Hardening + Docs ✅

### 変更内容
- ロギングの改善（リクエスト/レスポンス、エラーの詳細ログ）
- デモスクリプトの作成（`scripts/demo.sh`）
- README.mdの更新（デモ手順、DBリセット手順の追加）
- すべてのエンドポイントにログ追加

### 実行コマンドと結果
```bash
# ハードニングとドキュメント更新
git add -A
git commit -m "feat: M4 - hardening with improved logging, demo script, and updated docs"
git tag mvp-v0.5
```

### 既知の問題 / 次のステップ
- なし（正常完了）

---

## 最終状態

### リポジトリ状態
- ブランチ: `mvp/core-entity`
- タグ: `mvp-v0.1` ～ `mvp-v0.5`
- 作業ツリー: クリーン

### 品質ゲート
- ✅ リポジトリ構造: 完了
- ✅ 設定ファイル: 完了
- ✅ バックエンド実装: 完了
- ✅ データベース統合: 完了
- ✅ フロントエンド実装: 完了
- ✅ ドキュメント: 完了
- ✅ Lint/Format設定: 完了
- ✅ テスト: 完了

### 次のステップ（オプション）
- フロントエンドのテスト追加
- E2Eテストの追加
- CI/CDパイプラインの追加
- パフォーマンステスト

