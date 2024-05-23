from typing import Dict, List, Optional, Union

from pydantic import BaseModel, Field

hash_request_openapi = { "example": {"algorithm": "sha1", "message": "Example message to be hashed"}}
post_hash_openapi = { "description": "Hash the given message with given algorithm"}

algorithm_openapi = { "description": "Name of the hash algorithm"}
message_openapi = { "description": "Original message"}
hash_openapi = { "description": "Hash representation of the message"}

class HashRequest(BaseModel):
    algorithm: str = Field(None, **algorithm_openapi)
    message: str = Field(None, **message_openapi)

class HashResponse(HashRequest):
    hash: str = Field(None, **hash_openapi)
