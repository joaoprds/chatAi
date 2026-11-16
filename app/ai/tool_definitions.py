tools = [
    {
        "type": "function",
        "name": "get_product_stock",
        "description": (
            "Consult the inventory quantity and price of a product "
            "using its SKU. Use this when the user asks about "
            "product availability or stock."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "sku": {
                    "type": "string",
                    "description": "The product SKU."
                }
            },
            "required": ["sku"],
            "additionalProperties": False
        },
        "strict": True
    },
    {
        "type": "function",
        "name": "get_customer_orders",
        "description": (
            "Retrieve recent orders belonging to a customer. "
            "Use this when the user asks about customer orders."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "integer",
                    "description": "The customer ID."
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of orders to return."
                }
            },
            "required": ["customer_id", "limit"],
            "additionalProperties": False
        },
        "strict": True
    }
]