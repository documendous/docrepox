#!/usr/bin/env python
# type: ignore

import markdown

try:
    from chart import ddocs
except ModuleNotFoundError:
    from apps.ddocs.utils.chart import ddocs

markdown_dir = ddocs.chart["markdown_dir"]
templates_dir = ddocs.chart["templates_dir"]
items = ddocs.chart["items"]


def escape_django_tags(html):
    # Replace Django template tags with HTML-safe versions
    html = html.replace("{%", "&#123;%").replace("%}", "%&#125;")
    html = html.replace("{{", "&#123;&#123;").replace("}}", "&#125;&#125;")
    return html


def run():
    """
    Generates html from markdown
    """
    with open(ddocs.chart["styles_file"], "r") as f:
        styles_html = f.read()

    for each in items:
        markdown_file = each["markdown"]
        template_file = each["template"]
        markdown_file = f"{markdown_dir}/{markdown_file}"
        template_file = f"{templates_dir}/{template_file}"

        print(f"Reading from: {markdown_file}")
        with open(markdown_file, "r", encoding='utf-8') as f:
            text = f.read()
            html = styles_html
            html += markdown.markdown(
                text, extensions=["fenced_code"], output_format="html5"
            )

        # Escape Django tags to prevent interpretation
        html = escape_django_tags(html)

        print(f"Writing to {template_file}")
        with open(template_file, "w", encoding='utf-8') as f:
            f.write(html)


if __name__ == "__main__":
    run()
