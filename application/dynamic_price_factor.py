def calculate_percentile(data, num):
    rank=data.index(num)+1
    result=(rank/len(data) )
    if result>0.2:
        return round(result,2)
    else:
        return -round(result,2)
# print(f"The {number_to_check}th percentile in the list is: {result_percentile}")