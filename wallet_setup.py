import os, base64, zipfile
from pathlib import Path

WALLET_DIR = Path("/tmp/oracle_wallet")

def setup_wallet():
    WALLET_DIR.mkdir(parents=True, exist_ok=True)

    zip_path = WALLET_DIR / "wallet.zip"
    zip_path.write_bytes(
        base64.b64decode(os.environ["ORACLE_WALLET_ZIP_B64"])
    )

    with zipfile.ZipFile(zip_path) as z:
        z.extractall(WALLET_DIR)

    sqlnet = WALLET_DIR / "sqlnet.ora"
    sqlnet.write_text(
        "WALLET_LOCATION = (SOURCE = (METHOD = file)\n"
        f"  (METHOD_DATA = (DIRECTORY={WALLET_DIR})))\n\n"
        "SSL_SERVER_DN_MATCH=yes\n"
    )

    return str(WALLET_DIR)
