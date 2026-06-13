input_tuple = (2, 3, 4)
value_to_insert = 1

def insert_value_front(input_tuple, value_to_insert):
    # TODO
    # newTuple = (value_to_insert,)
    # output = (newTuple + input_tuple)
    # return output
    return (value_to_insert,) + input_tuple


output_tuple = insert_value_front(input_tuple, value_to_insert)
print(output_tuple)
