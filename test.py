# CSCE4310 Intro to AI
# Homework 3 - Update actions()
# Spring 2018

#     Name: Michael Bido-Chavez
#       ID: 10969213
#    email: michaebido-chavez@my.unt.edu

#  Partner: Zhachory Volker
#    email: ZhachoryVolker@my.unt.edu
#    email: zhach@google.com

#    Notes:
#       - tested with python3
#       - updated file name in main to match folder's test file
#       - two functions were created as helpers for actions
#       - from itertools import combinations, optimization
#       - final output from testing this was 2 consistently

import ast
from itertools import combinations

# in the case that the domino has equal number of pips on each side
def double_moves(table, my_dom):
    # all actions to be returned
    actions = []
    # potentially valid moves
    possibles = []
    # combinations generated
    combos = []
    # if a dominio on the table is a double, append to possibles
    for t in table:
        if t[0] == t[1]:
            possibles.append(t)
    # for all combinations of possible peices that are doubles
    for x in range(1, len(possibles) + 1):
        for combo in combinations(possibles, x):
            action = [my_dom]
            action.extend(combo)
            # if the move is valid, then append to all actions
            if sum([num[0] for num in action]) % 5 == 0:
                actions.append(action)
    return actions
            
# in the case that a normal move (where one side matches) is being played
# idx is the side of the domino being tested
#   e.g. my_dom = (3,4), idx = 0 would test table for matching my_dom[0]
def normal_moves(table, my_dom, idx):
    # all actions to be returned
    actions = []
    # potentially valid moves
    possibles = []
    # combinations generated
    combos = []
    # if one side of dom on table matches the played[index] piece, append
    for t in table:
        if my_dom[idx] == t[0] or my_dom[idx] == t[1]:
            possibles.append(t)
    # for all combinations of possible peices that match
    for x in range(1, len(possibles) + 1):
        for combo in combinations(possibles, x):
            action = [my_dom]
            action.extend(combo)
            if sum([r if r != my_dom[idx] else l for l, r in action]) % 5 == 0:
                actions.append(action)
    return actions

def actions(table, hand):
    '''
    :param table - the cards on the table:
    :param hand - the cards on the player's hand:
    :return: list of all possible actions given the Game table and the player's hand
    '''
    finalList = [] 
    # for each domino in hand
    for my_domino in hand:
        # append discard play
        finalList.append([my_domino])
        # if a double, call helper functions and add to move list, else play normal
        if my_domino[0] == my_domino[1]:
            double_moves_list = double_moves(table, my_domino)
            single_moves_list = normal_moves(table, my_domino, 0)
            finalList.extend(double_moves_list)
            finalList.extend(single_moves_list)
        else:
            first_moves_list = normal_moves(table, my_domino, 0)
            second_moves_list = normal_moves(table, my_domino, 1)
            finalList.extend(first_moves_list)
            finalList.extend(second_moves_list)
    # print("playing a hand")
    # print(hand)
    # print(finalList)
    return finalList


def sortLists(listOfLegalAction):
    finallist = []
    for legalAction in listOfLegalAction:
        temp = []
        for domino in legalAction:
            temp = temp + [sorted(domino)]
        finallist = finallist + [sorted([tuple(x) for x in temp])]

    return sorted(finallist)


def testLegalActionGeneration(table, hand, testcase):
    legalActions = actions(table,hand) # generating all the legal actions given the table and the hand
    legalActions = sortLists(legalActions) # sorting the list of legal actions
    testcase = sortLists(testcase) # sorting the list of legal actions in the test case

    if legalActions == testcase:
        return True

    return False


if __name__ == "__main__":

    ### Leave this file in the folder where you run the code from or modify the path accordingly
    F = open("studentTestCases_legalActions.txt","r")
    
    correct =0
    for line in F:
        split = line.split("##")
        split[0] = ast.literal_eval(split[0])
        split[1] = ast.literal_eval(split[1])
        split[2] = ast.literal_eval(split[2])
        if testLegalActionGeneration(split[0],split[1],split[2]):
            correct += 1
        else:
            print("This test case failed: "+ line)

    print("FinalScore: "+ str(correct))
