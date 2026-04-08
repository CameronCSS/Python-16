"""
- Student Grade Tracker -
- Enter a list of student names
- Enter a grade for each student
- Program outputs:

1. Each student with their grade (enumerate)
   1. John - 85
   2. Ann - 92
   3. Chad - 78

2. Name and grade paired together (zip)
   
3. Highest and lowest grade + who got them (max, min)
   John got the highest with 95
   Chad got the lowest with 62

4. Grade summary for each student using range (loop with range)
   - A, B, C, D, F breakdown
   - How many students in each grade band

All four concepts fit naturally:

enumerate — numbering the student list when printing
zip — pairing names list with grades list together
max / min — finding highest and lowest grade
range — looping through grade bands like range(0, 60), range(60, 70) etc
"""


students = []
grades = []

while True:
    name = input("Enter the Students name: ('e' to end)").title()
    if name.lower() == 'e':
        break
    else:
        students.append(name)
        continue
    
while True:
    for name in students:
        if len(grades) == len(students):
            break
        else:
            grade = int(input(f"Enter {name}'s grade: ('e' to end)"))
            grades.append(grade)
    break
        
report_card = list(zip(students, grades))

print("\nStudent Report:")
for index, (student, grade) in enumerate(report_card, 1):
    print(f"{index}. {student} - {grade}")


# Kind of a hacky way to read the values
# is it better to hard code if statements??
grade_range = [0, 60, 70, 80, 90, 100, 110]
letter_grade = ["holder", "F", "D", "C", "B", "A"]

grade_list = list(zip(grade_range, letter_grade))

student_letters = []

print("\nGrade Summary:") 
for student, grade in report_card:
    for index, (score, letter) in enumerate(grade_list):
        if grade in range(score, grade_range[index + 1]):
            print(f"{student} got an {letter_grade[index + 1]}")
            student_letters.append((letter_grade[index + 1]))
            
print("\nHighest vs Lowest grade") 
for student, grade in report_card:
    if grade == max(grades):
        print(f"{student} had the highest score: {grade}")
    elif grade == min(grades):
        print(f"{student} had the lowest score: {grade}")
                
            
final_counts = {}

print("\nGrade Counts:") 
final_counts[letter] = final_counts.get(letter, 0) + 1
    
for letter, count in final_counts.items():
    print(f"{count} students got a {letter}")