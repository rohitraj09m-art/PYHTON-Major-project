import json
import os

FILE_NAME = "students.json"


class Student:


    def __init__(self, roll_no, name, age, course, marks):

        self.roll_no = roll_no
        self.name = name
        self.age = age
        self.course = course
        self.marks = marks

    def calculate_total(self):

        return sum(self.marks)

    def calculate_average(self):

        if not self.marks:
            return 0.0
        return self.calculate_total() / len(self.marks)

    def calculate_grade(self):

        avg = self.calculate_average()
        if avg >= 90:
            return "A+"
        elif avg >= 80:
            return "A"
        elif avg >= 70:
            return "B"
        elif avg >= 60:
            return "C"
        elif avg >= 50:
            return "D"
        else:
            return "F (Fail)"

    def display_report(self):

        print("\n" + "=" * 50)
        print("          STUDENT COMPLETE REPORT CARD          ")
        print("=" * 50)
        print(f" Roll Number   : {self.roll_no}")
        print(f" Name          : {self.name}")
        print(f" Age           : {self.age}")
        print(f" Course        : {self.course}")
        print("-" * 50)
        print(f" Marks List    : {self.marks}")
        print(f" Total Marks   : {self.calculate_total()}")
        print(f" Average Marks : {self.calculate_average():.2f}")
        print(f" Grade         : {self.calculate_grade()}")
        print("=" * 50)

    def to_dict(self):

        return {
            "roll_no": self.roll_no,
            "name": self.name,
            "age": self.age,
            "course": self.course,
            "marks": self.marks
        }

    @classmethod
    def from_dict(cls, data):

        return cls(
            roll_no=data["roll_no"],
            name=data["name"],
            age=data["age"],
            course=data["course"],
            marks=data["marks"]
        )


class StudentManagementSystem:


    def __init__(self):
        self.students = {}
        self.load_students()

    def load_students(self):

        if os.path.exists(FILE_NAME):
            try:
                with open(FILE_NAME, "r") as file:
                    data = json.load(file)
                    for roll_no, s_data in data.items():
                        self.students[roll_no] = Student.from_dict(s_data)
            except (json.JSONDecodeError, IOError):
                self.students = {}

    def save_students(self):

        try:
            with open(FILE_NAME, "w") as file:
                json_data = {roll: obj.to_dict() for roll, obj in self.students.items()}
                json.dump(json_data, file, indent=4)
            return True
        except IOError:
            print("\n[Error] error in saving data!")
            return False

    def add_student(self):

        print("\n--- Create New Student Object ---")
        roll_no = input("Enter Roll Number : ").strip()

        if not roll_no:
            print("[!] Roll Number cannot be blank.")
            return

        if roll_no in self.students:
            print(f"[!] Roll Number {roll_no} already exists.")
            return

        name = input("Student Name: ").strip()
        course = input("Course (e.g. BCA, B.Tech): ").strip()

        try:
            age = int(input("Age: ").strip())
            num_subjects = int(input("Number of subjects?: ").strip())

            marks = []
            for i in range(1, num_subjects + 1):
                m = float(input(f"  Subject {i} Marks (Out of 100): ").strip())
                marks.append(m)

        except ValueError:
            print("[!] Invalid numeric input! Action cancelled.")
            return


        new_student = Student(roll_no, name, age, course, marks)
        self.students[roll_no] = new_student

        if self.save_students():
            print(f"\n[✓] Student object successfully created and saved.")

    def display_all_reports(self):

        if not self.students:
            print("\n[!] No record Found.")
            return

        for student in self.students.values():
            student.display_report()

    def search_and_display_report(self):

        print("\n--- Search Student Report ---")
        roll_no = input("Enter the Roll Number : ").strip()

        student = self.students.get(roll_no)
        if student:
            student.display_report()
        else:
            print(f"[!] Roll Number {roll_no} Not found.")

    def delete_student(self):

        print("\n--- Delete Student Record ---")
        roll_no = input("Enter the roll no: ").strip()

        if roll_no not in self.students:
            print(f"[!] Roll Number {roll_no} not found.")
            return

        confirm = input(f"Do you '{self.students[roll_no].name}' want to delete? (y/n): ").strip().lower()
        if confirm == 'y':
            del self.students[roll_no]
            if self.save_students():
                print(f"\n[✓] Student record deleted successfully.")


def main():
    system = StudentManagementSystem()

    while True:
        print("\n==========================================")
        print("  STUDENT MANAGEMENT SYSTEM (OOP BASED)   ")
        print("==========================================")
        print("1. Create Student Object (Add Details & Marks)")
        print("2. Search & Display Student Report")
        print("3. Display All Students Complete Reports")
        print("4. Delete Student Record")
        print("5. Exit")
        print("==========================================")

        choice = input("Choose Option (1-5): ").strip()

        if choice == '1':
            system.add_student()
        elif choice == '2':
            system.search_and_display_report()
        elif choice == '3':
            system.display_all_reports()
        elif choice == '4':
            system.delete_student()
        elif choice == '5':
            print("\nExiting Program...!")
            break
        else:
            print("\n[!] Invalid option! choose between 1 and 5.")


if __name__ == "__main__":
    main()