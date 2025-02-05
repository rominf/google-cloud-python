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
from collections import OrderedDict
import os
import re
from typing import (
    Dict,
    Mapping,
    MutableMapping,
    MutableSequence,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
    cast,
)
import warnings

from google.api_core import client_options as client_options_lib
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.exceptions import MutualTLSChannelError  # type: ignore
from google.auth.transport import mtls  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.cloud.dlp_v2 import gapic_version as package_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore

from google.cloud.location import locations_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore

from google.cloud.dlp_v2.services.dlp_service import pagers
from google.cloud.dlp_v2.types import dlp

from .transports.base import DEFAULT_CLIENT_INFO, DlpServiceTransport
from .transports.grpc import DlpServiceGrpcTransport
from .transports.grpc_asyncio import DlpServiceGrpcAsyncIOTransport
from .transports.rest import DlpServiceRestTransport


class DlpServiceClientMeta(type):
    """Metaclass for the DlpService client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = OrderedDict()  # type: Dict[str, Type[DlpServiceTransport]]
    _transport_registry["grpc"] = DlpServiceGrpcTransport
    _transport_registry["grpc_asyncio"] = DlpServiceGrpcAsyncIOTransport
    _transport_registry["rest"] = DlpServiceRestTransport

    def get_transport_class(
        cls,
        label: Optional[str] = None,
    ) -> Type[DlpServiceTransport]:
        """Returns an appropriate transport class.

        Args:
            label: The name of the desired transport. If none is
                provided, then the first transport in the registry is used.

        Returns:
            The transport class to use.
        """
        # If a specific transport is requested, return that one.
        if label:
            return cls._transport_registry[label]

        # No transport is requested; return the default (that is, the first one
        # in the dictionary).
        return next(iter(cls._transport_registry.values()))


class DlpServiceClient(metaclass=DlpServiceClientMeta):
    """The Cloud Data Loss Prevention (DLP) API is a service that
    allows clients to detect the presence of Personally Identifiable
    Information (PII) and other privacy-sensitive data in
    user-supplied, unstructured data streams, like text blocks or
    images.
    The service also includes methods for sensitive data redaction
    and scheduling of data scans on Google Cloud Platform based data
    sets.

    To learn more about concepts and find how-to guides see
    https://cloud.google.com/dlp/docs/.
    """

    @staticmethod
    def _get_default_mtls_endpoint(api_endpoint):
        """Converts api endpoint to mTLS endpoint.

        Convert "*.sandbox.googleapis.com" and "*.googleapis.com" to
        "*.mtls.sandbox.googleapis.com" and "*.mtls.googleapis.com" respectively.
        Args:
            api_endpoint (Optional[str]): the api endpoint to convert.
        Returns:
            str: converted mTLS api endpoint.
        """
        if not api_endpoint:
            return api_endpoint

        mtls_endpoint_re = re.compile(
            r"(?P<name>[^.]+)(?P<mtls>\.mtls)?(?P<sandbox>\.sandbox)?(?P<googledomain>\.googleapis\.com)?"
        )

        m = mtls_endpoint_re.match(api_endpoint)
        name, mtls, sandbox, googledomain = m.groups()
        if mtls or not googledomain:
            return api_endpoint

        if sandbox:
            return api_endpoint.replace(
                "sandbox.googleapis.com", "mtls.sandbox.googleapis.com"
            )

        return api_endpoint.replace(".googleapis.com", ".mtls.googleapis.com")

    # Note: DEFAULT_ENDPOINT is deprecated. Use _DEFAULT_ENDPOINT_TEMPLATE instead.
    DEFAULT_ENDPOINT = "dlp.googleapis.com"
    DEFAULT_MTLS_ENDPOINT = _get_default_mtls_endpoint.__func__(  # type: ignore
        DEFAULT_ENDPOINT
    )

    _DEFAULT_ENDPOINT_TEMPLATE = "dlp.{UNIVERSE_DOMAIN}"
    _DEFAULT_UNIVERSE = "googleapis.com"

    @classmethod
    def from_service_account_info(cls, info: dict, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            info.

        Args:
            info (dict): The service account private key info.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            DlpServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_info(info)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    @classmethod
    def from_service_account_file(cls, filename: str, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            file.

        Args:
            filename (str): The path to the service account private key json
                file.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            DlpServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> DlpServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            DlpServiceTransport: The transport used by the client
                instance.
        """
        return self._transport

    @staticmethod
    def deidentify_template_path(
        organization: str,
        deidentify_template: str,
    ) -> str:
        """Returns a fully-qualified deidentify_template string."""
        return "organizations/{organization}/deidentifyTemplates/{deidentify_template}".format(
            organization=organization,
            deidentify_template=deidentify_template,
        )

    @staticmethod
    def parse_deidentify_template_path(path: str) -> Dict[str, str]:
        """Parses a deidentify_template path into its component segments."""
        m = re.match(
            r"^organizations/(?P<organization>.+?)/deidentifyTemplates/(?P<deidentify_template>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def discovery_config_path(
        project: str,
        location: str,
        discovery_config: str,
    ) -> str:
        """Returns a fully-qualified discovery_config string."""
        return "projects/{project}/locations/{location}/discoveryConfigs/{discovery_config}".format(
            project=project,
            location=location,
            discovery_config=discovery_config,
        )

    @staticmethod
    def parse_discovery_config_path(path: str) -> Dict[str, str]:
        """Parses a discovery_config path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/discoveryConfigs/(?P<discovery_config>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def dlp_content_path(
        project: str,
    ) -> str:
        """Returns a fully-qualified dlp_content string."""
        return "projects/{project}/dlpContent".format(
            project=project,
        )

    @staticmethod
    def parse_dlp_content_path(path: str) -> Dict[str, str]:
        """Parses a dlp_content path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/dlpContent$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def dlp_job_path(
        project: str,
        dlp_job: str,
    ) -> str:
        """Returns a fully-qualified dlp_job string."""
        return "projects/{project}/dlpJobs/{dlp_job}".format(
            project=project,
            dlp_job=dlp_job,
        )

    @staticmethod
    def parse_dlp_job_path(path: str) -> Dict[str, str]:
        """Parses a dlp_job path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/dlpJobs/(?P<dlp_job>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def finding_path(
        project: str,
        location: str,
        finding: str,
    ) -> str:
        """Returns a fully-qualified finding string."""
        return "projects/{project}/locations/{location}/findings/{finding}".format(
            project=project,
            location=location,
            finding=finding,
        )

    @staticmethod
    def parse_finding_path(path: str) -> Dict[str, str]:
        """Parses a finding path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/findings/(?P<finding>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def inspect_template_path(
        organization: str,
        inspect_template: str,
    ) -> str:
        """Returns a fully-qualified inspect_template string."""
        return (
            "organizations/{organization}/inspectTemplates/{inspect_template}".format(
                organization=organization,
                inspect_template=inspect_template,
            )
        )

    @staticmethod
    def parse_inspect_template_path(path: str) -> Dict[str, str]:
        """Parses a inspect_template path into its component segments."""
        m = re.match(
            r"^organizations/(?P<organization>.+?)/inspectTemplates/(?P<inspect_template>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def job_trigger_path(
        project: str,
        job_trigger: str,
    ) -> str:
        """Returns a fully-qualified job_trigger string."""
        return "projects/{project}/jobTriggers/{job_trigger}".format(
            project=project,
            job_trigger=job_trigger,
        )

    @staticmethod
    def parse_job_trigger_path(path: str) -> Dict[str, str]:
        """Parses a job_trigger path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/jobTriggers/(?P<job_trigger>.+?)$", path
        )
        return m.groupdict() if m else {}

    @staticmethod
    def stored_info_type_path(
        organization: str,
        stored_info_type: str,
    ) -> str:
        """Returns a fully-qualified stored_info_type string."""
        return "organizations/{organization}/storedInfoTypes/{stored_info_type}".format(
            organization=organization,
            stored_info_type=stored_info_type,
        )

    @staticmethod
    def parse_stored_info_type_path(path: str) -> Dict[str, str]:
        """Parses a stored_info_type path into its component segments."""
        m = re.match(
            r"^organizations/(?P<organization>.+?)/storedInfoTypes/(?P<stored_info_type>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def common_billing_account_path(
        billing_account: str,
    ) -> str:
        """Returns a fully-qualified billing_account string."""
        return "billingAccounts/{billing_account}".format(
            billing_account=billing_account,
        )

    @staticmethod
    def parse_common_billing_account_path(path: str) -> Dict[str, str]:
        """Parse a billing_account path into its component segments."""
        m = re.match(r"^billingAccounts/(?P<billing_account>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_folder_path(
        folder: str,
    ) -> str:
        """Returns a fully-qualified folder string."""
        return "folders/{folder}".format(
            folder=folder,
        )

    @staticmethod
    def parse_common_folder_path(path: str) -> Dict[str, str]:
        """Parse a folder path into its component segments."""
        m = re.match(r"^folders/(?P<folder>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_organization_path(
        organization: str,
    ) -> str:
        """Returns a fully-qualified organization string."""
        return "organizations/{organization}".format(
            organization=organization,
        )

    @staticmethod
    def parse_common_organization_path(path: str) -> Dict[str, str]:
        """Parse a organization path into its component segments."""
        m = re.match(r"^organizations/(?P<organization>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_project_path(
        project: str,
    ) -> str:
        """Returns a fully-qualified project string."""
        return "projects/{project}".format(
            project=project,
        )

    @staticmethod
    def parse_common_project_path(path: str) -> Dict[str, str]:
        """Parse a project path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_location_path(
        project: str,
        location: str,
    ) -> str:
        """Returns a fully-qualified location string."""
        return "projects/{project}/locations/{location}".format(
            project=project,
            location=location,
        )

    @staticmethod
    def parse_common_location_path(path: str) -> Dict[str, str]:
        """Parse a location path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)$", path)
        return m.groupdict() if m else {}

    @classmethod
    def get_mtls_endpoint_and_cert_source(
        cls, client_options: Optional[client_options_lib.ClientOptions] = None
    ):
        """Deprecated. Return the API endpoint and client cert source for mutual TLS.

        The client cert source is determined in the following order:
        (1) if `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable is not "true", the
        client cert source is None.
        (2) if `client_options.client_cert_source` is provided, use the provided one; if the
        default client cert source exists, use the default one; otherwise the client cert
        source is None.

        The API endpoint is determined in the following order:
        (1) if `client_options.api_endpoint` if provided, use the provided one.
        (2) if `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable is "always", use the
        default mTLS endpoint; if the environment variable is "never", use the default API
        endpoint; otherwise if client cert source exists, use the default mTLS endpoint, otherwise
        use the default API endpoint.

        More details can be found at https://google.aip.dev/auth/4114.

        Args:
            client_options (google.api_core.client_options.ClientOptions): Custom options for the
                client. Only the `api_endpoint` and `client_cert_source` properties may be used
                in this method.

        Returns:
            Tuple[str, Callable[[], Tuple[bytes, bytes]]]: returns the API endpoint and the
                client cert source to use.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If any errors happen.
        """

        warnings.warn(
            "get_mtls_endpoint_and_cert_source is deprecated. Use the api_endpoint property instead.",
            DeprecationWarning,
        )
        if client_options is None:
            client_options = client_options_lib.ClientOptions()
        use_client_cert = os.getenv("GOOGLE_API_USE_CLIENT_CERTIFICATE", "false")
        use_mtls_endpoint = os.getenv("GOOGLE_API_USE_MTLS_ENDPOINT", "auto")
        if use_client_cert not in ("true", "false"):
            raise ValueError(
                "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
            )
        if use_mtls_endpoint not in ("auto", "never", "always"):
            raise MutualTLSChannelError(
                "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
            )

        # Figure out the client cert source to use.
        client_cert_source = None
        if use_client_cert == "true":
            if client_options.client_cert_source:
                client_cert_source = client_options.client_cert_source
            elif mtls.has_default_client_cert_source():
                client_cert_source = mtls.default_client_cert_source()

        # Figure out which api endpoint to use.
        if client_options.api_endpoint is not None:
            api_endpoint = client_options.api_endpoint
        elif use_mtls_endpoint == "always" or (
            use_mtls_endpoint == "auto" and client_cert_source
        ):
            api_endpoint = cls.DEFAULT_MTLS_ENDPOINT
        else:
            api_endpoint = cls.DEFAULT_ENDPOINT

        return api_endpoint, client_cert_source

    @staticmethod
    def _read_environment_variables():
        """Returns the environment variables used by the client.

        Returns:
            Tuple[bool, str, str]: returns the GOOGLE_API_USE_CLIENT_CERTIFICATE,
            GOOGLE_API_USE_MTLS_ENDPOINT, and GOOGLE_CLOUD_UNIVERSE_DOMAIN environment variables.

        Raises:
            ValueError: If GOOGLE_API_USE_CLIENT_CERTIFICATE is not
                any of ["true", "false"].
            google.auth.exceptions.MutualTLSChannelError: If GOOGLE_API_USE_MTLS_ENDPOINT
                is not any of ["auto", "never", "always"].
        """
        use_client_cert = os.getenv(
            "GOOGLE_API_USE_CLIENT_CERTIFICATE", "false"
        ).lower()
        use_mtls_endpoint = os.getenv("GOOGLE_API_USE_MTLS_ENDPOINT", "auto").lower()
        universe_domain_env = os.getenv("GOOGLE_CLOUD_UNIVERSE_DOMAIN")
        if use_client_cert not in ("true", "false"):
            raise ValueError(
                "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
            )
        if use_mtls_endpoint not in ("auto", "never", "always"):
            raise MutualTLSChannelError(
                "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
            )
        return use_client_cert == "true", use_mtls_endpoint, universe_domain_env

    @staticmethod
    def _get_client_cert_source(provided_cert_source, use_cert_flag):
        """Return the client cert source to be used by the client.

        Args:
            provided_cert_source (bytes): The client certificate source provided.
            use_cert_flag (bool): A flag indicating whether to use the client certificate.

        Returns:
            bytes or None: The client cert source to be used by the client.
        """
        client_cert_source = None
        if use_cert_flag:
            if provided_cert_source:
                client_cert_source = provided_cert_source
            elif mtls.has_default_client_cert_source():
                client_cert_source = mtls.default_client_cert_source()
        return client_cert_source

    @staticmethod
    def _get_api_endpoint(
        api_override, client_cert_source, universe_domain, use_mtls_endpoint
    ):
        """Return the API endpoint used by the client.

        Args:
            api_override (str): The API endpoint override. If specified, this is always
                the return value of this function and the other arguments are not used.
            client_cert_source (bytes): The client certificate source used by the client.
            universe_domain (str): The universe domain used by the client.
            use_mtls_endpoint (str): How to use the mTLS endpoint, which depends also on the other parameters.
                Possible values are "always", "auto", or "never".

        Returns:
            str: The API endpoint to be used by the client.
        """
        if api_override is not None:
            api_endpoint = api_override
        elif use_mtls_endpoint == "always" or (
            use_mtls_endpoint == "auto" and client_cert_source
        ):
            _default_universe = DlpServiceClient._DEFAULT_UNIVERSE
            if universe_domain != _default_universe:
                raise MutualTLSChannelError(
                    f"mTLS is not supported in any universe other than {_default_universe}."
                )
            api_endpoint = DlpServiceClient.DEFAULT_MTLS_ENDPOINT
        else:
            api_endpoint = DlpServiceClient._DEFAULT_ENDPOINT_TEMPLATE.format(
                UNIVERSE_DOMAIN=universe_domain
            )
        return api_endpoint

    @staticmethod
    def _get_universe_domain(
        client_universe_domain: Optional[str], universe_domain_env: Optional[str]
    ) -> str:
        """Return the universe domain used by the client.

        Args:
            client_universe_domain (Optional[str]): The universe domain configured via the client options.
            universe_domain_env (Optional[str]): The universe domain configured via the "GOOGLE_CLOUD_UNIVERSE_DOMAIN" environment variable.

        Returns:
            str: The universe domain to be used by the client.

        Raises:
            ValueError: If the universe domain is an empty string.
        """
        universe_domain = DlpServiceClient._DEFAULT_UNIVERSE
        if client_universe_domain is not None:
            universe_domain = client_universe_domain
        elif universe_domain_env is not None:
            universe_domain = universe_domain_env
        if len(universe_domain.strip()) == 0:
            raise ValueError("Universe Domain cannot be an empty string.")
        return universe_domain

    @staticmethod
    def _compare_universes(
        client_universe: str, credentials: ga_credentials.Credentials
    ) -> bool:
        """Returns True iff the universe domains used by the client and credentials match.

        Args:
            client_universe (str): The universe domain configured via the client options.
            credentials (ga_credentials.Credentials): The credentials being used in the client.

        Returns:
            bool: True iff client_universe matches the universe in credentials.

        Raises:
            ValueError: when client_universe does not match the universe in credentials.
        """

        default_universe = DlpServiceClient._DEFAULT_UNIVERSE
        credentials_universe = getattr(credentials, "universe_domain", default_universe)

        if client_universe != credentials_universe:
            raise ValueError(
                "The configured universe domain "
                f"({client_universe}) does not match the universe domain "
                f"found in the credentials ({credentials_universe}). "
                "If you haven't configured the universe domain explicitly, "
                f"`{default_universe}` is the default."
            )
        return True

    def _validate_universe_domain(self):
        """Validates client's and credentials' universe domains are consistent.

        Returns:
            bool: True iff the configured universe domain is valid.

        Raises:
            ValueError: If the configured universe domain is not valid.
        """
        self._is_universe_domain_valid = (
            self._is_universe_domain_valid
            or DlpServiceClient._compare_universes(
                self.universe_domain, self.transport._credentials
            )
        )
        return self._is_universe_domain_valid

    @property
    def api_endpoint(self):
        """Return the API endpoint used by the client instance.

        Returns:
            str: The API endpoint used by the client instance.
        """
        return self._api_endpoint

    @property
    def universe_domain(self) -> str:
        """Return the universe domain used by the client instance.

        Returns:
            str: The universe domain used by the client instance.
        """
        return self._universe_domain

    def __init__(
        self,
        *,
        credentials: Optional[ga_credentials.Credentials] = None,
        transport: Optional[Union[str, DlpServiceTransport]] = None,
        client_options: Optional[Union[client_options_lib.ClientOptions, dict]] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the dlp service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, DlpServiceTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (Optional[Union[google.api_core.client_options.ClientOptions, dict]]):
                Custom options for the client.

                1. The ``api_endpoint`` property can be used to override the
                default endpoint provided by the client when ``transport`` is
                not explicitly provided. Only if this property is not set and
                ``transport`` was not explicitly provided, the endpoint is
                determined by the GOOGLE_API_USE_MTLS_ENDPOINT environment
                variable, which have one of the following values:
                "always" (always use the default mTLS endpoint), "never" (always
                use the default regular endpoint) and "auto" (auto-switch to the
                default mTLS endpoint if client certificate is present; this is
                the default value).

                2. If the GOOGLE_API_USE_CLIENT_CERTIFICATE environment variable
                is "true", then the ``client_cert_source`` property can be used
                to provide a client certificate for mTLS transport. If
                not provided, the default SSL client certificate will be used if
                present. If GOOGLE_API_USE_CLIENT_CERTIFICATE is "false" or not
                set, no client certificate will be used.

                3. The ``universe_domain`` property can be used to override the
                default "googleapis.com" universe. Note that the ``api_endpoint``
                property still takes precedence; and ``universe_domain`` is
                currently not supported for mTLS.

            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        self._client_options = client_options
        if isinstance(self._client_options, dict):
            self._client_options = client_options_lib.from_dict(self._client_options)
        if self._client_options is None:
            self._client_options = client_options_lib.ClientOptions()
        self._client_options = cast(
            client_options_lib.ClientOptions, self._client_options
        )

        universe_domain_opt = getattr(self._client_options, "universe_domain", None)

        (
            self._use_client_cert,
            self._use_mtls_endpoint,
            self._universe_domain_env,
        ) = DlpServiceClient._read_environment_variables()
        self._client_cert_source = DlpServiceClient._get_client_cert_source(
            self._client_options.client_cert_source, self._use_client_cert
        )
        self._universe_domain = DlpServiceClient._get_universe_domain(
            universe_domain_opt, self._universe_domain_env
        )
        self._api_endpoint = None  # updated below, depending on `transport`

        # Initialize the universe domain validation.
        self._is_universe_domain_valid = False

        api_key_value = getattr(self._client_options, "api_key", None)
        if api_key_value and credentials:
            raise ValueError(
                "client_options.api_key and credentials are mutually exclusive"
            )

        # Save or instantiate the transport.
        # Ordinarily, we provide the transport, but allowing a custom transport
        # instance provides an extensibility point for unusual situations.
        transport_provided = isinstance(transport, DlpServiceTransport)
        if transport_provided:
            # transport is a DlpServiceTransport instance.
            if credentials or self._client_options.credentials_file or api_key_value:
                raise ValueError(
                    "When providing a transport instance, "
                    "provide its credentials directly."
                )
            if self._client_options.scopes:
                raise ValueError(
                    "When providing a transport instance, provide its scopes "
                    "directly."
                )
            self._transport = cast(DlpServiceTransport, transport)
            self._api_endpoint = self._transport.host

        self._api_endpoint = self._api_endpoint or DlpServiceClient._get_api_endpoint(
            self._client_options.api_endpoint,
            self._client_cert_source,
            self._universe_domain,
            self._use_mtls_endpoint,
        )

        if not transport_provided:
            import google.auth._default  # type: ignore

            if api_key_value and hasattr(
                google.auth._default, "get_api_key_credentials"
            ):
                credentials = google.auth._default.get_api_key_credentials(
                    api_key_value
                )

            Transport = type(self).get_transport_class(cast(str, transport))
            self._transport = Transport(
                credentials=credentials,
                credentials_file=self._client_options.credentials_file,
                host=self._api_endpoint,
                scopes=self._client_options.scopes,
                client_cert_source_for_mtls=self._client_cert_source,
                quota_project_id=self._client_options.quota_project_id,
                client_info=client_info,
                always_use_jwt_access=True,
                api_audience=self._client_options.api_audience,
            )

    def inspect_content(
        self,
        request: Optional[Union[dlp.InspectContentRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dlp.InspectContentResponse:
        r"""Finds potentially sensitive info in content.
        This method has limits on input size, processing time,
        and output size.

        When no InfoTypes or CustomInfoTypes are specified in
        this request, the system will automatically choose what
        detectors to run. By default this may be all types, but
        may change over time as detectors are updated.

        For how to guides, see
        https://cloud.google.com/dlp/docs/inspecting-images and
        https://cloud.google.com/dlp/docs/inspecting-text,

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dlp_v2

            def sample_inspect_content():
                # Create a client
                client = dlp_v2.DlpServiceClient()

                # Initialize request argument(s)
                request = dlp_v2.InspectContentRequest(
                )

                # Make the request
                response = client.inspect_content(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dlp_v2.types.InspectContentRequest, dict]):
                The request object. Request to search for potentially
                sensitive info in a ContentItem.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dlp_v2.types.InspectContentResponse:
                Results of inspecting an item.
        """
        # Create or coerce a protobuf request object.
        # Minor optimization to avoid making a copy if the user passes
        # in a dlp.InspectContentRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, dlp.InspectContentRequest):
            request = dlp.InspectContentRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.inspect_content]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def redact_image(
        self,
        request: Optional[Union[dlp.RedactImageRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dlp.RedactImageResponse:
        r"""Redacts potentially sensitive info from an image.
        This method has limits on input size, processing time,
        and output size. See
        https://cloud.google.com/dlp/docs/redacting-sensitive-data-images
        to learn more.

        When no InfoTypes or CustomInfoTypes are specified in
        this request, the system will automatically choose what
        detectors to run. By default this may be all types, but
        may change over time as detectors are updated.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dlp_v2

            def sample_redact_image():
                # Create a client
                client = dlp_v2.DlpServiceClient()

                # Initialize request argument(s)
                request = dlp_v2.RedactImageRequest(
                )

                # Make the request
                response = client.redact_image(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dlp_v2.types.RedactImageRequest, dict]):
                The request object. Request to search for potentially
                sensitive info in an image and redact it
                by covering it with a colored rectangle.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dlp_v2.types.RedactImageResponse:
                Results of redacting an image.
        """
        # Create or coerce a protobuf request object.
        # Minor optimization to avoid making a copy if the user passes
        # in a dlp.RedactImageRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, dlp.RedactImageRequest):
            request = dlp.RedactImageRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.redact_image]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def deidentify_content(
        self,
        request: Optional[Union[dlp.DeidentifyContentRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dlp.DeidentifyContentResponse:
        r"""De-identifies potentially sensitive info from a
        ContentItem. This method has limits on input size and
        output size. See
        https://cloud.google.com/dlp/docs/deidentify-sensitive-data
        to learn more.

        When no InfoTypes or CustomInfoTypes are specified in
        this request, the system will automatically choose what
        detectors to run. By default this may be all types, but
        may change over time as detectors are updated.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dlp_v2

            def sample_deidentify_content():
                # Create a client
                client = dlp_v2.DlpServiceClient()

                # Initialize request argument(s)
                request = dlp_v2.DeidentifyContentRequest(
                )

                # Make the request
                response = client.deidentify_content(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dlp_v2.types.DeidentifyContentRequest, dict]):
                The request object. Request to de-identify a ContentItem.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dlp_v2.types.DeidentifyContentResponse:
                Results of de-identifying a
                ContentItem.

        """
        # Create or coerce a protobuf request object.
        # Minor optimization to avoid making a copy if the user passes
        # in a dlp.DeidentifyContentRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, dlp.DeidentifyContentRequest):
            request = dlp.DeidentifyContentRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.deidentify_content]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def reidentify_content(
        self,
        request: Optional[Union[dlp.ReidentifyContentRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dlp.ReidentifyContentResponse:
        r"""Re-identifies content that has been de-identified. See
        https://cloud.google.com/dlp/docs/pseudonymization#re-identification_in_free_text_code_example
        to learn more.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dlp_v2

            def sample_reidentify_content():
                # Create a client
                client = dlp_v2.DlpServiceClient()

                # Initialize request argument(s)
                request = dlp_v2.ReidentifyContentRequest(
                    parent="parent_value",
                )

                # Make the request
                response = client.reidentify_content(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dlp_v2.types.ReidentifyContentRequest, dict]):
                The request object. Request to re-identify an item.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dlp_v2.types.ReidentifyContentResponse:
                Results of re-identifying an item.
        """
        # Create or coerce a protobuf request object.
        # Minor optimization to avoid making a copy if the user passes
        # in a dlp.ReidentifyContentRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, dlp.ReidentifyContentRequest):
            request = dlp.ReidentifyContentRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.reidentify_content]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_info_types(
        self,
        request: Optional[Union[dlp.ListInfoTypesRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dlp.ListInfoTypesResponse:
        r"""Returns a list of the sensitive information types
        that DLP API supports. See
        https://cloud.google.com/dlp/docs/infotypes-reference to
        learn more.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dlp_v2

            def sample_list_info_types():
                # Create a client
                client = dlp_v2.DlpServiceClient()

                # Initialize request argument(s)
                request = dlp_v2.ListInfoTypesRequest(
                )

                # Make the request
                response = client.list_info_types(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dlp_v2.types.ListInfoTypesRequest, dict]):
                The request object. Request for the list of infoTypes.
            parent (str):
                The parent resource name.

                The format of this value is as follows:

                ::

                    locations/<var>LOCATION_ID</var>

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dlp_v2.types.ListInfoTypesResponse:
                Response to the ListInfoTypes
                request.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a dlp.ListInfoTypesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, dlp.ListInfoTypesRequest):
            request = dlp.ListInfoTypesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_info_types]

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def create_inspect_template(
        self,
        request: Optional[Union[dlp.CreateInspectTemplateRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        inspect_template: Optional[dlp.InspectTemplate] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dlp.InspectTemplate:
        r"""Creates an InspectTemplate for reusing frequently
        used configuration for inspecting content, images, and
        storage. See
        https://cloud.google.com/dlp/docs/creating-templates to
        learn more.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dlp_v2

            def sample_create_inspect_template():
                # Create a client
                client = dlp_v2.DlpServiceClient()

                # Initialize request argument(s)
                request = dlp_v2.CreateInspectTemplateRequest(
                    parent="parent_value",
                )

                # Make the request
                response = client.create_inspect_template(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dlp_v2.types.CreateInspectTemplateRequest, dict]):
                The request object. Request message for
                CreateInspectTemplate.
            parent (str):
                Required. Parent resource name.

                The format of this value varies depending on the scope
                of the request (project or organization) and whether you
                have `specified a processing
                location <https://cloud.google.com/dlp/docs/specifying-location>`__:

                -  Projects scope, location specified:
                   ``projects/``\ PROJECT_ID\ ``/locations/``\ LOCATION_ID
                -  Projects scope, no location specified (defaults to
                   global): ``projects/``\ PROJECT_ID
                -  Organizations scope, location specified:
                   ``organizations/``\ ORG_ID\ ``/locations/``\ LOCATION_ID
                -  Organizations scope, no location specified (defaults
                   to global): ``organizations/``\ ORG_ID

                The following example ``parent`` string specifies a
                parent project with the identifier ``example-project``,
                and specifies the ``europe-west3`` location for
                processing data:

                ::

                    parent=projects/example-project/locations/europe-west3

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            inspect_template (google.cloud.dlp_v2.types.InspectTemplate):
                Required. The InspectTemplate to
                create.

                This corresponds to the ``inspect_template`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dlp_v2.types.InspectTemplate:
                The inspectTemplate contains a
                configuration (set of types of sensitive
                data to be detected) to be used anywhere
                you otherwise would normally specify
                InspectConfig. See
                https://cloud.google.com/dlp/docs/concepts-templates
                to learn more.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, inspect_template])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a dlp.CreateInspectTemplateRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, dlp.CreateInspectTemplateRequest):
            request = dlp.CreateInspectTemplateRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if inspect_template is not None:
                request.inspect_template = inspect_template

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_inspect_template]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_inspect_template(
        self,
        request: Optional[Union[dlp.UpdateInspectTemplateRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        inspect_template: Optional[dlp.InspectTemplate] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dlp.InspectTemplate:
        r"""Updates the InspectTemplate.
        See https://cloud.google.com/dlp/docs/creating-templates
        to learn more.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dlp_v2

            def sample_update_inspect_template():
                # Create a client
                client = dlp_v2.DlpServiceClient()

                # Initialize request argument(s)
                request = dlp_v2.UpdateInspectTemplateRequest(
                    name="name_value",
                )

                # Make the request
                response = client.update_inspect_template(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dlp_v2.types.UpdateInspectTemplateRequest, dict]):
                The request object. Request message for
                UpdateInspectTemplate.
            name (str):
                Required. Resource name of organization and
                inspectTemplate to be updated, for example
                ``organizations/433245324/inspectTemplates/432452342``
                or projects/project-id/inspectTemplates/432452342.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            inspect_template (google.cloud.dlp_v2.types.InspectTemplate):
                New InspectTemplate value.
                This corresponds to the ``inspect_template`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Mask to control which fields get
                updated.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dlp_v2.types.InspectTemplate:
                The inspectTemplate contains a
                configuration (set of types of sensitive
                data to be detected) to be used anywhere
                you otherwise would normally specify
                InspectConfig. See
                https://cloud.google.com/dlp/docs/concepts-templates
                to learn more.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, inspect_template, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a dlp.UpdateInspectTemplateRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, dlp.UpdateInspectTemplateRequest):
            request = dlp.UpdateInspectTemplateRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name
            if inspect_template is not None:
                request.inspect_template = inspect_template
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_inspect_template]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_inspect_template(
        self,
        request: Optional[Union[dlp.GetInspectTemplateRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dlp.InspectTemplate:
        r"""Gets an InspectTemplate.
        See https://cloud.google.com/dlp/docs/creating-templates
        to learn more.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dlp_v2

            def sample_get_inspect_template():
                # Create a client
                client = dlp_v2.DlpServiceClient()

                # Initialize request argument(s)
                request = dlp_v2.GetInspectTemplateRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_inspect_template(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dlp_v2.types.GetInspectTemplateRequest, dict]):
                The request object. Request message for
                GetInspectTemplate.
            name (str):
                Required. Resource name of the organization and
                inspectTemplate to be read, for example
                ``organizations/433245324/inspectTemplates/432452342``
                or projects/project-id/inspectTemplates/432452342.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dlp_v2.types.InspectTemplate:
                The inspectTemplate contains a
                configuration (set of types of sensitive
                data to be detected) to be used anywhere
                you otherwise would normally specify
                InspectConfig. See
                https://cloud.google.com/dlp/docs/concepts-templates
                to learn more.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a dlp.GetInspectTemplateRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, dlp.GetInspectTemplateRequest):
            request = dlp.GetInspectTemplateRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_inspect_template]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_inspect_templates(
        self,
        request: Optional[Union[dlp.ListInspectTemplatesRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListInspectTemplatesPager:
        r"""Lists InspectTemplates.
        See https://cloud.google.com/dlp/docs/creating-templates
        to learn more.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dlp_v2

            def sample_list_inspect_templates():
                # Create a client
                client = dlp_v2.DlpServiceClient()

                # Initialize request argument(s)
                request = dlp_v2.ListInspectTemplatesRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_inspect_templates(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.dlp_v2.types.ListInspectTemplatesRequest, dict]):
                The request object. Request message for
                ListInspectTemplates.
            parent (str):
                Required. Parent resource name.

                The format of this value varies depending on the scope
                of the request (project or organization) and whether you
                have `specified a processing
                location <https://cloud.google.com/dlp/docs/specifying-location>`__:

                -  Projects scope, location specified:
                   ``projects/``\ PROJECT_ID\ ``/locations/``\ LOCATION_ID
                -  Projects scope, no location specified (defaults to
                   global): ``projects/``\ PROJECT_ID
                -  Organizations scope, location specified:
                   ``organizations/``\ ORG_ID\ ``/locations/``\ LOCATION_ID
                -  Organizations scope, no location specified (defaults
                   to global): ``organizations/``\ ORG_ID

                The following example ``parent`` string specifies a
                parent project with the identifier ``example-project``,
                and specifies the ``europe-west3`` location for
                processing data:

                ::

                    parent=projects/example-project/locations/europe-west3

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dlp_v2.services.dlp_service.pagers.ListInspectTemplatesPager:
                Response message for
                ListInspectTemplates.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a dlp.ListInspectTemplatesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, dlp.ListInspectTemplatesRequest):
            request = dlp.ListInspectTemplatesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_inspect_templates]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListInspectTemplatesPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_inspect_template(
        self,
        request: Optional[Union[dlp.DeleteInspectTemplateRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes an InspectTemplate.
        See https://cloud.google.com/dlp/docs/creating-templates
        to learn more.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dlp_v2

            def sample_delete_inspect_template():
                # Create a client
                client = dlp_v2.DlpServiceClient()

                # Initialize request argument(s)
                request = dlp_v2.DeleteInspectTemplateRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_inspect_template(request=request)

        Args:
            request (Union[google.cloud.dlp_v2.types.DeleteInspectTemplateRequest, dict]):
                The request object. Request message for
                DeleteInspectTemplate.
            name (str):
                Required. Resource name of the organization and
                inspectTemplate to be deleted, for example
                ``organizations/433245324/inspectTemplates/432452342``
                or projects/project-id/inspectTemplates/432452342.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a dlp.DeleteInspectTemplateRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, dlp.DeleteInspectTemplateRequest):
            request = dlp.DeleteInspectTemplateRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_inspect_template]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def create_deidentify_template(
        self,
        request: Optional[Union[dlp.CreateDeidentifyTemplateRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        deidentify_template: Optional[dlp.DeidentifyTemplate] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dlp.DeidentifyTemplate:
        r"""Creates a DeidentifyTemplate for reusing frequently
        used configuration for de-identifying content, images,
        and storage. See
        https://cloud.google.com/dlp/docs/creating-templates-deid
        to learn more.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dlp_v2

            def sample_create_deidentify_template():
                # Create a client
                client = dlp_v2.DlpServiceClient()

                # Initialize request argument(s)
                request = dlp_v2.CreateDeidentifyTemplateRequest(
                    parent="parent_value",
                )

                # Make the request
                response = client.create_deidentify_template(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dlp_v2.types.CreateDeidentifyTemplateRequest, dict]):
                The request object. Request message for
                CreateDeidentifyTemplate.
            parent (str):
                Required. Parent resource name.

                The format of this value varies depending on the scope
                of the request (project or organization) and whether you
                have `specified a processing
                location <https://cloud.google.com/dlp/docs/specifying-location>`__:

                -  Projects scope, location specified:
                   ``projects/``\ PROJECT_ID\ ``/locations/``\ LOCATION_ID
                -  Projects scope, no location specified (defaults to
                   global): ``projects/``\ PROJECT_ID
                -  Organizations scope, location specified:
                   ``organizations/``\ ORG_ID\ ``/locations/``\ LOCATION_ID
                -  Organizations scope, no location specified (defaults
                   to global): ``organizations/``\ ORG_ID

                The following example ``parent`` string specifies a
                parent project with the identifier ``example-project``,
                and specifies the ``europe-west3`` location for
                processing data:

                ::

                    parent=projects/example-project/locations/europe-west3

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            deidentify_template (google.cloud.dlp_v2.types.DeidentifyTemplate):
                Required. The DeidentifyTemplate to
                create.

                This corresponds to the ``deidentify_template`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dlp_v2.types.DeidentifyTemplate:
                DeidentifyTemplates contains
                instructions on how to de-identify
                content. See
                https://cloud.google.com/dlp/docs/concepts-templates
                to learn more.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, deidentify_template])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a dlp.CreateDeidentifyTemplateRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, dlp.CreateDeidentifyTemplateRequest):
            request = dlp.CreateDeidentifyTemplateRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if deidentify_template is not None:
                request.deidentify_template = deidentify_template

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.create_deidentify_template
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_deidentify_template(
        self,
        request: Optional[Union[dlp.UpdateDeidentifyTemplateRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        deidentify_template: Optional[dlp.DeidentifyTemplate] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dlp.DeidentifyTemplate:
        r"""Updates the DeidentifyTemplate.
        See
        https://cloud.google.com/dlp/docs/creating-templates-deid
        to learn more.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dlp_v2

            def sample_update_deidentify_template():
                # Create a client
                client = dlp_v2.DlpServiceClient()

                # Initialize request argument(s)
                request = dlp_v2.UpdateDeidentifyTemplateRequest(
                    name="name_value",
                )

                # Make the request
                response = client.update_deidentify_template(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dlp_v2.types.UpdateDeidentifyTemplateRequest, dict]):
                The request object. Request message for
                UpdateDeidentifyTemplate.
            name (str):
                Required. Resource name of organization and deidentify
                template to be updated, for example
                ``organizations/433245324/deidentifyTemplates/432452342``
                or projects/project-id/deidentifyTemplates/432452342.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            deidentify_template (google.cloud.dlp_v2.types.DeidentifyTemplate):
                New DeidentifyTemplate value.
                This corresponds to the ``deidentify_template`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Mask to control which fields get
                updated.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dlp_v2.types.DeidentifyTemplate:
                DeidentifyTemplates contains
                instructions on how to de-identify
                content. See
                https://cloud.google.com/dlp/docs/concepts-templates
                to learn more.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, deidentify_template, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a dlp.UpdateDeidentifyTemplateRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, dlp.UpdateDeidentifyTemplateRequest):
            request = dlp.UpdateDeidentifyTemplateRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name
            if deidentify_template is not None:
                request.deidentify_template = deidentify_template
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.update_deidentify_template
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_deidentify_template(
        self,
        request: Optional[Union[dlp.GetDeidentifyTemplateRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dlp.DeidentifyTemplate:
        r"""Gets a DeidentifyTemplate.
        See
        https://cloud.google.com/dlp/docs/creating-templates-deid
        to learn more.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dlp_v2

            def sample_get_deidentify_template():
                # Create a client
                client = dlp_v2.DlpServiceClient()

                # Initialize request argument(s)
                request = dlp_v2.GetDeidentifyTemplateRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_deidentify_template(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dlp_v2.types.GetDeidentifyTemplateRequest, dict]):
                The request object. Request message for
                GetDeidentifyTemplate.
            name (str):
                Required. Resource name of the organization and
                deidentify template to be read, for example
                ``organizations/433245324/deidentifyTemplates/432452342``
                or projects/project-id/deidentifyTemplates/432452342.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dlp_v2.types.DeidentifyTemplate:
                DeidentifyTemplates contains
                instructions on how to de-identify
                content. See
                https://cloud.google.com/dlp/docs/concepts-templates
                to learn more.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a dlp.GetDeidentifyTemplateRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, dlp.GetDeidentifyTemplateRequest):
            request = dlp.GetDeidentifyTemplateRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_deidentify_template]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_deidentify_templates(
        self,
        request: Optional[Union[dlp.ListDeidentifyTemplatesRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListDeidentifyTemplatesPager:
        r"""Lists DeidentifyTemplates.
        See
        https://cloud.google.com/dlp/docs/creating-templates-deid
        to learn more.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dlp_v2

            def sample_list_deidentify_templates():
                # Create a client
                client = dlp_v2.DlpServiceClient()

                # Initialize request argument(s)
                request = dlp_v2.ListDeidentifyTemplatesRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_deidentify_templates(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.dlp_v2.types.ListDeidentifyTemplatesRequest, dict]):
                The request object. Request message for
                ListDeidentifyTemplates.
            parent (str):
                Required. Parent resource name.

                The format of this value varies depending on the scope
                of the request (project or organization) and whether you
                have `specified a processing
                location <https://cloud.google.com/dlp/docs/specifying-location>`__:

                -  Projects scope, location specified:
                   ``projects/``\ PROJECT_ID\ ``/locations/``\ LOCATION_ID
                -  Projects scope, no location specified (defaults to
                   global): ``projects/``\ PROJECT_ID
                -  Organizations scope, location specified:
                   ``organizations/``\ ORG_ID\ ``/locations/``\ LOCATION_ID
                -  Organizations scope, no location specified (defaults
                   to global): ``organizations/``\ ORG_ID

                The following example ``parent`` string specifies a
                parent project with the identifier ``example-project``,
                and specifies the ``europe-west3`` location for
                processing data:

                ::

                    parent=projects/example-project/locations/europe-west3

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dlp_v2.services.dlp_service.pagers.ListDeidentifyTemplatesPager:
                Response message for
                ListDeidentifyTemplates.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a dlp.ListDeidentifyTemplatesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, dlp.ListDeidentifyTemplatesRequest):
            request = dlp.ListDeidentifyTemplatesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.list_deidentify_templates
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListDeidentifyTemplatesPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_deidentify_template(
        self,
        request: Optional[Union[dlp.DeleteDeidentifyTemplateRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a DeidentifyTemplate.
        See
        https://cloud.google.com/dlp/docs/creating-templates-deid
        to learn more.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dlp_v2

            def sample_delete_deidentify_template():
                # Create a client
                client = dlp_v2.DlpServiceClient()

                # Initialize request argument(s)
                request = dlp_v2.DeleteDeidentifyTemplateRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_deidentify_template(request=request)

        Args:
            request (Union[google.cloud.dlp_v2.types.DeleteDeidentifyTemplateRequest, dict]):
                The request object. Request message for
                DeleteDeidentifyTemplate.
            name (str):
                Required. Resource name of the organization and
                deidentify template to be deleted, for example
                ``organizations/433245324/deidentifyTemplates/432452342``
                or projects/project-id/deidentifyTemplates/432452342.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a dlp.DeleteDeidentifyTemplateRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, dlp.DeleteDeidentifyTemplateRequest):
            request = dlp.DeleteDeidentifyTemplateRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.delete_deidentify_template
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def create_job_trigger(
        self,
        request: Optional[Union[dlp.CreateJobTriggerRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        job_trigger: Optional[dlp.JobTrigger] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dlp.JobTrigger:
        r"""Creates a job trigger to run DLP actions such as
        scanning storage for sensitive information on a set
        schedule. See
        https://cloud.google.com/dlp/docs/creating-job-triggers
        to learn more.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dlp_v2

            def sample_create_job_trigger():
                # Create a client
                client = dlp_v2.DlpServiceClient()

                # Initialize request argument(s)
                job_trigger = dlp_v2.JobTrigger()
                job_trigger.status = "CANCELLED"

                request = dlp_v2.CreateJobTriggerRequest(
                    parent="parent_value",
                    job_trigger=job_trigger,
                )

                # Make the request
                response = client.create_job_trigger(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dlp_v2.types.CreateJobTriggerRequest, dict]):
                The request object. Request message for CreateJobTrigger.
            parent (str):
                Required. Parent resource name.

                The format of this value varies depending on whether you
                have `specified a processing
                location <https://cloud.google.com/dlp/docs/specifying-location>`__:

                -  Projects scope, location specified:
                   ``projects/``\ PROJECT_ID\ ``/locations/``\ LOCATION_ID
                -  Projects scope, no location specified (defaults to
                   global): ``projects/``\ PROJECT_ID

                The following example ``parent`` string specifies a
                parent project with the identifier ``example-project``,
                and specifies the ``europe-west3`` location for
                processing data:

                ::

                    parent=projects/example-project/locations/europe-west3

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            job_trigger (google.cloud.dlp_v2.types.JobTrigger):
                Required. The JobTrigger to create.
                This corresponds to the ``job_trigger`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dlp_v2.types.JobTrigger:
                Contains a configuration to make dlp
                api calls on a repeating basis. See
                https://cloud.google.com/dlp/docs/concepts-job-triggers
                to learn more.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, job_trigger])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a dlp.CreateJobTriggerRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, dlp.CreateJobTriggerRequest):
            request = dlp.CreateJobTriggerRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if job_trigger is not None:
                request.job_trigger = job_trigger

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_job_trigger]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_job_trigger(
        self,
        request: Optional[Union[dlp.UpdateJobTriggerRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        job_trigger: Optional[dlp.JobTrigger] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dlp.JobTrigger:
        r"""Updates a job trigger.
        See
        https://cloud.google.com/dlp/docs/creating-job-triggers
        to learn more.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dlp_v2

            def sample_update_job_trigger():
                # Create a client
                client = dlp_v2.DlpServiceClient()

                # Initialize request argument(s)
                request = dlp_v2.UpdateJobTriggerRequest(
                    name="name_value",
                )

                # Make the request
                response = client.update_job_trigger(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dlp_v2.types.UpdateJobTriggerRequest, dict]):
                The request object. Request message for UpdateJobTrigger.
            name (str):
                Required. Resource name of the project and the
                triggeredJob, for example
                ``projects/dlp-test-project/jobTriggers/53234423``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            job_trigger (google.cloud.dlp_v2.types.JobTrigger):
                New JobTrigger value.
                This corresponds to the ``job_trigger`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Mask to control which fields get
                updated.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dlp_v2.types.JobTrigger:
                Contains a configuration to make dlp
                api calls on a repeating basis. See
                https://cloud.google.com/dlp/docs/concepts-job-triggers
                to learn more.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, job_trigger, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a dlp.UpdateJobTriggerRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, dlp.UpdateJobTriggerRequest):
            request = dlp.UpdateJobTriggerRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name
            if job_trigger is not None:
                request.job_trigger = job_trigger
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_job_trigger]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def hybrid_inspect_job_trigger(
        self,
        request: Optional[Union[dlp.HybridInspectJobTriggerRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dlp.HybridInspectResponse:
        r"""Inspect hybrid content and store findings to a
        trigger. The inspection will be processed
        asynchronously. To review the findings monitor the jobs
        within the trigger.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dlp_v2

            def sample_hybrid_inspect_job_trigger():
                # Create a client
                client = dlp_v2.DlpServiceClient()

                # Initialize request argument(s)
                request = dlp_v2.HybridInspectJobTriggerRequest(
                    name="name_value",
                )

                # Make the request
                response = client.hybrid_inspect_job_trigger(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dlp_v2.types.HybridInspectJobTriggerRequest, dict]):
                The request object. Request to search for potentially
                sensitive info in a custom location.
            name (str):
                Required. Resource name of the trigger to execute a
                hybrid inspect on, for example
                ``projects/dlp-test-project/jobTriggers/53234423``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dlp_v2.types.HybridInspectResponse:
                Quota exceeded errors will be thrown
                once quota has been met.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a dlp.HybridInspectJobTriggerRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, dlp.HybridInspectJobTriggerRequest):
            request = dlp.HybridInspectJobTriggerRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.hybrid_inspect_job_trigger
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_job_trigger(
        self,
        request: Optional[Union[dlp.GetJobTriggerRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dlp.JobTrigger:
        r"""Gets a job trigger.
        See
        https://cloud.google.com/dlp/docs/creating-job-triggers
        to learn more.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dlp_v2

            def sample_get_job_trigger():
                # Create a client
                client = dlp_v2.DlpServiceClient()

                # Initialize request argument(s)
                request = dlp_v2.GetJobTriggerRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_job_trigger(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dlp_v2.types.GetJobTriggerRequest, dict]):
                The request object. Request message for GetJobTrigger.
            name (str):
                Required. Resource name of the project and the
                triggeredJob, for example
                ``projects/dlp-test-project/jobTriggers/53234423``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dlp_v2.types.JobTrigger:
                Contains a configuration to make dlp
                api calls on a repeating basis. See
                https://cloud.google.com/dlp/docs/concepts-job-triggers
                to learn more.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a dlp.GetJobTriggerRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, dlp.GetJobTriggerRequest):
            request = dlp.GetJobTriggerRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_job_trigger]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_job_triggers(
        self,
        request: Optional[Union[dlp.ListJobTriggersRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListJobTriggersPager:
        r"""Lists job triggers.
        See
        https://cloud.google.com/dlp/docs/creating-job-triggers
        to learn more.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dlp_v2

            def sample_list_job_triggers():
                # Create a client
                client = dlp_v2.DlpServiceClient()

                # Initialize request argument(s)
                request = dlp_v2.ListJobTriggersRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_job_triggers(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.dlp_v2.types.ListJobTriggersRequest, dict]):
                The request object. Request message for ListJobTriggers.
            parent (str):
                Required. Parent resource name.

                The format of this value varies depending on whether you
                have `specified a processing
                location <https://cloud.google.com/dlp/docs/specifying-location>`__:

                -  Projects scope, location specified:
                   ``projects/``\ PROJECT_ID\ ``/locations/``\ LOCATION_ID
                -  Projects scope, no location specified (defaults to
                   global): ``projects/``\ PROJECT_ID

                The following example ``parent`` string specifies a
                parent project with the identifier ``example-project``,
                and specifies the ``europe-west3`` location for
                processing data:

                ::

                    parent=projects/example-project/locations/europe-west3

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dlp_v2.services.dlp_service.pagers.ListJobTriggersPager:
                Response message for ListJobTriggers.

                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a dlp.ListJobTriggersRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, dlp.ListJobTriggersRequest):
            request = dlp.ListJobTriggersRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_job_triggers]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListJobTriggersPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_job_trigger(
        self,
        request: Optional[Union[dlp.DeleteJobTriggerRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a job trigger.
        See
        https://cloud.google.com/dlp/docs/creating-job-triggers
        to learn more.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dlp_v2

            def sample_delete_job_trigger():
                # Create a client
                client = dlp_v2.DlpServiceClient()

                # Initialize request argument(s)
                request = dlp_v2.DeleteJobTriggerRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_job_trigger(request=request)

        Args:
            request (Union[google.cloud.dlp_v2.types.DeleteJobTriggerRequest, dict]):
                The request object. Request message for DeleteJobTrigger.
            name (str):
                Required. Resource name of the project and the
                triggeredJob, for example
                ``projects/dlp-test-project/jobTriggers/53234423``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a dlp.DeleteJobTriggerRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, dlp.DeleteJobTriggerRequest):
            request = dlp.DeleteJobTriggerRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_job_trigger]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def activate_job_trigger(
        self,
        request: Optional[Union[dlp.ActivateJobTriggerRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dlp.DlpJob:
        r"""Activate a job trigger. Causes the immediate execute
        of a trigger instead of waiting on the trigger event to
        occur.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dlp_v2

            def sample_activate_job_trigger():
                # Create a client
                client = dlp_v2.DlpServiceClient()

                # Initialize request argument(s)
                request = dlp_v2.ActivateJobTriggerRequest(
                    name="name_value",
                )

                # Make the request
                response = client.activate_job_trigger(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dlp_v2.types.ActivateJobTriggerRequest, dict]):
                The request object. Request message for
                ActivateJobTrigger.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dlp_v2.types.DlpJob:
                Combines all of the information about
                a DLP job.

        """
        # Create or coerce a protobuf request object.
        # Minor optimization to avoid making a copy if the user passes
        # in a dlp.ActivateJobTriggerRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, dlp.ActivateJobTriggerRequest):
            request = dlp.ActivateJobTriggerRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.activate_job_trigger]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def create_discovery_config(
        self,
        request: Optional[Union[dlp.CreateDiscoveryConfigRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        discovery_config: Optional[dlp.DiscoveryConfig] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dlp.DiscoveryConfig:
        r"""Creates a config for discovery to scan and profile
        storage.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dlp_v2

            def sample_create_discovery_config():
                # Create a client
                client = dlp_v2.DlpServiceClient()

                # Initialize request argument(s)
                discovery_config = dlp_v2.DiscoveryConfig()
                discovery_config.status = "PAUSED"

                request = dlp_v2.CreateDiscoveryConfigRequest(
                    parent="parent_value",
                    discovery_config=discovery_config,
                )

                # Make the request
                response = client.create_discovery_config(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dlp_v2.types.CreateDiscoveryConfigRequest, dict]):
                The request object. Request message for
                CreateDiscoveryConfig.
            parent (str):
                Required. Parent resource name.

                The format of this value is as follows:
                ``projects/``\ PROJECT_ID\ ``/locations/``\ LOCATION_ID

                The following example ``parent`` string specifies a
                parent project with the identifier ``example-project``,
                and specifies the ``europe-west3`` location for
                processing data:

                ::

                    parent=projects/example-project/locations/europe-west3

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            discovery_config (google.cloud.dlp_v2.types.DiscoveryConfig):
                Required. The DiscoveryConfig to
                create.

                This corresponds to the ``discovery_config`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dlp_v2.types.DiscoveryConfig:
                Configuration for discovery to scan resources for profile generation.
                   Only one discovery configuration may exist per
                   organization, folder, or project.

                   The generated data profiles are retained according to
                   the [data retention policy]
                   (https://cloud.google.com/dlp/docs/data-profiles#retention).

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, discovery_config])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a dlp.CreateDiscoveryConfigRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, dlp.CreateDiscoveryConfigRequest):
            request = dlp.CreateDiscoveryConfigRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if discovery_config is not None:
                request.discovery_config = discovery_config

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_discovery_config]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_discovery_config(
        self,
        request: Optional[Union[dlp.UpdateDiscoveryConfigRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        discovery_config: Optional[dlp.DiscoveryConfig] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dlp.DiscoveryConfig:
        r"""Updates a discovery configuration.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dlp_v2

            def sample_update_discovery_config():
                # Create a client
                client = dlp_v2.DlpServiceClient()

                # Initialize request argument(s)
                discovery_config = dlp_v2.DiscoveryConfig()
                discovery_config.status = "PAUSED"

                request = dlp_v2.UpdateDiscoveryConfigRequest(
                    name="name_value",
                    discovery_config=discovery_config,
                )

                # Make the request
                response = client.update_discovery_config(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dlp_v2.types.UpdateDiscoveryConfigRequest, dict]):
                The request object. Request message for
                UpdateDiscoveryConfig.
            name (str):
                Required. Resource name of the project and the
                configuration, for example
                ``projects/dlp-test-project/discoveryConfigs/53234423``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            discovery_config (google.cloud.dlp_v2.types.DiscoveryConfig):
                Required. New DiscoveryConfig value.
                This corresponds to the ``discovery_config`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Mask to control which fields get
                updated.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dlp_v2.types.DiscoveryConfig:
                Configuration for discovery to scan resources for profile generation.
                   Only one discovery configuration may exist per
                   organization, folder, or project.

                   The generated data profiles are retained according to
                   the [data retention policy]
                   (https://cloud.google.com/dlp/docs/data-profiles#retention).

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, discovery_config, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a dlp.UpdateDiscoveryConfigRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, dlp.UpdateDiscoveryConfigRequest):
            request = dlp.UpdateDiscoveryConfigRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name
            if discovery_config is not None:
                request.discovery_config = discovery_config
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_discovery_config]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_discovery_config(
        self,
        request: Optional[Union[dlp.GetDiscoveryConfigRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dlp.DiscoveryConfig:
        r"""Gets a discovery configuration.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dlp_v2

            def sample_get_discovery_config():
                # Create a client
                client = dlp_v2.DlpServiceClient()

                # Initialize request argument(s)
                request = dlp_v2.GetDiscoveryConfigRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_discovery_config(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dlp_v2.types.GetDiscoveryConfigRequest, dict]):
                The request object. Request message for
                GetDiscoveryConfig.
            name (str):
                Required. Resource name of the project and the
                configuration, for example
                ``projects/dlp-test-project/discoveryConfigs/53234423``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dlp_v2.types.DiscoveryConfig:
                Configuration for discovery to scan resources for profile generation.
                   Only one discovery configuration may exist per
                   organization, folder, or project.

                   The generated data profiles are retained according to
                   the [data retention policy]
                   (https://cloud.google.com/dlp/docs/data-profiles#retention).

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a dlp.GetDiscoveryConfigRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, dlp.GetDiscoveryConfigRequest):
            request = dlp.GetDiscoveryConfigRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_discovery_config]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_discovery_configs(
        self,
        request: Optional[Union[dlp.ListDiscoveryConfigsRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListDiscoveryConfigsPager:
        r"""Lists discovery configurations.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dlp_v2

            def sample_list_discovery_configs():
                # Create a client
                client = dlp_v2.DlpServiceClient()

                # Initialize request argument(s)
                request = dlp_v2.ListDiscoveryConfigsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_discovery_configs(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.dlp_v2.types.ListDiscoveryConfigsRequest, dict]):
                The request object. Request message for
                ListDiscoveryConfigs.
            parent (str):
                Required. Parent resource name.

                The format of this value is as follows:
                ``projects/``\ PROJECT_ID\ ``/locations/``\ LOCATION_ID

                The following example ``parent`` string specifies a
                parent project with the identifier ``example-project``,
                and specifies the ``europe-west3`` location for
                processing data:

                ::

                    parent=projects/example-project/locations/europe-west3

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dlp_v2.services.dlp_service.pagers.ListDiscoveryConfigsPager:
                Response message for
                ListDiscoveryConfigs.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a dlp.ListDiscoveryConfigsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, dlp.ListDiscoveryConfigsRequest):
            request = dlp.ListDiscoveryConfigsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_discovery_configs]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListDiscoveryConfigsPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_discovery_config(
        self,
        request: Optional[Union[dlp.DeleteDiscoveryConfigRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a discovery configuration.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dlp_v2

            def sample_delete_discovery_config():
                # Create a client
                client = dlp_v2.DlpServiceClient()

                # Initialize request argument(s)
                request = dlp_v2.DeleteDiscoveryConfigRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_discovery_config(request=request)

        Args:
            request (Union[google.cloud.dlp_v2.types.DeleteDiscoveryConfigRequest, dict]):
                The request object. Request message for
                DeleteDiscoveryConfig.
            name (str):
                Required. Resource name of the project and the config,
                for example
                ``projects/dlp-test-project/discoveryConfigs/53234423``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a dlp.DeleteDiscoveryConfigRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, dlp.DeleteDiscoveryConfigRequest):
            request = dlp.DeleteDiscoveryConfigRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_discovery_config]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def create_dlp_job(
        self,
        request: Optional[Union[dlp.CreateDlpJobRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        inspect_job: Optional[dlp.InspectJobConfig] = None,
        risk_job: Optional[dlp.RiskAnalysisJobConfig] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dlp.DlpJob:
        r"""Creates a new job to inspect storage or calculate
        risk metrics. See
        https://cloud.google.com/dlp/docs/inspecting-storage and
        https://cloud.google.com/dlp/docs/compute-risk-analysis
        to learn more.

        When no InfoTypes or CustomInfoTypes are specified in
        inspect jobs, the system will automatically choose what
        detectors to run. By default this may be all types, but
        may change over time as detectors are updated.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dlp_v2

            def sample_create_dlp_job():
                # Create a client
                client = dlp_v2.DlpServiceClient()

                # Initialize request argument(s)
                request = dlp_v2.CreateDlpJobRequest(
                    parent="parent_value",
                )

                # Make the request
                response = client.create_dlp_job(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dlp_v2.types.CreateDlpJobRequest, dict]):
                The request object. Request message for
                CreateDlpJobRequest. Used to initiate
                long running jobs such as calculating
                risk metrics or inspecting Google Cloud
                Storage.
            parent (str):
                Required. Parent resource name.

                The format of this value varies depending on whether you
                have `specified a processing
                location <https://cloud.google.com/dlp/docs/specifying-location>`__:

                -  Projects scope, location specified:
                   ``projects/``\ PROJECT_ID\ ``/locations/``\ LOCATION_ID
                -  Projects scope, no location specified (defaults to
                   global): ``projects/``\ PROJECT_ID

                The following example ``parent`` string specifies a
                parent project with the identifier ``example-project``,
                and specifies the ``europe-west3`` location for
                processing data:

                ::

                    parent=projects/example-project/locations/europe-west3

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            inspect_job (google.cloud.dlp_v2.types.InspectJobConfig):
                An inspection job scans a storage
                repository for InfoTypes.

                This corresponds to the ``inspect_job`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            risk_job (google.cloud.dlp_v2.types.RiskAnalysisJobConfig):
                A risk analysis job calculates
                re-identification risk metrics for a
                BigQuery table.

                This corresponds to the ``risk_job`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dlp_v2.types.DlpJob:
                Combines all of the information about
                a DLP job.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, inspect_job, risk_job])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a dlp.CreateDlpJobRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, dlp.CreateDlpJobRequest):
            request = dlp.CreateDlpJobRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if inspect_job is not None:
                request.inspect_job = inspect_job
            if risk_job is not None:
                request.risk_job = risk_job

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_dlp_job]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_dlp_jobs(
        self,
        request: Optional[Union[dlp.ListDlpJobsRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListDlpJobsPager:
        r"""Lists DlpJobs that match the specified filter in the
        request. See
        https://cloud.google.com/dlp/docs/inspecting-storage and
        https://cloud.google.com/dlp/docs/compute-risk-analysis
        to learn more.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dlp_v2

            def sample_list_dlp_jobs():
                # Create a client
                client = dlp_v2.DlpServiceClient()

                # Initialize request argument(s)
                request = dlp_v2.ListDlpJobsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_dlp_jobs(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.dlp_v2.types.ListDlpJobsRequest, dict]):
                The request object. The request message for listing DLP
                jobs.
            parent (str):
                Required. Parent resource name.

                The format of this value varies depending on whether you
                have `specified a processing
                location <https://cloud.google.com/dlp/docs/specifying-location>`__:

                -  Projects scope, location specified:
                   ``projects/``\ PROJECT_ID\ ``/locations/``\ LOCATION_ID
                -  Projects scope, no location specified (defaults to
                   global): ``projects/``\ PROJECT_ID

                The following example ``parent`` string specifies a
                parent project with the identifier ``example-project``,
                and specifies the ``europe-west3`` location for
                processing data:

                ::

                    parent=projects/example-project/locations/europe-west3

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dlp_v2.services.dlp_service.pagers.ListDlpJobsPager:
                The response message for listing DLP
                jobs.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a dlp.ListDlpJobsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, dlp.ListDlpJobsRequest):
            request = dlp.ListDlpJobsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_dlp_jobs]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListDlpJobsPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_dlp_job(
        self,
        request: Optional[Union[dlp.GetDlpJobRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dlp.DlpJob:
        r"""Gets the latest state of a long-running DlpJob.
        See https://cloud.google.com/dlp/docs/inspecting-storage
        and
        https://cloud.google.com/dlp/docs/compute-risk-analysis
        to learn more.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dlp_v2

            def sample_get_dlp_job():
                # Create a client
                client = dlp_v2.DlpServiceClient()

                # Initialize request argument(s)
                request = dlp_v2.GetDlpJobRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_dlp_job(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dlp_v2.types.GetDlpJobRequest, dict]):
                The request object. The request message for [DlpJobs.GetDlpJob][].
            name (str):
                Required. The name of the DlpJob
                resource.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dlp_v2.types.DlpJob:
                Combines all of the information about
                a DLP job.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a dlp.GetDlpJobRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, dlp.GetDlpJobRequest):
            request = dlp.GetDlpJobRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_dlp_job]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_dlp_job(
        self,
        request: Optional[Union[dlp.DeleteDlpJobRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a long-running DlpJob. This method indicates
        that the client is no longer interested in the DlpJob
        result. The job will be canceled if possible.
        See https://cloud.google.com/dlp/docs/inspecting-storage
        and
        https://cloud.google.com/dlp/docs/compute-risk-analysis
        to learn more.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dlp_v2

            def sample_delete_dlp_job():
                # Create a client
                client = dlp_v2.DlpServiceClient()

                # Initialize request argument(s)
                request = dlp_v2.DeleteDlpJobRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_dlp_job(request=request)

        Args:
            request (Union[google.cloud.dlp_v2.types.DeleteDlpJobRequest, dict]):
                The request object. The request message for deleting a
                DLP job.
            name (str):
                Required. The name of the DlpJob
                resource to be deleted.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a dlp.DeleteDlpJobRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, dlp.DeleteDlpJobRequest):
            request = dlp.DeleteDlpJobRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_dlp_job]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def cancel_dlp_job(
        self,
        request: Optional[Union[dlp.CancelDlpJobRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Starts asynchronous cancellation on a long-running
        DlpJob. The server makes a best effort to cancel the
        DlpJob, but success is not guaranteed.
        See https://cloud.google.com/dlp/docs/inspecting-storage
        and
        https://cloud.google.com/dlp/docs/compute-risk-analysis
        to learn more.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dlp_v2

            def sample_cancel_dlp_job():
                # Create a client
                client = dlp_v2.DlpServiceClient()

                # Initialize request argument(s)
                request = dlp_v2.CancelDlpJobRequest(
                    name="name_value",
                )

                # Make the request
                client.cancel_dlp_job(request=request)

        Args:
            request (Union[google.cloud.dlp_v2.types.CancelDlpJobRequest, dict]):
                The request object. The request message for canceling a
                DLP job.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # Minor optimization to avoid making a copy if the user passes
        # in a dlp.CancelDlpJobRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, dlp.CancelDlpJobRequest):
            request = dlp.CancelDlpJobRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.cancel_dlp_job]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def create_stored_info_type(
        self,
        request: Optional[Union[dlp.CreateStoredInfoTypeRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        config: Optional[dlp.StoredInfoTypeConfig] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dlp.StoredInfoType:
        r"""Creates a pre-built stored infoType to be used for
        inspection. See
        https://cloud.google.com/dlp/docs/creating-stored-infotypes
        to learn more.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dlp_v2

            def sample_create_stored_info_type():
                # Create a client
                client = dlp_v2.DlpServiceClient()

                # Initialize request argument(s)
                request = dlp_v2.CreateStoredInfoTypeRequest(
                    parent="parent_value",
                )

                # Make the request
                response = client.create_stored_info_type(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dlp_v2.types.CreateStoredInfoTypeRequest, dict]):
                The request object. Request message for
                CreateStoredInfoType.
            parent (str):
                Required. Parent resource name.

                The format of this value varies depending on the scope
                of the request (project or organization) and whether you
                have `specified a processing
                location <https://cloud.google.com/dlp/docs/specifying-location>`__:

                -  Projects scope, location specified:
                   ``projects/``\ PROJECT_ID\ ``/locations/``\ LOCATION_ID
                -  Projects scope, no location specified (defaults to
                   global): ``projects/``\ PROJECT_ID
                -  Organizations scope, location specified:
                   ``organizations/``\ ORG_ID\ ``/locations/``\ LOCATION_ID
                -  Organizations scope, no location specified (defaults
                   to global): ``organizations/``\ ORG_ID

                The following example ``parent`` string specifies a
                parent project with the identifier ``example-project``,
                and specifies the ``europe-west3`` location for
                processing data:

                ::

                    parent=projects/example-project/locations/europe-west3

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            config (google.cloud.dlp_v2.types.StoredInfoTypeConfig):
                Required. Configuration of the
                storedInfoType to create.

                This corresponds to the ``config`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dlp_v2.types.StoredInfoType:
                StoredInfoType resource message that
                contains information about the current
                version and any pending updates.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, config])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a dlp.CreateStoredInfoTypeRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, dlp.CreateStoredInfoTypeRequest):
            request = dlp.CreateStoredInfoTypeRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if config is not None:
                request.config = config

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_stored_info_type]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_stored_info_type(
        self,
        request: Optional[Union[dlp.UpdateStoredInfoTypeRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        config: Optional[dlp.StoredInfoTypeConfig] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dlp.StoredInfoType:
        r"""Updates the stored infoType by creating a new
        version. The existing version will continue to be used
        until the new version is ready. See
        https://cloud.google.com/dlp/docs/creating-stored-infotypes
        to learn more.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dlp_v2

            def sample_update_stored_info_type():
                # Create a client
                client = dlp_v2.DlpServiceClient()

                # Initialize request argument(s)
                request = dlp_v2.UpdateStoredInfoTypeRequest(
                    name="name_value",
                )

                # Make the request
                response = client.update_stored_info_type(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dlp_v2.types.UpdateStoredInfoTypeRequest, dict]):
                The request object. Request message for
                UpdateStoredInfoType.
            name (str):
                Required. Resource name of organization and
                storedInfoType to be updated, for example
                ``organizations/433245324/storedInfoTypes/432452342`` or
                projects/project-id/storedInfoTypes/432452342.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            config (google.cloud.dlp_v2.types.StoredInfoTypeConfig):
                Updated configuration for the
                storedInfoType. If not provided, a new
                version of the storedInfoType will be
                created with the existing configuration.

                This corresponds to the ``config`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Mask to control which fields get
                updated.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dlp_v2.types.StoredInfoType:
                StoredInfoType resource message that
                contains information about the current
                version and any pending updates.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, config, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a dlp.UpdateStoredInfoTypeRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, dlp.UpdateStoredInfoTypeRequest):
            request = dlp.UpdateStoredInfoTypeRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name
            if config is not None:
                request.config = config
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_stored_info_type]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_stored_info_type(
        self,
        request: Optional[Union[dlp.GetStoredInfoTypeRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dlp.StoredInfoType:
        r"""Gets a stored infoType.
        See
        https://cloud.google.com/dlp/docs/creating-stored-infotypes
        to learn more.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dlp_v2

            def sample_get_stored_info_type():
                # Create a client
                client = dlp_v2.DlpServiceClient()

                # Initialize request argument(s)
                request = dlp_v2.GetStoredInfoTypeRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_stored_info_type(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dlp_v2.types.GetStoredInfoTypeRequest, dict]):
                The request object. Request message for
                GetStoredInfoType.
            name (str):
                Required. Resource name of the organization and
                storedInfoType to be read, for example
                ``organizations/433245324/storedInfoTypes/432452342`` or
                projects/project-id/storedInfoTypes/432452342.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dlp_v2.types.StoredInfoType:
                StoredInfoType resource message that
                contains information about the current
                version and any pending updates.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a dlp.GetStoredInfoTypeRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, dlp.GetStoredInfoTypeRequest):
            request = dlp.GetStoredInfoTypeRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_stored_info_type]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_stored_info_types(
        self,
        request: Optional[Union[dlp.ListStoredInfoTypesRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListStoredInfoTypesPager:
        r"""Lists stored infoTypes.
        See
        https://cloud.google.com/dlp/docs/creating-stored-infotypes
        to learn more.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dlp_v2

            def sample_list_stored_info_types():
                # Create a client
                client = dlp_v2.DlpServiceClient()

                # Initialize request argument(s)
                request = dlp_v2.ListStoredInfoTypesRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_stored_info_types(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.dlp_v2.types.ListStoredInfoTypesRequest, dict]):
                The request object. Request message for
                ListStoredInfoTypes.
            parent (str):
                Required. Parent resource name.

                The format of this value varies depending on the scope
                of the request (project or organization) and whether you
                have `specified a processing
                location <https://cloud.google.com/dlp/docs/specifying-location>`__:

                -  Projects scope, location specified:
                   ``projects/``\ PROJECT_ID\ ``/locations/``\ LOCATION_ID
                -  Projects scope, no location specified (defaults to
                   global): ``projects/``\ PROJECT_ID

                The following example ``parent`` string specifies a
                parent project with the identifier ``example-project``,
                and specifies the ``europe-west3`` location for
                processing data:

                ::

                    parent=projects/example-project/locations/europe-west3

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dlp_v2.services.dlp_service.pagers.ListStoredInfoTypesPager:
                Response message for
                ListStoredInfoTypes.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a dlp.ListStoredInfoTypesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, dlp.ListStoredInfoTypesRequest):
            request = dlp.ListStoredInfoTypesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_stored_info_types]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListStoredInfoTypesPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_stored_info_type(
        self,
        request: Optional[Union[dlp.DeleteStoredInfoTypeRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a stored infoType.
        See
        https://cloud.google.com/dlp/docs/creating-stored-infotypes
        to learn more.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dlp_v2

            def sample_delete_stored_info_type():
                # Create a client
                client = dlp_v2.DlpServiceClient()

                # Initialize request argument(s)
                request = dlp_v2.DeleteStoredInfoTypeRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_stored_info_type(request=request)

        Args:
            request (Union[google.cloud.dlp_v2.types.DeleteStoredInfoTypeRequest, dict]):
                The request object. Request message for
                DeleteStoredInfoType.
            name (str):
                Required. Resource name of the organization and
                storedInfoType to be deleted, for example
                ``organizations/433245324/storedInfoTypes/432452342`` or
                projects/project-id/storedInfoTypes/432452342.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a dlp.DeleteStoredInfoTypeRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, dlp.DeleteStoredInfoTypeRequest):
            request = dlp.DeleteStoredInfoTypeRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_stored_info_type]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def hybrid_inspect_dlp_job(
        self,
        request: Optional[Union[dlp.HybridInspectDlpJobRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dlp.HybridInspectResponse:
        r"""Inspect hybrid content and store findings to a job.
        To review the findings, inspect the job. Inspection will
        occur asynchronously.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dlp_v2

            def sample_hybrid_inspect_dlp_job():
                # Create a client
                client = dlp_v2.DlpServiceClient()

                # Initialize request argument(s)
                request = dlp_v2.HybridInspectDlpJobRequest(
                    name="name_value",
                )

                # Make the request
                response = client.hybrid_inspect_dlp_job(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dlp_v2.types.HybridInspectDlpJobRequest, dict]):
                The request object. Request to search for potentially
                sensitive info in a custom location.
            name (str):
                Required. Resource name of the job to execute a hybrid
                inspect on, for example
                ``projects/dlp-test-project/dlpJob/53234423``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dlp_v2.types.HybridInspectResponse:
                Quota exceeded errors will be thrown
                once quota has been met.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a dlp.HybridInspectDlpJobRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, dlp.HybridInspectDlpJobRequest):
            request = dlp.HybridInspectDlpJobRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.hybrid_inspect_dlp_job]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def finish_dlp_job(
        self,
        request: Optional[Union[dlp.FinishDlpJobRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Finish a running hybrid DlpJob. Triggers the
        finalization steps and running of any enabled actions
        that have not yet run.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dlp_v2

            def sample_finish_dlp_job():
                # Create a client
                client = dlp_v2.DlpServiceClient()

                # Initialize request argument(s)
                request = dlp_v2.FinishDlpJobRequest(
                    name="name_value",
                )

                # Make the request
                client.finish_dlp_job(request=request)

        Args:
            request (Union[google.cloud.dlp_v2.types.FinishDlpJobRequest, dict]):
                The request object. The request message for finishing a
                DLP hybrid job.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # Minor optimization to avoid making a copy if the user passes
        # in a dlp.FinishDlpJobRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, dlp.FinishDlpJobRequest):
            request = dlp.FinishDlpJobRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.finish_dlp_job]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def __enter__(self) -> "DlpServiceClient":
        return self

    def __exit__(self, type, value, traceback):
        """Releases underlying transport's resources.

        .. warning::
            ONLY use as a context manager if the transport is NOT shared
            with other clients! Exiting the with block will CLOSE the transport
            and may cause errors in other clients!
        """
        self.transport.close()


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)


__all__ = ("DlpServiceClient",)
