
def uci_to_num(move="a7a6"): #,    a7a6  d7d6  b8c6  b7b6  a2c3  b8c8 
   
    start_position = move[0:2] # b8
    end_position = move[2:4] # c6

    row = start_position[0]
    col = start_position[1]
    row1 = end_position[0]
    col1 = end_position[1]
    #print(row+col+' '+row1+col1)
        
    '''#create a dictionary'''
    start_position = {"a": 0, "b": 1, "c": 2, "d": 3,
                        "e": 4, "f": 5, "g": 6, "h": 7}
    
    r1 = start_position[row]
    r2 = start_position[row1]

    start_position = {"1": 7, "2": 6, "3": 5, "4": 4,
                        "5": 3, "6": 2, "7": 1, "8": 0}
       
    c1 = start_position[col]
    c2 = start_position[col1]

    start_position_tuple = (c1,r1)
    end_position_tuple = (c2,r2)

    #return tuple
    #print(start_position_tuple,end_position_tuple)
    return start_position_tuple,end_position_tuple
 
 # do the opposite of above
 
def num_to_uci(start_pos, end_pos):
    #start_position = (6, 6)  #sample positions for testing purpose (1,6) (1, 5)
    #end_position = (5, 6)   # same as above (2, 6) (2, 5) 
    row1 = start_pos[0]
    col1 = start_pos[1]
    row2 = end_pos[0]
    col2 = end_pos[1]
    print(row1, col1)
    print(row2, col2)

    '''#create a dictionary'''
    
    start_position = {0: "a", 1: "b", 2: "c", 3: "d",
                      4: "e", 5: "f", 6: "g", 7: "h"}

    r1 = start_position[col1]
    r2 = start_position[col2]

    end_position = {7: 1, 6: 2, 5: 3, 4: 4,
                3: 5, 2: 6, 1: 7, 0: 8}

    c1 = end_position[row1]
    c2 = end_position[row2]

    print(r1+str(c1))
    print(r2+str(c2))
    return r1+str(c1),r2+str(c2)


if __name__ == "__main__":
    model_move()