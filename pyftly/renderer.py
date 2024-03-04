# class Renderer:
#     @staticmethod
#     def render_to_js(component):
#         js_code = f"""
#         document.addEventListener("DOMContentLoaded", function() {{
#             var root = document.getElementById('root');
#             var element = document.createElement('div');
#             element.innerHTML = `{component.render()}`;
#             root.appendChild(element);
#         }});
#         """
#         return js_code

import re
import jsmin

class Renderer:

    @staticmethod
    def render_inner(app_code, component_defs):
        js_code = ""
        elements = re.findall(r"<[^>]+>|[^<]+", app_code)
        # Iterate over each element in the app code
        for element in elements:
            if element.strip() == "" or element.strip()=="\n": continue
            # If the element is a tag
            if element.startswith("<"):
                # If element is a user-defined component
                if element.startswith("<") and not element.startswith("</"):
                    # Extract the component name from the tag
                    component_name = re.match(r"<(\w+)", element).group(1)
                    if component_name in component_defs: # if user defined component, not html tag
                        # Extract the props from the tag, e.g. title="Title" content="Content"
                        props = re.findall(r"(\w+)=\"(.*?)\"", element)

                        # Create a new instance of the component
                        component = component_defs[component_name](dict(props))
                        # Render the component to JavaScript code
                        component_js_code = Renderer.render_inner(component.render(), component_defs)
                        # Append the JavaScript code to the main code
                        js_code += component_js_code
                    else: # if html tag, not user defined component
                        # Append the tag to the main code
                        js_code += element
                else: # if closing tag

                    # Extract the component name from the closing tag
                    component_name = re.match(r"</(\w+)", element).group(1)

                    if component_name not in component_defs:
                        js_code += element

            else: # If the element is text
                # Append the text to the main code
                js_code += element

        return js_code

    @staticmethod
    def render_to_js(app, component_defs):
        app_code = app.render()

        js_code = Renderer.render_inner(app_code, component_defs)




        # Wrap the JavaScript code in a function
        js_code = f"""
        document.addEventListener("DOMContentLoaded", function() {{
            var root = document.getElementById('root');
            root.innerHTML = ` {js_code} `;
        }});
        """

        return jsmin.jsmin(js_code)

