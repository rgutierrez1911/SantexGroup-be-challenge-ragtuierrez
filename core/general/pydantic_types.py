from uuid import uuid1
FLOAT_TYPE = (float,)

class Money(float):
  
  @classmethod
  def __get_validators__(cls):
    # one or more validators may be yielded which will be called in the
    # order to validate the input, each validator will receive as an input
    # the value returned from the previous validator
    yield cls.validate
      
  @classmethod
  def validate(cls, v:float):
    if not  isinstance(v, (int , float)):
      raise Exception("The field should be a float type")
    rounded_money = round(v,2)
    return cls(rounded_money)


def generate_rounded(
  decimal_point: int = 2,
  class_name: str = None,
  base_type = FLOAT_TYPE
  
):

  new_class_name = class_name if class_name else f"generated_rounded_{str(uuid1())}"
  @classmethod
  def get_validators(cls):
    yield cls.validate
  @classmethod
  def validate(cls, v: float):
    if not isinstance(v, (int, float)):
      raise Exception("The field should be a float type")
    rounded = round(v, decimal_point)
    return cls(rounded)



  decimal_specific_new_class = type(
    new_class_name,
    base_type,
    {
      "__get_validators__": get_validators,
      "validate": validate,
    }
  )

  return decimal_specific_new_class


GeneratedMoney = generate_rounded(decimal_point=2, class_name="GeneratedMoney")
