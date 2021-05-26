import pathlib
import shutil
import logging

from picymcsortpy.hash import FileHash
from picymcsortpy.timestamp import get_timestamp


def sort_files(source_folder, destination_folder, remove_source_file=True):
    """Main function for sorting files

    """
    source_folder = pathlib.Path(source_folder)
    destination_folder = pathlib.Path(destination_folder).resolve()
    destination_folder.mkdir(parents=True, exist_ok=True)

    fh = FileHash()
    logging.basicConfig(format='%(asctime)s : %(message)s',
                        level=logging.INFO,
                        filename=destination_folder.joinpath("picymcsortpy.log").as_posix()
                        )

    files = _get_all_files(source_folder)

    for file in files:
        file_hash = fh.md5(file)

        timestamp = get_timestamp(file)
        if timestamp is None:
            new_destination = destination_folder / "unsorted"
            new_filename = f"{file_hash}{file.suffix}"
        else:
            # Create new file path
            new_destination = destination_folder.joinpath(timestamp.strftime('%Y'), timestamp.strftime('%m'))
            new_filename = f"{timestamp.strftime('%Y%m%d_%H%M%S')}_{file_hash}{file.suffix}"

        # Create folder
        new_destination.mkdir(parents=True, exist_ok=True)

        # Create new filepath
        new_filepath = new_destination / new_filename

        if new_filepath.exists():
            # This is a duplicate file
            logging.info(f"{file_hash} : duplicate files : {file.as_posix()} : {new_filepath.as_posix()}")
        else:
            # Copy file to new location
            shutil.copy2(file, new_filepath)

            # Verify copy
            if file_hash == fh.md5(new_filepath):
                logging.info(f"{file_hash} : copy ok : {file.as_posix()} -> {new_filepath.as_posix()}")
            else:
                # Remove the copied file if the hashes is not equal
                logging.info(f"{file_hash} : copy failed : removing {new_filepath.as_posix()}")
                new_filepath.unlink(missing_ok=True)

        # Clean-up source file
        if remove_source_file and new_filepath.exists():
            logging.info(f"{file_hash} : cleaning up : removing {file.as_posix()}")
            file.unlink(missing_ok=True)


def _get_all_files(source_folder):
    p = source_folder.glob('**/*')
    files = [x.resolve() for x in p if x.is_file()]
    return files


if __name__ == "__main__":
    sort_files("../tmp/source",
               "../tmp/destination",
               remove_source_file=True)
