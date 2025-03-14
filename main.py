from dotenv import load_dotenv
import json
from openai import OpenAI
import sys

load_dotenv()

def get_gpt4_json_response(prompt):
  client = OpenAI()

  completion = client.chat.completions.create(
      model="gpt-4o",
      messages=[
        {
          "role": "system",
          "content": "You are an AI assistant."
        },
        {
          "role": "user",
          "content": prompt
        }
      ],
      response_format={
          "type": "json_schema",
          "json_schema": {
            "name": "math_response",
            "strict": True,
            "schema": {
              "type": "object",
              "properties": {
                "steps": {
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "explanation": {
                        "type": "string"
                      },
                      "output": {
                        "type": "string"
                      }
                    },
                    "required": [
                      "explanation",
                      "output"
                    ],
                    "additionalProperties": False
                  }
                },
                "final_answer": {
                  "type": "string"
                }
              },
              "additionalProperties": False,
              "required": [
                "steps",
                "final_answer"
              ]
            }
          }
        },
  )

  # return completion.choices[0].message.content

  return json.loads(completion.choices[0].message.content)

if __name__ == "__main__":
  if len(sys.argv) < 2:
    print("Usage: python main.py \"Your prompt here\"")
    sys.exit(1)
  
  user_prompt = sys.argv[1]
  response = get_gpt4_json_response(user_prompt)
  # print(response)
  print(json.dumps(response, indent=2))