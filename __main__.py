import pulumi  # NOQA
from pulumi import Output
import pulumi_aws as aws

default_identity = aws.get_caller_identity()
current_region = aws.get_region()

my_bucket = aws.s3.Bucket(
    "myLittleBucketOfJoy",
    bucket="test-0084gqy7e869mrqchq4a-my-little-bucket-of-joy",
    acl="private",
    tags={"Name": "My Little Bucket of Joy"},
)

test_role_policy_assume_role_policy_sfn = aws.iam.get_policy_document(
    statements=[
        {
            "principals": [
                {"type": "Service", "identifiers": ["states.amazonaws.com"]}
            ],
            "actions": ["sts:AssumeRole"],
        }
    ]
)

test_role = aws.iam.Role(
    "testRole",
    name="test-role",
    assume_role_policy=test_role_policy_assume_role_policy_sfn.json,
    tags={"my_tag": "tag_value"},
)

test_role_policy = aws.iam.get_policy_document(
    statements=[
        {
            "actions": [
                "states:SendTaskFailure",
                "states:SendTaskHeartbeat",
                "states:SendTaskSuccess",
            ],
            "resources": [
                f"arn:aws:states:{current_region.name}:{default_identity.account_id}:stateMachine:my-state-machine"
            ],
        },
        {
            "actions": ["s3:PutObject"],
            "resources": [Output.concat(my_bucket.arn, "/*")],
        },
    ]
)


test_role_policy = aws.iam.RolePolicy(
    "testRolePolicy",
    name="test-role-policy",
    role=test_role.name,
    policy=test_role_policy.json,
)
