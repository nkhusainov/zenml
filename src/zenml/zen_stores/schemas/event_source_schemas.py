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
"""SQL Model Implementations for Action Plans."""
import base64
import json
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional
from uuid import UUID

from pydantic import Field
from pydantic.json import pydantic_encoder
from sqlalchemy import TEXT, Column
from sqlmodel import Relationship

from zenml import EventSourceResponseMetadata
from zenml.models import (
    EventSourceRequest,
    EventSourceResponse,
    EventSourceResponseBody,
    EventSourceUpdate,
)
from zenml.zen_stores.schemas.base_schemas import NamedSchema
from zenml.zen_stores.schemas.schema_utils import build_foreign_key_field
from zenml.zen_stores.schemas.user_schemas import UserSchema
from zenml.zen_stores.schemas.workspace_schemas import WorkspaceSchema

if TYPE_CHECKING:
    from zenml.zen_stores.schemas import TriggerSchema


class EventSourceSchema(NamedSchema, table=True):
    """SQL Model for tag."""

    __tablename__ = "event_source"

    workspace_id: UUID = build_foreign_key_field(
        source=__tablename__,
        target=WorkspaceSchema.__tablename__,
        source_column="workspace_id",
        target_column="id",
        ondelete="CASCADE",
        nullable=False,
    )
    workspace: "WorkspaceSchema" = Relationship(back_populates="event_sources")

    user_id: Optional[UUID] = build_foreign_key_field(
        source=__tablename__,
        target=UserSchema.__tablename__,
        source_column="user_id",
        target_column="id",
        ondelete="SET NULL",
        nullable=True,
    )
    user: Optional["UserSchema"] = Relationship(back_populates="event_sources")

    triggers: List["TriggerSchema"] = Relationship(
        back_populates="event_source"
    )

    flavor: str = Field(nullable=False)
    plugin_type: str = Field(nullable=False)
    plugin_subtype: str = Field(nullable=False)
    description: str = Field(sa_column=Column(TEXT, nullable=True))

    configuration: bytes

    @classmethod
    def from_request(cls, request: EventSourceRequest) -> "EventSourceSchema":
        """Convert an `EventSourceRequest` to an `EventSourceSchema`.

        Args:
            request: The request model to convert.

        Returns:
            The converted schema.
        """
        return cls(
            workspace_id=request.workspace,
            user_id=request.user,
            flavor=request.flavor,
            plugin_type=request.plugin_type,
            plugin_subtype=request.plugin_subtype,
            name=request.name,
            description=request.description,
            configuration=base64.b64encode(
                json.dumps(
                    request.configuration,
                    sort_keys=False,
                    default=pydantic_encoder,
                ).encode("utf-8")
            ),
        )

    def to_model(self, hydrate: bool = False) -> EventSourceResponse:
        """Convert an `EventSourceSchema` to an `EventSourceResponse`.

        Args:
            hydrate: Flag deciding whether to hydrate the output model(s)
                by including metadata fields in the response.

        Returns:
            The created `EventSourceResponse`.
        """
        body = EventSourceResponseBody(
            created=self.created,
            updated=self.updated,
            user=self.user.to_model() if self.user else None,
            flavor=self.flavor,
            plugin_type=self.plugin_type,
            plugin_subtype=self.plugin_subtype,
        )
        metadata = None
        if hydrate:
            metadata = EventSourceResponseMetadata(
                workspace=self.workspace.to_model(),
                description=self.description,
                configuration=json.loads(
                    base64.b64decode(self.configuration).decode()
                ),
            )
        return EventSourceResponse(
            id=self.id,
            name=self.name,
            body=body,
            metadata=metadata,
        )

    def update(self, update: EventSourceUpdate) -> "EventSourceSchema":
        """Updates a `EventSourceSchema` from a `EventSourceUpdate`.

        Args:
            update: The `EventSourceUpdate` to update from.

        Returns:
            The updated `EventSourceSchema`.
        """
        for field, value in update.dict(exclude_unset=True).items():
            if field == "configuration":
                self.configuration = base64.b64encode(
                    json.dumps(update.configuration).encode("utf-8")
                )
            elif field in [
                "flavor",
                "plugin_type",
                "plugin_subtype",
                "rotate_secret",
            ]:
                pass
            else:
                setattr(self, field, value)
        self.updated = datetime.utcnow()
        return self
