"""
Title:       Critical Thinking Assignment #6
Author:      Minh Nguyen
Created:     2025-07-06
Description:

User Input:

Program Output:

"""


from typing import List, Dict

class User:

    def __init__(self, user_id: str, password: str):
        self.user_id = user_id
        self.password = password

    def authenticate(self, password: str) -> bool:
        return self.password == password


class Student(User):

    def __init__(self, user_id: str, password: str):
        super().__init__(user_id, password)
        self.registered_courses = []  # List of Course IDs

    def register_course(self, course_id: str):
        if course_id not in self.registered_courses:
            self.registered_courses.append(course_id)

    def drop_course(self, course_id: str):
        if course_id in self.registered_courses:
            self.registered_courses.remove(course_id)

    def list_registered_courses(self) -> List[str]:
        return self.registered_courses


class Admin(User):
    """For now, no extra methods required; actions done through RegistrationSystem class."""


class Course:

    def __init__(self, course_id: str, title: str, description: str, credits: int, capacity: int):
        self.course_id = course_id.upper()
        self.title = title
        self.description = description
        self.credits = credits
        self.capacity = capacity
        self.registered_students = []  # List of student IDs

    def update_details(self, title=None, description=None, credits=None, capacity=None):
        if title is not None:
            self.title = title
        if description is not None:
            self.description = description
        if credits is not None:
            self.credits = credits
        if capacity is not None:
            self.capacity = capacity

    def is_full(self) -> bool:
        return len(self.registered_students) >= self.capacity

    def add_student(self, student_id: str):
        if not self.is_full() and student_id not in self.registered_students:
            self.registered_students.append(student_id)
        else:
            raise Exception("Course is full or student already registered.")

    def remove_student(self, student_id: str):
        if student_id in self.registered_students:
            self.registered_students.remove(student_id)

    def __str__(self):
        return (f"ID: {self.course_id}, Title: {self.title}, Credits: {self.credits}, "
                f"Capacity: {self.capacity}, Registered: {len(self.registered_students)}")


