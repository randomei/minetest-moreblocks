import argparse
import json
import multiprocessing
import pathlib

import progressbar

import pymtdb


def create_filter(stairsplus_dump: pathlib.Path):
    f = {}
    with stairsplus_dump.open() as fh:
        data = json.load(fh)

    for shaped_node in data['shaped_nodes'].keys():
        f[shaped_node.encode()] = shaped_node.encode()

    for alias, shaped_node in data['aliases'].items():
        f[alias.encode()] = shaped_node.encode()

    return f


def process(row):
    data = row[0]
    mapblock = pymtdb.MapBlockSimple.import_from_serialized(data)
    return frozenset(mapblock.iter_nodes())


def main(args):
    all_nodes = set()
    if args.pg_connection:
        import psycopg2
        conn = psycopg2.connect(args.pg_connection)
        cur = conn.cursor()

    else:
        import sqlite3
        con = sqlite3.connect(args.sqlite_file, check_same_thread=False)
        cur = con.cursor()

    cur.execute('SELECT COUNT(*) FROM blocks')
    num_blocks = cur.fetchone()[0]

    cur.execute('SELECT data FROM blocks')

    with progressbar.ProgressBar() as bar, multiprocessing.Pool() as pool:
        for nodes in bar(pool.imap_unordered(process, cur, chunksize=10),
                         max_value=num_blocks):
            all_nodes.update(nodes)

    whitelist = set()
    f = create_filter(args.stairsplus_dump)
    for node in all_nodes:
        shaped_node = f.get(node)
        if shaped_node:
            whitelist.add(shaped_node)

    if args.output:
        output = args.output
    else:
        output = args.stairsplus_dump.parent / 'stairsplus.whitelist'

    with output.open('wb') as fh:
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
    p.add_argument('--output', '-o', type=pathlib.Path)
    p.add_argument('stairsplus_dump', type=existing_file)
    return p.parse_args(args=args, namespace=namespace)


if __name__ == "__main__":
    main(parse_args())
