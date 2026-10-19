"""Download the original-author files this analysis reads, and verify them against the frozen manifests.

The author repository Mijan/LFNS_MSB carries no licence at its root, so a public copy of this work does not
redistribute its files. The three manifests in simulation/public_data/ record every file this analysis reads --
its path, its Git blob SHA, its size and its source URL at the pinned commit -- which is enough to fetch them
and prove they are the same bytes the reported results were computed from.

A file already present and matching its recorded SHA is left alone, so re-running costs nothing. A download
whose SHA does not match the manifest is never written; the script reports it and exits non-zero.

Usage: python simulation/code/fetch_author_sources.py
"""
import hashlib
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / 'public_data'
SOURCE = PUBLIC / 'fgf2_author_repository'
MANIFESTS = ('fgf2_source_manifest.json', 'fgf2_expanded_source_manifest.json', 'fgf2_b3_source_manifest.json')
REPO = 'Mijan/LFNS_MSB'
COMMIT = '5c917abda0618d75c00c9cab45f24ed893dd71f1'


def git_blob_sha(raw):
    """Git's object id for a blob: sha1 over the header and the content."""
    return hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()


def wanted():
    """Every file entry of every manifest, as path -> recorded blob SHA."""
    files = {}
    for name in MANIFESTS:
        for entry in json.loads((PUBLIC / name).read_text(encoding='utf-8')):
            if isinstance(entry, dict) and 'path' in entry and 'blob_sha' in entry:
                files[entry['path']] = entry['blob_sha']
    return files


def fetch(url):
    request = urllib.request.Request(url, headers={'User-Agent': 'fgf2-fetch'})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def main():
    files = wanted()
    present = downloaded = 0
    failures = []
    for path, sha in sorted(files.items()):
        target = SOURCE / path
        if target.is_file() and git_blob_sha(target.read_bytes()) == sha:
            present += 1
            continue
        url = f'https://raw.githubusercontent.com/{REPO}/{COMMIT}/{path}'
        try:
            raw = fetch(url)
        except urllib.error.URLError as error:
            failures.append(f'{path}: download failed ({error})')
            continue
        if git_blob_sha(raw) != sha:
            failures.append(f'{path}: blob SHA does not match the manifest; not written')
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
        downloaded += 1
    print(f'{len(files)} files listed: {present} already present and verified, {downloaded} downloaded')
    for failure in failures:
        print('  ', failure)
    if failures:
        print(f'{len(failures)} file(s) missing; the analysis cannot run until they are in place.')
        return 1
    print(f'All author files verified against the pinned commit {COMMIT[:12]}.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
