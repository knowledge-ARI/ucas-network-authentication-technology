# 在 VS Code 中运行并截图

五个新实验分别放在独立的 Python 文件中。请由你在 VS Code 集成终端逐项运行，截图用于报告中的实验证据。当前报告中的截图和结果分析仍待补充。

## 打开项目与终端

1. 在 VS Code 选择“文件 → 打开文件夹”，打开本文件所在的 `任务二_开源密码库实验` 文件夹。
2. 选择“终端 → 选择默认配置文件 → 命令提示符”，再选择“终端 → 新建终端”。新终端应位于项目文件夹。
3. 在 VS Code 中选择 Python 解释器。可先输入 `python --version` 检查终端使用的解释器。

程序通过 Python 解释器直接执行，不需要传统编译步骤。若提示缺少 `cryptography`，由你在这个终端执行 `python -m pip install -r requirements.txt`，再重新运行对应实验。如果 `python` 命令找不到，请先在 VS Code 选择或配置本机 Python，并新建终端。

## 逐项运行

在 VS Code 的同一个项目终端中，**每次运行一条，完成并截图后再运行下一条**：

```text
python run_experiment.py 01
python run_experiment.py 02
python run_experiment.py 03
python run_experiment.py 04
python run_experiment.py 05
```

入口程序会显示项目目录、实际 Python 路径、系统与库版本、运行时间和脚本名，然后执行相应的独立实验文件：

- 01：`01_aes_gcm.py`（AES-GCM）
- 02：`02_rsa_oaep.py`（RSA-OAEP）
- 03：`03_rsa_pss.py`（RSA-PSS）
- 04：`04_ecdh_hkdf.py`（ECDH 与 HKDF）
- 05：`05_sha256.py`（SHA-256）

## 保存真实截图

等待终端出现“实验X完成”后，使用 Win+Shift+S 截取 VS Code 终端。画面应包含运行命令、实际环境、脚本名和实验输出。截图保存在项目的 `screenshots` 文件夹中，分别命名为：

```text
01_aes_gcm.png
02_rsa_oaep.png
03_rsa_pss.png
04_ecdh_hkdf.png
05_sha256.png
```

如果一屏放不下，可用两张截图保留完整输出，并在文件名末尾加 `_1`、`_2`。遇到错误时保留报错画面，不把预期结果写成实测结果。截图保存后告诉我，我会将图片插入相应章节，并据此补写结果分析。

旧版自动运行记录存放在 `历史版本_20261007`，不用于新版报告的本人截图。
