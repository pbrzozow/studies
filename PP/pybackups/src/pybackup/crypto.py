from pathlib import Path

from cryptography.fernet import Fernet


def generate_key(output_path: Path) -> None:
    key = Fernet.generate_key()
    output_path.write_bytes(key)
    output_path.chmod(0o600)


def load_fernet(key_file: Path) -> Fernet:
    if not key_file.exists():
        raise FileNotFoundError(f"key file not found: {key_file}")
    return Fernet(key_file.read_bytes())


def encrypt_file(source: Path, dest: Path, fernet: Fernet) -> None:
    dest.write_bytes(fernet.encrypt(source.read_bytes()))


def decrypt_file(source: Path, dest: Path, fernet: Fernet) -> None:
    dest.write_bytes(fernet.decrypt(source.read_bytes()))
