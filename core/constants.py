
global token_path
token_path = ""


def modify_token_path (base_path:str , controller:str , actual_path:str):
  global token_path
  token_path = f"{base_path}/{controller}/{actual_path}"

  print(f"\n>>>>>>>TOKEN PATH >>>>> {token_path}")
  
  return token_path
  