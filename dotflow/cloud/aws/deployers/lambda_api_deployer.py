"""Lambda + API Gateway deployment."""

from __future__ import annotations

import contextlib

from dotflow.cloud.aws.deployers.base_lambda_deployer import BaseLambdaDeployer


class LambdaApiDeployer(BaseLambdaDeployer):
    """Deploy dotflow pipeline as Lambda + API Gateway."""

    def _configure_trigger(self, name: str, **kwargs) -> None:
        """Create HTTP API with Lambda integration."""
        apigw = self._boto3.client("apigatewayv2", region_name=self._region)
        api_name = f"{name}-api"

        api_id = self._find_api(apigw, api_name)

        if not api_id:
            print("  Creating API Gateway...")
            response = apigw.create_api(Name=api_name, ProtocolType="HTTP")
            api_id = response["ApiId"]

            integration = apigw.create_integration(
                ApiId=api_id,
                IntegrationType="AWS_PROXY",
                IntegrationUri=self._function_arn,
                PayloadFormatVersion="2.0",
            )

            apigw.create_route(
                ApiId=api_id,
                RouteKey="POST /workflow",
                Target=f"integrations/{integration['IntegrationId']}",
            )

            apigw.create_stage(
                ApiId=api_id, StageName="$default", AutoDeploy=True
            )

            with contextlib.suppress(
                self._lambda.exceptions.ResourceConflictException
            ):
                self._lambda.add_permission(
                    FunctionName=name,
                    StatementId=f"{api_name}-invoke",
                    Action="lambda:InvokeFunction",
                    Principal="apigateway.amazonaws.com",
                    SourceArn=(
                        f"arn:aws:execute-api:{self._region}:"
                        f"{self._account_id}:{api_id}/*"
                    ),
                )

        url = (
            f"https://{api_id}.execute-api."
            f"{self._region}.amazonaws.com/workflow"
        )
        print(f"  Endpoint: {url}")

    def _find_api(self, apigw, name: str) -> str | None:
        """Find existing API by name."""
        for api in apigw.get_apis().get("Items", []):
            if api["Name"] == name:
                return api["ApiId"]
        return None
