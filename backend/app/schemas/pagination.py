"""
Schemas para paginação de resultados.
"""
from typing import Generic, TypeVar, List
from pydantic import BaseModel, Field

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    """Response paginado genérico."""
    items: List[T] = Field(description="Lista de itens da página atual")
    total: int = Field(description="Total de itens disponíveis")
    page: int = Field(description="Página atual (1-indexed)")
    page_size: int = Field(description="Número de itens por página")
    total_pages: int = Field(description="Total de páginas disponíveis")

    class Config:
        from_attributes = True
