from openai import AsyncOpenAI
import httpx
from settings import settings
import asyncio
import json
import os
from pathlib import Path
import httpx
from openai import OpenAI


system_prompt = """
You will be provided with text primarily in Persian that has been extracted using Tesseract OCR. Due to limitations of the OCR engine, the text may contain typos, misrecognized characters, and may include headers, footers, or other trivial content from the PDF pages.

Your task is to clean and correct the text while preserving its original intent and phrasing. Please follow these steps carefully:

### Step 1: Analyze the Text

- Carefully read and analyze the text to fully understand its underlying meaning. This will help you identify and correct typos and misspellings.

### Step 2: Remove Trivial Text

- Remove any trivial content such as headers, footers, small-sized text that precedes paragraphs, and incomplete sentences.

### Step 3: Correct Typos

- After understanding the intent of the text, correct any typos and misrecognized characters. For example:
  - "چ" might be detected as "ج".
  - "پ" might be detected as "ب".
  - There may be spacing issues or other problems that need correction.
- Make sure not to change the intent and phrasing of the text.
- Ensure that the corrected sentences are valid and coherent.

**Important Instructions:**

- Do not alter the original intent and phrasing of the text.
- Provide the corrected text in Persian.
- Do not include any additional explanations or comments; only present the corrected text.
"""


def refine_extracted_text_LLM(text: str, system_prompt: str):
    proxies = {
        "http://": settings.get_environment_variable("OPENAI_PROXY"),
        "https://": settings.get_environment_variable("OPENAI_PROXY"),
    }


    openai_client = OpenAI(
        api_key=settings.get_environment_variable("OPENAI_API_KEY"),
        base_url=settings.get_environment_variable("OPENAI_BASE_URL"),
        http_client=httpx.Client(proxies=proxies, verify=False),
    )

    completion =  openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text},
        ],
    )
    return completion.choices[0].message.content

async def refine_extracted_text_LLM_async(text: str, system_prompt: str):
    proxies = {
        "http://": settings.get_environment_variable("OPENAI_PROXY"),
        "https://": settings.get_environment_variable("OPENAI_PROXY"),
    }

    async with httpx.AsyncClient(proxies=proxies, verify=False) as client:
        openai_client = AsyncOpenAI(
            api_key=settings.get_environment_variable("OPENAI_API_KEY"),
            base_url=settings.get_environment_variable("OPENAI_BASE_URL"),
            http_client=client,
        )

        completion = await openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text},
            ],
        )
        return completion.choices[0].message.content

async def process_json_file(input_file: str, system_prompt: str):

    with open(input_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    tasks = []
    for key, text in data.items():
        tasks.append(refine_extracted_text_LLM_async(text, system_prompt))

    refined_texts = await asyncio.gather(*tasks)

    # Save the results in a new JSON file
    output_data = {key: refined_texts[i] for i, key in enumerate(data.keys())}
    input_path = Path(input_file)
    output_file = input_path.parent / f"{input_path.stem}-post_process{input_path.suffix}"

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(output_data, file, ensure_ascii=False, indent=4)

async def main():
    input_file = "ocr_pipeline/output_json/1288-Test-Araye-Adabi-Pasokh-[konkur.in].json"
    await process_json_file(input_file, system_prompt)

if __name__ == "__main__":
    asyncio.run(main())