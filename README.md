# GitHub Activity Logger

A set of Python tools to collect and summarize GitHub user activity.

## Installation

This project uses [uv](https://github.com/astral-sh/uv) for dependency management. It is recommended to replace `python` with `uv run` as each script is self-contained.

```bash
uv run gh_daylog.py octocat 2025-04-22
uv run gh_day_summary.py octocat-2025-04-22.ndjson
``` 

## Tools

### gh_daylog.py
Collects all GitHub events for a specified user on a given calendar date and saves them as newline-delimited JSON.

```bash
# Set your GitHub token (optional but recommended for better rate limits)
export GH_TOKEN="ghp_xxx"

# Collect events for a user on a specific date
python gh_daylog.py octocat 2025-04-22
```

### gh_day_summary.py
Generates a human-readable Markdown summary from the collected events, including:
- Per-repository activity digest
- Detailed commit history with diff links
- PR and Issue interaction summary

```bash
# Generate summary from collected events
python gh_day_summary.py octocat-2025-04-22.ndjson
```

## Example Output

The summary includes:

1. **Per-repo digest** - Quick overview of activity counts by type for each repository
2. **Commit roll-up** - Detailed commit history organized by repository and branch, including:
   - Commit messages
   - SHA hashes
   - Compare diff links
3. **PR / Issue interaction summary** - Chronological list of:
   - Pull request reviews and comments
   - Issue creation and comments
   - Branch creation
   - Other GitHub interactions

Real output for `mgoin`:

```
uv run gh_day_summary.py mgoin-2025-04-23.ndjson
# Per-repo digest

* **mgoin/hf_model_stats** – 3 × push commits
* **mgoin/llmgoin** – 2 × push commits
* **neuralmagic/vllm** – 1 × branches created, 127 × push commits
* **state-spaces/mamba** – 1 × issue opened
* **vllm-project/vllm** – 7 × reviews, 26 × review comments, 5 × issue comments, 2 × pr opened, 3 × push commits, 2 × pr closed, 1 × branches created

# Commit roll-up

## mgoin/hf_model_stats
### main
- acbbba9  Update RedHatAI stats 2025-04-23
↪︎ compare diff: https://github.com/mgoin/hf_model_stats/compare/419927ca59e005fa1b479d3e502e950e086e6b43...acbbba9cc3733e38eefd3eba1270d4e379ad76ca
- 419927c  Update ibm-granite stats 2025-04-23
↪︎ compare diff: https://github.com/mgoin/hf_model_stats/compare/0f148f618a38c0ca10d27fc097962ed773db18cd...419927ca59e005fa1b479d3e502e950e086e6b43
- 0f148f6  Update nm-testing stats 2025-04-23
↪︎ compare diff: https://github.com/mgoin/hf_model_stats/compare/7a3bae6a534311ff196587b0ae25419420814115...0f148f618a38c0ca10d27fc097962ed773db18cd

## mgoin/llmgoin
### main
- 8dcd4ee  Create gradio_chat.py
↪︎ compare diff: https://github.com/mgoin/llmgoin/compare/ba64213dc6d0fdf1eb07d35bcad00826c7496106...8dcd4ee066fa496defa862228944812b26a08a53
- ba64213  Create mma_test.cu
↪︎ compare diff: https://github.com/mgoin/llmgoin/compare/ef28997a5d03c665b257036f63f348266e2622bc...ba64213dc6d0fdf1eb07d35bcad00826c7496106

## neuralmagic/vllm
### test-initialization-v1
- 93e561e  Improve error for structured output backend selection (#16717)
- 8a7368e  [Misc] Remove redundant comment (#16703)
- 3cd91dc  Help user create custom model for Transformers backend remote code models (#16719)
- 3092375  [V1][Performance] Implement custom serializaton for MultiModalKwargs [Rebased] (#16432)
- 2cbd4d2  [V1][Spec Dec Bug Fix] Respect Spec Dec Method Specification (#16636)
- 3c776dc  Adding vllm buildkite job for IBM Power (#16679)
- 2b05b8c  [V1][Frontend] Improve Shutdown And Logs (#11737)
- 95aca28  [rocm][V0] fix selection logic for custom PA in V0 (#16426)
- cb072ce  [Bugfix] Update Florence-2 tokenizer to make grounding tasks work (#16734)
- 607029e  [Bugfix] Revert max_prompt_len validation for decoder-only models. (#16741)
- 9dbf7a2  [V1] Remove log noise when idle (#16735)
- 8cac35b  [Ray] Improve documentation on batch inference (#16609)
- a648152  [misc] ignore marlin_moe_wna16 local gen codes (#16760)
- 61a44a0  [Doc] Add more tips to avoid OOM (#16765)
- d8e557b  [doc] add open-webui example (#16747)
- 5b1aca2  [Bugfix] Fix GLM4 model (#16618)
- 207da28  [Doc] Fix a 404 link in installation/cpu.md (#16773)
- 99ed526  [Misc] refactor examples series - lmcache (#16758)
- d27ea94  Improve configs - `TokenizerPoolConfig` + `DeviceConfig` (#16603)
- c69bf4e  fix: hyperlink (#16778)
↪︎ compare diff: https://github.com/neuralmagic/vllm/compare/254d1b47a011555a53a19adc4c359cd871778bd6...ab101e2d7eb5aac371f87ec5746ab1f011a3324e
### categorize-kernel-tests
- f0b8239  Wrong location
↪︎ compare diff: https://github.com/neuralmagic/vllm/compare/6e9f325f00d476f10f1d2486364709af91f241a1...f0b82390b2de06080834aefb61c49b0dc3bad254
### enable-v1-usage-stats
- b82124d  Reformat
↪︎ compare diff: https://github.com/neuralmagic/vllm/compare/24dfb08a6b130f6906ab743c47a13fe0088e24d0...b82124d21ae3e0044fe52a3e51b6d707c186569e

## vllm-project/vllm
### main
- 6317a51  Categorize `tests/kernels/` based on kernel type (#16799)
↪︎ compare diff: https://github.com/vllm-project/vllm/compare/aa72d9a4ea6b31a845bf4fbd5a97d3175a8c329a...6317a5174a4f3cbd57c44d15023042cecc576f9e
- 83d9337  [Core][V1][TPU] Enable structured decoding on TPU V1 (#16499)
↪︎ compare diff: https://github.com/vllm-project/vllm/compare/5175b884f70d82d57ad7ce5229f579e45d0c502a...83d933718c82f71e4971b6febe781743a2a52919
### tpu-v1-sampler-recompilation-test
- d7650c5  Disable enforce eager for struct_output test
↪︎ compare diff: https://github.com/vllm-project/vllm/compare/d4fb4db38e47b6beb714bcadb17cf317afd5a8bc...d7650c527d60f783a3882df436e7fcd62e03dc3f


# PR / Issue interaction summary

## neuralmagic/vllm
- Created branch `fix-missing-kernel-test`

## state-spaces/mamba
- Issue #720 OPENED: mamba-ssm fails to build on torch==2.7.0

## vllm-project/vllm
- Reviewed PR #17070 → approved
- Commented on PR #17073: Could we do this distinction based on GPU memory in GB?…
- Reviewed PR #17073 → commented
- Commented on Issue #17070: Maybe this won't work in the docker in this case because torch has not been inst…
- Commented on Issue #17070: it works if i disable build isolation i.e. `uv pip install mamba-ssm==2.2.4 --no…
- Commented on PR #17070: ```suggestion…
- Commented on PR #17070: ```suggestion…
- Reviewed PR #17070 → commented
- Commented on Issue #16859: Now that torch 2.7 has released (https://pypi.org/project/torch/2.7.0/) can this…
- PR #17060 OPENED: Add missing rocm_skinny_gemms kernel test to CI
- PR #16799 CLOSED: Categorize `tests/kernels/` based on kernel type
- Commented on PR #16850: These comments would be useful to put in the function description, if other user…
- Reviewed PR #16850 → commented
- Commented on Issue #16736: I think it is non-trivial to set the head size since this is a calculated config…
- Commented on PR #16850: Why not pass in the output here if you added the ability to do inplace?…
- Commented on PR #16850: Why can you get rid of the weight scale expand? fp8.py usually makes per-tensor …
- Commented on PR #16850: FYI @LucasWilkinson …
- Commented on PR #16850: Should we do this warning even if atomic add wasn't enabled?…
- Commented on PR #16850: So we need much smaller workspaces in all cases now? Just making sure that all t…
- Commented on PR #16850: Nice optimization for this function. This gave me an idea for an easy comment fo…
- Commented on PR #16850: Please add comments for the operations here, as this answered a question I had w…
- Reviewed PR #16850 → commented
- Commented on PR #16850: Ditto about comments on these cases just to be explicit…
- Commented on PR #16850: Did we actually support HQQ for MoE before?…
- Commented on PR #16850: cruft?…
- Commented on PR #16850: It looks like FZP_GET_IF isn't called anywhere?…
- Commented on PR #16850: Why does this file now have an entrypoint for moe marlin?…
- Commented on PR #16850: Why did you move to using auto in many places?…
- Commented on PR #16850: Can you add comments to the beginning of each of these sections? I don't underst…
- Commented on PR #16850: Why the +1?…
- Commented on PR #16850: It looks like "vllm::kU8" is included here actually so we should update the comm…
- Commented on PR #16850: This is not for the MOE generation right? So should be `MARLIN_GEN_SCRIPT`…
- Commented on PR #16850: Curious why you need cutlass_extensions?…
- Commented on PR #16850: Please add a comment for this case…
- Commented on PR #16850: Please add a comment for this case…
- Commented on PR #16850: Uncomment?…
- Commented on PR #16850: Won't `"csrc/quantization/gptq_marlin/*.cu"` include the following kernels speci…
- Reviewed PR #16850 → commented
- Reviewed PR #16850 → commented
- Commented on Issue #16986: I could not find any clear error with the failing tests other than timeouts and …
- PR #17016 OPENED: Disable enforce_eager for tests/v1/tpu/test_sampler.py
- Created branch `tpu-v1-sampler-recompilation-test`
- PR #16499 CLOSED: [Core][V1][TPU] Enable structured decoding on TPU V1
```