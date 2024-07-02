import os
os.environ["CHATGPT_API_KEY"] = "sk-xxxx" 
os.environ["CHATGPT_API_BASE"] = "xxx" # 官方 API 地址：https://api.openai.com/v1/

# !!! 若要使用 CI，注释掉上面两行并把东西放在 CI 的 secret 里
