import argparse
import json
import multiprocessing
import pathlib
import time

import progressbar

import pymtdb


def create_filter(stairsplus_dump: pathlib.Path):
    print('creating filter from dump...')
    f = {}
    with stairsplus_dump.open() as fh:
        data = json.load(fh)

    for shaped_node in data['shaped_nodes'].keys():
        f[shaped_node.encode()] = shaped_node.encode()

    for alias, shaped_node in data['aliases'].items():
        f[alias.encode()] = shaped_node.encode()

    return f


def count_blocks(args):
    if args.pg_connection:
        import psycopg2
        conn = psycopg2.connect(args.pg_connection)
        cur = conn.cursor()

    else:
        import sqlite3
        con = sqlite3.connect(args.sqlite_file)
        cur = con.cursor()

    print('counting blocks...')
    start = time.time()
    cur.execute('SELECT COUNT(*) FROM blocks')
    num_blocks = cur.fetchone()[0]
    print(f'num_blocks: {num_blocks} (fetched in {time.time()-start}s)')
    return num_blocks


def initializer(args):
    global CURSOR, CHUNK_SIZE
    CHUNK_SIZE = args.chunk_size
    if args.pg_connection:
        import psycopg2
        conn = psycopg2.connect(args.pg_connection)
        CURSOR = conn.cursor()

    else:
        import sqlite3
        con = sqlite3.connect(args.sqlite_file)
        CURSOR = con.cursor()


def process(offset):
    global CURSOR, CHUNK_SIZE
    CURSOR.execute(f'SELECT data FROM blocks LIMIT {CHUNK_SIZE} OFFSET {offset}')
    return frozenset(
        node
        for row in CURSOR
        for node in pymtdb.MapBlockSimple.import_from_serialized(row[0]).node_names
    )


def create_whitelist(filter_, all_nodes):
    print('creating whitelist')
    return set(
        shaped_node for shaped_node in map(filter_.get, all_nodes) if shaped_node
    )


def main(args):
    filter_ = create_filter(args.stairsplus_dump)
    num_blocks = count_blocks(args)
    offsets = range(0, num_blocks, args.chunk_size)

    all_nodes = set()
    with progressbar.ProgressBar() as bar, multiprocessing.Pool(
        processes=args.workers, initializer=initializer, initargs=(args,)
    ) as pool:
        for nodes in bar(pool.imap_unordered(process, offsets),
                         max_value=len(offsets)):
            all_nodes.update(nodes)

    whitelist = create_whitelist(filter_, all_nodes)

    if args.output:
        output = args.output
    else:
        output = args.stairsplus_dump.parent / 'stairsplus.whitelist'

    with output.open('wb') as fh:
        print(f'writing whitelist to {output!r}')
        fh.write(b'\n'.join(sorted(whitelist)))


def existing_file(path: str) -> pathlib.Path:
    file_path = pathlib.Path(path)
    if not file_path.exists():
        raise argparse.ArgumentTypeError(f'{path!r} does not exist.')
    if not file_path.is_file():
        raise argparse.ArgumentTypeError(f'{path!r} is not a file.')
    return file_path


def parse_args(args=None, namespace=None):
    p = argparse.ArgumentParser()
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument('--pg_connection', '-c')
    g.add_argument('--sqlite_file', '-s', type=existing_file)
    p.add_argument('--chunk_size', type=int, default=64)
    p.add_argument('--workers', type=int)
    p.add_argument('--output', '-o', type=pathlib.Path)
    p.add_argument('stairsplus_dump', type=existing_file)
    return p.parse_args(args=args, namespace=namespace)


if __name__ == "__main__":
    main(parse_args())
