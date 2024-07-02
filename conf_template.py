max_length = 4095

model="gpt-3.5-turbo"
# model="gpt-4o"

target_lang = {
    "en": "English",
    # "fr": "French"
}

dir_to_translate = "/path/to/dir"

exclude_list = []

tips_translated_by_chatgpt = {
    "en": "\n\n> This doc was automatically translated by GPT and has not been proofread yet. Please give us feedback in issue if any omissions.\n"
    # "fr": "\n\n> Ce document a été traduit automatiquement par GPT et n'a pas encore été relu. Veuillez nous faire part de vos commentaires en cas d'omission.\n"
}

template = {
    "en": "",
    # "fr": ""
}