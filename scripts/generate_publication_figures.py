#!/usr/bin/env python3
"""Generate the public SC26 agricultural-AI figures from image folders.

This script is a standalone version of the figure-generation workflow in
`notebooks/TACC_SC26.ipynb`. It computes deterministic RGB descriptors,
cotton-visibility proxy counts, stage summaries, a PCA view, and the
pre/post visual comparison panel.

The proxy is an image-derived visibility surrogate, not ground-truth boll
counting.
"""

from __future__ import annotations

import argparse
import time
from pathlib import Path

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.ndimage as ndimage
from PIL import Image, ImageFile
from sklearn.decomposition import PCA

ImageFile.LOAD_TRUNCATED_IMAGES = True
VALID_EXTS = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".bmp", ".webp"}


def is_valid_image_file(path: Path) -> bool:
    return (
        path.is_file()
        and path.suffix.lower() in VALID_EXTS
        and not path.name.startswith("._")
        and not path.name.startswith(".")
    )


def classify_stage(name: str) -> str:
    lowered = name.lower()
    if "pre" in lowered:
        return "pre_defoliation"
    if "post" in lowered:
        return "post_defoliation"
    if "rose" in lowered:
        return "rose_nursery"
    return "unknown"


def compute_white_boll_proxy(img: Image.Image, stage: str = "unknown"):
    arr = np.array(img.convert("RGB")).astype(np.float32)
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]

    intensity = (r + g + b) / 3.0
    max_c = np.max(arr, axis=2)
    min_c = np.min(arr, axis=2)
    saturation = (max_c - min_c) / (max_c + 1e-6)
    exg = 2 * g - r - b

    if stage == "post_defoliation":
        mask = (intensity > 160) & (saturation < 0.15) & (exg < 5) & (r > 140) & (b > 140)
        mask = ndimage.binary_opening(mask, structure=np.ones((5, 5)))
    else:
        mask = (intensity > 150) & (saturation < 0.20) & (exg < 10) & (r > 130) & (b > 130)
        mask = ndimage.binary_opening(mask, structure=np.ones((4, 4)))

    heatmap = ndimage.gaussian_filter(mask.astype(float), sigma=25)
    labeled_mask, _ = ndimage.label(mask)
    slices = ndimage.find_objects(labeled_mask)

    bboxes = []
    for sl in slices:
        if sl is None:
            continue
        y_slice, x_slice = sl
        h = y_slice.stop - y_slice.start
        w = x_slice.stop - x_slice.start
        if 5 <= w <= 150 and 5 <= h <= 150:
            area = w * h
            aspect = w / float(h)
            if 25 <= area <= 6000 and 0.2 <= aspect <= 5.0:
                bboxes.append((x_slice.start, y_slice.start, w, h))

    return bboxes, len(bboxes), float(mask.mean()), heatmap


def extract_features(img: Image.Image, stage: str = "unknown") -> dict[str, float]:
    arr = np.array(img.convert("RGB")).astype(np.float32)
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    exg = 2 * g - r - b
    ngrdi = (g - r) / (g + r + 1e-6)
    rbr = r / (b + 1e-6)
    brightness = (r + g + b) / 3.0
    _, proxy_count, proxy_area, _ = compute_white_boll_proxy(img, stage)
    return {
        "mean_r": float(r.mean()),
        "mean_g": float(g.mean()),
        "mean_b": float(b.mean()),
        "mean_exg": float(exg.mean()),
        "std_exg": float(exg.std()),
        "mean_ngrdi": float(ngrdi.mean()),
        "mean_rbr": float(rbr.mean()),
        "bright_fraction": float((brightness > 180).mean()),
        "boll_count_proxy": float(proxy_count),
        "white_region_fraction": float(proxy_area),
    }


def build_table(root_dir: Path, sample_limit: int) -> tuple[pd.DataFrame, dict[str, list[str]]]:
    rows = []
    exemplar_paths = {"pre_defoliation": [], "post_defoliation": []}
    for directory in sorted(root_dir.rglob("*")):
        if not directory.is_dir():
            continue
        files = sorted(f for f in directory.iterdir() if is_valid_image_file(f))
        if not files:
            continue
        stage = classify_stage(directory.name)
        for f in files[:sample_limit]:
            try:
                t0 = time.time()
                img = Image.open(f).convert("RGB")
                rows.append({
                    "directory": directory.name,
                    "stage": stage,
                    "path": str(f),
                    "latency_s": time.time() - t0,
                    **extract_features(img, stage),
                })
                if stage in exemplar_paths and len(exemplar_paths[stage]) < 6:
                    exemplar_paths[stage].append(str(f))
            except Exception:
                continue
    return pd.DataFrame(rows), exemplar_paths


def clean_axes(ax) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def make_pca_publication(df: pd.DataFrame, out_dir: Path) -> None:
    feat_cols = [
        "mean_r", "mean_g", "mean_b", "mean_exg", "std_exg",
        "mean_ngrdi", "mean_rbr", "bright_fraction",
        "boll_count_proxy", "white_region_fraction",
    ]
    plot_df = df[df["stage"].isin(["pre_defoliation", "post_defoliation"])].copy()
    if plot_df.empty:
        return
    z = PCA(n_components=2, random_state=42).fit_transform(plot_df[feat_cols].fillna(0.0).values)
    plot_df["pc1"], plot_df["pc2"] = z[:, 0], z[:, 1]

    fig, ax = plt.subplots(figsize=(7.2, 5.6), dpi=300)
    for stage, marker in [("pre_defoliation", "o"), ("post_defoliation", "^")]:
        sub = plot_df[plot_df["stage"] == stage]
        ax.scatter(sub["pc1"], sub["pc2"], s=34, alpha=0.82, marker=marker, label=stage.replace("_", "-"))
    clean_axes(ax)
    ax.set_xlabel("PC1")
    ax.set_ylabel("PC2")
    ax.set_title("Stage separation in image-level agricultural descriptor space", pad=10)
    ax.legend(frameon=False, loc="best")
    ax.grid(alpha=0.16, linewidth=0.6)
    fig.tight_layout()
    fig.savefig(out_dir / "fig_pca_publication.png", bbox_inches="tight")
    plt.close(fig)


