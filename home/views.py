from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
import pyodbc 
import json
from itertools import combinations
from itertools import combinations_with_replacement


connection_string = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=LAPTOP-BKNAJCDL;"
    "DATABASE=testdb;"
    "Trusted_Connection=yes;"
)

# Establish the connection
connection = pyodbc.connect(connection_string)

# Create a cursor object using the connection
cursor = connection.cursor()

sql_query = "SELECT MAKE, Model, ContainerNumber, Yard, VanningDateTime, NumberOfStock FROM booking"

allCarsQuery = "SELECT * from cars"

# Execute the query
cursor.execute(sql_query)


# Fetch the results
results = cursor.fetchall()

# Print the results
testCase = results[0:19]

def categorize_containers_by_name_count(previous):
    containersNumbers = {
        "six": [], "five": [], "four": [], "three": [], "two": []
    }
    
    count = previous[0][5]
    i = 0
    j = count
    carList = []
    containerInfo = {}
    while(i < len(previous)):
        if(i == j):
            containerInfo["VanningDate"] = previous[i-1][4]
            containerInfo["Yard"] = previous[i-1][3]
            containerInfo["Container"] = sorted(carList)
            count = previous[i-1][5]
            if count == 6:
                containersNumbers["six"].append(containerInfo)
            elif count == 5:
                containersNumbers["five"].append(containerInfo)
            elif count == 4:
                containersNumbers["four"].append(containerInfo)
            elif count == 3:
                containersNumbers["three"].append(containerInfo)
            elif count == 2:
                containersNumbers["two"].append(containerInfo)
            carList = []
            containerInfo = {}
            count = previous[i][5]
            j = j + count
        elif(i<j):
            name = previous[i][0] + " " + previous[i][1]
            carList.append(name)
            i = i + 1
    
    return containersNumbers

from itertools import combinations

def searchContainers(n, containerSorted, newSorted, new, result=None):
    if result is None:
        result = []
    
    if n >= 6:
        possibleCombs = list(set(combinations(newSorted, 6)))
        for comb in possibleCombs:
            for container in containerSorted['six']:
                if list(comb) == container['Container']:
                    result.append(container)
                    for car in container['Container']:
                        if car in new:
                            new.remove(car)
        return searchContainers(5, containerSorted, newSorted, new, result)
    elif n == 5:
        possibleCombs = list(set(combinations(newSorted, 5)))
        for comb in possibleCombs:
            for container in containerSorted['five']:
                if list(comb) == container['Container']:
                    result.append(container)
                    for car in container['Container']:
                        if car in new:
                            new.remove(car)
        return searchContainers(4, containerSorted, newSorted, new, result)
    elif n == 4:
        possibleCombs = list(set(combinations(newSorted, 4)))
        for comb in possibleCombs:
            for container in containerSorted['four']:
                if list(comb) == container['Container']:
                    result.append(container)
                    for car in container['Container']:
                        if car in new:
                            new.remove(car)
        return searchContainers(3, containerSorted, newSorted, new, result)
    elif n == 3:
        possibleCombs = list(set(combinations(newSorted, 3)))
        for comb in possibleCombs:
            for container in containerSorted['three']:
                if list(comb) == container['Container']:
                    result.append(container)
                    for car in container['Container']:
                        if car in new:
                            new.remove(car)
        return searchContainers(2, containerSorted, newSorted, new, result)
    elif n == 2:
        possibleCombs = list(set(combinations(newSorted, 2)))
        for comb in possibleCombs:
            for container in containerSorted['two']:
                if list(comb) == container['Container']:
                    result.append(container)
                    for car in container['Container']:
                        if car in new:
                            new.remove(car)
        return searchContainers(1, containerSorted, newSorted, new, result)
    elif n <= 1:
        print("No combinations found for: ", new)
        final_result = result[:]  # Copy the result before clearing it
        result.clear()  # Clear the result list
        return final_result


