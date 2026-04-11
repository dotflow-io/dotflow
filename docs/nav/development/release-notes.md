# Release Notes

## v0.15.0

- [📦 PyPI - Build 0.15.0](https://github.com/dotflow-io/dotflow/releases/tag/v0.15.0)
- [🪲 Bug: _serialize_context crashes when storage is a list of non-Context objects](https://github.com/dotflow-io/dotflow/pull/249)
- [⚙️ Feature: Add Alibaba Cloud Function Compute deployer](https://github.com/dotflow-io/dotflow/pull/238)
- [⚙️ Feature: Implement Server provider for remote API communication](https://github.com/dotflow-io/dotflow/pull/240)
- [⚙️ Feature: dotflow deploy CLI — cross-cloud infrastructure generation](https://github.com/dotflow-io/dotflow/pull/183)
- [⚙️ Feature: Add warning/debug log levels and workflow-level logging to Log ABC](https://github.com/dotflow-io/dotflow/pull/189)
- [⚙️ Feature: OpenTelemetry integration — traces and spans per workflow/task](https://github.com/dotflow-io/dotflow/pull/190)
- [📌 Remove external dotflow-mongodb package references](https://github.com/dotflow-io/dotflow/pull/200)
- [⚙️ Refactor: Separate Engine from Execution Strategy](https://github.com/dotflow-io/dotflow/pull/202)
- [⚠️ Security: Remove shell injection vulnerability in write_file_system](https://github.com/dotflow-io/dotflow/pull/213)
- [🪲 Bug: Parallel strategy still uses Execution instead of TaskEngine](https://github.com/dotflow-io/dotflow/pull/214)
- [🪲 Bug: StorageFile.get() returns empty list for missing keys — breaks resume=True](https://github.com/dotflow-io/dotflow/pull/223)
- [🪲 Bug: StorageDefault uses ctypes.cast(id) — unsafe memory access](https://github.com/dotflow-io/dotflow/pull/226)
- [🪲 Bug: traceback_error() ignores error parameter — uses sys.exc_info()](https://github.com/dotflow-io/dotflow/pull/225)
- [🪲 Bug: SerializerTask.model_dump_json() mutates self and produces truncated invalid JSON](https://github.com/dotflow-io/dotflow/pull/224)
- [🪲 Bug: Async task execution creates new event loops with asyncio.run()](https://github.com/dotflow-io/dotflow/pull/227)
- [🪲 Bug: Module class uses spec_from_file_location instead of importlib.import_module](https://github.com/dotflow-io/dotflow/pull/229)
- [🪲 Bug: StorageFile.post() crashes with AttributeError on corrupted task files](https://github.com/dotflow-io/dotflow/pull/230)
- [🪲 Bug: InitCommand uses hardcoded TEMPLATE_REPO instead of Settings constant](https://github.com/dotflow-io/dotflow/pull/231)
- [🪲 Bug: CLI --storage s3/gcs crashes with TypeError — missing required bucket argument](https://github.com/dotflow-io/dotflow/pull/232)
- [🪲 Bug: Context setters silently ignore invalid values](https://github.com/dotflow-io/dotflow/pull/234)
- [🪲 Fix PR #202 review issues — duration, executor leak, checkpoint, docstring](https://github.com/dotflow-io/dotflow/pull/222)
- [🪲 Fix deploy scheduled platforms, add ECSScheduledDeployer and ScheduleResolver](https://github.com/dotflow-io/dotflow/pull/236)

## v0.14.1

- [📦 PyPI - Build 0.14.1](https://github.com/dotflow-io/dotflow/releases/tag/v0.14.1)
- [🪲 Fix co_varnames to only include parameters, not local variables](https://github.com/dotflow-io/dotflow/pull/161)
- [🪲 Fix method ordering to use regex matching instead of string search](https://github.com/dotflow-io/dotflow/pull/163)
- [🪲 Fix fork multiprocessing on macOS with OBJC safety flag](https://github.com/dotflow-io/dotflow/pull/165)
- [🪲 Fix timeout thread leak in ThreadPoolExecutor](https://github.com/dotflow-io/dotflow/pull/166)
- [🪲 Add thread-safe lock to Background list append](https://github.com/dotflow-io/dotflow/pull/167)
- [🪲 Fix race condition in queue overlap dispatch](https://github.com/dotflow-io/dotflow/pull/169)
- [🪲 Track and join spawned threads on scheduler stop](https://github.com/dotflow-io/dotflow/pull/170)
- [🪲 Save and restore signal handlers on scheduler start/stop](https://github.com/dotflow-io/dotflow/pull/171)
- [⚠️ Update vulnerable dependencies](https://github.com/dotflow-io/dotflow/pull/156)
- [📌 Add NotifyDiscord provider](https://github.com/dotflow-io/dotflow/pull/185)

## v0.14.0

- [📦 PyPI - Build 0.14.0](https://github.com/dotflow-io/dotflow/releases/tag/v0.14.0)
- [📌 Workflow scheduler — cron-based recurring execution](https://github.com/dotflow-io/dotflow/pull/126)
- [📌 Workflow observability — task.errors and retry tracking](https://github.com/dotflow-io/dotflow/pull/113)
- [📌 Checkpoint-based durable state (resume from failure)](https://github.com/dotflow-io/dotflow/pull/118)
- [📌 StorageS3 provider for AWS S3 persistence](https://github.com/dotflow-io/dotflow/pull/114)
- [📌 StorageGCS provider for Google Cloud Storage persistence](https://github.com/dotflow-io/dotflow/pull/116)
- [📌 Rewrite dotflow init with interactive cookiecutter template](https://github.com/dotflow-io/dotflow/pull/121)
- [📌 Async/await support for actions](https://github.com/dotflow-io/dotflow/pull/122)
- [📌 Thread-safety in Action retry and task status RETRY](https://github.com/dotflow-io/dotflow/pull/99)
- [🪲 Fix backoff mutating retry_delay permanently across calls](https://github.com/dotflow-io/dotflow/pull/100)
- [📘 Fix documentation gaps — incorrect references, missing parameters](https://github.com/dotflow-io/dotflow/pull/120)

## v0.13.2

- [📦 PyPI - Build 0.13.2](https://github.com/dotflow-io/dotflow/releases/tag/v0.13.2)
- [🪲 BUG: Fix Background mode results unreliable](https://github.com/dotflow-io/dotflow/pull/85)
- [🪲 BUG: Fix busy-wait loop and enable multiprocessing on macOS](https://github.com/dotflow-io/dotflow/pull/78)
- [🪲 Fix typo in workflow filename and export WorkflowStatus](https://github.com/dotflow-io/dotflow/pull/91)
- [🪲 Fix typo _excution → _execution in execution.py](https://github.com/dotflow-io/dotflow/pull/94)
- [🪲 Fix TaskBuilder.add() return type annotation](https://github.com/dotflow-io/dotflow/pull/79)
- [⬆️ Configure PyPI publish workflows with OIDC](https://github.com/dotflow-io/dotflow/pull/97)

## v0.13.1

- [📦 PyPI - Build 0.13.1](https://github.com/dotflow-io/dotflow/releases/tag/v0.13.1)
- [⚠️ Update dependencies](https://github.com/dotflow-io/dotflow/pull/61)

## v0.13.0

- [📦 PyPI - Build 0.13.0](https://github.com/dotflow-io/dotflow/releases/tag/v0.13.0)
- [📌 Action with timeout, retry_delay and backoff](https://github.com/dotflow-io/dotflow/pull/56)
- [📌 Notification with Telegram](https://github.com/dotflow-io/dotflow/pull/59)

## v0.12.0

- [📦 PyPI - Build 0.12.0](https://github.com/dotflow-io/dotflow/releases/tag/v0.12.0)
- [📌 Separate tasks into groups](https://github.com/dotflow-io/dotflow/pull/54)
- [📌 Workflow result](https://github.com/dotflow-io/dotflow/pull/52)

## v0.11.1

- [📦 PyPI - Build 0.11.1](https://github.com/dotflow-io/dotflow/releases/tag/v0.11.1)
- [🪲 BUG: Problem with context of type 'pydantic class'](https://github.com/dotflow-io/dotflow/pull/50)

## v0.11.0

- [📦 PyPI - Build 0.11.0](https://github.com/dotflow-io/dotflow/releases/tag/v0.11.0)

## v0.10.0

- [📦 PyPI - Build 0.10.0](https://github.com/dotflow-io/dotflow/releases/tag/v0.10.0)
- [📌 Storage MongoDB](https://github.com/dotflow-io/dotflow/pull/42)
- [📌 ABC Config / Storage](https://github.com/dotflow-io/dotflow/pull/43)
- [📌 Update Documentation](https://github.com/dotflow-io/dotflow/pull/44)

## v0.9.1

- [📦 PyPI - Build 0.9.1](https://github.com/dotflow-io/dotflow/releases/tag/v0.9.1)
- [🪲 BUG: Fixed ImportError NoneType Python 3.9](https://github.com/dotflow-io/dotflow/commit/406d6e57ae2e21476f1e570e83e5be495c844e9a)

## v0.9.0

- [📦 PyPI - Build 0.9.0](https://github.com/dotflow-io/dotflow/releases/tag/v0.9.0)
- [📌 Bulk task inclusion option](https://github.com/dotflow-io/dotflow/pull/40)

## v0.8.2

- [📦 PyPI - Build 0.8.2](https://github.com/dotflow-io/dotflow/releases/tag/v0.8.2)
- [🪲 Fixed class-type step without init](https://github.com/dotflow-io/dotflow/commit/4991f5a61022ac0035c6dcc203458e152bca47e8)

## v0.8.1

- [📦 PyPI - Build 0.8.1](https://github.com/dotflow-io/dotflow/releases/tag/v0.8.1)
- [🪲 Fixed context switching](https://github.com/dotflow-io/dotflow/commit/ca9be8d313d900a90d66e026c57a151f6effc6dc)

## v0.8.0

- [📦 PyPI - Build 0.8.0](https://github.com/dotflow-io/dotflow/releases/tag/v0.8.0)
- [📌 Create CLI to manage workflow](https://github.com/dotflow-io/dotflow/pull/37)

## v0.7.0

- [📦 PyPI - Build 0.7.0](https://github.com/dotflow-io/dotflow/releases/tag/v0.7.0)
- [📌 Communication layer implementation](https://github.com/dotflow-io/dotflow/pull/34)

## v0.6.0

- [📦 PyPI - Build 0.6.0](https://github.com/dotflow-io/dotflow/releases/tag/v0.6.0)

## v0.5.0

- [📦 PyPI - Build 0.5.1](https://github.com/dotflow-io/dotflow/releases/tag/v0.5.0)
- [📌 CLI - Command-Line Interface](https://github.com/dotflow-io/dotflow/pull/29)
- [📌 Step adaptation with class structure](https://github.com/dotflow-io/dotflow/pull/31)

## v0.4.1

- [📦 PyPI - Build 0.4.1](https://github.com/dotflow-io/dotflow/releases/tag/v0.4.1)

## v0.4.0

- [📦 PyPI - Build 0.4.0](https://github.com/dotflow-io/dotflow/releases/tag/v0.4.0)
- [📌 Improvement of the API to start the workflow task](https://github.com/dotflow-io/dotflow/issues/23)
- [📌 Improved API interface for decorators](https://github.com/dotflow-io/dotflow/issues/19)
- [📌 Improvement unit tests](https://github.com/dotflow-io/dotflow/issues/14)

## v0.3.0

- [📦 PyPI - Build 0.3.0](https://github.com/dotflow-io/dotflow/releases/tag/v0.3.0)
- [📌 Improvement of the API to start the workflow task](https://github.com/dotflow-io/dotflow/issues/10)

## v0.2.0

- [📦 PyPI - Build 0.2.0](https://github.com/dotflow-io/dotflow/releases/tag/v0.2.0)
- [📌 Create documentation](https://github.com/dotflow-io/dotflow/issues/6)
- [📌 Import of the context class](https://github.com/dotflow-io/dotflow/issues/9)

## v0.1.0

- [📦 PyPI - Build 0.1.0](https://github.com/dotflow-io/dotflow/releases/tag/v0.1.0)