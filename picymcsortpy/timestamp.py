from datetime import datetime
from picymcsortpy.exif_tool import ExifTool


def get_timestamp(file):

    with ExifTool() as etool:
        metadata = etool.get_metadata(file.as_posix())[0]

    timestamp = _get_timestamp_str(metadata)

    if timestamp is None or timestamp[:4] == '0000':
        return None

    timestamp = datetime.strptime(timestamp, '%Y:%m:%d %H:%M:%S')

    if timestamp.year == 0000:
        return None

    return timestamp


def _get_timestamp_str(metadata):
    requested_keys = ('EXIF:DateTimeOriginal',
                     'EXIF:CreateDate',
                     'QuickTime:CreateDate',
                     'QuickTime:TrackCreateDate',
                     'QuickTime:MediaCreateDate',
                     'XMP:DateCreated')

    for key in requested_keys:
        if key in metadata:
            return metadata[key]
    return None


# def _get_file_change_date(metadata):
#     if "File:FileInodeChangeDate" in metadata:
#         # File:FileInodeChangeDate: 2018:10:23 15:15:59+02:00
#         timestamp_parts = metadata["File:FileInodeChangeDate"].split('+')
#         timestamp = datetime.strptime(timestamp_parts[0], '%Y:%m:%d %H:%M:%S')
#         extra_time = datetime.strptime(timestamp_parts[1], '%H:%M')
#         timestamp = timestamp + timedelta(extra_time.hour) + timedelta(extra_time.minute)
#         return timestamp
#     else:
#         return None
