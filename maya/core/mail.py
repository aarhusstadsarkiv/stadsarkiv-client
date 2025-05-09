from maya.core.templates import templates
from maya.core.logging import get_log


log = get_log()


async def get_template_content(template_path: str, context_values: dict) -> str:
    """
    Get template content from a jinja2 template and a dict of context values
    """

    # Get the template as string
    template = templates.get_template(template_path)
    html_content = template.render(context_values)

    return html_content