class RegistrationSystem:

    def __init__(self):
        self.courses: Dict[str, Course] = {}
        self.students: Dict[str, Student] = {}
        self.admins: Dict[str, Admin] = {}

        # Pre-Registered Admin Accounts
        self.admins['admin'] = Admin('admin', 'password')

        # Pre-Registered Student Accounts
        self.students['student1'] = Student('student1', 'pass123')
        self.students['student2'] = Student('student2', 'pass123')

    def authenticate_user(self, user_id: str, password: str) -> User:
        user_id = user_id.lower()
        if user_id == 'admin' and user_id in self.admins:
            admin = self.admins[user_id]
            if admin.authenticate(password):
                return admin
        elif user_id in self.students:
            student = self.students[user_id]
            if student.authenticate(password):
                return student
        raise Exception("Invalid username or password.")

    # --- Admin Functions ---

    def add_course(self, course_id: str, title: str, description: str, credits: int, capacity: int):
        course_id = course_id.upper()
        if course_id in self.courses:
            raise Exception("Course with this ID already exists.")
        self.courses[course_id] = Course(course_id, title, description, credits, capacity)

    def remove_course(self, course_id: str):
        course_id = course_id.upper()
        if course_id not in self.courses:
            raise Exception("Course not found.")
        # Remove course from all students
        for student in self.students.values():
            if course_id in student.registered_courses:
                student.drop_course(course_id)
        del self.courses[course_id]

    def update_course(self, course_id: str, title=None, description=None, credits=None, capacity=None):
        course_id = course_id.upper()
        if course_id not in self.courses:
            raise Exception("Course not found.")
        self.courses[course_id].update_details(title, description, credits, capacity)

    def search_courses(self, search_term: str) -> List[Course]:
        search_term = search_term.lower()
        results = []
        for course in self.courses.values():
            if search_term in course.course_id.lower() or search_term in course.title.lower():
                results.append(course)
        return results

    def list_students_for_course(self, course_id: str) -> List[str]:
        course_id = course_id.upper()
        if course_id not in self.courses:
            raise Exception("Course not found.")
        return self.courses[course_id].registered_students

    def list_courses_for_student(self, student_id: str) -> List[str]:
        student_id = student_id.lower()
        if student_id not in self.students:
            raise Exception("Student not found.")
        return self.students[student_id].list_registered_courses()

    # --- Students Functions ---

    def register_student_for_course(self, student_id: str, course_id: str):
        student_id = student_id.lower()
        course_id = course_id.upper()
        if student_id not in self.students:
            raise Exception("Student not found.")
        if course_id not in self.courses:
            raise Exception("Course not found.")
        student = self.students[student_id]
        course = self.courses[course_id]
        if course.is_full():
            raise Exception("Course is full.")
        if course_id in student.registered_courses:
            raise Exception("Student already registered for this course.")
        course.add_student(student_id)
        student.register_course(course_id)

    def drop_student_from_course(self, student_id: str, course_id: str):
        student_id = student_id.lower()
        course_id = course_id.upper()
        if student_id not in self.students:
            raise Exception("Student not found.")
        if course_id not in self.courses:
            raise Exception("Course not found.")
        student = self.students[student_id]
        course = self.courses[course_id]
        if course_id not in student.registered_courses:
            raise Exception("Student is not registered for this course.")
        course.remove_student(student_id)
        student.drop_course(course_id)

    def view_available_courses(self) -> List[Course]:
        return list(self.courses.values())

    def generate_report_student_courses(self, student_id: str) -> str:
        student_id = student_id.lower()
        if student_id not in self.students:
            raise Exception("Student not found.")
        student = self.students[student_id]
        if not student.registered_courses:
            return "No registered courses."
        report_lines = []
        for cid in student.registered_courses:
            course = self.courses.get(cid)
            if course:
                report_lines.append(f"{course.course_id}: {course.title} ({course.credits} credits)")
        return "\n".join(report_lines)


