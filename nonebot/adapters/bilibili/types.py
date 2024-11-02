from typing import NamedTuple

class HeaderTuple(NamedTuple):
    pack_len: int
    raw_header_size: int
    ver: int
    operation: int
    seq_id: int