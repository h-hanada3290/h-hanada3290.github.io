import json
import base64
import zlib
import sys

def decode_session_data(encoded_data):
    """
    Flaskセッションのエンコードされたデータをデコードします。
    Base64とZlib圧縮を考慮します。
    
    Args:
        encoded_data (str): エンコードされたセッションデータ。

    Returns:
        dict or None: デコードされたセッションデータ、またはNone。
    """
    if not encoded_data:
        return None
    
    # URLセーフなBase64デコード
    decoded_bytes = base64.urlsafe_b64decode(encoded_data)
    
    # Zlib圧縮を解除
    try:
        decompressed_bytes = zlib.decompress(decoded_bytes)
    except zlib.error:
        # 圧縮されていない場合はそのまま使用
        decompressed_bytes = decoded_bytes

    # JSONとしてデコード
    try:
        return json.loads(decompressed_bytes)
    except json.JSONDecodeError:
        return None

def find_locks_in_csv(file_path):
    """
    CSVファイル内の各セッションデータから'locks'情報を抽出して表示します。

    Args:
        file_path (str): CSVファイルのパス。
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                if i == 0:  # ヘッダー行をスキップ
                    continue

                parts = line.strip().split(',')
                # セッションデータが格納されている列のインデックスを適切に設定してください
                session_data = parts[1] # 仮に2列目にあると想定

                decoded_session = decode_session_data(session_data)
                
                if decoded_session and 'locks' in decoded_session:
                    print(f"--- 行 {i+1} のロック情報 ---")
                    print(json.dumps(decoded_session['locks'], indent=2))
                    print("-" * 20)

    except FileNotFoundError:
        print(f"エラー: ファイルが見つかりません。パスを確認してください: {file_path}")
    except Exception as e:
        print(f"予期せぬエラーが発生しました: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使い方: python check_session_locks.py <csv_file_path>")
    else:
        csv_file_path = sys.argv[1]
        find_locks_in_csv(csv_file_path)

```
eof

### 使用方法

1.  上記のコードを `check_session_locks.py` として保存します。
2.  ターミナルで以下のコマンドを実行します。

    ```bash
    python check_session_locks.py your_sessions.csv
    
