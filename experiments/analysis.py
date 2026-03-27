#!/usr/bin/env python3

import argparse
import json
import os
import sys
from typing import Dict, Any

import numpy as np


def load_samples(path: str) -> np.ndarray:
    """Load complex64 GNU Radio raw samples from file."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Input file not found: {path}")

    samples = np.fromfile(path, dtype=np.complex64)
    if samples.size == 0:
        raise ValueError("Input sample file is empty.")

    return samples


def estimate_dominant_frequency(samples: np.ndarray, sample_rate: float) -> float:
    
    n = len(samples)
    window = np.hanning(n)
    windowed = samples * window

    spectrum = np.fft.fft(windowed)
    freqs = np.fft.fftfreq(n, d=1.0 / sample_rate)

    peak_idx = np.argmax(np.abs(spectrum))
    return float(abs(freqs[peak_idx]))


def estimate_amplitude(samples: np.ndarray) -> float:
    
    return float(np.max(np.abs(samples)))


def compute_metrics(
    samples: np.ndarray,
    sample_rate: float,
    expected_frequency: float,
    expected_amplitude: float,
) -> Dict[str, float]:
    measured_frequency = estimate_dominant_frequency(samples, sample_rate)
    measured_amplitude = estimate_amplitude(samples)

    frequency_error = abs(measured_frequency - expected_frequency)

    if expected_amplitude == 0:
        amplitude_error_percent = 0.0 if measured_amplitude == 0 else float("inf")
    else:
        amplitude_error_percent = abs(measured_amplitude - expected_amplitude) / abs(expected_amplitude) * 100.0

    return {
        "measured_frequency": measured_frequency,
        "measured_amplitude": measured_amplitude,
        "frequency_error": frequency_error,
        "amplitude_error_percent": amplitude_error_percent,
    }


def evaluate(metrics: Dict[str, float], freq_threshold: float, amp_threshold_percent: float) -> str:
    if metrics["frequency_error"] > freq_threshold:
        return "FAIL"
    if metrics["amplitude_error_percent"] > amp_threshold_percent:
        return "FAIL"
    return "PASS"


def build_result(
    block_name: str,
    input_file: str,
    metrics: Dict[str, float],
    expected_frequency: float,
    expected_amplitude: float,
    freq_threshold: float,
    amp_threshold_percent: float,
    status: str,
) -> Dict[str, Any]:
    return {
        "block": block_name,
        "status": status,
        "input_file": input_file,
        "expected": {
            "frequency": expected_frequency,
            "amplitude": expected_amplitude,
        },
        "metrics": {
            "measured_frequency": metrics["measured_frequency"],
            "measured_amplitude": metrics["measured_amplitude"],
            "frequency_error": metrics["frequency_error"],
            "amplitude_error_percent": metrics["amplitude_error_percent"],
        },
        "thresholds": {
            "frequency_error_hz": freq_threshold,
            "amplitude_error_percent": amp_threshold_percent,
        },
    }


def write_json(path: str, data: Dict[str, Any]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze sig_source captured samples.")
    parser.add_argument("--input", required=True, help="Path to raw complex sample file (e.g. rx_output.dat)")
    parser.add_argument("--output", required=True, help="Path to output JSON file (e.g. result.json)")
    parser.add_argument("--sample-rate", type=float, required=True, help="Sample rate in Hz")
    parser.add_argument("--expected-frequency", type=float, required=True, help="Expected tone frequency in Hz")
    parser.add_argument("--expected-amplitude", type=float, required=True, help="Expected signal amplitude")
    parser.add_argument("--freq-threshold", type=float, default=1.0, help="Allowed frequency error in Hz")
    parser.add_argument(
        "--amp-threshold-percent",
        type=float,
        default=5.0,
        help="Allowed amplitude error in percent",
    )
    parser.add_argument("--block-name", default="sig_source", help="Block name for JSON report")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        samples = load_samples(args.input)

        metrics = compute_metrics(
            samples=samples,
            sample_rate=args.sample_rate,
            expected_frequency=args.expected_frequency,
            expected_amplitude=args.expected_amplitude,
        )

        status = evaluate(
            metrics=metrics,
            freq_threshold=args.freq_threshold,
            amp_threshold_percent=args.amp_threshold_percent,
        )

        result = build_result(
            block_name=args.block_name,
            input_file=args.input,
            metrics=metrics,
            expected_frequency=args.expected_frequency,
            expected_amplitude=args.expected_amplitude,
            freq_threshold=args.freq_threshold,
            amp_threshold_percent=args.amp_threshold_percent,
            status=status,
        )

        write_json(args.output, result)
        print(f"Analysis complete. Status: {status}. Output written to {args.output}")
        return 0

    except Exception as exc:
        error_result = {
            "block": args.block_name,
            "status": "ERROR",
            "error": str(exc),
            "input_file": args.input,
        }
        try:
            write_json(args.output, error_result)
        except Exception:
            pass
        print(f"Analysis failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())