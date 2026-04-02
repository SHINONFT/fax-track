"""
GA4 Measurement ID を index.html に埋め込む + QRコード付きPDFを更新するセットアップスクリプト

使い方:
  python setup.py G-XXXXXXXXXX

引数:
  GA4 Measurement ID（例: G-ABC1234567）
    → Googleアナリティクス > 管理 > データストリーム > ウェブ > 測定ID
"""

import sys
import re
import subprocess
from pathlib import Path

# ──────────────────────────────────────────
# GA4 ID を index.html に埋め込む
# ──────────────────────────────────────────

def embed_ga_id(ga_id: str):
    path = Path(__file__).parent / "index.html"
    html = path.read_text(encoding="utf-8")

    if "GA_MEASUREMENT_ID" not in html:
        # すでに埋め込み済みか確認
        if ga_id in html:
            print(f"✅ GA4 ID はすでに設定済みです: {ga_id}")
            return
        # 別のIDが入っている場合は置換
        html = re.sub(r"G-[A-Z0-9]+", ga_id, html)
        path.write_text(html, encoding="utf-8")
        print(f"✅ GA4 ID を更新しました: {ga_id}")
        return

    html = html.replace("GA_MEASUREMENT_ID", ga_id)
    path.write_text(html, encoding="utf-8")
    print(f"✅ GA4 ID を埋め込みました: {ga_id}")


# ──────────────────────────────────────────
# QRコード付きPDFを更新する
# ──────────────────────────────────────────

def update_pdf_qr(tracking_url: str):
    """
    kasuhara_fax.pdf の QR コードを tracking_url に更新する。
    fax プロジェクトフォルダの update_qr.py を呼び出す。
    """
    update_script = Path(__file__).parent.parent / "files (1)" / "update_qr.py"
    if not update_script.exists():
        print(f"\n📋 次のコマンドでPDFのQRコードを更新してください:")
        print(f"   python update_qr.py \"{tracking_url}\"")
        return

    result = subprocess.run(
        [sys.executable, str(update_script), tracking_url],
        capture_output=True, text=True
    )
    print(result.stdout)
    if result.returncode != 0:
        print(f"⚠️  PDF更新エラー: {result.stderr}")


# ──────────────────────────────────────────
# メイン
# ──────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("\nGA4 Measurement IDを引数として指定してください:")
        print("  python setup.py G-XXXXXXXXXX")
        sys.exit(1)

    ga_id = sys.argv[1].strip()
    if not re.match(r"^G-[A-Z0-9]+$", ga_id):
        print(f"❌ 無効なGA4 ID形式: {ga_id}")
        print("   形式: G-XXXXXXXXXX（例: G-ABC1234567）")
        sys.exit(1)

    print(f"\n🔧 セットアップ開始: {ga_id}\n")
    embed_ga_id(ga_id)

    # GitHub Pages URL（GitHubユーザー名に合わせて変更）
    tracking_url = "https://shinonft.github.io/fax-track/"

    print(f"\n📋 次のステップ:")
    print(f"   1. GitHub Pages URL: {tracking_url}")
    print(f"   2. PDFのQRコード更新: python update_qr.py \"{tracking_url}\"")
    print(f"   3. GitHub に push: cd fax-track && git push")
    print(f"   4. FAX送信再開: python step2_send_fax.py")


if __name__ == "__main__":
    main()
