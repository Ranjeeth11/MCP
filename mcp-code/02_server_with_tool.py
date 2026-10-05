"""Step 2: the Product Catalog server with ONE tool (an action)."""

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


if __name__ == "__main__":
    mcp.run()
