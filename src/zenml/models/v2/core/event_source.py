#  Copyright (c) ZenML GmbH 2024. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at:
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
#  or implied. See the License for the specific language governing
#  permissions and limitations under the License.
"""Collection of all models concerning event configurations."""
from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import Field

from zenml.constants import STR_FIELD_MAX_LENGTH
from zenml.enums import PluginSubType, PluginType
from zenml.models.v2.base.scoped import (
    WorkspaceScopedFilter,
    WorkspaceScopedRequest,
    WorkspaceScopedResponse,
    WorkspaceScopedResponseBody,
    WorkspaceScopedResponseMetadata,
)
from zenml.models.v2.base.update import update_model

# ------------------ Request Model ------------------


class EventSourceRequest(WorkspaceScopedRequest):
    """BaseModel for all event sources."""

    name: str = Field(
        title="The name of the event source.",
        max_length=STR_FIELD_MAX_LENGTH,
    )
    flavor: str = Field(
        title="The flavor of event source.",
        max_length=STR_FIELD_MAX_LENGTH,
    )
    plugin_type: PluginType = Field(
        title="The plugin type of the event source.",
        max_length=STR_FIELD_MAX_LENGTH,
    )
    plugin_subtype: PluginSubType = Field(
        title="The plugin subtype of the event source.",
        max_length=STR_FIELD_MAX_LENGTH,
    )
    description: str = Field(
        default="",
        title="The description of the event source.",
        max_length=STR_FIELD_MAX_LENGTH,
    )

    configuration: Dict[str, Any] = Field(
        title="The event source configuration.",
    )


# ------------------ Update Model ------------------


@update_model
class EventSourceUpdate(EventSourceRequest):
    """Update model for event sources."""

    name: str = Field(
        title="The name of the stack component.",
        max_length=STR_FIELD_MAX_LENGTH,
    )
    description: str = Field(
        default="",
        title="The description of the event source.",
        max_length=STR_FIELD_MAX_LENGTH,
    )
    configuration: Dict[str, Any] = Field(
        title="The event source configuration.",
    )
    rotate_secret: Optional[bool] = Field(
        title="In case the secret needs to be rotated."
    )


# ------------------ Response Model ------------------


class EventSourceResponseBody(WorkspaceScopedResponseBody):
    """ResponseBody for event sources."""

    flavor: str = Field(
        title="The flavor of event source.",
        max_length=STR_FIELD_MAX_LENGTH,
    )
    plugin_type: PluginType = Field(
        title="The plugin type of the event source.",
        max_length=STR_FIELD_MAX_LENGTH,
    )
    plugin_subtype: PluginSubType = Field(
        title="The plugin subtype of the event source.",
        max_length=STR_FIELD_MAX_LENGTH,
    )
    created: datetime = Field(
        title="The timestamp when this event filter was created."
    )
    updated: datetime = Field(
        title="The timestamp when this event filter was last updated.",
    )


class EventSourceResponseMetadata(WorkspaceScopedResponseMetadata):
    """Response metadata for event sources."""

    description: str = Field(
        default="",
        title="The description of the event source.",
        max_length=STR_FIELD_MAX_LENGTH,
    )
    configuration: Dict[str, Any] = Field(
        title="The event source configuration.",
    )


class EventSourceResponse(
    WorkspaceScopedResponse[
        EventSourceResponseBody, EventSourceResponseMetadata
    ]
):
    """Response model for event sources."""

    name: str = Field(
        title="The name of the event source.",
        max_length=STR_FIELD_MAX_LENGTH,
    )

    def get_hydrated_version(self) -> "EventSourceResponse":
        """Get the hydrated version of this event source.

        Returns:
            An instance of the same entity with the metadata field attached.
        """
        from zenml.client import Client

        return Client().zen_store.get_event_source(self.id)

    # Body and metadata properties
    @property
    def flavor(self) -> str:
        """The `flavor` property.

        Returns:
            the value of the property.
        """
        return self.get_body().flavor

    @property
    def plugin_type(self) -> PluginType:
        """The `plugin_type` property.

        Returns:
            the value of the property.
        """
        return self.get_body().plugin_type

    @property
    def plugin_subtype(self) -> PluginSubType:
        """The `plugin_subtype` property.

        Returns:
            the value of the property.
        """
        return self.get_body().plugin_subtype

    @property
    def created(self) -> datetime:
        """The`created` property.

        Returns:
            the value of the property.
        """
        return self.get_body().created

    @property
    def updated(self) -> datetime:
        """The `updated` property.

        Returns:
            the value of the property.
        """
        return self.get_body().updated

    @property
    def description(self) -> str:
        """The `description` property.

        Returns:
            the value of the property.
        """
        return self.get_metadata().description

    @property
    def configuration(self) -> Dict[str, Any]:
        """The `configuration` property.

        Returns:
            the value of the property.
        """
        return self.get_metadata().configuration


# ------------------ Filter Model ------------------


class EventSourceFilter(WorkspaceScopedFilter):
    """Model to enable advanced filtering of all EventSourceModels."""

    name: Optional[str] = Field(
        default=None,
        description="Name of the event source",
    )
    flavor: Optional[str] = Field(
        default=None,
        description="Flavor of the event source",
    )
    plugin_type: Optional[str] = Field(
        title="The plugin type of the event source.",
        max_length=STR_FIELD_MAX_LENGTH,
    )
    plugin_subtype: Optional[str] = Field(
        title="The plugin sub type of the event source.",
        max_length=STR_FIELD_MAX_LENGTH,
    )
