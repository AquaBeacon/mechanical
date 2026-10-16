"""Fetch only the official STEP member via HTTP ranges, retaining provenance."""
from pathlib import Path
import hashlib
import io
import json
import struct
import urllib.request
import zipfile
import zlib

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assemblies/child_horizontal_plate_frame/ref'
URL = 'https://cad.bluerobotics.com/BLUEROV2-R4.zip'


def request(start=None, end=None):
    headers = {} if start is None else {'Range': f'bytes={start}-{end}'}
    method = 'HEAD' if start is None else 'GET'
    response = urllib.request.urlopen(urllib.request.Request(URL, headers=headers, method=method), timeout=45)
    if start is not None and response.status != 206:
        response.close()
        raise RuntimeError('Server did not honor range; refusing full archive download')
    return response


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    with request() as response:
        length = int(response.headers['Content-Length'])
        modified = response.headers.get('Last-Modified')
    tail_start = max(0, length - 131072)
    with request(tail_start, length - 1) as response:
        tail = response.read()
    archive = zipfile.ZipFile(io.BytesIO(tail))
    member = next(i for i in archive.infolist() if i.filename.upper().endswith('.STEP'))
    target = OUT / Path(member.filename).name
    offset = member.header_offset + tail_start
    if not target.exists():
        with request(offset, offset + 29) as response:
            header = response.read()
        signature, _, _, method, _, _, _, _, _, name_length, extra_length = struct.unpack('<I5H3I2H', header)
        if signature != 0x04034B50 or method != zipfile.ZIP_DEFLATED:
            raise RuntimeError('Unexpected ZIP member format')
        start = offset + 30 + name_length + extra_length
        decompressor = zlib.decompressobj(-15)
        crc = 0
        size = 0
        with request(start, start + member.compress_size - 1) as response, target.open('wb') as output:
            while block := response.read(1024 * 1024):
                decoded = decompressor.decompress(block)
                output.write(decoded)
                crc = zlib.crc32(decoded, crc)
                size += len(decoded)
            decoded = decompressor.flush()
            output.write(decoded)
            crc = zlib.crc32(decoded, crc)
            size += len(decoded)
        if size != member.file_size or crc != member.CRC:
            raise RuntimeError('Downloaded STEP failed ZIP size/CRC validation')
    report = {'url': URL, 'product_page': 'https://bluerobotics.com/store/rov/bluerov2/',
              'retrieved_date': '2026-10-07', 'archive_last_modified': modified,
              'archive_member': member.filename, 'archive_size_bytes': length,
              'member_size_bytes': target.stat().st_size,
              'sha256': hashlib.sha256(target.read_bytes()).hexdigest(),
              'use': 'Manufacturer CAD original for layout study only; geometry not used as a child part.'}
    (OUT / 'source.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
