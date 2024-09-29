import json
import os.path

from openai.types.chat import ChatCompletion

from app._config.settings import Settings
from openai import OpenAI

from app.route.models.correct_response import CorrectResponse, ModifiedCode
from app.route.services.prompts.prompt_file import PromptFile


def correct(code: str) -> CorrectResponse:
    # 템플릿 로드
    template_path = os.path.join(os.path.dirname(__file__), 'prompts', PromptFile.CORRECT_TEMPLATE)
    template = _load_template(template_path)

    prompt = template.format(code=code)

    response_data = _call_openai_api(prompt)

    return _parse_correct_response(response_data)


def _load_template(file_path) -> str:
    with open(file_path, 'r') as file:
        return file.read()


def _parse_correct_response(response_data: json) -> CorrectResponse:
    modified_codes_data = response_data["modified_codes"]
    # ModifiedCode 리스트 생성
    modified_codes = [
        ModifiedCode(line=item["line"], code=item["code"])
        for item in modified_codes_data
    ]
    return CorrectResponse(reason=response_data["reason"], modified_codes=modified_codes)


def _call_openai_api(prompt: str) -> json:
    client = OpenAI(api_key=Settings.OPEN_API_KEY)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": prompt},
        ],
        max_tokens=150,
        n=1,  # 한 질문에 응답의 개수
        stop=None,  # 모델 중단 기준 문자열
        temperature=0.4,  # 같은 질문에 일관성 정도 (0~1 : 높을수록 창의적인 답변)

        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)
