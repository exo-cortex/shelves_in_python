
def union(_ranges):
	output = []
	for start, end in sorted(_ranges):
		if output and output[-1][1] >= start - 1:
			output[-1][1] = max(output[-1][1], end)
		else:
			output.append([start, end])
	return output

# def fit_to_size(_list, _th, _totalSize):
#     if sum(_list) + (len(_list) + 2) * _th > _totalSize:
#         print("the sum of all board sizes plus thickness of boards in between is larger than the allowed size!")
#         return _list
#     new_list = _list
#     new_list += [_totalSize - sum(new_list) - (2 + len(new_list)) * _th] # fill up to _totalSize
#     return new_list

def fit_to_size(_list, _th, _totalSize):
	if sum(_list) + (2 + len(_list)) * _th > _totalSize:
		print(sum(_list) + (2 + len(_list)) * _th)
		print("the sum of all board sizes plus thickness of boards in between is larger than the allowed size!")
		return []
	return [_totalSize - sum(_list) - (2 + len(_list)) * _th] # fill up to _totalSize
