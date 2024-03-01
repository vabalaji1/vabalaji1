# %%
import pandas as pd
import json
from dotMake import DotMake as dm 


# %%
# tmp = open('./dataset/requirement.json')
# requirements = json.load(tmp)

# tmp2 = open('./dataset/courses3.json')
# tmpCourse = json.load(tmp2)

# for type in tmpCourse:
#     if type['code'] == "ADMN":
#         for course in type['courses']:
#             print(course['crse'])

# %%
pre0 = open('./dataset/prerequisites0.json')
pre00 = json.load(pre0)
pre1 = open('./dataset/prerequisites1.json')
pre11 = json.load(pre1)

# %%
graph = dm()
coursesTaken = dict()
coursesTaken["CSCI 1100"] = graph.addNode(val="CSCI 1100", shape="record", clusterName="FreshFall")
coursesTaken["MATH 1010"] = graph.addNode(val="MATH 1010", shape="record", clusterName="FreshFall")
coursesTaken["MATH 1020"] = graph.addNode(val="MATH 1020", shape="record", clusterName="FreshSpring")

ff = ["CSCI 1100"]
fs = ["CSCI 1200"]
sf = ["CSCI 2200", "CSCI 2500"]
ss = ["CSCI 2300", "CSCI 2600"]
jf = ["CSCI 4430"]
js = ["CSCI 4210"]

allS = [ff,fs,sf,ss,jf,js]
allSName = ["FreshFall", "FreshSpring", "SophFall", "SophSpring", "JunFall", "JunSpring"]



# %%
def getCoursesForKey(data, key):
    courses = []

    def extractCourses(nestedData):
        if 'type' in nestedData and nestedData['type'] == 'or':
            courses.append(nestedData['nested'][0]['course'])
        elif 'type' in nestedData and nestedData['type'] == 'and':
            for item in nestedData['nested']:
                extractCourses(item)
        elif 'course' in nestedData:
            courses.append(nestedData['course'])

    if key in data and 'prerequisites' in data[key]:
        
        #print("HI")
        prerequisites = data[key]['prerequisites']
        if 'nested' in prerequisites:
            for item in prerequisites['nested']:
                extractCourses(item)
        else:
            extractCourses(prerequisites)
    return courses

