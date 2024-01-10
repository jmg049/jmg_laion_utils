from argparse import ArgumentParser
import os
from tqdm import tqdm
import pandas as pd
from pathlib import Path
from dataclasses import dataclass
from random import Random
import json

from rich import print as rprint
from rich.markdown import Markdown


@dataclass
class Entry:
    _id: str
    text: str
    image_path: str

    def __dict__(self):
        return {"_id": self._id, "text": self.text, "image_path": self.image_path}

    def __str__(self):
        return f"Entry(_id={self._id}, text={self.text}, image_path={self.image_path})"


def get_random_entries(root_dir: str, n_entries: int) -> list[str]:
    files = []
    for f in tqdm(os.scandir(root_dir), desc="Scanning files"):
        if f.name.endswith(".json"):
            files.append(os.path.join(root_dir, f))
    random_files = rand.sample(files, k=n_entries)
    return random_files


def create_entries(random_files: list[str]) -> list[Entry]:
    entries = []

    for file in tqdm(random_files, desc="Reading files"):
        with open(file, "r") as f:
            data = json.load(f)
            _id = data["key"]
            text = data["caption"]
            image_path = Path(file).with_suffix(".jpg")
            entries.append(Entry(_id, text, image_path))

    return entries


def to_csv(entries: list[Entry], out_file: str) -> pd.DataFrame:
    df = pd.DataFrame.from_records([e.__dict__() for e in entries])
    df.to_csv(out_file, index=False)
    return df


if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument(
        "--laion_dir", type=str, help="Path to directory containing laion json files"
    )
    parser.add_argument("--n_entries", type=int, help="Number of entries to take")
    parser.add_argument("--out_file", type=str, help="Path to output csv file")
    parser.add_argument("--seed", type=int, help="Random seed", default=42)

    args = parser.parse_args()

    laion_dir = args.laion_dir
    n_entries = args.n_entries
    out_file = args.out_file
    seed = args.seed

    rprint(f"Root dir: [yellow bold]{laion_dir}[/yellow bold]")
    rprint(f"Output file: [yellow bold]{out_file}[/yellow bold]")
    rprint(f"Taking [yellow bold]{n_entries}[/yellow bold] random files")
    rprint(f"Random seed: [yellow bold]{seed}[/yellow bold]")

    os.makedirs(os.path.dirname(out_file), exist_ok=True)

    rand = Random(seed)

    random_files = get_random_entries(laion_dir, n_entries)
    entries = create_entries(random_files)
    df = to_csv(entries, out_file)
    df_markdown = Markdown(df.head(10).to_markdown())
    rprint(df_markdown)
    rprint("[green bold]Done![/green bold]")
