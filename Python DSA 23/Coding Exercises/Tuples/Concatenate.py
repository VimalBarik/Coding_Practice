input_tuple = ('Hello', 'World', 'from', 'Python')


def concatenate_strings(input_tuple):
    # s = ""
    # for i in input_tuple:
    #     s += " " + i
    # return s.rstrip()
    return " ".join(input_tuple)



output_string = concatenate_strings(input_tuple)
print(output_string)