# %%
for ii in range(0, 8):
    curFile = f"./dataset/courses{str(ii)}.json"
    preFile = f"./dataset/prerequisites{str(ii)}.json"
    pre0 = open(preFile)
    pre = json.load(pre0)
    tmp = open(curFile)
    tmpCourse = json.load(tmp)
    count = 0
    for type in tmpCourse:
        if type['code'] == "CSCI":
            for course in type['courses']:
                courseSplit = course['id'].split('-')
                courseName = ' '.join(courseSplit)
                if int(courseSplit[1]) > 6000:
                    continue
                if courseName in coursesTaken:
                    continue
                coursesNeeded = []
                crns = set()
                for section in course['sections']:
                    value = None
                    try:
                        value = pre.get(str(section['crn']))
                        #print(value, section['crn'], course['id'], curFile, preFile)
                    except:
                        continue

                    coursesNeeded = getCoursesForKey(pre, str(section['crn']))
                    isValid = True
                    otherReq = []
                    csReq = []
                    for preReq in coursesNeeded:
                        codes = preReq.split(' ')
                        
                        if codes[0] == "CSCI" and preReq not in coursesTaken:
                            isValid = False
                            break
                        elif codes[0] != "CSCI":
                            otherReq.append(preReq)
                        elif codes[0] == "CSCI":
                            csReq.append(preReq)
                    
                    
                    if isValid:
                        firstReq = ''
                        secondReq = ''
                        thirdReq = ''
                        nodeVal = courseName
                        if len(otherReq) > 0:
                            firstReq = otherReq[0]
                            nodeVal = "<f0> " + nodeVal + "| <f1> " + firstReq
                            
                            if len(otherReq) > 1:
                                
                                secondReq = otherReq[1]
                                nodeVal = nodeVal + "| <f2> " + secondReq
                                if len(otherReq) > 2:
                                    thirdReq = otherReq[2]
                                    nodeVal = nodeVal + "| " + thirdReq

                        
                        # if "CSCI 2300" in csReq:
                        #     coursesTaken[courseName] = graph.addNode(val = nodeVal, shape="record", color = "red")
                        # else:
                        #     coursesTaken[courseName] = graph.addNode(val = nodeVal, shape="record")
                        found = False
                        essential = False
                        for i in range(0, len(allS)):
                            if courseName in allS[i]:
                                coursesTaken[courseName] = graph.addNode(val = nodeVal, shape="record", clusterName=  allSName[i])
                                found = True
                                essential = True
                                break
                            
                        courseNameSplit = courseName.split(' ')
                        if found  == False and int(courseNameSplit[1]) >= 4000 and section['attribute'] == "Communication Intensive":
                            if ii %2 == 0:

                                coursesTaken[courseName] = graph.addNode(val = nodeVal, shape="record", color = "green", clusterName=  "SenFall")
                            
                            else:
                                coursesTaken[courseName] = graph.addNode(val = nodeVal, shape="record", color = "green", clusterName=  "SenSpring")
                            found = True

                        
                        if found:
                            for curReq in csReq:
                                if essential:
                                    graph.addEdge(start = coursesTaken[curReq], end = coursesTaken[courseName], color='red')
                                else:
                                    graph.addEdge(start = coursesTaken[curReq], end = coursesTaken[courseName])


                    break
                # if count ==20:
                #     # print(courseName)
                #     # print(coursesNeeded)
                #     # print(crns)
                # count +=1
        elif type['code'] == "MATH":
            for course in type['courses']:
                courseSplit = course['id'].split('-')
                courseName = ' '.join(courseSplit)
                if int(courseSplit[1]) > 6000:
                    continue
                if courseName in coursesTaken:
                    continue
                coursesNeeded = []
                crns = set()
                for section in course['sections']:
                    value = None
                    try:
                        value = pre.get(str(section['crn']))
                        # print(value, section['crn'], course['id'], curFile, preFile)
                    except:
                        continue

                    coursesNeeded = getCoursesForKey(pre, str(section['crn']))
                    isValid = True
                    otherReq = []
                    csReq = []
                    for preReq in coursesNeeded:
                        codes = preReq.split(' ')
                        
                        if codes[0] == "MATH" and preReq not in coursesTaken:
                            isValid = False
                            break
                        elif codes[0] != "MATH":
                            otherReq.append(preReq)
                        elif codes[0] == "MATH":
                            csReq.append(preReq)
                    
                    
                    if isValid:
                        firstReq = ''
                        secondReq = ''
                        thirdReq = ''
                        nodeVal = courseName
                        if len(otherReq) > 0:
                            firstReq = otherReq[0]
                            nodeVal = "<f0> " + nodeVal + "| <f1> " + firstReq
                            
                            if len(otherReq) > 1:
                                
                                secondReq = otherReq[1]
                                nodeVal = nodeVal + "| <f2> " + secondReq
                                if len(otherReq) > 2:
                                    thirdReq = otherReq[2]
                                    nodeVal = nodeVal + "| " + thirdReq

                        
                        # if "CSCI 2300" in csReq:
                        #     coursesTaken[courseName] = graph.addNode(val = nodeVal, shape="record", color = "red")
                        # else:
                        #     coursesTaken[courseName] = graph.addNode(val = nodeVal, shape="record")
                        found = False
                        essential = False
                        coursesTaken[courseName] = graph.addNode(val = nodeVal, shape="record", clusterName=  "MATH")
                        found = True
                            
                        courseNameSplit = courseName.split(' ')
                        if found  == False and int(courseNameSplit[1]) >= 4000 and section['attribute'] == "Communication Intensive":
                            if ii %2 == 0:

                                coursesTaken[courseName] = graph.addNode(val = nodeVal, shape="record", color = "green", clusterName=  "SenFall")
                            
                            else:
                                coursesTaken[courseName] = graph.addNode(val = nodeVal, shape="record", color = "green", clusterName=  "SenSpring")
                            found = True

                        
                        if found:
                            for curReq in csReq:
                                if essential:
                                    graph.addEdge(start = coursesTaken[curReq], end = coursesTaken[courseName], color='red')
                                else:
                                    graph.addEdge(start = coursesTaken[curReq], end = coursesTaken[courseName])


                    break
                # if count ==20:
                #     # print(courseName)
                #     # print(coursesNeeded)
                #     # print(crns)
                # count +=1





# %%
#graph.addEdge(coursesTaken["CSCI 1100"], coursesTaken["CSCI 1200"])
print(graph)


