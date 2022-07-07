"""Pagination utilities."""

import typing

from fastapi import Query
from fastapi_pagination import create_page as _create_page
from fastapi_pagination import paginate as _paginate
from fastapi_pagination import set_page as _set_page
from fastapi_pagination.bases import AbstractPage, AbstractParams, RawParams
from fastapi_pagination.ext.sqlalchemy import paginate as _paginate_sqlalchemy
from httpx import Client
from httpx._types import PrimitiveData
from pydantic import BaseModel
from sqlalchemy.orm import Query as SQLAlchemyQuery

T = typing.TypeVar("T")  # noqa: WPS111

DEFAULT_LIMIT: typing = 20
MAX_LIMIT: typing = 100


class PageMeta(BaseModel):
    status: str = "ok"
    count: int
    total_count: int
    page_offset: int


class PageParams(BaseModel, AbstractParams):
    page_limit: int = Query(DEFAULT_LIMIT, ge=1, le=MAX_LIMIT, description="Page size limit")
    page_offset: int = Query(0, ge=0, description="Page offset")

    def to_raw_params(self) -> RawParams:
        return RawParams(
            limit=self.page_limit,
            offset=self.page_offset,
        )


class Page(AbstractPage[T], typing.Generic[T]):
    """
    A fastapi_pagination model in style of TerminalOne APIs.
    """

    meta: PageMeta
    data: typing.Sequence[T]

    __params_type__ = PageParams  # Set params related to Page

    @classmethod
    def create(
        cls,
        items: typing.Sequence[T],
        total: int,
        params: AbstractParams,
    ) -> "Page[T]":
        if not isinstance(params, PageParams):
            raise ValueError("Page should be used with LimitOffsetParams")

        return cls(
            data=items,
            meta=PageMeta(
                count=len(items),
                total_count=total,
                page_offset=params.page_offset,
            ),
        )

    class Config(object):
        allow_population_by_field_name = True
        fields = {"items": {"alias": "data"}}


# HACK: fastapi_pagination.paginate doesn't detect page type for some reason
# so we add a couple of stubs calling _set_page() explictly instead:

def paginate(
    sequence: typing.Sequence[T],
    params: PageParams = None,
    length_function: typing.Callable[[typing.Sequence[T]], int] = len,
) -> Page:
    _set_page(Page)
    return _paginate(sequence=sequence, params=params, length_function=length_function)


def paginate_sqlalchemy(query: SQLAlchemyQuery, params: typing.Optional[AbstractParams] = None) -> Page:
    _set_page(Page)
    return _paginate_sqlalchemy(query=query, params=params)