def make_six_panel_grid(exemplar_paths: dict[str, list[str]], out_dir: Path) -> None:
    pre_paths = exemplar_paths.get("pre_defoliation", [])
    post_paths = exemplar_paths.get("post_defoliation", [])
    if not pre_paths or not post_paths:
        return

    pre_img = Image.open(pre_paths[0]).convert("RGB")
    post_img = Image.open(post_paths[0]).convert("RGB")
    pre_bboxes, pre_count, _, pre_hm = compute_white_boll_proxy(pre_img, "pre_defoliation")
    post_bboxes, post_count, _, post_hm = compute_white_boll_proxy(post_img, "post_defoliation")

    fig, axes = plt.subplots(2, 3, figsize=(18, 10), dpi=300)
    panel_data = [
        (axes[0, 0], np.array(pre_img), "Pre-Defoliation: Raw Image", None),
        (axes[0, 1], pre_hm, "Pre-Defoliation: Heatmap", None),
        (axes[0, 2], np.array(pre_img), f"Pre-Defoliation Boll Count: {pre_count}", pre_bboxes),
        (axes[1, 0], np.array(post_img), "Post-Defoliation: Raw Image", None),
        (axes[1, 1], post_hm, "Post-Defoliation: Heatmap", None),
        (axes[1, 2], np.array(post_img), f"Post-Defoliation Boll Count: {post_count}", post_bboxes),
    ]
    for ax, image, title, bboxes in panel_data:
        ax.imshow(image, cmap="hot" if "Heatmap" in title else None)
        if bboxes:
            for x, y, w, h in bboxes:
                ax.add_patch(patches.Rectangle((x, y), w, h, linewidth=1.5, edgecolor="lime", facecolor="none"))
        ax.set_title(title, fontsize=14, fontweight="bold", color="green" if "Count" in title else "black")
        ax.axis("off")
    fig.suptitle("Cotton Defoliation Stage Comparison: Raw vs. Heatmap vs. Detection", fontsize=18, y=1.02)
    fig.tight_layout()
    fig.savefig(out_dir / "fig_2x3_pre_post_grid.png", bbox_inches="tight")
    plt.close(fig)


def make_quantitative_panel(df: pd.DataFrame, out_dir: Path) -> None:
    plot_df = df[df["stage"].isin(["pre_defoliation", "post_defoliation"])].copy()
    if plot_df.empty:
        return
    summary = plot_df.groupby("stage", as_index=False).agg(
        samples=("path", "count"),
        avg_latency_s=("latency_s", "mean"),
        mean_boll_count_proxy=("boll_count_proxy", "mean"),
        mean_white_region_fraction=("white_region_fraction", "mean"),
        mean_exg=("mean_exg", "mean"),
    )
    summary.to_csv(out_dir / "stage_summary_table.csv", index=False)

    fig, axes = plt.subplots(1, 2, figsize=(10.2, 4.2), dpi=300)
    for stage in ["pre_defoliation", "post_defoliation"]:
        sub = plot_df[plot_df["stage"] == stage]
        axes[0].scatter(sub["white_region_fraction"], sub["boll_count_proxy"], s=24, alpha=0.78, label=stage.replace("_", "-"))
    clean_axes(axes[0])
    axes[0].set_xlabel("White-region fraction")
    axes[0].set_ylabel("Cotton visibility proxy (Boll Count)")
    axes[0].set_title("Visibility density vs proxy count")
    axes[0].legend(frameon=False)
    axes[0].grid(alpha=0.16, linewidth=0.6)

    x = np.arange(len(summary))
    width = 0.36
    axes[1].bar(x - width / 2, summary["mean_boll_count_proxy"], width=width, label="Mean proxy count")
    axes[1].bar(x + width / 2, summary["mean_white_region_fraction"] * 100, width=width, label="Mean white fraction (x100)")
    clean_axes(axes[1])
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(summary["stage"].str.replace("_", "-"))
    axes[1].set_title("Stage-wise contrast in cotton visibility")
    axes[1].legend(frameon=False)
    axes[1].grid(axis="y", alpha=0.16, linewidth=0.6)
    fig.tight_layout()
    fig.savefig(out_dir / "fig_quantitative_panel.png", bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root-dir", required=True, type=Path)
    parser.add_argument("--out-dir", required=True, type=Path)
    parser.add_argument("--sample-limit", type=int, default=80)
    args = parser.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)
    df, exemplar_paths = build_table(args.root_dir, sample_limit=args.sample_limit)
    df.to_csv(args.out_dir / "inventory_analysis_table.csv", index=False)
    make_pca_publication(df, args.out_dir)
    make_six_panel_grid(exemplar_paths, args.out_dir)
    make_quantitative_panel(df, args.out_dir)
    print(f"Saved figures and tables to {args.out_dir}")


if __name__ == "__main__":
    main()