def optimalContainers(noOfContainers, newSorted, subsets, solution=None, flagCombo=1):
    if solution is None:
        solution = []
    
    while(flagCombo == 1):
        flagCombo = 0
        if(noOfContainers == 1):
            for subset in subsets:
                optimalSolutions = {}
                optimalSolutions['Found'] = []
                optimalSolutions['NotFound'] = []
                if(subset['Container'] == newSorted):
                    flagCombo = 1
                    optimalSolutions['Found'].append(subset)
                    solution.append(optimalSolutions)
                else:
                    flagCombo = 1
                    optimalSolutions['Found'].append(subset)
                    newSortedCopy = newSorted[:]
                    subsetCars = subset['Container']
                    for subsetCar in subsetCars:
                        if subsetCar in newSortedCopy:
                            newSortedCopy.remove(subsetCar)


                    optimalSolutions['NotFound'] = newSortedCopy
                    solution.append(optimalSolutions)
            
            return optimalContainers(noOfContainers + 1, newSorted, subsets, solution, flagCombo)
            
        elif(noOfContainers > 1):
            combos = combinations_with_replacement(subsets, noOfContainers)
            for comb in combos:
                concatResult = []
                optimalSolutions = {}
                optimalSolutions['Found'] = []
                optimalSolutions['NotFound'] = []

                #to concatenate the combo
                for element in comb:
                    concatResult = concatResult + element['Container']
                
                if(sorted(concatResult) == newSorted):
                    flagCombo = 1
                    for element in comb:
                        optimalSolutions['Found'].append(element)
                    solution.append(optimalSolutions)
                elif(len(concatResult) <= len(newSorted)):
                    flagCombo = 1
                    Found = []
                    notFound = []
                    flag = 0 
                    i=0
                    j=0
                    sortedConcatResult = sorted(concatResult)

                    while(j < len(newSorted)):
                        if(j >= len(newSorted) and i != len(concatResult)):
                            flag = 1
                            break
                        elif(i >= len(concatResult)):
                            notFound.append(newSorted[j])
                            j += 1
                        else:
                            if(sortedConcatResult[i] == newSorted[j]):
                                Found.append(sortedConcatResult[i])
                                i += 1
                                j += 1
                            else:
                                notFound.append(newSorted[j])
                                j += 1
                    
                    if(flag == 0):
                        optimalSolutions['NotFound'] = notFound
                        for element in comb:
                            optimalSolutions['Found'].append(element)
                        
                        solution.append(optimalSolutions)

            return optimalContainers(noOfContainers + 1, newSorted, subsets, solution, flagCombo)
    
    if len(solution) == 0:
        return 0
    else:
        final_solution = solution[:]  
        solution.clear()  
        return final_solution


def remove_unique_containers(data):
    result = []
    seen_containers = []
    for containerInfo in data:
        if containerInfo['Container'] not in seen_containers:
            seen_containers.append(containerInfo['Container'])
            result.append(containerInfo)
    return result


def index(request):
    context = {
        "variable": "HI"
    }
    return render(request, "index.html", context)

def carContainers(request):
    cursor.execute(allCarsQuery)
    allCars = cursor.fetchall()

    data = []
    for row in allCars:
        data.append({
            'MAKE': row.MAKE,
            'Model': row.Model
        })

    Answer = [[{'VanningDate': "2023/7/19", 'Yard': 'ATL NAGOYA', 'Container': ['AUDI AUDI', 'MERCEDES BENZ', 'MERCEDES BENZ', 'MERCEDES BENZ GLA180', 'MERCEDES C200']}, {'VanningDate': "2023/8/4", 'Yard': 'ATL OSAKA', 'Container': ['MERCEDES BENZ', 'MERCEDES BENZ']}], [{'VanningDate': "2013/7/19", 'Yard': 'ATL NAGOYA', 'Container': ['AUDI AUDI', 'MERCEDES BENZ', 'MERCEDES BENZ', 'MERCEDES BENZ GLA180', 'MERCEDES C200']}, {'VanningDate': "2013/6/10", 'Yard': 'ATL OSAKA', 'Container': ['MERCEDES BENZ', 'MERCEDES BENZ']}]]

    context = {
        "allCars": data,
        # "Answer": Answer
    }
    return render(request, "carContainers.html", context)

def requestCombinations(request):
    # cursor.execute(allCarsQuery)
    # allCars = cursor.fetchall()
    if request.method == 'GET':
        try:
            cars = []
            for key in request.GET:
                if key.startswith('array['):
                    cars.append(request.GET[key])
            
            # print(cars) 
            new = cars
            # new = ['AUDI AUDI', 'MERCEDES BENZ', 'MERCEDES BENZ', 'MERCEDES BENZ GLA180', 'MERCEDES C200', 'MERCEDES BENZ', 'MERCEDES BENZ']
            newSorted = sorted(new) 
            containerSorted = categorize_containers_by_name_count(results)
            result1 = searchContainers(len(newSorted), containerSorted, newSorted, new)
            uniqueContainers = remove_unique_containers(result1)
            print("Results:")
            print("                   Container                                              Number of Cars     Vanning Date       Yard")
            for container in result1:
                print(container['Container'] , "\t" , len(container['Container']), "\t", container['VanningDate'], "\t", container['Yard'])

            subsets = []
            for set in uniqueContainers:
                subsets.append(set)

            print("END")
            Answer = optimalContainers(1, newSorted, subsets)

            if(Answer == 0):
                print("No optimal solution found")
            else:
                print(len(Answer))
                print(Answer)
            
            
            return JsonResponse({'message': 'Array received successfully', 'cars': cars, 'Answer': Answer})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)


LISASD = [['MERCEDES BENZ', 'MERCEDES BENZ', 'MERCEDES BENZ', 'MERCEDES BENZ'], ['MERCEDES BENZ', 'MERCEDES BENZ', 'MERCEDES BENZ'], ['MERCEDES BENZ', 'MERCEDES BENZ']]