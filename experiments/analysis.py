#!/usr/bin/env python3
import argparse
import json
import numpy as np


def analyze_signal_source(
    input_file: str,
    output_file: str,
    sample_rate: float,
    expected_freq: float,
    expected_amp: float,
    freq_tol: float,
    amp_tol: float,
) -> None:
    data = np.fromfile(input_file, dtype=np.complex64)

    if len(data) == 0:
        raise RuntimeError("Input capture file is empty.")

    # Measured amplitude from average magnitude
    measured_amp = float(np.mean(np.abs(data)))

    # Measured frequency from FFT peak
    nfft = min(65536, len(data))
    window = np.hanning(nfft).astype(np.float32)
    spectrum = np.fft.fftshift(np.fft.fft(data[:nfft] * window))
    freqs = np.fft.fftshift(np.fft.fftfreq(nfft, d=1.0 / sample_rate))

    peak_index = int(np.argmax(np.abs(spectrum)))
    measured_freq = float(freqs[peak_index])

    # Error calculations
    amp_error = float(abs(measured_amp - expected_amp))
    freq_error = float(abs(measured_freq - expected_freq))

    # Pass/fail checks
    amp_check = amp_error <= amp_tol
    freq_check = freq_error <= freq_tol
    overall_pass = bool(amp_check and freq_check)

    result = {
        "expected_amplitude": expected_amp,
        "measured_amplitude": measured_amp,
        "amplitude_error": amp_error,
        "amplitude_tolerance": amp_tol,
        "expected_frequency_hz": expected_freq,
        "measured_frequency_hz": measured_freq,
        "frequency_error_hz": freq_error,
        "frequency_tolerance_hz": freq_tol,
        "amplitude_check": amp_check,
        "frequency_check": freq_check,
        "pass": overall_pass,
    }

    with open(output_file, "w") as f:
        json.dump(result, f, indent=2)

    print(json.dumps(result, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze File Sink IQ output for signal source validation.")
    parser.add_argument("--input", required=True, help="Path to captured .dat file")
    parser.add_argument("--output", required=True, help="Path to output JSON file")
    parser.add_argument("--sample-rate", type=float, required=True, help="Sample rate in Hz")
    parser.add_argument("--expected-freq", type=float, required=True, help="Expected tone frequency in Hz")
    parser.add_argument("--expected-amp", type=float, required=True, help="Expected amplitude")
    parser.add_argument("--freq-tol", type=float, required=True, help="Allowed frequency error in Hz")
    parser.add_argument("--amp-tol", type=float, required=True, help="Allowed amplitude error")
    args = parser.parse_args()

    analyze_signal_source(
        input_file=args.input,
        output_file=args.output,
        sample_rate=args.sample_rate,
        expected_freq=args.expected_freq,
        expected_amp=args.expected_amp,
        freq_tol=args.freq_tol,
        amp_tol=args.amp_tol,
    )


if __name__ == "__main__":
    main()