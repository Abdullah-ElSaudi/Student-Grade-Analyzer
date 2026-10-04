import csv
import statistics

# ==============================================================================
# 1. HELPER & DATA FUNCTIONS 
# ==============================================================================

def add_students(students):
    while True:
        while True:
            student_id = input("\nEnter Student ID (at least 5 characters): ").strip()
            if len(student_id) < 5:
                print("❌ Student ID must be at least 5 characters long.")
            elif any(s['id'].lower() == student_id.lower() for s in students):
                print(f"❌ Student ID '{student_id}' already exists! Enter a unique ID.")
            else:
                break

        name = input("Enter Student Name (must have at least two names): ").strip()
        while name.count(' ') < 1:
            print("❌ Student Name must have at least two names (e.g. John Doe).")
            name = input("Enter Student Name (must have at least two names): ").strip()

        while True:
            try:
                score = float(input("Enter Student Score (0-100): "))
                if 0 <= score <= 100:
                    break  
                else:
                    print("❌ Student Score must be in range 0 to 100.")
            except ValueError:
                print("❌ Invalid input! Please enter a numeric score (e.g., 85.5).")

        status = 'Pass' if score >= 50 else 'Fail'

        if score >= 90:
            grade = 'A'
        elif score >= 80:
            grade = 'B'    
        elif score >= 70:
            grade = 'C'    
        elif score >= 60:
            grade = 'D'
        else:
            grade = 'F'

        student = {
            "id": student_id,
            "name": name,
            "score": score,
            "grade": grade,
            "status": status
        }
        students.append(student)
        print(f"✅ Added '{name}' successfully!")

        yes_no = input("Do you want to add another student? (y/n): ").strip().lower()
        if yes_no in ['n', 'no']:
            break

def print_summary_report(students):
    
    if not students:
        print("❌ No students available to generate a report!")
        return

    highest_score = max(students, key=lambda x: x['score'])
    lowest_score = min(students, key=lambda x: x['score'])
    num_pass = sum(1 for s in students if s['status'] == 'Pass')
    num_fail = sum(1 for s in students if s['status'] == 'Fail')

    num_students_A = sum(1 for s in students if s['grade'] == 'A')  
    num_students_B = sum(1 for s in students if s['grade'] == 'B')
    num_students_C = sum(1 for s in students if s['grade'] == 'C')
    num_students_D = sum(1 for s in students if s['grade'] == 'D')
    num_students_F = sum(1 for s in students if s['grade'] == 'F')            

    average_score = sum(s['score'] for s in students) / len(students)
    scores_list = [s['score'] for s in students]
    median_score = statistics.median(scores_list)

    pass_percentage = (num_pass / len(students)) * 100
    fail_percentage = (num_fail / len(students)) * 100

    print(f"""
    ================================
            SUMMARY REPORT
    ================================

    Total Students: {len(students)}

    Average Score: {average_score:.1f}
    Median Score: {median_score:.1f}

    Highest Score: {highest_score['score']} ({highest_score['name']})
    Lowest Score: {lowest_score['score']} ({lowest_score['name']})

    Passed: {num_pass}
    Failed: {num_fail}

    Pass Rate: {pass_percentage:.0f}%
    Failure Rate: {fail_percentage:.0f}%

    Grade Distribution:
    A: {num_students_A}
    B: {num_students_B}
    C: {num_students_C}
    D: {num_students_D}
    F: {num_students_F}
    ================================
    """)
    

def search_student(students):
    if not students:
        print("❌ No students available to search!")
        return

    search_term = input("\nEnter Student ID or Name to search: ").strip().lower()
    found = False
    
    for s in students:
        if search_term in s['id'].lower() or search_term in s['name'].lower():
            print(f"✅ Found: {s['name']} | ID: {s['id']} | Score: {s['score']} | Grade: {s['grade']} | Status: {s['status']}")
            found = True
            
    if not found:
        print(f"❌ No student found matching '{search_term}'.")


def save_to_csv(students, filename="students.csv"):

    if not students:
        print("❌ No data to save! Add students first.")
        return

    try:
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            fieldnames = ["id", "name", "score", "grade", "status"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()   
            writer.writerows(students) 
        print(f"✅ Data successfully saved to '{filename}'.")
    except Exception as e:
        print(f"❌ Error saving data: {e}")


def load_from_csv(filename="students.csv"):

    loaded_students = []
    try:
        with open(filename, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                row['score'] = float(row['score'])
                loaded_students.append(row)
        print(f"✅ Successfully loaded {len(loaded_students)} student(s) from '{filename}'.")
    except FileNotFoundError:
        print(f"⚠️ Notice: File '{filename}' not found.")
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        
    return loaded_students

# ==============================================================================
# 2. MAIN INTERACTIVE MENU 
# ==============================================================================

def main():
    students = []  

    while True:
        print("""
        ====================================
              STUDENT GRADE ANALYZER        
        ====================================
        1. Add Students 
        2. View Summary Report 
        3. Search Student 
        4. Save Data to CSV 
        5. Load Data from CSV 
        6. Exit 
        ====================================
        """)
        
        choice = input("Enter your choice (1-6): ").strip()
        
        if choice == '1':
            print("\n--- ➕ Add Students ---")
            add_students(students)

        elif choice == '2':
            print("\n--- 📊 Summary Report ---")
            print_summary_report(students)

        elif choice == '3':
            print("\n--- 🔍 Search Student ---")
            search_student(students)

        elif choice == '4':
            print("\n--- 💾 Save Data ---")
            save_to_csv(students)

        elif choice == '5':
            print("\n--- 📂 Load Data ---")
            students = load_from_csv()

        elif choice == '6':
            print("\n👋 Goodbye! Thank you for using Student Grade Analyzer.")
            break

        else:
            print("❌ Invalid choice! Please enter a number from 1 to 6.")


if __name__ == "__main__":
    main()