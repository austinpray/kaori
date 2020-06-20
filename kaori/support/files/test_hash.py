from pathlib import Path

from .hash import file_digest, hashed_file_name


def test_hash_file():
    fixture = Path(__file__) \
        .parent \
        .joinpath('../../../tests/fixtures/kaori.png')

    # openssl dgst -sha512 -binary tests/fixtures/kaori.png | openssl base64 -A
    expected_sha = 'sha512-' \
                   '557ea4829ecd24bf24ef09d7452f9381a5096d1d04a62875e2283359e8571d5f636c521433cd8a212c2778dd2d84496d34ed68b1745c1813aa5c05f1bdc176af'
    assert file_digest(fixture.open('rb')) == expected_sha


def test_hash_file_name():
    assert hashed_file_name('/ayy/lmao.png', 'sha512-ABC') == '/ayy/lmao-sha512-ABC.png'
    assert hashed_file_name('lmao.png', 'sha512-ABC') == 'lmao-sha512-ABC.png'
