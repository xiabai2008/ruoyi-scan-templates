#!/usr/bin/env python3
"""生成带 Ed25519 签名的 manifest.json（插件模板仓库发布脚本）

供应链约束（与 Ruoyi-Scan 主仓库 lib/plugin_repo.py 的 verify_manifest 保持一致）：
  - files 字典按 sort_keys=True + ensure_ascii=False 序列化后签名（与消费者端一致）
  - 私钥由调用方显式传入（CI 从 GitHub Secrets 注入，用后即删），严禁提交到仓库
  - 幂等：不写入 generated_at 时间戳——文件内容不变时 manifest 字节不变，
    CI 据此判断"无变化则跳过提交"，避免每次 push 都产生噪音 commit

用法：
  python scripts/sign_manifest.py --out-dir <repo_root> --key-path <signing.key> [--version 1.1.0]
"""
import argparse
import hashlib
import json
import os
import sys

try:
    from cryptography.hazmat.primitives import serialization
except ImportError:
    sys.exit("缺少 cryptography：请先执行 pip install cryptography")


def sha256(path: str) -> str:
    """计算文件 SHA256"""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def build_files(out_dir: str) -> dict:
    """扫描仓库内容：排除 .git/、manifest.json 自身与私钥文件（只描述分发内容）

    供应链安全：signing.key* 为发布私钥（含其 .pub 副产物），严禁进入分发清单；
    signing.pub 是发布者公钥，保留在清单中供消费者下载。
    """
    hashes = {}
    _EXCLUDE_NAMES = ("manifest.json", "signing.key", "signing.key.pub")
    for root, dirs, names in os.walk(out_dir):
        dirs[:] = [d for d in dirs if d != ".git"]
        for n in sorted(names):
            if n in _EXCLUDE_NAMES:
                continue
            p = os.path.join(root, n)
            rel = os.path.relpath(p, out_dir).replace("\\", "/")
            hashes[rel] = sha256(p)
    return hashes


def sign_manifest(files: dict, key_path: str) -> str:
    """用 Ed25519 私钥对 files 字典签名（与消费者端 verify_manifest 序列化一致）"""
    with open(key_path, "rb") as f:
        key = serialization.load_pem_private_key(f.read(), password=None)
    payload = json.dumps(files, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return key.sign(payload).hex()


def main() -> int:
    ap = argparse.ArgumentParser(description="生成带 Ed25519 签名的 manifest.json")
    ap.add_argument("--out-dir", required=True, help="仓库根目录")
    ap.add_argument("--key-path", required=True, help="Ed25519 私钥 PEM 路径（从 Secrets 注入，用后即删）")
    ap.add_argument("--version", default="1.1.0", help="manifest 版本号")
    args = ap.parse_args()

    manifest_path = os.path.join(args.out_dir, "manifest.json")
    files = build_files(args.out_dir)
    manifest = {
        "schema": "ruoyi-scan-plugin-repo",
        "version": args.version,
        "files": files,
        "signature": sign_manifest(files, args.key_path),
    }
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print("签名 manifest 已生成: %s（%d 个文件）" % (manifest_path, len(files)))
    print("签名长度: %d 字节（Ed25519 应为 64）" % len(bytes.fromhex(manifest["signature"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())