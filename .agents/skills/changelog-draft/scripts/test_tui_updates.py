#!/usr/bin/env python3

import unittest

from add_tui_updates import add_tui_updates, is_tui_subject, normalize_subject
from convert_to_release_json import convert
from fetch_prs import extract_markers


class TuiUpdatesTest(unittest.TestCase):
    def test_extract_markers_recognizes_tui(self) -> None:
        self.assertEqual(
            extract_markers("CHANGELOG-TUI: Added inline command menus"),
            [{"category": "TUI", "text": "Added inline command menus"}],
        )

    def test_tui_subject_requires_a_standalone_token(self) -> None:
        for subject in [
            "TUI: add inline menus (#1)",
            "[TUI] Add inline menus (#1)",
            "feat(tui): add inline menus (#1)",
            "Polish the TUI zero state (#1)",
        ]:
            self.assertTrue(is_tui_subject(subject), subject)
        self.assertFalse(is_tui_subject("Make the menu more intuitive (#1)"))

    def test_normalize_subject_removes_internal_prefixes(self) -> None:
        self.assertEqual(
            normalize_subject("[CODE-123] TUI: add inline menus (#456)"),
            "Add inline menus",
        )
        self.assertEqual(
            normalize_subject("feat(tui): add inline menus (#456)"),
            "Add inline menus",
        )

    def test_moves_generic_tui_entries_and_honors_surface_markers(self) -> None:
        changelog = {
            "newFeatures": [],
            "improvements": ["Generic TUI text", "Desktop text", "Remove me"],
            "bugFixes": [],
            "images": [],
            "oz_updates": [],
        }
        prs = [
            {
                "commit_subject": "TUI: add generic entry (#1)",
                "explicit_entries": [
                    {"category": "IMPROVEMENT", "text": "Generic TUI text"}
                ],
            },
            {
                "commit_subject": "feat(tui): add status menu (#2)",
                "explicit_entries": [],
            },
            {
                "commit_subject": "Add status details (#22)",
                "title": "TUI: add status details",
                "explicit_entries": [],
            },
            {
                "commit_subject": "TUI: explicit text wins (#3)",
                "explicit_entries": [
                    {"category": "TUI", "text": "Explicit TUI text"},
                    {"category": "IMPROVEMENT", "text": "Remove me"},
                ],
            },
            {
                "commit_subject": "TUI: keep this in Oz (#4)",
                "explicit_entries": [
                    {"category": "OZ", "text": "Explicit Oz text"}
                ],
            },
        ]

        result = add_tui_updates(changelog, prs)

        self.assertEqual(result["improvements"], ["Desktop text"])
        self.assertEqual(
            result["tui_updates"],
            [
                "Generic TUI text",
                "Add status menu",
                "Add status details",
                "Explicit TUI text",
            ],
        )

    def test_converter_maps_tui_entries(self) -> None:
        release = convert(
            {
                "entries": [
                    {
                        "category": "TUI",
                        "text": "Added inline menus",
                        "pr_number": 123,
                        "url": "https://github.com/warpdotdev/warp/pull/123",
                    }
                ]
            }
        )
        self.assertEqual(
            release["tui_updates"],
            [
                "Added inline menus "
                "([#123](https://github.com/warpdotdev/warp/pull/123))"
            ],
        )


if __name__ == "__main__":
    unittest.main()
