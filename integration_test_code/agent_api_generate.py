__doc__ = """
use LLM to generate Java Spring Boot API integration test code
this class want to help generate Java Spring Boot API integration test code
1. find API relate code, such as request parameter class and API path
2. generate integration test code with template code
3. add mock some bean and mock data into test code

I think there is an AI agent task because it has to ask AI many times 
we will give a Spring boot Controller file content to AI.
firstly, we have to ask AI where it is related code and get code file path, for this step we can require structure JSON format
secondly, we can read code file and get code content
thirdly, we can ask AI to generate integration test code with template prompt
"""

import json
import os
from ollama import chat
from pydantic import BaseModel


example_code_path = ['spring-request/src/test/java/pro/demo/springrequest/UserControllerIntegrationTest.java']

class RequestParameter(BaseModel):
    class_name: str
    full_file_path: str
    package_name: str
    name: str


class APIInformation(BaseModel):
    method_name: str
    api_path: str
    relative_file_path: str
    full_file_path: str
    class_name: str
    request_parameter_for_url: list[RequestParameter]
    request_body: list[RequestParameter]


class APIGenerator:
    def __init__(self):
        pass

    def analyze(self, file_path):
        """
        analyze API relate code
        """
        # read file
        code_content = ''
        with open(file_path, 'r', encoding='utf-8') as f:
            code_content = f.read()
        api_information = self.find_api_relation_code(code_content, file_path)
        if api_information is None:
            raise Exception("can not find API relate code")


        request_body_file_content = ''
        if api_information.request_body:
            for parameter in api_information.request_body:
                path = parameter.full_file_path
                request_body_file_content += open(path, 'r', encoding='utf-8').read()
        request_parameter_file_content = ''
        if api_information.request_parameter_for_url:
            for parameter in api_information.request_parameter_for_url:
                path = parameter.full_file_path
                request_parameter_file_content += open(path, 'r', encoding='utf-8').read()


        example_code = ''
        for file in example_code_path:
            example_code = open(file, 'r', encoding='utf-8').read()

        # generate integration test code
        message = f"here's Java code with SpringBoot framework, I ask you generate integration test code, full_file_path = {file_path}, content = {code_content}, api_information = {api_information}, request_body_file_content = {request_body_file_content}, request_parameter_file_content = {request_parameter_file_content} I want to generate test case which include assertion for different assert annotation, for example @NotBlank @Size @NotNull, you have to use Spring Boot mvc test framework, and you have to mock some bean and mock data, this is a example code {example_code}"

        response = self.generate_integration_test_code(message)
        print(response)
        open('result.txt', 'w', encoding='utf-8').write(response)



    def find_api_relation_code(self, code_content, file_path) -> APIInformation:
        """
        find API relate code, such as request parameter class and API path
        """
        message = f"here's Java code with SpringBoot framework, I ask you read it and find API endpoint information, full_file_path = {file_path}, content = {code_content} in general, API endpoint is a method with annotation like @GetMapping, @PostMapping, @PutMapping, @DeleteMapping, @RequestMapping and it has a path, such as @GetMapping(\"/hello/name\"), I want to know method name, api path, relative file path, full file path, request parameter for url, request body. try to figure out parameter class type and full file path"
        print("request = " + message)
        response = chat(
            model="deepseek-r1:32b",
            messages=[
                {
                    "role": "user",
                    "content": message

                }],
            stream=False,
            format=APIInformation.model_json_schema()
        )
        print(response.message.content)
        return APIInformation(**json.loads(response.message.content))

    def generate_integration_test_code(self, message):
        response = chat(
            model="deepseek-r1:32b",
            messages=[
                {
                    "role": "user",
                    "content": message

                }],
            stream=False
        )
        return response.message.content


if __name__ == '__main__':
    api_generator = APIGenerator()
    api_generator.analyze(
        '')
