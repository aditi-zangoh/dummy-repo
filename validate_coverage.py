#!/usr/bin/env python
"""
Coverage validation script for CI/CD pipeline
"""

import os
import subprocess
import sys


def main():
    """Run coverage validation"""
    print("🚀 Starting coverage validation...")

    # Set environment variables
    env = os.environ.copy()
    env["PATH"] = env.get("PATH", "") + ":/home/runner/.local/bin"

    try:
        # Run tests with coverage
        print("Running Django tests with coverage...")
        result = subprocess.run(
            ["coverage", "run", "--source=.", "manage.py", "test"],
            env=env,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            print("❌ Tests failed!")
            print(result.stdout)
            print(result.stderr)
            return 1

        print("✅ All tests passed!")

        # Check coverage report
        print("Generating coverage report...")
        result = subprocess.run(
            ["coverage", "report", "--show-missing", "--fail-under=90"],
            env=env,
            capture_output=True,
            text=True,
        )

        print(result.stdout)

        if result.returncode != 0:
            print("❌ Coverage below 90% threshold!")
            print(result.stderr)
            return 1

        print("✅ Coverage meets 90% requirement!")

        # Extract coverage percentage
        lines = result.stdout.strip().split("\n")
        for line in lines:
            if "TOTAL" in line:
                parts = line.split()
                if len(parts) >= 4:
                    coverage_pct = parts[3].rstrip("%")
                    print(f"📊 Final coverage: {coverage_pct}%")
                    break

        return 0

    except Exception as e:
        print(f"❌ Error running coverage validation: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
