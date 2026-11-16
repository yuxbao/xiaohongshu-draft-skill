import json
import tempfile
import unittest
import zipfile
from pathlib import Path

import importlib.util

helper = Path(__file__).resolve().parents[1] / "skills/xiaohongshu-draft/scripts/package_draft.py"
spec = importlib.util.spec_from_file_location("package_draft", helper)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
package = module.package


class PackageDraftTests(unittest.TestCase):
    def test_preserves_unicode_copy_and_image_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            images = root / 'images'
            images.mkdir()
            raw_image = b'original image bytes'
            (images / '图-01.PNG').write_bytes(raw_image)
            copy = root / '文案.md'
            raw_copy = '# 标题\n\n中文正文与 emoji 🌱\n#分享'.encode('utf-8')
            copy.write_bytes(raw_copy)
            output = root / 'bundle.zip'
            package(copy, images, output)
            with zipfile.ZipFile(output) as archive:
                self.assertEqual(archive.read('draft.md'), raw_copy)
                self.assertEqual(archive.read('images/图-01.PNG'), raw_image)
                self.assertNotIn(str(root), archive.read('manifest.json').decode('utf-8'))

    def test_does_not_overwrite_an_existing_bundle(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            images = root / 'images'
            images.mkdir()
            (images / 'image.png').write_bytes(b'image')
            copy = root / 'draft.md'
            copy.write_text('draft', encoding='utf-8')
            output = root / 'bundle.zip'
            output.write_bytes(b'keep existing content')
            with self.assertRaises(FileExistsError):
                package(copy, images, output)
            self.assertEqual(output.read_bytes(), b'keep existing content')

    def test_skips_symlinks_and_subdirectories(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            images = root / 'images'
            images.mkdir()
            (images / 'selected.png').write_bytes(b'selected')
            private = root / 'private.png'
            private.write_bytes(b'outside selection')
            (images / 'linked.png').symlink_to(private)
            nested = images / 'nested'
            nested.mkdir()
            (nested / 'nested.png').write_bytes(b'nested')
            copy = root / 'draft.md'
            copy.write_text('draft', encoding='utf-8')
            included = package(copy, images, root / 'bundle.zip')
            self.assertEqual([p.name for p in included], ['selected.png'])

    def test_packages_copy_images_in_natural_order_and_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            images = root / "images"
            images.mkdir()
            (images / "slide-10.png").write_bytes(b"ten")
            (images / "slide-2.jpg").write_bytes(b"two")
            (images / "ignore.gif").write_bytes(b"gif")
            copy = root / "draft.md"
            copy.write_text("# Draft\n\nBody", encoding="utf-8")
            output = root / "bundle.zip"

            included = package(copy, images, output)

            self.assertEqual([p.name for p in included], ["slide-2.jpg", "slide-10.png"])
            with zipfile.ZipFile(output) as archive:
                self.assertEqual(archive.namelist(), [
                    "draft.md", "images/slide-2.jpg", "images/slide-10.png", "manifest.json"
                ])
                manifest = json.loads(archive.read("manifest.json"))
                self.assertEqual(manifest["images"], ["images/slide-2.jpg", "images/slide-10.png"])
                self.assertIn("local bundle only", manifest["publication_status"])

    def test_rejects_missing_images(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            copy = root / "draft.md"
            copy.write_text("draft", encoding="utf-8")
            images = root / "images"
            images.mkdir()
            with self.assertRaisesRegex(ValueError, "no supported images"):
                package(copy, images, root / "bundle.zip")


if __name__ == "__main__":
    unittest.main()
