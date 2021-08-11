# -*- coding: utf-8 -*-
import logging
from typing import Dict, Any, Optional
from pydantic import BaseModel, validator
from .data_model_validators import LoggerFieldType
from .constants import LOGGER_FORMATTER


# -------------------------------------------------
#   For logger_mixin.py
#
class LoggerConfig(BaseModel):
    logger: Optional[LoggerFieldType]
    name: Optional[str]
    level: Optional[int]
    formatter: Optional[str] = LOGGER_FORMATTER
    propagate: bool = False
    unique_logger: bool = False
    enable_log_file: bool = False
    enable_debug: bool = False
    unique_name: Optional[str]
    log_file_path: Optional[str]
    log_file_name: Optional[str]

    @validator('level')
    def is_logging_level(cls, v):
        if v and v not in logging._levelToName.keys():
            raise ValueError('level must be logging level')
        return v


# -------------------------------------------------
#   For api_client.py
#
class TargetAPI(BaseModel):
    url: str
    method: str
    header: Optional[Dict]
    parameters: Optional[Dict]
    save_response: bool = False


class ApiClientConfig(BaseModel):
    name: str
    description: str
    config: Dict[str, TargetAPI]


class ProxyModel(BaseModel):
    http_proxy: str
    https_proxy: str
    no_proxy: str


class RequestResponse(BaseModel):
    success: bool = False
    data: Any = None
    code: int = 0
    message: Optional[str]
