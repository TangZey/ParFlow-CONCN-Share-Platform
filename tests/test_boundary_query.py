from pathlib import Path
import sys
import unittest


BACKEND_DIR = Path(__file__).resolve().parents[1] / "parflow-website" / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from boundary_query import parse_bbox, parse_boundary_ids  # noqa: E402


class BoundaryQueryTests(unittest.TestCase):
    def test_parse_ids_validates_deduplicates_and_preserves_order(self):
        first = "01020000000000"
        second = "01020300000000"
        self.assertEqual(
            parse_boundary_ids(f"{first},{second},{first}"),
            [first, second],
        )

    def test_parse_ids_rejects_invalid_or_excessive_values(self):
        with self.assertRaises(ValueError):
            parse_boundary_ids("not-a-basin")
        with self.assertRaises(ValueError):
            parse_boundary_ids("01020000000000,01020300000000", max_ids=1)

    def test_parse_bbox(self):
        self.assertEqual(
            parse_bbox("100.5,20,110.5,30"),
            (100.5, 20.0, 110.5, 30.0),
        )
        for invalid in ("100,20,90,30", "100,20,110", "x,20,110,30"):
            with self.subTest(invalid=invalid):
                with self.assertRaises(ValueError):
                    parse_bbox(invalid)


if __name__ == "__main__":
    unittest.main()
