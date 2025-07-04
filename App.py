"""
Title:       Portfolio Project
Author:      Minh Nguyen
Created:     2025-07-06
Description:
    This Python program simulates a student course registration system that supports user authentication, course management, and student enrollment functionalities.
    It features a secure login system with predefined credentials for administrators and students.
    Administrators can manage courses by adding, removing, updating course details, and searching courses by title or ID.
    Students can browse available courses, register for courses within capacity limits, drop courses, and view their registered courses. The system enforces course capacity restrictions to prevent over-registration.
    Additionally, the program generates reports on courses registered by each student and enables administrators to view student lists for specific courses and courses registered by individual students. The interactive menu-driven interface provides distinct options for admins and students to efficiently manage and navigate the system.

"""


from typing import List, Dict

class User:

    def __init__(self, user_id: str, password: str):
        """
        Creates a new User with a user ID and password.

        Arguments:
            user_id (str): A name or ID to identify the user.
            password (str): The user's password to log in.
        """
        self.user_id = user_id
        self.password = password

    def authenticate(self, password: str) -> bool:
        """
        Checks if the given password is correct.

        Argument:
            password (str): The password you want to check.

        Returns:
            bool: Returns True if the password is right, False if it's wrong.
        """
        return self.password == password


class Student(User):

    def __init__(self, user_id: str, password: str):
        """
        Creates a new Student using the User class.

        Arguments:
            user_id (str): A name or ID to identify the student.
            password (str): The student's password to log in.

        Attributes:
            registered_courses (List[str]): A list of course names or IDs the student is signed up for.
        """
        super().__init__(user_id, password)
        self.registered_courses = []

    def register_course(self, course_id: str):
        """
        Adds a course to the student's course list if it's not already added.

        Argument:
            course_id (str): The name or ID of the course to add.
        """
        if course_id not in self.registered_courses:
            self.registered_courses.append(course_id)

    def drop_course(self, course_id: str):
        """
        Removes a course from the student's course list if it's there.

        Argument:
            course_id (str): The ID of the course to remove.
        """
        if course_id in self.registered_courses:
            self.registered_courses.remove(course_id)

    def view_registered_courses(self) -> List[str]:
        """
        Shows all the courses the student is currently registered in.

        Returns:
            List[str]: A list of course names or IDs.
        """
        return self.registered_courses


class Admin(User):
    """For now, no extra methods required; actions done through RegistrationSystem class."""


class Course:

    def __init__(self, course_id: str, title: str, description: str, credits: int, capacity: int):
        """
        Creates a new Course with the provided details (Arguments).

        Arguments:
            course_id (str): A short name or code for the course (automatically made uppercase).
            title (str): The name of the course.
            description (str): A short summary of what the course is about.
            credits (int): How many credits the course is worth.
            capacity (int): The maximum number of students allowed in the course.

        Attributes:
            registered_students (List[str]): A list of student IDs who signed up for the course.
        """
        self.course_id = course_id.upper()
        self.title = title
        self.description = description
        self.credits = credits
        self.capacity = capacity
        self.registered_students = []

    def update_details(self, title=None, description=None, credits=None, capacity=None):
        """
        Changes the course details

        You can update one, some, or all of the following:
        - title
        - description
        - credits
        - capacity

        Only the values you provide will be updated.

        Arguments:
            title (str, optional): New course name.
            description (str, optional): New summary of the course.
            credits (int, optional): New number of credits.
            capacity (int, optional): New student limit.
        """
        if title is not None:
            self.title = title
        if description is not None:
            self.description = description
        if credits is not None:
            self.credits = credits
        if capacity is not None:
            self.capacity = capacity

    def is_full(self) -> bool:
        """
        Checks if the course is full (If the course is full, no more students can join).

        Returns:
            bool: True if the course reached its limit; False if there is still space.
        """
        return len(self.registered_students) >= self.capacity

    def add_student(self, student_id: str):
        """
        Adds a student to the course if there is room and the student isn't already signed up.

        Argument:
            student_id (str): The ID of the student to add.

        Raises:
            Exception: If the course is full or the student is already on the list.
        """
        if not self.is_full() and student_id not in self.registered_students:
            self.registered_students.append(student_id)
        else:
            raise Exception("Course is full or student already registered.")

    def remove_student(self, student_id: str):
        """
        Takes a student out of the course if they are signed up.

        Argument:
            student_id (str): The ID of the student to remove.
        """
        if student_id in self.registered_students:
            self.registered_students.remove(student_id)

    def __str__(self):
        """
        Shows course information as a string.

        Returns:
            str: A summary including course ID, title, credits, capacity, and how many students are registered.
        """
        return (f"ID: {self.course_id}, Title: {self.title}, Credits: {self.credits}, "
                f"Capacity: {self.capacity}, Registered: {len(self.registered_students)}")


