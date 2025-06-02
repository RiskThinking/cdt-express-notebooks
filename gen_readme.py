import json
from pathlib import Path
from typing import List


def generate_badge_links(
    filename: str, repo_path="RiskThinking/cdt-express-notebooks/blob/main"
):
    github_url = f"https://github.com/{repo_path}/{filename}"
    colab_url = f"https://colab.research.google.com/github/{repo_path}/{filename}"
    kaggle_url = f"https://kaggle.com/kernels/welcome?src=https://github.com/{repo_path}/{filename}"
    sagemaker_url = (
        f"https://studiolab.sagemaker.aws/import/github/{repo_path}/{filename}"
    )

    badges = [
        f'<a href="{github_url}"><img src="https://img.shields.io/badge/View%20on-GitHub-181717?logo=github&style=for-the-badge" height="20" alt="View on GitHub"></a>',
        f'<a href="{colab_url}"><img src="https://colab.research.google.com/assets/colab-badge.svg" height="20" alt="Open In Colab"></a>',
        f'<a href="{kaggle_url}"><img src="https://kaggle.com/static/images/open-in-kaggle.svg" height="20" alt="Open in Kaggle"></a>',
        f'<a href="{sagemaker_url}"><img src="https://img.shields.io/badge/Open%20in-SageMaker-orange?style=for-the-badge" height="20" alt="Open in SageMaker"></a>',
    ]

    return " ".join(badges)


def generate_table_format(notebooks: List[dict]):
    table = "| # | Title | Description | # of API Calls |\n"
    table += "|---|-------|-------------|----------------|\n"

    for notebook in notebooks:
        title = f"**{notebook['title']}**"
        badges = generate_badge_links(notebook["filename"])
        table += f"| {notebook['id']} | {title} | {notebook['description']}<br />{badges} | {notebook['num_api_calls']} |\n"

    return table


def generate_section_format(notebooks: List[dict]):
    sections = []

    for notebook in notebooks:
        section = f"## {notebook['id']}. **{notebook['title']}**\n"
        section += generate_badge_links(notebook["filename"]) + "\n\n"
        section += notebook["description"] + "\n"
        sections.append(section)

    return "\n".join(sections)


def main():
    script_dir = Path(__file__).resolve().parent
    with open(script_dir / "notebooks.json", "r") as f:
        data = json.load(f)

    repo = data["repository"]
    notebooks = data["notebooks"]
    readme_content = f"# {repo['name']}\n\n{repo['description']}\n\n"
    readme_content += generate_table_format(notebooks)
    readme_content += f"\n\n{"\n".join(repo['notes'])}"

    with open(script_dir / "README.md", "w") as f:
        f.write(readme_content)

    print("README.md generated successfully!")
    print(f"Generated from {len(notebooks)} notebooks")


if __name__ == "__main__":
    main()
