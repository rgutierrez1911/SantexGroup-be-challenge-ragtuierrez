
def row_to_dict(row: object):
  return {x.name: getattr(row, x.name) for x in row.__table__.columns}


def list_alchemy_to_list_dict(rows: list):
  rows_dict = []
  for row in rows:
    rows_dict.append(row_to_dict(row=row))
  return rows_dict
