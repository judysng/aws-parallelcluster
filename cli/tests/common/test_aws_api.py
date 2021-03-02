# Copyright 2021 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance
# with the License. A copy of the License is located at
#
# http://aws.amazon.com/apache2.0/
#
# or in the "LICENSE.txt" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES
# OR CONDITIONS OF ANY KIND, express or implied. See the License for the specific language governing permissions and
# limitations under the License.
#
# This module contains all the classes representing the Resources objects.
# These objects are obtained from the configuration file through a conversion based on the Schema classes.
#
import pytest
from assertpy import assert_that

from common.boto3.common import AWSClientError
from tests.common.dummy_aws_api import DummyAWSApi

FAKE_STACK_NAME = "parallelcluster-name"


@pytest.mark.parametrize(
    "response,is_error",
    [
        (
            AWSClientError(function_name="describe_stack", message=f"Stack with id {FAKE_STACK_NAME} does not exist"),
            True,
        ),
        ({"Stacks": [{"StackName": FAKE_STACK_NAME, "CreationTime": 0, "StackStatus": "CREATED"}]}, False),
    ],
)
def test_stack_exists(mocker, response, is_error):
    """Verify that CfnClient.stack_exists behaves as expected."""
    should_exist = not is_error
    mocker.patch("common.aws.aws_api.AWSApi.instance", return_value=DummyAWSApi())
    mocker.patch("common.boto3.cfn.CfnClient.describe_stack", side_effect=response)
    assert_that(DummyAWSApi().instance().cfn.stack_exists(FAKE_STACK_NAME)).is_equal_to(should_exist)
