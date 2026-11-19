// news-image-20261119 — deliver the finished front page for 19 November 2026.
// The entry is a single PNG (entry.png). Before it is handed to the grader,
// this program proves the file is what it claims to be: a real PNG, no
// larger than 1024 px on either side, no larger than 1 MiB. Anything that
// fails a check stops the run with a plain-English reason, so a broken
// render can never be submitted by accident.
//
// Usage:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, existsSync, mkdirSync, readFileSync, statSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const SIZE_LIMIT = 1024 * 1024; // 1 MiB, per RULES.txt
const SIDE_LIMIT = 1024; // at most 1024 by 1024 pixels

const PNG_SIGNATURE = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);

function reject(reason: string): never {
  throw new Error(`entry.png is not shippable: ${reason}`);
}

interface PngGeometry {
  width: number;
  height: number;
}

function readGeometry(buf: Buffer): PngGeometry {
  // A PNG opens with its 8-byte signature, then the IHDR chunk, whose
  // first eight payload bytes are the width and height (big-endian).
  if (buf.length < 33) reject(`only ${buf.length} bytes, too short to be a PNG`);
  if (!buf.subarray(0, 8).equals(PNG_SIGNATURE)) reject('first 8 bytes are not the PNG signature');
  if (buf.toString('ascii', 12, 16) !== 'IHDR') reject('first chunk is not IHDR');
  const width = buf.readUInt32BE(16);
  const height = buf.readUInt32BE(20);
  return { width, height };
}

function checkGeometry(g: PngGeometry): void {
  if (g.width < 1 || g.height < 1) reject(`impossible dimensions ${g.width}x${g.height}`);
  if (g.width > SIDE_LIMIT || g.height > SIDE_LIMIT) {
    reject(`dimensions ${g.width}x${g.height} exceed the ${SIDE_LIMIT}x${SIDE_LIMIT} ceiling`);
  }
}

const projectRoot = dirname(fileURLToPath(import.meta.url));
const entryPath = resolve(projectRoot, 'entry.png');
if (!existsSync(entryPath)) reject(`missing file: ${entryPath}`);

const image = readFileSync(entryPath);
if (image.length > SIZE_LIMIT) {
  reject(`${image.length} bytes exceeds the 1 MiB ceiling`);
}
const geometry = readGeometry(image);
checkGeometry(geometry);

const destination = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(destination, { recursive: true });
const delivered = join(destination, 'entry.png');
copyFileSync(entryPath, delivered);
const deliveredBytes = statSync(delivered).size;
if (deliveredBytes !== image.length) {
  reject(`copy mismatch: wrote ${deliveredBytes} bytes, expected ${image.length}`);
}
console.log(
  `delivered entry.png (${geometry.width}x${geometry.height}, ${deliveredBytes} bytes) -> ${delivered}`,
);
