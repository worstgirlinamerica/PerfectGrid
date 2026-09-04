import deepl
import os

key = os.environ["DEEPL_API_KEY"]
translator = deepl.Translator(key)

with open("README.md", "r", encoding="utf-8") as f:
    text = f.read()

languages = {
    "zh": "ZH",
    "pt": "PT-PT",
    "es": "ES",
    "ja": "JA",
    "fr": "FR",
    "de": "DE",
    "ko": "KO",
}

for code, deepl_code in languages.items():
    result = translator.translate_text(text, target_lang=deepl_code)
    with open(f"docs/README.{code}.md", "w", encoding="utf-8") as f:
        f.write(str(result))
    print(f"Wrote docs/README.{code}.md")
