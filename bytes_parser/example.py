
import random

from pandas import DataFrame
from bytes_parser.formatter import frame_field_formatter
from bytes_parser.frame_struct import Frame, Row


def bit_fields( val: bytes, str_format: str, labels: list[str],
               *args, **kwargs) -> list[tuple[str, str]]:
    return [(label, f"{((int.from_bytes(val) & (0x01 << i)) >> i):{str_format}}")
            for i, label in enumerate(labels)]


my_frame: Frame = Frame('my_frame_1', [
    Row('FIELD_1', 1, ['X']),
    Row('FIELD_2', 2, ['b']),
    Row('FIELD_3', 2, ['b']),
    Row('FIELD_4', 2),
    Row('FIELD_5', 4),
    Row('FIELD_6', 4),
    Row("BITFIELD", 2, ['d', [*[f"BIT{i}" for i in range(16)]]], bit_fields),
    Row('CRC8', 1, ['X']),
], 'little')


my_frame2: Frame = Frame('my_frame_2', [
    Row('FIELD_1', 1, ['X']),
    Row('FIELD_2', 2, ['b']),
    Row('FIELD_3', 2, ['b']),
    Row('FIELD_4', 2),
    Row('FIELD_5', 4),
    Row('CRC8', 1, ['X']),
], 'little')


unknown_frame: Frame = Frame('UndefinedFrame', [
    Row('UndefinedData', 0, ['X'])
], 'little')


raw_data: bytes = random.randbytes(18)
raw_data2: bytes = random.randbytes(12)


def parse(data: bytes) -> DataFrame:
    if len(data) == 18:
        return frame_field_formatter(my_frame, data)
    elif len(data) == 12:
        return frame_field_formatter(my_frame2, data)
    else:
        return frame_field_formatter(unknown_frame, data)

print('raw_data=', raw_data.hex(' ').upper())
print('raw_data2=', raw_data2.hex(' ').upper())
print(parse(raw_data))
print(parse(raw_data2))
print(parse(b'gsdssf'))
