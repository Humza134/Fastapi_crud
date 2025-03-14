from sqlmodel import SQLModel, Field, Relationship

# class Product(SQLModel, table=True):
#     id: int | None = Field(default=None, primary_key=True)
#     name: str
#     description: str
#     price: float
#     expiry: str | None = None
#     brand: str | None = None
#     weight: float | None = None
#     category: str # It shall be pre defined by Platform
#     sku: str | None = None
    # rating: list["ProductRating"] = Relationship(back_populates="product")
    # image: str # Multiple | URL Not Media | One to Manu Relationship
    # quantity: int | None = None # Shall it be managed by Inventory Microservice
    # color: str | None = None # One to Manu Relationship
    # rating: float | None = None # One to Manu Relationship

# Category Table

class CategoryBase(SQLModel):
    name: str = Field(index=True, unique=True)
    
class Category(CategoryBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    products: list["Product"] = Relationship(back_populates="category")

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(Category):
    pass

class CategoryUpdate(SQLModel):
    name: str | None = None

# Product Table

class ProductBase(SQLModel):
    name: str = Field(index=True)
    description: str
    price: float
    expiry: str | None = None
    brand: str | None = None
    weight: float | None = None
    category_id: int | None = Field(default=None, foreign_key="category.id")

class Product(ProductBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    category: Category = Relationship(back_populates="products")
    reviews: list["Review"] = Relationship(back_populates="product")

class ProductCreate(ProductBase):
    pass

class ProductResponse(Product):
    pass

class ProductUpdate(SQLModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    expiry: str | None = None
    brand: str | None = None
    weight: float | None = None


# Review Table

class ReviewBase(SQLModel):
    content: str
    rating: int
    product_id: int | None = Field(default=None, foreign_key="product.id")

class Review(ReviewBase):
    id: int | None = Field(default=None, primary_key=True)
    product: Product = Relationship(back_populates="reviews")

class ReviewCreate(ReviewBase):
    pass

class ReviewResponse(Review):
    pass

class ReviewUpdate(SQLModel):
    content: str | None
    rating: int | None

# class ProductRating(SQLModel, table=True):
#     id: int | None = Field(default=None, primary_key=True)
#     product_id: int = Field(foreign_key="product.id")
#     rating: int
#     review: str | None = None
#     product = Relationship(back_populates="rating")
    
    # user_id: int # One to Manu Relationship
    

# class ProductUpdate(SQLModel):
#     name: str | None = None
#     description: str | None = None
#     price: float | None = None
#     expiry: str | None = None
#     brand: str | None = None
#     weight: float | None = None
#     category: str | None = None
#     sku: str | None = None