"""Main module."""

from pyftly.renderer import Renderer


def render(app, component_defs=None):

    js_code = Renderer.render_to_js(app, component_defs)

    # Write the JavaScript code to a file
    with open("build/rendered_component.js", "w+") as js_file:
        js_file.write(js_code)

    with open("build/index.html", "w+") as html_file:
        html_file.write(
            f"""
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <script src="rendered_component.js"></script>
    <title>Document</title>
  </head>
  <body>
    <div id="root"></div>
  </body>
</html>
"""
        )
