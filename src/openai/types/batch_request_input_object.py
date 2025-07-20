# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union
from typing_extensions import Literal

from .._models import BaseModel
from .embedding_create_params import EmbeddingCreateParams
from .completion_create_params import CompletionCreateParamsNonStreaming
from .chat.completion_create_params import CompletionCreateParamsNonStreaming

__all__ = ["BatchRequestInputObject"]


class BatchRequestInputObject(BaseModel):
    """
    The per-line object of the batch input file
    """

    custom_id: str
    """A developer-provided per-request id that will be used to match outputs to inputs. Must be unique for each request in a batch."""

    method: Literal["POST"]
    """The HTTP method to be used for the request. Currently only POST is supported."""

    url: Literal["/v1/chat/completions", "/v1/embeddings", "/v1/completions"]
    """The OpenAI API relative URL to be used for the request. Currently /v1/chat/completions, /v1/embeddings, and /v1/completions are supported."""

    body: Union[CompletionCreateParamsNonStreaming, EmbeddingCreateParams, CompletionCreateParamsNonStreaming]
    """The request body to be sent to the OpenAI API. The type of this field depends on the value of `url`"""