def input_int(prompt: str, min_val=None, max_val=None) -> int:
    while True:
        try:
            value = int(input(prompt))
            if (min_val is not None and value < min_val) or (max_val is not None and value > max_val):
                print(f"Value must be between {min_val} and {max_val}.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def input_nonempty(prompt: str) -> str:
    while True:
        s = input(prompt).strip()
        if s:
            return s
        else:
            print("Input cannot be empty.")

def admin_menu(system: RegistrationSystem, admin: Admin):
    while True:
        print("\n--- Admin Menu ---")
        print("1. Add course")
        print("2. Remove course")
        print("3. Update course")
        print("4. Search courses")
        print("5. List students in a course")
        print("6. List courses of a student")
        print("7. Logout")
        choice = input_nonempty("Enter choice: ")

        try:
            if choice == '1':
                course_id = input_nonempty("Course ID: ").upper()
                title = input_nonempty("Title: ")
                description = input_nonempty("Description: ")
                credits = input_int("Credits: ", 1)
                capacity = input_int("Capacity: ", 1)
                system.add_course(course_id, title, description, credits, capacity)
                print(f"Course {course_id} added successfully.")
            elif choice == '2':
                course_id = input_nonempty("Course ID to remove: ").upper()
                system.remove_course(course_id)
                print(f"Course {course_id} removed successfully.")
            elif choice == '3':
                course_id = input_nonempty("Course ID to update: ").upper()
                print("Leave blank to keep current value.")
                title = input("New Title: ").strip() or None
                description = input("New Description: ").strip() or None
                credits_input = input("New Credits: ").strip()
                credits = int(credits_input) if credits_input.isdigit() else None
                capacity_input = input("New Capacity: ").strip()
                capacity = int(capacity_input) if capacity_input.isdigit() else None
                system.update_course(course_id, title, description, credits, capacity)
                print(f"Course {course_id} updated successfully.")
            elif choice == '4':
                term = input_nonempty("Enter search term (ID or title): ")
                results = system.search_courses(term)
                if not results:
                    print("No courses found.")
                else:
                    for c in results:
                        print(c)
            elif choice == '5':
                course_id = input_nonempty("Course ID: ").upper()
                students = system.list_students_for_course(course_id)
                if not students:
                    print("No students registered for this course.")
                else:
                    print(f"Students registered for {course_id}:")
                    for sid in students:
                        print(f"- {sid}")
            elif choice == '6':
                student_id = input_nonempty("Student ID: ").lower()
                courses = system.list_courses_for_student(student_id)
                if not courses:
                    print("Student is not registered for any courses.")
                else:
                    print(f"Courses registered by {student_id}:")
                    for cid in courses:
                        print(f"- {cid}")
            elif choice == '7':
                print("Logging out...")
                break
            else:
                print("Invalid choice, please try again.")
        except Exception as e:
            print(f"Error: {e}")


def student_menu(system: RegistrationSystem, student: Student):
    while True:
        print(f"\n--- Student Menu ({student.user_id}) ---")
        print("1. View available courses")
        print("2. Register for a course")
        print("3. Drop a course")
        print("4. View registered courses")
        print("5. Logout")
        choice = input_nonempty("Enter choice: ")

        try:
            if choice == '1':
                courses = system.view_available_courses()
                if not courses:
                    print("No courses available.")
                else:
                    for c in courses:
                        status = "Full" if c.is_full() else "Available"
                        print(f"{c} - Status: {status}")
            elif choice == '2':
                course_id = input_nonempty("Enter course ID to register: ").upper()
                system.register_student_for_course(student.user_id, course_id)
                print(f"Registered for course {course_id}.")
            elif choice == '3':
                course_id = input_nonempty("Enter course ID to drop: ").upper()
                system.drop_student_from_course(student.user_id, course_id)
                print(f"Dropped course {course_id}.")
            elif choice == '4':
                report = system.generate_report_student_courses(student.user_id)
                print("Registered courses:")
                print(report)
            elif choice == '5':
                print("Logging out...")
                break
            else:
                print("Invalid choice, please try again.")
        except Exception as e:
            print(f"Error: {e}")

def main():
    system = RegistrationSystem()

    print("Welcome to Student Course Registration System")
    print("\nPlease use pre-registered accounts to log-in")
    print("{:<15} {:<15} {:<25}".format("Role", "User ID", "Password"))
    print("{:<15} {:<15} {:<25}".format("Admin", "admin", "<password>"))
    print("{:<15} {:<15} {:<25}".format("Students", "student1", "<pass123>"))
    print("{:<15} {:<15} {:<25}".format("Students", "student2", "<pass123>"))

    while True:
        print("\nPlease use pre-registered accounts to log-in")
        print("{:<15} {:<15} {:<25}".format("Role", "User ID", "Password"))
        print("{:<15} {:<15} {:<25}".format("Admin", "admin", "<password>"))
        print("{:<15} {:<15} {:<25}".format("Students", "student1", "<pass123>"))
        print("{:<15} {:<15} {:<25}".format("Students", "student2", "<pass123>"))
        print("\n--- Login ---")
        user_id = input_nonempty("User ID: ").lower()
        password = input_nonempty("Password: ")

        try:
            user = system.authenticate_user(user_id, password)
            print(f"Welcome, {user.user_id}!")
            if isinstance(user, Admin):
                admin_menu(system, user)
            elif isinstance(user, Student):
                student_menu(system, user)
        except Exception as e:
            print(f"Login failed: {e}")

        cont = input("Do you want to login again? (y/n): ").strip().lower()
        if cont != 'y':
            print("Exiting system. Goodbye!")
            break


if __name__ == "__main__":
    main()
