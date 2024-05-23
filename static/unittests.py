import hashlib
import unittest
from algorithms import Algorithm

cz_text = """Jestliže nejste s prací spokojen, můžete ji vrátit k doplnění stisknutím
        tlačítka Vrátit práci k doplnění. Studentovi, který práci odevzdal bude následně automaticky
        poslán e-mail o vrácení práce k přepracování a bude zařazen zpět mezi studenty, kteří práci neodevzdali.
        Jestliže chcete k e-mailu připojit důvod vrácení práce, můžete ho vyplnit do následujícího políčka."""

class TestMd5(unittest.TestCase):

    def setUp(self) -> None:
        self.algorithm = Algorithm("", "md5")

    def test_md5_empty_message(self):
        """Test that the MD5 hash function correctly handles strings with leading and trailing whitespaces
        and removes them before processing."""

        hashlib_hash = hashlib.md5(self.algorithm.message.encode()).hexdigest()
        self.assertEqual(self.algorithm.hash(), hashlib_hash)

    def test_md5_single_character(self):
        """Test the SHA-1 hash of a single character."""

        self.algorithm = Algorithm("a", "md5")
        hashlib_hash = hashlib.md5(self.algorithm.message.encode()).hexdigest()
        self.assertEqual(self.algorithm.hash(), hashlib_hash)

    def test_md5_with_single_character(self):
        """Test that the MD5 hash function correctly handles a string with a single character."""

        self.algorithm = Algorithm("a", "md5")
        hashlib_hash = hashlib.md5(self.algorithm.message.encode()).hexdigest()
        self.assertEqual(self.algorithm.hash(), hashlib_hash)

    def test_md5_with_multiple_characters(self):
        """Test that the MD5 hash function correctly handles a string with multiple characters."""

        self.algorithm = Algorithm("abcdefghijklmnopqrstuvwxyz", "md5")
        hashlib_hash = hashlib.md5(self.algorithm.message.encode()).hexdigest()
        self.assertEqual(self.algorithm.hash(), hashlib_hash)

    def test_md5_with_large_string(self):
        """Test that the MD5 hash function correctly handles a large string."""

        self.algorithm = Algorithm("a"*1000, "md5")
        hashlib_hash = hashlib.md5(self.algorithm.message.encode()).hexdigest()
        self.assertEqual(self.algorithm.hash(), hashlib_hash)

    def test_md5_special_characters(self):
        """Test the MD5 hash of a string with special characters."""

        self.algorithm = Algorithm("!@#$%^&*()_+-=[]{}|;:,.<>?", "md5")
        hashlib_hash = hashlib.md5(self.algorithm.message.encode()).hexdigest()
        self.assertEqual(self.algorithm.hash(), hashlib_hash)

    def test_md5_czech_text(self):
        """Test the MD5 hash of a string with czech text with interpuction."""

        self.algorithm = Algorithm(cz_text, "md5")
        hashlib_hash = hashlib.md5(self.algorithm.message.encode()).hexdigest()
        self.assertEqual(self.algorithm.hash(), hashlib_hash)

class TestSha1(unittest.TestCase):

    def setUp(self) -> None:
        self.algorithm = Algorithm("", "sha1")

    def test_sha1_empty_string(self):
        """Test the SHA-1 hash of an empty string."""

        hashlib_hash = hashlib.sha1(self.algorithm.message.encode()).hexdigest()
        self.assertEqual(self.algorithm.hash(), hashlib_hash)

    def test_sha1_single_character(self):
        """Test the SHA-1 hash of a single character."""

        self.algorithm = Algorithm("a", "sha1")
        hashlib_hash = hashlib.sha1(self.algorithm.message.encode()).hexdigest()
        self.assertEqual(self.algorithm.hash(), hashlib_hash)

    def test_sha1_multiple_characters(self):
        """Test the SHA-1 hash of multiple characters."""

        self.algorithm = Algorithm("abcdefghijklmnopqrstuvwxyz", "sha1")
        hashlib_hash = hashlib.sha1(self.algorithm.message.encode()).hexdigest()
        self.assertEqual(self.algorithm.hash(), hashlib_hash)

    def test_sha1_large_string(self):
        """Test the SHA-1 hash of a large string."""

        self.algorithm = Algorithm("a" * 1000, "sha1")
        hashlib_hash = hashlib.sha1(self.algorithm.message.encode()).hexdigest()
        self.assertEqual(self.algorithm.hash(), hashlib_hash)

    def test_sha1_special_characters(self):
        """Test the SHA-1 hash of a string with special characters."""

        self.algorithm = Algorithm("!@#$%^&*()_+-=[]{}|;:,.<>?", "sha1")
        hashlib_hash = hashlib.sha1(self.algorithm.message.encode()).hexdigest()
        self.assertEqual(self.algorithm.hash(), hashlib_hash)

    def test_sha1_czech_text(self):
        """Test the SHA-1 hash of a string with czech text with interpuction."""

        self.algorithm = Algorithm(cz_text, "sha1")
        hashlib_hash = hashlib.sha1(self.algorithm.message.encode()).hexdigest()
        self.assertEqual(self.algorithm.hash(), hashlib_hash)

class TestSha256(unittest.TestCase):

    def setUp(self) -> None:
        self.algorithm = Algorithm("", "sha256")

    def test_sha256_empty_string(self):
        """Test the SHA-256 hash of an empty string."""

        hashlib_hash = hashlib.sha256(self.algorithm.message.encode()).hexdigest()
        self.assertEqual(self.algorithm.hash(), hashlib_hash)

    def test_sha256_single_character(self):
        """Test the SHA-256 hash of a single character."""

        self.algorithm = Algorithm("a", "sha256")
        hashlib_hash = hashlib.sha256(self.algorithm.message.encode()).hexdigest()
        self.assertEqual(self.algorithm.hash(), hashlib_hash)

    def test_sha256_multiple_characters(self):
        """Test the SHA-256 hash of multiple characters."""

        self.algorithm = Algorithm("abcdefghijklmnopqrstuvwxyz", "sha256")
        hashlib_hash = hashlib.sha256(self.algorithm.message.encode()).hexdigest()
        self.assertEqual(self.algorithm.hash(), hashlib_hash)

    def test_sha256_large_string(self):
        """Test the SHA-256 hash of a large string."""

        self.algorithm = Algorithm("a" * 1000, "sha256")
        hashlib_hash = hashlib.sha256(self.algorithm.message.encode()).hexdigest()
        self.assertEqual(self.algorithm.hash(), hashlib_hash)

    def test_sha256_special_characters(self):
        """Test the SHA-256 hash of a string with special characters."""

        self.algorithm = Algorithm("!@#$%^&*()_+-=[]{}|;:,.<>?", "sha256")
        hashlib_hash = hashlib.sha256(self.algorithm.message.encode()).hexdigest()
        self.assertEqual(self.algorithm.hash(), hashlib_hash)

    def test_sha256_czech_text(self):
        """Test the SHA-256 hash of a string with czech text with interpuction."""

        self.algorithm = Algorithm(cz_text, "sha256")
        hashlib_hash = hashlib.sha256(self.algorithm.message.encode()).hexdigest()
        self.assertEqual(self.algorithm.hash(), hashlib_hash)

if __name__ == '__main__':
    unittest.main()
