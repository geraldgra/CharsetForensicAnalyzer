BLOCK_SIZE = 64 * 1024


def read_blocks(path):

    with open(path, "rb") as f:

        offset = 0

        while True:

            block = f.read(BLOCK_SIZE)

            if not block:
                break

            yield block, offset

            offset += len(block)