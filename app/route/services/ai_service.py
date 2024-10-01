from json import loads
from os import path
from time import sleep

import aiofiles
from openai import OpenAIError, APITimeoutError, AsyncOpenAI

from app._config.settings import Settings
from app.route.models.correct_response import CorrectResponse, ModifiedCode
from app.route.services.exception.enum.error_enum import ErrorEnum
from app.route.services.exception.openai_exception import OpenaiException
from app.route.services.prompts.prompt_file import PromptFile
from app.web.logger import logger


async def correct(code: str) -> CorrectResponse:
    # 템플릿 로드
    template_path = path.join(path.dirname(__file__), 'prompts', PromptFile.CORRECT_TEMPLATE)
    template = await _load_template(template_path)

    prompt = template.format(code=code)

    response_data = await _call_openai_api(prompt)

    return await _parse_correct_response(response_data)


async def _load_template(file_path) -> str:
    async with aiofiles.open(file_path, 'r') as file:
        return await file.read()


async def _parse_correct_response(response_data: dict) -> CorrectResponse:
    modified_codes_data = response_data["modified_codes"]
    # ModifiedCode 리스트 생성
    modified_codes = [
        ModifiedCode(line=item["line"], code=item["code"])
        for item in modified_codes_data
    ]
    return CorrectResponse(reason=response_data["reason"], modified_codes=modified_codes)


async def _call_openai_api(prompt: str,  max_retries: int = 2, delay: int = 1) -> dict:
    retries = 0
    client = AsyncOpenAI(api_key=Settings.OPEN_API_KEY, timeout=20, max_retries=1) # 20s

    while retries < max_retries:
        try:
            response = await client.chat.completions.create(
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
            return loads(response.choices[0].message.content)

        except APITimeoutError as e:
            # Timeout 발생 시 재시도
            retries += 1
            if retries < max_retries:
                logger.error(f"OpenAI API 연결 실패: {e}. {delay}초 후 재시도 ({retries}/{max_retries})")
                sleep(delay)
            else:
                raise OpenaiException(ErrorEnum.OPNEAI_SERVER_ERROR, _extract_openai_error(e))

        except OpenAIError as e:
            raise OpenaiException(ErrorEnum.OPNEAI_SERVER_ERROR, _extract_openai_error(e))


def _extract_openai_error(e: OpenAIError) -> dict:
    response = getattr(e, 'response', None)  # response가 없으면 None 반환
    status_code = response.status_code if response else "Unknown"  # response가 없으면 'Unknown'

    return {
        "error_type": type(e).__name__,  # 예외 클래스 이름
        "message": str(e),  # 예외 메시지
        "status_code": status_code  # 상태 코드
    }