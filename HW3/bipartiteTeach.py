import pandas as pd
import json
from dotMake import DotMake as dm 


comboCount = dict()
instructorTotal = dict()
instructorPercent = dict()
instructorNode = dict()
courseNode = dict()
graph = dm()


for i in range(6,8):
    curFile = f"./dataset/courses{str(i)}.json"
    tmp = open(curFile)
    tmpCourse = json.load(tmp)
    counter= 0
    for department in tmpCourse:
        if department['code'] == "CSCI":
            for course in department['courses']:
                title = course['title']
                if title == "Master's Project" or title == "Master's Thesis" or title == "Dissertation" or title == "Masters Thesis":
                    continue
                for section in course['sections']:
                    for timeslot in section['timeslots']:
                        instructor = timeslot['instructor']
                        if instructor == "TBA":
                            continue
                        group = instructor.split(', ')
                        for ind in group:
                            if ind in instructorNode:
                                continue
                            #if counter %2 ==0:
                            instructorNode[ind] = graph.addNode(val = ind, clusterName="Professor")
                            # else:
                            #     instructorNode[ind] = graph.addNode(val = ind, clusterName="ProfessorPt2")
                            # counter+=1
                    


for i in range(0, 8):
    curFile = f"./dataset/courses{str(i)}.json"
    tmp = open(curFile)
    tmpCourse = json.load(tmp)

    for department in tmpCourse:
        if department['code'] == "CSCI":
            for course in department['courses']:
                title = course['title']
                if title == "Master's Project" or title == "Master's Thesis" or title == "Dissertation" or title == "Masters Thesis":
                    continue
                for section in course['sections']:
                    if section['act'] < 20:
                        continue
                    for timeslot in section['timeslots']:
                        instructor = timeslot['instructor']
                        group = instructor.split(', ')
                        for ind in group:

                            if ind not in instructorNode:
                                continue
                            combo = tuple([ind,title])
                            comboCount[combo] = comboCount.get(combo, 0) + 1


for i in range(16, 28):
    curFile = f"./dataset/courses({str(i)}).json"
    tmp = open(curFile)
    tmpCourse = json.load(tmp)

    for department in tmpCourse:
        if department['code'] == "CSCI":
            for course in department['courses']:
                title = course['title']
                if title == "Master's Project" or title == "Master's Thesis" or title == "Dissertation" or title == "Masters Thesis":
                    continue
                for section in course['sections']:
                    for timeslot in section['timeslots']:
                        instructor = timeslot['instructor']
                        group = instructor.split(', ')
                        for ind in group:

                            if ind not in instructorNode:
                                continue
                            combo = tuple([ind,title])
                            comboCount[combo] = comboCount.get(combo, 0) + 1




for (instructor, _), count in comboCount.items():
    instructorTotal[instructor] = instructorTotal.get(instructor, 0) + count


for combo, count in comboCount.items():
    instructorPercent[combo] = count / instructorTotal[combo[0]]

for combo, percent in instructorPercent.items():
    if percent < .1:
        continue
    instructor = combo[0]
    course = combo[1]
    if instructor == "TBA":
        continue
    if course not in courseNode:
        courseNode[course] = graph.addNode(val = course, clusterName="Course", shape='polygon')
    tempPct = 10 * percent
    graph.addEdge(start = instructorNode[instructor], end = courseNode[course], weight = tempPct)


print(graph)





