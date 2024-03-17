
import click
import json
import zipfile
from pathlib import Path

def convert_to_md(content: dict, depth: int, max_depth: int = 3) -> str:
    """
    Converts the XMind content to Markdown format.

    Args:
        content (dict): The XMind content to convert.
        depth (int): The current depth of the content.
        max_depth (int, optional): The maximum depth of the markdown file. Defaults to 3.

    Returns:
        str: The converted Markdown content.
    """
    md = ""
    md += (('#'*depth + ' ') if (depth<=max_depth) else ("\t"*(depth-max_depth-1)+'+ ')) + content["title"] + "\n"
    if "children" in content:
        for child in content["children"]:
            md += convert_to_md(child, depth+1, max_depth)
    return md

def filter_data(data: dict) -> dict:
    """
    Filters the XMind data to remove unnecessary information.

    Args:
        data (dict): The XMind data to filter.

    Returns:
        dict: The filtered XMind data.
    """
    filtered_data = {"title": data["title"].replace("\n", " ")}
    if "children" in data:
        filtered_data["children"] = [filter_data(x) for x in data["children"]["attached"] if "title" in x]
    return filtered_data

def read_zip_file(filepath: str) -> dict:
    """
    Reads the content.json file from a .xmind archive, which is a zip file.

    Args:
        filepath (str): The path to the zip file.

    Returns:
        dict: The content of the content.json file.
    Raises:
        FileNotFoundError: If the content.json file does not exist in the zip file.
    """
    data = {}
    with zipfile.ZipFile(filepath, 'r') as zip_ref:
        if 'content.json' in zip_ref.namelist():
            with zip_ref.open('content.json') as f:
                data = json.load(f)
        else:
            raise FileNotFoundError("content.json does not exist in the zip file")
    return data

@click.command()
@click.option('--d', default=3, help='Max depth of the markdown file')
@click.argument('fn', type=click.Path(exists=True, dir_okay=False))
def main(fn: str, d: int) -> None:
    """
    Converts an XMind file to Markdown format.

    Args: \n
        fn (str): The path to the XMind file.  \n
        d (int): The maximum subtitles depth of the markdown file.
    """
    filepath = Path(fn)
    data = read_zip_file(filepath)
    md_final = convert_to_md(filter_data(data[0]['rootTopic']), 1, d)
    output_file = filepath.with_suffix('.md')
    with output_file.open("w") as f:
        f.write(md_final)
