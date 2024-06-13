# Report Translator

该代码自 [Auto-i18n](https://github.com/linyuxuanlin/Auto-i18n) 上修改，是其针对测试报告的特化版本。

其进行了以下改进：
- OpenAI API 升级：去除了过时的 API 使用
- 文件夹批量翻译
- 代码块提取
- 改进的 promote
- 上下文

同时删除了如 Front Matter 等不需要的内容。

## 使用方法

获取代码后，安装必要的模块：
```bash
pip install -r requirements.txt
```

配置你的环境：
- env.py 中配置你的 API 和提供该 API 的 URL（如你使用的某免费 API）。请基于 env_template.py 修改
- conf.py 中客制化你的配置，如 token 长度、目标语言、文件夹等。请基于 conf_template.py 修改
- 运行它：`python auto-translate.py`

## Tip

免费 API：[GPT_API_free](https://github.com/chatanywhere/GPT_API_free)