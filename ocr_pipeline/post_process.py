from openai import AsyncOpenAI
import httpx
from settings import settings
import asyncio
import json
import os
from pathlib import Path
import httpx
import json
from openai import OpenAI
from system_prompts import system_prompt_question_generation, system_prompt_OCR, webpage


def refine_extracted_text_LLM(text: str, system_prompt: str):
    proxies = {
        "http://": settings.get_environment_variable("OPENAI_PROXY"),
        "https://": settings.get_environment_variable("OPENAI_PROXY"),
    }
    openai_client = OpenAI(
        api_key=settings.get_environment_variable("OPENAI_API_KEY"),
        http_client=httpx.Client(proxies=proxies, verify=False),
    )
    
    user_query = f"""
    The context from which to generate questions is delimited with XML tags as follows:
    <context>
    {text}
    </context>
    """
    completion = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_query},
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
    output_file = (
        input_path.parent / f"{input_path.stem}-post_process{input_path.suffix}"
    )

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(output_data, file, ensure_ascii=False, indent=4)


async def main():
    input_file = (
        "ocr_pipeline/output_json/1288-Test-Araye-Adabi-Pasokh-[konkur.in].json"
    )
    await process_json_file(input_file, system_prompt_OCR)


if __name__ == "__main__":
    # asyncio.run(main())
    print(
        refine_extracted_text_LLM(
            text=webpage, system_prompt=system_prompt_question_generation
        )
    )
