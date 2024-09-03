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
"""Github event flavors."""

try:
    from zenml.integrations.github.plugins.github_webhook_event_source_flavor import (
        GithubWebhookEventSourceFlavor,
    )

    __all__ = ["GithubWebhookEventSourceFlavor"]
except (ImportError, ModuleNotFoundError) as e:
    from zenml.exceptions import IntegrationError
    from zenml.integrations.constants import GITHUB

    raise IntegrationError(
        f"The `{GITHUB}` integration that you are trying to use is not "
        "properly installed. Please make sure that you have the correct "
        f"installation with: `zenml integration install {GITHUB}`"
    )
