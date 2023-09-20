# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from .catalog import (
    AttributesConfig,
    Catalog,
    CatalogAttribute,
    CompletionConfig,
    ProductLevelConfig,
)
from .catalog_service import (
    AddCatalogAttributeRequest,
    GetAttributesConfigRequest,
    GetCompletionConfigRequest,
    GetDefaultBranchRequest,
    GetDefaultBranchResponse,
    ListCatalogsRequest,
    ListCatalogsResponse,
    RemoveCatalogAttributeRequest,
    ReplaceCatalogAttributeRequest,
    SetDefaultBranchRequest,
    UpdateAttributesConfigRequest,
    UpdateCatalogRequest,
    UpdateCompletionConfigRequest,
)
from .common import (
    AttributeConfigLevel,
    Audience,
    ColorInfo,
    Condition,
    CustomAttribute,
    FulfillmentInfo,
    Image,
    Interval,
    LocalInventory,
    PriceInfo,
    Rating,
    RecommendationsFilteringOption,
    Rule,
    SearchSolutionUseCase,
    SolutionType,
    UserInfo,
)
from .completion_service import CompleteQueryRequest, CompleteQueryResponse
from .control import Control
from .control_service import (
    CreateControlRequest,
    DeleteControlRequest,
    GetControlRequest,
    ListControlsRequest,
    ListControlsResponse,
    UpdateControlRequest,
)
from .import_config import (
    BigQuerySource,
    CompletionDataInputConfig,
    GcsSource,
    ImportCompletionDataRequest,
    ImportCompletionDataResponse,
    ImportErrorsConfig,
    ImportMetadata,
    ImportProductsRequest,
    ImportProductsResponse,
    ImportUserEventsRequest,
    ImportUserEventsResponse,
    ProductInlineSource,
    ProductInputConfig,
    UserEventImportSummary,
    UserEventInlineSource,
    UserEventInputConfig,
)
from .model import Model
from .model_service import (
    CreateModelMetadata,
    CreateModelRequest,
    DeleteModelRequest,
    GetModelRequest,
    ListModelsRequest,
    ListModelsResponse,
    PauseModelRequest,
    ResumeModelRequest,
    TuneModelMetadata,
    TuneModelRequest,
    TuneModelResponse,
    UpdateModelRequest,
)
from .prediction_service import PredictRequest, PredictResponse
from .product import Product
from .product_service import (
    AddFulfillmentPlacesMetadata,
    AddFulfillmentPlacesRequest,
    AddFulfillmentPlacesResponse,
    AddLocalInventoriesMetadata,
    AddLocalInventoriesRequest,
    AddLocalInventoriesResponse,
    CreateProductRequest,
    DeleteProductRequest,
    GetProductRequest,
    ListProductsRequest,
    ListProductsResponse,
    RemoveFulfillmentPlacesMetadata,
    RemoveFulfillmentPlacesRequest,
    RemoveFulfillmentPlacesResponse,
    RemoveLocalInventoriesMetadata,
    RemoveLocalInventoriesRequest,
    RemoveLocalInventoriesResponse,
    SetInventoryMetadata,
    SetInventoryRequest,
    SetInventoryResponse,
    UpdateProductRequest,
)
from .promotion import Promotion
from .purge_config import PurgeMetadata, PurgeUserEventsRequest, PurgeUserEventsResponse
from .search_service import ExperimentInfo, SearchRequest, SearchResponse
from .serving_config import ServingConfig
from .serving_config_service import (
    AddControlRequest,
    CreateServingConfigRequest,
    DeleteServingConfigRequest,
    GetServingConfigRequest,
    ListServingConfigsRequest,
    ListServingConfigsResponse,
    RemoveControlRequest,
    UpdateServingConfigRequest,
)
from .user_event import CompletionDetail, ProductDetail, PurchaseTransaction, UserEvent
from .user_event_service import (
    CollectUserEventRequest,
    RejoinUserEventsMetadata,
    RejoinUserEventsRequest,
    RejoinUserEventsResponse,
    WriteUserEventRequest,
)

