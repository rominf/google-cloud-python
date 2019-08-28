# -*- coding: utf-8 -*-
#
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Wraps the Google Cloud Storage client library for use in tables helper."""

import time

from google.api_core import exceptions

try:
    import pandas
except ImportError:  # pragma: NO COVER
    pandas = None

try:
    from google.cloud import storage
except ImportError:  # pragma: NO COVER
    storage = None

_PANDAS_REQUIRED = "pandas is required to verify type DataFrame."
_STORAGE_REQUIRED = (
    "google-cloud-storage is required to create Google Cloud Storage client."
)


class GcsClient(object):
    """Uploads Pandas DataFrame to a bucket in Google Cloud Storage."""

    def __init__(self, client=None, credentials=None):
        """Constructor.

        Args:
            client (Optional[storage.Client]): A Google Cloud Storage Client
                instance.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
        """
        if storage is None:
            raise ImportError(_STORAGE_REQUIRED)

        if client is not None:
            self.client = client
        elif credentials is not None:
            self.client = storage.Client(credentials=credentials)
        else:
            self.client = storage.Client()

    def ensure_bucket_exists(self, project, region):
        """Checks if a bucket named '{project}-automl-tables-staging' exists.

        Creates this bucket if it doesn't exist.

        Args:
            project (str): The project that stores the bucket.
            region (str): The region of the bucket.

        Returns:
            A string representing the created bucket name.
        """
        bucket_name = "{}-automl-tables-staging".format(project)

        try:
            self.client.get_bucket(bucket_name)
        except exceptions.NotFound:
            bucket = self.client.bucket(bucket_name)
            bucket.create(project=project, location=region)
        return bucket_name

    def upload_pandas_dataframe(self, bucket_name, dataframe, uploaded_csv_name=None):
        """Uploads a Pandas DataFrame as CSV to the bucket.

        Args:
            bucket_name (str): The bucket name to upload the CSV to.
            dataframe (pandas.DataFrame): The Pandas Dataframe to be uploaded.
            uploaded_csv_name (Optional[str]): The name for the uploaded CSV.

        Returns:
            A string representing the GCS URI of the uploaded CSV.
        """
        if pandas is None:
            raise ImportError(_PANDAS_REQUIRED)

        if not isinstance(dataframe, pandas.DataFrame):
            raise ValueError("'dataframe' must be a pandas.DataFrame instance.")

        if uploaded_csv_name is None:
            uploaded_csv_name = "automl-tables-dataframe-{}.csv".format(
                int(time.time())
            )
        csv_string = dataframe.to_csv()

        bucket = self.client.get_bucket(bucket_name)
        blob = bucket.blob(uploaded_csv_name)
        blob.upload_from_string(csv_string)

        return "gs://{}/{}".format(bucket_name, uploaded_csv_name)