"""在 VS Code 集成终端中运行一项密码实验。

用法：python run_experiment.py 01（实验编号 01 至 05）。
"""

import argparse
import platform
import runpy
import sys
from datetime import datetime
from pathlib import Path

import cryptography


SCRIPTS = {
    "01": "01_aes_gcm.py",
    "02": "02_rsa_oaep.py",
    "03": "03_rsa_pss.py",
    "04": "04_ecdh_hkdf.py",
    "05": "05_sha256.py",
}


def main():
    parser = argparse.ArgumentParser(description="运行网络认证技术的一项密码实验")
    parser.add_argument("experiment", choices=SCRIPTS.keys(), help="实验编号 01 至 05")
    args = parser.parse_args()

    folder = Path(__file__).resolve().parent
    script = folder / SCRIPTS[args.experiment]
    print("项目目录：", folder, flush=True)
    print("Python 解释器：", sys.executable, flush=True)
    print("运行环境：", platform.platform(), flush=True)
    print("Python 版本：", platform.python_version(), flush=True)
    print("cryptography 版本：", cryptography.__version__, flush=True)
    print("执行时间：", datetime.now().astimezone().isoformat(timespec="seconds"), flush=True)
    print("实验脚本：", script.name, flush=True)
    print("-" * 48, flush=True)
    runpy.run_path(str(script), run_name="__main__")


if __name__ == "__main__":
    main()
