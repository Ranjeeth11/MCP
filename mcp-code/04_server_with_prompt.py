"""Step 4: add a prompt (a reusable instruction template)."""

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


@mcp.prompt()
def product_description(product_id: str, tone: str = "friendly") -> str:
    """Write a short marketing description for a product."""
    return (
        f"Write a 3-sentence {tone} marketing description for product {product_id}. "
        f"Use the get_product tool to fetch its name, price and stock first. "
        f"If it is out of stock, say it is coming back soon."
    )


if __name__ == "__main__":
    mcp.run()
