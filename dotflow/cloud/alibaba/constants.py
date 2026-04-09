"""Alibaba Cloud constants."""

SDK_NOT_FOUND = (
    "alibabacloud-fc-open20210406 is required: "
    "pip install dotflow[deploy-alibaba]"
)

CREDENTIALS_NOT_FOUND = (
    "Alibaba Cloud credentials not found. "
    "Run 'aliyun configure' or set "
    "ALIBABA_CLOUD_ACCESS_KEY_ID and "
    "ALIBABA_CLOUD_ACCESS_KEY_SECRET."
)

PLATFORMS = {
    "alibaba-fc",
    "alibaba-fc-scheduled",
}

SCHEDULED_PLATFORMS = {"alibaba-fc-scheduled"}

DEFAULT_REGION = "cn-hangzhou"
