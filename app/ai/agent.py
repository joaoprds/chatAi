
import json

from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.ai.client import client
from app.ai.tool_definitions import tools
from app.ai.schemas import (
    GetProductStockInput,
    GetCustomerOrdersInput,
)
from app.ai.tools import (
    get_product_stock,
    get_customer_orders,
)
from app.core.config import settings


MAX_TOOL_ROUNDS = 5


def execute_tool(
    db: Session,
    company_id: int,
    tool_name: str,
    arguments: str,
) -> dict:

    try:
        parsed_arguments = json.loads(arguments)

        if tool_name == "get_product_stock":
            params = GetProductStockInput.model_validate(
                parsed_arguments
            )

            return get_product_stock(
                db=db,
                company_id=company_id,
                params=params,
            )

        if tool_name == "get_customer_orders":
            params = GetCustomerOrdersInput.model_validate(
                parsed_arguments
            )

            return get_customer_orders(
                db=db,
                company_id=company_id,
                params=params,
            )

        return {
            "success": False,
            "message": "Unknown tool."
        }

    except (json.JSONDecodeError, ValidationError) as exc:
        return {
            "success": False,
            "message": "Invalid tool arguments.",
            "details": str(exc),
        }


def run_agent(
    db: Session,
    company_id: int,
    user_message: str,
) -> str:

    input_items = [
        {
            "role": "user",
            "content": user_message,
        }
    ]

    instructions = """
    You are an enterprise operations assistant.

    You can answer questions about products, inventory,
    customers and orders.

    Rules:
    - Use available tools when business data is required.
    - Never invent inventory quantities or order information.
    - Only use information returned by the tools.
    - If a tool reports that information was not found,
      communicate that clearly.
    - You are a read-only assistant.
    - Never claim that you modified business data.
    - Answer in the same language as the user.
    """

    for _ in range(MAX_TOOL_ROUNDS):

        response = client.responses.create(
            model=settings.openai_model,
            instructions=instructions,
            input=input_items,
            tools=tools,
        )

        function_calls = [
            item
            for item in response.output
            if item.type == "function_call"
        ]

        if not function_calls:
            return response.output_text

        # Preserve the model's response, including its tool calls.
        input_items.extend(response.output)

        for tool_call in function_calls:

            result = execute_tool(
                db=db,
                company_id=company_id,
                tool_name=tool_call.name,
                arguments=tool_call.arguments,
            )

            input_items.append({
                "type": "function_call_output",
                "call_id": tool_call.call_id,
                "output": json.dumps(
                    result,
                    ensure_ascii=False,
                    default=str,
                ),
            })

    raise RuntimeError(
        "Maximum number of tool execution rounds exceeded."
    )
