# Colab GPU Provenance Notes

The attached `notebooks/TACC_SC26.ipynb` includes a Colab GPU fallback/proxy
workflow used when direct Stampede3 access was unavailable.

Verified notebook evidence:

- notebook metadata records a Colab GPU session with `accelerator: GPU`, `machine_shape: hm`, and `gpuType: H100`;
- the notebook writes `LLM_colab_paper_fixed.py`;
- the generated script logs `rank=0`, `world_size=1`, and `local_rank=0`;
- the generated script selects CUDA when available and records the CUDA device
  name in `paper_results.json`;
- the generated script writes per-domain sample counts and average latency to
  `paper_results_table.csv`;
- the generated script produces `fig1_domain_distribution.png` and
  `fig2_latency_analysis.png`;
- the notebook also contains a Qwen2.5-VL descriptor workflow with
  `throughput_img_per_s` in the stage summary.

Current verification boundary:

The audited public Drive outputs contain the public figure CSVs and
`model_comparison_results.csv`. They do not contain a parsed 4/8/16/32 scaling
table or log that can be compared directly against the paper's Table III.

For SC26 AE, add the exact scaling provenance file if available, preferably one
of:

- `scaling_results.csv` with GPU count, runtime, throughput, efficiency, and
  communication/overhead columns;
- the Colab notebook output cell that produced the final scaling numbers;
- raw Colab logs plus a parser script;
- raw Stampede3 SLURM logs plus the SLURM batch scripts.
