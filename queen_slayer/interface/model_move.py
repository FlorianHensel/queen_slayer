
#def model_move(moveNeal="b8 c6"):
moveNeal = "b8 c6"
    #need to split the string
   # move
   
start_position = moveNeal[0:2] # b8
end_position = moveNeal[3:5] # c6
#print(start_position)
#print(end_position)

#tart_position = "b8"
#end_position = "c6"
row = start_position[0]
col = start_position[1]
row1 = end_position[0]
col1 = end_position[1]
print(row+col+' '+row1+col1)


#first_row_element = start_position[0] # b
#second_col_element = start_position[1] # 8
    
'''#create a dictionary'''
start_position = {"a": 0, "b": 1, "c": 2, "d": 3,
                     "e": 4, "f": 5, "g": 6, "h": 7}
r1 = start_position[row]
r2 = start_position[row1]
#row_element = {v: k for k, v in start_position.items()}

start_position = {"1": 7, "2": 6, "3": 5, "4": 4,
                    "5": 3, "6": 2, "7": 1, "8": 0}
c1 = start_position[col]
c2 = start_position[col1]

start_position_tuple = (c1,r1)
end_position_tuple = (c2,r2)

#col_element = {v: k for k, v in start_position[1].items()}



#return tuple
#tart_position = 1st part of the string
#end_position = 2nd part of the string

#print(r1,c1,r2,c2)
print(start_position_tuple,end_position_tuple)

#return r1c1, r2c2

    