class RegistrationSystem:

    def __init__(self):
        """
        Starts the registration system with empty lists of courses, students, and admins.

        Also pre-registers default admin and student accounts with preset credentials.

        Attributes:
            courses (Dict[str, Course]): A dictionary mapping course IDs to Course objects.
            students (Dict[str, Student]): A dictionary mapping student IDs to Student objects.
            admins (Dict[str, Admin]): A dictionary mapping admin IDs to Admin objects.
        """
        self.courses: Dict[str, Course] = {}
        self.students: Dict[str, Student] = {}
        self.admins: Dict[str, Admin] = {}

        # Pre-Registered Admin Accounts
        self.admins['admin'] = Admin('admin', 'password')

        # Pre-Registered Student Accounts
        self.students['student1'] = Student('student1', 'pass123')
        self.students['student2'] = Student('student2', 'pass123')

    def authenticate_user(self, user_id: str, password: str) -> User:
        """
        Checks if a user as admin or student can log in with the given ID and password.

        Arguments:
            user_id (str): The username to check.
            password (str): The password to check.

        Returns:
            User: The user object if login is successful.

        Raises:
            Exception: If the username or password is wrong.
        """
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
        """
        Adds a new course to the system.

        Arguments:
            course_id (str): The course code (like "CS101").
            title (str): The name of the course.
            description (str): A short explanation of what the course is about.
            credits (int): How many credits the course gives.
            capacity (int): The max number of students who can join.

        Raises:
            Exception: If the course ID already exists.
        """
        course_id = course_id.upper()
        if course_id in self.courses:
            raise Exception("Course with this ID already exists.")
        self.courses[course_id] = Course(course_id, title, description, credits, capacity)

    def remove_course(self, course_id: str):
        """
        Removes a course from the system and removes it from all students' lists.

        Arguments:
            course_id (str): The course code to remove.

        Raises:
            Exception: If the course does not exist.
        """
        course_id = course_id.upper()
        if course_id not in self.courses:
            raise Exception("Course not found.")
        # Remove course from all students
        for student in self.students.values():
            if course_id in student.registered_courses:
                student.drop_course(course_id)
        del self.courses[course_id]

    def update_course(self, course_id: str, title=None, description=None, credits=None, capacity=None):
        """
        Changes details of an existing course.

        Only the information you give will be changed. If you leave something out, it stays the same.

        Arguments:
            course_id (str): The course code to update.
            title (str, optional): New course name. Default is no change.
            description (str, optional): New course summary. Default is no change.
            credits (int, optional): New number of credits. Default is no change.
            capacity (int, optional): New max students allowed. Default is no change.

        Raises:
            Exception: If the course does not exist.
        """
        course_id = course_id.upper()
        if course_id not in self.courses:
            raise Exception("Course not found.")
        self.courses[course_id].update_details(title, description, credits, capacity)

    def search_courses(self, search_term: str) -> List[Course]:
        """
        Finds courses by its ID or title.

        The search ignores uppercase or lowercase letters.

        Arguments:
            search_term (str): The word to look for in course IDs and titles.

        Returns:
            List[Course]: A list of courses that match the search. Empty if none found.
        """
        search_term = search_term.lower()
        results = []
        for course in self.courses.values():
            if search_term in course.course_id.lower() or search_term in course.title.lower():
                results.append(course)
        return results

    def list_students_for_course(self, course_id: str) -> List[str]:
        """
        Gets the list of students signed up for a given course.

        Arguments:
            course_id (str): The course code to check.

        Returns:
            List[str]: Student IDs registered in the course.

        Raises:
            Exception: If the course does not exist.
        """
        course_id = course_id.upper()
        if course_id not in self.courses:
            raise Exception("Course not found.")
        return self.courses[course_id].registered_students

    def list_courses_for_student(self, student_id: str) -> List[str]:
        """
        Gets the list of courses a student is signed up for.

        Arguments:
            student_id (str): The student's ID.

        Returns:
            List[str]: Course IDs the student is registered in.

        Raises:
            Exception: If the student does not exist.
        """
        student_id = student_id.lower()
        if student_id not in self.students:
            raise Exception("Student not found.")
        return self.students[student_id].view_registered_courses()

    # --- Students Functions ---

    def register_student_for_course(self, student_id: str, course_id: str):
        """
        Signs a student up for a course.

        Checks if the student and course exist, makes sure the course is not full,
        and that the student is not already signed up.

        Arguments:
            student_id (str): The student's ID.
            course_id (str): The course code.

        Raises:
            Exception: If student or course is not found,
                       if the course is full,
                       or if the student is already signed up for the course.
        """
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
        """
        Removes a student from a course.

        Checks that the student and course exist, and that the student is registered.
        Updates both the course and student records.

        Arguments:
            student_id (str): The student's ID.
            course_id (str): The course code.

        Raises:
            Exception: If student or course is not found,
                       or if the student is not registered for the course.
        """
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
        """
        Shows all courses in the system.

        This returns every course

        Returns:
            List[Course]: A list of all courses.
        """
        return list(self.courses.values())

    def generate_report_student_courses(self, student_id: str) -> str:
        """
        Creates a report showing all courses a student is signed up for.

        Arguments:
            student_id (str): The student's ID.

        Returns:
            str: A list of courses with their ID, title, and credits,
                 or a message if the student has no courses.

        Raises:
            Exception: If the student does not exist.
        """
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
    """
    Ask the user to enter a whole number.

    Keeps asking until the user types a valid number.
    The number must be inside that range if min/max val are set.

    Args:
        prompt (str): Message shown to the user.
        min_val (int, optional): Lowest number allowed.
        max_val (int, optional): Highest number allowed.

    Returns:
        int: The number the user typed (valid and inside the range if set).
    """
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
    """
    Asks the user to type something that is not empty.

    Keeps asking until the user types at least one non-space character.

    Args:
        prompt (str): The message shown to the user.

    Returns:
        str: The text the user typed (not empty).
    """
    while True:
        s = input(prompt).strip()
        if s:
            return s
        else:
            print("Input cannot be empty.")


def admin_menu(system: RegistrationSystem, admin: Admin):
    """
    Displays the admin menu options.

    Admin can:
    1. Add a new course
    2. Remove a course
    3. Update course details
    4. Search courses by ID or title
    5. List students registered in a course
    6. List courses registered by a student
    7. Logout

    Args:
        system (RegistrationSystem): The registration system instance.
        admin (Admin): The logged-in admin user.

    Runs until admin chooses to logout.
    """
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
    """
    Displays the student menu options.

    Student menu functions:
        1. View all available courses
        2. Register for a course
        3. Drop a course
        4. View currently registered courses
        5. Logout

    Loops until the student chooses to logout.

    Args:
        system (RegistrationSystem): The course registration system instance.
        student (Student): The logged-in student.

    Exceptions from RegistrationSystem methods are caught and shown.
    """
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