__all__ = (
    "AttributesConfig",
    "Catalog",
    "CatalogAttribute",
    "CompletionConfig",
    "ProductLevelConfig",
    "AddCatalogAttributeRequest",
    "GetAttributesConfigRequest",
    "GetCompletionConfigRequest",
    "GetDefaultBranchRequest",
    "GetDefaultBranchResponse",
    "ListCatalogsRequest",
    "ListCatalogsResponse",
    "RemoveCatalogAttributeRequest",
    "ReplaceCatalogAttributeRequest",
    "SetDefaultBranchRequest",
    "UpdateAttributesConfigRequest",
    "UpdateCatalogRequest",
    "UpdateCompletionConfigRequest",
    "Audience",
    "ColorInfo",
    "Condition",
    "CustomAttribute",
    "FulfillmentInfo",
    "Image",
    "Interval",
    "LocalInventory",
    "PriceInfo",
    "Rating",
    "Rule",
    "UserInfo",
    "AttributeConfigLevel",
    "RecommendationsFilteringOption",
    "SearchSolutionUseCase",
    "SolutionType",
    "CompleteQueryRequest",
    "CompleteQueryResponse",
    "Control",
    "CreateControlRequest",
    "DeleteControlRequest",
    "GetControlRequest",
    "ListControlsRequest",
    "ListControlsResponse",
    "UpdateControlRequest",
    "BigQuerySource",
    "CompletionDataInputConfig",
    "GcsSource",
    "ImportCompletionDataRequest",
    "ImportCompletionDataResponse",
    "ImportErrorsConfig",
    "ImportMetadata",
    "ImportProductsRequest",
    "ImportProductsResponse",
    "ImportUserEventsRequest",
    "ImportUserEventsResponse",
    "ProductInlineSource",
    "ProductInputConfig",
    "UserEventImportSummary",
    "UserEventInlineSource",
    "UserEventInputConfig",
    "Model",
    "CreateModelMetadata",
    "CreateModelRequest",
    "DeleteModelRequest",
    "GetModelRequest",
    "ListModelsRequest",
    "ListModelsResponse",
    "PauseModelRequest",
    "ResumeModelRequest",
    "TuneModelMetadata",
    "TuneModelRequest",
    "TuneModelResponse",
    "UpdateModelRequest",
    "PredictRequest",
    "PredictResponse",
    "Product",
    "AddFulfillmentPlacesMetadata",
    "AddFulfillmentPlacesRequest",
    "AddFulfillmentPlacesResponse",
    "AddLocalInventoriesMetadata",
    "AddLocalInventoriesRequest",
    "AddLocalInventoriesResponse",
    "CreateProductRequest",
    "DeleteProductRequest",
    "GetProductRequest",
    "ListProductsRequest",
    "ListProductsResponse",
    "RemoveFulfillmentPlacesMetadata",
    "RemoveFulfillmentPlacesRequest",
    "RemoveFulfillmentPlacesResponse",
    "RemoveLocalInventoriesMetadata",
    "RemoveLocalInventoriesRequest",
    "RemoveLocalInventoriesResponse",
    "SetInventoryMetadata",
    "SetInventoryRequest",
    "SetInventoryResponse",
    "UpdateProductRequest",
    "Promotion",
    "PurgeMetadata",
    "PurgeUserEventsRequest",
    "PurgeUserEventsResponse",
    "ExperimentInfo",
    "SearchRequest",
    "SearchResponse",
    "ServingConfig",
    "AddControlRequest",
    "CreateServingConfigRequest",
    "DeleteServingConfigRequest",
    "GetServingConfigRequest",
    "ListServingConfigsRequest",
    "ListServingConfigsResponse",
    "RemoveControlRequest",
    "UpdateServingConfigRequest",
    "CompletionDetail",
    "ProductDetail",
    "PurchaseTransaction",
    "UserEvent",
    "CollectUserEventRequest",
    "RejoinUserEventsMetadata",
    "RejoinUserEventsRequest",
    "RejoinUserEventsResponse",
    "WriteUserEventRequest",
)
