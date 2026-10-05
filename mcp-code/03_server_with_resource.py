"""Step 3: add resources (read-only information/context)."""

import json

from pydantic import BaseModel

from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

PRODUCTS = {
    "P100": {"name": "Wireless Mouse", "price": 25.0, "stock": 40},
    "P200": {"name": "Mechanical Keyboard", "price": 80.0, "stock": 12},
    "P300": {"name": "USB-C Hub", "price": 35.0, "stock": 0},
}


class Product(BaseModel):
    id: str
    name: str
    price: float
    stock: int


mcp = MCPServer("Product Catalog")


@mcp.tool()
def get_product(product_id: str) -> Product:
    """Look up a product by its ID (for example P100)."""
    product = PRODUCTS.get(product_id.upper())
    if product is None:
        raise ToolError(f"Unknown product ID: {product_id}")
    return Product(id=product_id.upper(), **product)


@mcp.resource("catalog://products", mime_type="application/json")
def all_products() -> str:
    """The full product catalog as JSON."""
    return json.dumps(PRODUCTS, indent=2)


@mcp.resource("catalog://products/{product_id}", mime_type="application/json")
def one_product(product_id: str) -> str:
    """A single product, addressed by URI (a resource template)."""
    return json.dumps(PRODUCTS.get(product_id.upper(), {}), indent=2)


if __name__ == "__main__":
    mcp.run()
