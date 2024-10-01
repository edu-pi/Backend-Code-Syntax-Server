from json import loads
from os import path
from time import sleep

import aiofiles
from openai import OpenAIError, APITimeoutError, AsyncOpenAI

from app.config.settings import Settings
from app.route.models.correct_response import CorrectResponse, ModifiedCode
from app.route.models.hint_response import HintResponse
from app.route.services.exception.enum.error_enum import ErrorEnum
from app.route.services.exception.openai_exception import OpenaiException
from app.route.services.prompts.prompt_file_name import PromptFileName
from app.web.logger import logger


async def correct(code: str) -> CorrectResponse:
    template_path = path.join(path.dirname(__file__), 'prompts', PromptFileName.CORRECT_TEMPLATE)
    template = await _load_template(template_path)

    prompt = template.format(code=code)
    response_data = await _call_openai_api(prompt)

    return await CorrectResponse.of(response_data)


async def hint(line: int, code: str) -> HintResponse:
    template_path = path.join(path.dirname(__file__), 'prompts', PromptFileName.HINT_TEMPLATE)
    template = await _load_template(template_path)

    prompt = template.format(line=line, code=code)
    response_data = await _call_openai_api(prompt)

    return await HintResponse.of(response_data)


async def _load_template(file_path) -> str:
    async with aiofiles.open(file_path, 'r') as file:
        return await file.read()


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
                raise OpenaiException(ErrorEnum.OPNEAI_SERVER_ERROR, e)

        except OpenAIError as e:
            raise OpenaiException(ErrorEnum.OPNEAI_SERVER_ERROR, e)


