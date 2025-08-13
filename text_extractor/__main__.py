"""Command-line interface for the text extraction tool."""

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

from . import extract_text_from_file


def main(argv: Optional[list[str]] = None) -> int:
    """Main CLI entry point.

    Parameters
    ----------
    argv : list[str], optional
        Command line arguments. If None, uses sys.argv.

    Returns
    -------
    int
        Exit code (0 for success, 1 for error).
    """
    parser = argparse.ArgumentParser(
        description="Extract text from various file formats",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m text_extractor document.pdf
  python -m text_extractor --json document.docx
  python -m text_extractor --output result.txt document.csv
        """,
    )

    parser.add_argument(
        "file_path",
        help="Path to the file to extract text from",
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results in JSON format",
    )

    parser.add_argument(
        "--output",
        "-o",
        help="Output file path (default: stdout)",
    )

    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Verbose output with additional information",
    )

    args = parser.parse_args(argv)

    try:
        # Extract text from file
        result = extract_text_from_file(args.file_path)

        # Prepare output
        if args.json:
            output_data = {
                "text": result.text,
                "file_type": result.file_type,
                "ocr_used": result.ocr_used,
                "pages": [
                    {
                        "page_number": page.page_number,
                        "text": page.text,
                        "ocr": page.ocr,
                    }
                    for page in result.pages
                ],
            }
            output_text = json.dumps(output_data, indent=2, ensure_ascii=False)
        else:
            output_lines = []
            if args.verbose:
                output_lines.extend(
                    [
                        f"File: {args.file_path}",
                        f"Type: {result.file_type}",
                        f"OCR Used: {result.ocr_used}",
                        f"Pages: {len(result.pages)}",
                        "-" * 40,
                    ]
                )
            output_lines.append(result.text)
            output_text = "\n".join(output_lines)

        # Write output
        if args.output:
            output_path = Path(args.output)
            output_path.write_text(output_text, encoding="utf-8")
            if args.verbose:
                print(f"Results written to: {output_path}", file=sys.stderr)
        else:
            print(output_text)

        return 0

    except FileNotFoundError:
        print(f"Error: File not found: {args.file_path}", file=sys.stderr)
        return 1

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    except Exception as e:
        print(f"Error: Unexpected error occurred: {e}", file=sys.stderr)
        if args.verbose:
            import traceback

            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
