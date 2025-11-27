import os, json, pathlib
print("当前工作目录:", pathlib.Path.cwd())
mem = pathlib.Path("PYTHON/hezhaoyi_memory.json").resolve()
print("记忆文件绝对路径:", mem)
print("文件存在？", mem.exists())