# --------------------------------------------------------------------------
#
# Copyright (c) Microsoft Corporation. All rights reserved.
#
# The MIT License (MIT)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the ""Software""), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED *AS IS*, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#
# --------------------------------------------------------------------------
import itertools
from typing import (
    Callable,
    Optional,
    TypeVar,
    Iterator,
    Iterable,
    Tuple,
    Any,
)
import logging

from .exceptions import AzureError


_LOGGER = logging.getLogger(__name__)

ReturnType = TypeVar("ReturnType")
ResponseType = TypeVar("ResponseType")


class PageIterator(Iterator[Iterator[ReturnType]]):
    def __init__(
        self,
        get_next: Callable[[Optional[str]], ResponseType],
        extract_data: Callable[[ResponseType], Tuple[str, Iterable[ReturnType]]],
        continuation_token: Optional[str] = None,
    ):
        """Return an iterator of pages.

        :param get_next: Callable that take the continuation token and return a HTTP response
        :param extract_data: Callable that take an HTTP response and return a tuple continuation token,
         list of ReturnType
        :param str continuation_token: The continuation token needed by get_next
        """
        self._get_next = get_next
        self._extract_data = extract_data
        self.continuation_token = continuation_token
        self._did_a_call_already = False
        self._response: Optional[ResponseType] = None
        self._current_page: Optional[Iterable[ReturnType]] = None

    def __iter__(self) -> Iterator[Iterator[ReturnType]]:
        return self

    def __next__(self) -> Iterator[ReturnType]:
        """Get the next page in the iterator.

        :returns: An iterator of objects in the next page.
        :rtype: iterator[ReturnType]
        :raises StopIteration: If there are no more pages to return.
        :raises AzureError: If the request fails.
        """
        if self.continuation_token is None and self._did_a_call_already:
            raise StopIteration("End of paging")
        try:
            self._response = self._get_next(self.continuation_token)
        except AzureError as error:
            if not error.continuation_token:
                error.continuation_token = self.continuation_token
            raise

        self._did_a_call_already = True

        self.continuation_token, self._current_page = self._extract_data(self._response)

        return iter(self._current_page)

    next = __next__  # Python 2 compatibility. Can't be removed as some people are using ".next()" even in Py3


class ItemPaged(Iterator[ReturnType]):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Return an iterator of items.

        args and kwargs will be passed to the PageIterator constructor directly,
        except page_iterator_class
        """
        self._args = args
        self._kwargs = kwargs
        self._page_iterator: Optional[Iterator[ReturnType]] = None
        self._page_iterator_class = self._kwargs.pop("page_iterator_class", PageIterator)

    def by_page(self, continuation_token: Optional[str] = None) -> Iterator[Iterator[ReturnType]]:
        """Get an iterator of pages of objects, instead of an iterator of objects.

        :param str continuation_token:
            An opaque continuation token. This value can be retrieved from the
            continuation_token field of a previous generator object. If specified,
            this generator will begin returning results from this point.
        :returns: An iterator of pages (themselves iterator of objects)
        :rtype: iterator[iterator[ReturnType]]
        """
        return self._page_iterator_class(continuation_token=continuation_token, *self._args, **self._kwargs)

    def __repr__(self) -> str:
        return "<iterator object azure.core.paging.ItemPaged at {}>".format(hex(id(self)))

    def __iter__(self) -> Iterator[ReturnType]:
        return self

    def __next__(self) -> ReturnType:
        """Get the next item in the iterator.

        :returns: The next item in the iterator.
        :rtype: ReturnType
        :raises StopIteration: If there are no more items to return.
        """
        if self._page_iterator is None:
            self._page_iterator = itertools.chain.from_iterable(self.by_page())
        return next(self._page_iterator)

    next = __next__  # Python 2 compatibility. Can't be removed as some people are using ".next()" even in Py3
