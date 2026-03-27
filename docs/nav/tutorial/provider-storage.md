# Storage Provider

The `storage` provider defines where task outputs are persisted.

## Available providers

- `StorageDefault`: keeps data in memory during workflow execution.
- `StorageFile`: persists output to disk (good for local runs and debugging).

## Example

{* ./docs_src/config/storage_provider.py ln[1:25] hl[12:14,17:19] *}

## Extra examples

File storage only:

{* ./docs_src/storage/storage_file.py ln[1:21] hl[11,13:15] *}

## References

- [StorageDefault](https://dotflow-io.github.io/dotflow/nav/reference/storage-init/)
- [StorageFile](https://dotflow-io.github.io/dotflow/nav/reference/storage-file/)
