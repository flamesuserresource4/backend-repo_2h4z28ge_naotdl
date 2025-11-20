"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

# Example schemas (replace with your own):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Add your own schemas here:
# --------------------------------------------------

class Farmhouse(BaseModel):
    """
    Farmhouses available for browsing and booking
    Collection name: "farmhouse"
    """
    name: str = Field(..., description="Farmhouse name")
    location: str = Field(..., description="City or area")
    description: str = Field(..., description="Short description")
    price_per_night: float = Field(..., ge=0, description="Nightly rate")
    guests: int = Field(..., ge=1, description="Max guests")
    bedrooms: int = Field(..., ge=0)
    bathrooms: int = Field(..., ge=0)
    image_url: Optional[str] = Field(None, description="Cover image URL")
    rating: Optional[float] = Field(4.8, ge=0, le=5)

class Booking(BaseModel):
    """
    Bookings for farmhouses
    Collection name: "booking"
    """
    farmhouse_id: str = Field(..., description="ID of the farmhouse")
    name: str = Field(..., description="Guest full name")
    email: str = Field(..., description="Guest email")
    check_in: date = Field(..., description="Check-in date")
    check_out: date = Field(..., description="Check-out date")
    guests: int = Field(..., ge=1)
    notes: Optional[str] = Field(None, description="Special requests")

# Note: The Flames database viewer will automatically:
# 1. Read these schemas from GET /schema endpoint
# 2. Use them for document validation when creating/editing
# 3. Handle all database operations (CRUD) directly
# 4. You don't need to create any database endpoints!
