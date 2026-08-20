---
name: nerdd-molecular-predictions
description: Predict molecular properties using NERDD, e.g. metabolite prediction, CYP activation and inhibitor likelihood, and natural-product likeness. Use to query available modules, submit a job, and retrieve its results.
---

# NERDD predictions

Use the bundled helpers for NERDD. They query the live API, so module metadata, accepted options, and output schemas remain current.

## Select a module

Run `scripts/list_modules.py` to obtain the compact JSON response from `/modules`. It lists module IDs, names, versions, and output formats without making per-module requests.

```bash
python scripts/list_modules.py
```

After choosing a candidate, run `scripts/get_module.py MODULE_ID` to obtain its full interface metadata from `/modules/{module_id}`, including its description, `job_parameters` (defaults and permitted choices), and `result_properties`. Important: use the module's `id`:

```bash
python scripts/get_module.py cypstrate
```

Choose a module only after comparing its `description`, `job_parameters`, and `result_properties`. `module_id` is the identifier needed by the job helper. Molecular input may be SMILES, SDF, or InChI.

## Create and wait for a job

`scripts/create_job.py` submits a multipart job to `/{module}/jobs` and immediately prints the newly created job object, including its ID. It accepts only new molecular input.

```bash
python scripts/create_job.py --module cypstrate --input 'CCO' \
  --param prediction_mode=full_coverage
```

Use repeatable `--input`, `--file`, and `--param` options. Values supplied through `--param NAME=VALUE` are JSON-decoded when possible, so booleans/numbers work naturally; module parameters and supported values come from `get_module.py`.

To submit multiple molecules, provide repeated `--input` values or create an SDF/SMILES file and pass it with `--file`. To wait for a submitted job, pass its ID to `scripts/wait_for_completion.py`. It waits for the job to finish and prints the final job object. Predictions may take some time.

```bash
python scripts/wait_for_completion.py JOB_ID
```

To inspect a current status without waiting, use `scripts/get_status.py`:

```bash
python scripts/get_status.py JOB_ID
```

The completed job's `output_files` list provides the available SDF and CSV exports, and `results_url` provides its JSON results endpoint.

Treat a failed job as a reported prediction failure: preserve its job metadata and error output; do not silently substitute another module or retry indefinitely.
