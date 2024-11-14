"""NHANES Download Module 
"""
import logging 

from pathlib import Path
import csv 
import re 

import requests

logger = logging.getLogger(__name__)
logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s", level=logging.DEBUG)

def read_cycle_data_files(data_file_csv: Path) -> list[dict]:
    """Expects a CSV formatted like the search results 

    Args:
        data_file_csv (Path): _description_

    Returns:
        list[dict]: _description_
    """
    with open(data_file_csv, "r") as f:
        reader = csv.DictReader(f)
        return list(reader)
    
def filename_from_long_name(long_name: str, release_cycle_code: str) -> str:
    """Extracts "DEMO_J" from "Demographic Variables and Sample Weights (DEMO_J)"
    """
    regex_pattern = f"\((\w+_{release_cycle_code})\)" # ("XYZ_{cycle_code}")
    res = re.findall(regex_pattern, long_name)
    if len(res) == 1:
        return res[0]
    else:
        exit(1)


def data_file_name_to_download_url(
        data_files: list, 
        release_cycle_years: str, release_cycle_code: str, 
        base_url: str = "https://wwwn.cdc.gov/Nchs/Nhanes/"
) -> list[dict]:
    """Converts the CSV list of data files to a list of URLs for download

    Args:
        data_files (list): _description_
        release_cycle_years (str): _description_
        release_cycle_code (str): _description_
        base_url (_type_, optional): _description_. Defaults to "https://wwwn.cdc.gov/Nchs/Nhanes/".

    Returns:
        _type_: _description_
    """

    file_urls = []

    for file in data_files:
        filename = filename_from_long_name(
            long_name=file["data_file_name"], release_cycle_code=release_cycle_code
        )

        file_urls.append(
            {
                "filename": filename,
                "url": f"{base_url}/{release_cycle_years}/{filename}.xpt"
            }
        )

    return file_urls     

def download_file(file_url: str, filename: str, output_dir: Path) -> None:
    """Use requests to get the data and save it to a output folder
    """

    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir.joinpath(f"{filename}.xpt")

    logging.info(f"Beginning to download: {file_url}")
    response = requests.get(file_url, stream=True)
    if response.status_code == 200:
        with open(output_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        logging.debug("Success.")
    else:
        logging.error(f"Failed to download {file_url}. Status code: {response.status_code}")


def main(data_file_csv: Path, release_cycle_years: str, release_cycle_code: str, output_dir: Path):

    data_files = read_cycle_data_files(data_file_csv=data_file_csv)

    files_to_download = data_file_name_to_download_url(
        data_files=data_files, release_cycle_code=release_cycle_code, release_cycle_years=release_cycle_years
    )

    for f in files_to_download:
        download_file(file_url=f["url"], filename=f["filename"], output_dir=output_dir)

if __name__ == "__main__":
    # TODO support user input 
    data_file_csv = Path("data_file_lists").joinpath("cycle_2017-2018.csv")
    release_cycle_years="2017-2018"
    release_cycle_code="J"
    output_dir = Path(f"output_data/nhanes_{release_cycle_years}")
    
    main(
        data_file_csv=data_file_csv,
        release_cycle_years=release_cycle_years,
        release_cycle_code=release_cycle_code,
        output_dir=output_dir
    )