from jinja2 import Environment,FileSystemLoader



def render_html(template_file: str, args: dict , template_folder :str) -> str:
  
  file_loader = FileSystemLoader(searchpath= template_folder)
  
  enviroment = Environment(loader=file_loader)
  template = enviroment.get_template(template_file)

  
  return template.render(**args)
