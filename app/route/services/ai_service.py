import os.path

from app._config.settings import Settings
from openai import OpenAI

from app.route.models.correct_response import CorrectResponse
from app.route.services.prompts.prompt_file import PromptFile


def correct(code: str):
    # AI 질문
    return _send_code_to_openai(code)


def load_template(file_path: str) -> str:
    with open(file_path, 'r') as file:
        return file.read()


def _send_code_to_openai(source_code: str) -> str:
    # 템플릿 로드
    template_path = os.path.join(os.path.dirname(__file__), 'prompts', PromptFile.CORRECT_TEMPLATE)
    template = load_template(template_path)

    # 템플릿에 코드 삽입
    prompt = template.format(code=source_code)

    # OpenAI API 호출
    client = OpenAI(api_key=Settings.OPEN_API_KEY)

    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": prompt},
        ],
        max_tokens=150,
        n=1,             # 한 질문에 응답의 개수
        stop=None,       # 모델 중단 시키는 기준 문자열
        temperature=0.2,  # 같은 질문에 일관성 정도 (0~1 : 높을수록 창의적인 답변)
        response_format=CorrectResponse
    )
    # 결과 반환
    return response.choices[0].message.parsed

