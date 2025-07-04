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
        """
        Initializes a User instance with a user ID and password.

        Args:
            user_id (str): The unique identifier for the user.
            password (str): The user's password for authentication.
        """
        self.user_id = user_id
        self.password = password

    def authenticate(self, password: str) -> bool:
        """
        Checks if the provided password matches the user's password.

        Args:
            password (str): The password to verify.

        Returns:
            bool: True if the password matches, False otherwise.
        """
        return self.password == password


class Student(User):

    def __init__(self, user_id: str, password: str):
        """
        Initializes a Student instance inheriting from User.

        Args:
            user_id (str): The unique identifier for the student.
            password (str): The password for student authentication.

        Attributes:
            registered_courses (List[str]): List of course IDs the student is currently registered for.
        """
        super().__init__(user_id, password)
        self.registered_courses = []  # List of Course IDs

    def register_course(self, course_id: str):
        """
        Adds a course ID to the student's list of registered courses if not already registered.

        Args:
            course_id (str): The unique identifier of the course to register.
        """
        if course_id not in self.registered_courses:
            self.registered_courses.append(course_id)

    def drop_course(self, course_id: str):
        """
        Removes a course ID from the student's registered courses if present.

        Args:
            course_id (str): The unique identifier of the course to drop.
        """
        if course_id in self.registered_courses:
            self.registered_courses.remove(course_id)

    def view_registered_courses(self) -> List[str]:
        """
        Returns a list of course IDs the student is currently registered in.

        Returns:
            List[str]: List of registered course IDs.
        """
        return self.registered_courses


class Admin(User):
    """For now, no extra methods required; actions done through RegistrationSystem class."""


class Course:

    def __init__(self, course_id: str, title: str, description: str, credits: int, capacity: int):
        """
        Initializes a Course instance with the provided details.

        Args:
            course_id (str): Unique identifier for the course (converted to uppercase).
            title (str): The course title.
            description (str): A brief description of the course content.
            credits (int): Number of credits the course is worth.
            capacity (int): Maximum number of students allowed to register.

        Attributes:
            registered_students (List[str]): List of student IDs currently registered.
        """
        self.course_id = course_id.upper()
        self.title = title
        self.description = description
        self.credits = credits
        self.capacity = capacity
        self.registered_students = []

    def update_details(self, title=None, description=None, credits=None, capacity=None):
        """
        Updates course details with any provided new values.

        Only non-None arguments will update the corresponding attribute.

        Args:
            title (str, optional): New title for the course.
            description (str, optional): New course description.
            credits (int, optional): New credit value.
            capacity (int, optional): New maximum student capacity.
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
        Checks whether the course has reached its registration capacity.

        Returns:
            bool: True if the number of registered students is greater than or equal to capacity; False otherwise.
        """
        return len(self.registered_students) >= self.capacity

    def add_student(self, student_id: str):
        """
        Registers a student in the course if there is space and the student is not already registered.

        Args:
            student_id (str): The ID of the student to add.

        Raises:
            Exception: If the course is full or the student is already registered.
        """
        if not self.is_full() and student_id not in self.registered_students:
            self.registered_students.append(student_id)
        else:
            raise Exception("Course is full or student already registered.")

    def remove_student(self, student_id: str):
        """
        Removes a student from the registered students list if present.

        Args:
            student_id (str): The ID of the student to remove.
        """
        if student_id in self.registered_students:
            self.registered_students.remove(student_id)

    def __str__(self):
        """
        Returns a string representation of the course including ID, title, credits, capacity, and number of registered students.

        Returns:
            str: Formatted course information.
        """
        return (f"ID: {self.course_id}, Title: {self.title}, Credits: {self.credits}, "
                f"Capacity: {self.capacity}, Registered: {len(self.registered_students)}")


class RegistrationSystem:

    def __init__(self):
        """
        Initializes the RegistrationSystem instance.

        Sets up empty dictionaries to store courses, students, and admins.
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
        Authenticates a user (admin or student) based on user ID and password.

        Checks the credentials against the stored admin and student records.
        Returns the authenticated user object if successful; otherwise, raises an exception.

        Args:
            user_id (str): The unique identifier of the user.
            password (str): The password provided for authentication.

        Returns:
            User: The authenticated user object (Admin or Student).

        Raises:
            Exception: If authentication fails due to invalid username or password.
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

        Creates a new course with the specified details and adds it to the course list.
        Raises an exception if a course with the same ID already exists.

        Args:
            course_id (str): The unique identifier for the new course.
            title (str): The title of the course.
            description (str): A brief description of the course.
            credits (int): The number of credits the course offers.
            capacity (int): The maximum number of students allowed to register.

        Raises:
            Exception: If a course with the given ID already exists.
        """
        course_id = course_id.upper()
        if course_id in self.courses:
            raise Exception("Course with this ID already exists.")
        self.courses[course_id] = Course(course_id, title, description, credits, capacity)

    def remove_course(self, course_id: str):
        """
        Removes a course from the system and deregisters all students from it.

        This method deletes the course from the course list and updates all students
        who were registered for the course by removing the course from their records.

        Args:
            course_id (str): The unique identifier of the course to remove.

        Raises:
            Exception: If the course with the given ID is not found.
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
        Updates the details of an existing course.

        Only the provided fields will be updated; fields set to None will remain unchanged.

        Args:
            course_id (str): The unique identifier of the course to update.
            title (str, optional): The new title of the course. Defaults to None.
            description (str, optional): The new description of the course. Defaults to None.
            credits (int, optional): The new number of credits for the course. Defaults to None.
            capacity (int, optional): The new capacity for the course. Defaults to None.

        Raises:
            Exception: If the course with the given ID is not found.
        """
        course_id = course_id.upper()
        if course_id not in self.courses:
            raise Exception("Course not found.")
        self.courses[course_id].update_details(title, description, credits, capacity)

    def search_courses(self, search_term: str) -> List[Course]:
        """
        Searches for courses where the course ID or title contains the given search term.

        The search is case-insensitive and returns all matching courses.

        Args:
            search_term (str): The term to search for within course IDs and titles.

        Returns:
            List[Course]: A list of courses matching the search criteria. Returns an empty list if no matches are found.
        """
        search_term = search_term.lower()
        results = []
        for course in self.courses.values():
            if search_term in course.course_id.lower() or search_term in course.title.lower():
                results.append(course)
        return results

    def list_students_for_course(self, course_id: str) -> List[str]:
        """
        Retrieves a list of student IDs registered for a specific course.

        Args:
            course_id (str): The unique identifier of the course.

        Returns:
            List[str]: A list of student IDs currently registered in the course.

        Raises:
            Exception: If the course ID is not found in the system.
        """
        course_id = course_id.upper()
        if course_id not in self.courses:
            raise Exception("Course not found.")
        return self.courses[course_id].registered_students

    def list_courses_for_student(self, student_id: str) -> List[str]:
        """
        Retrieves a list of course IDs for courses a student is registered in.

        Args:
            student_id (str): The unique identifier of the student.

        Returns:
            List[str]: A list of course IDs the student is currently registered for.

        Raises:
            Exception: If the student ID is not found in the system.
        """
        student_id = student_id.lower()
        if student_id not in self.students:
            raise Exception("Student not found.")
        return self.students[student_id].view_registered_courses()

    # --- Students Functions ---

    def register_student_for_course(self, student_id: str, course_id: str):
        """
        Registers a student for a specified course.

        This method checks if both the student and course exist, verifies course capacity,
        and ensures the student is not already registered before adding the student to the course.

        Args:
            student_id (str): The unique identifier of the student.
            course_id (str): The unique identifier of the course.

        Raises:
            Exception: If the student or course is not found,
                       if the course is already full,
                       or if the student is already registered for the course.
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
        Removes a student from a specified course.

        This method updates both the student and course records to reflect the change.
        It checks that both the student and course exist and that the student is currently registered for the course.

        Args:
            student_id (str): The unique identifier for the student.
            course_id (str): The unique identifier for the course.

        Raises:
            Exception: If the student or course is not found, or if the student is not registered for the course.
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
        Returns a list of all available courses in the system.

        This includes all courses regardless of their capacity status
        (e.g., full or not full). It is up to the caller to filter or display them as needed.

        Returns:
            List[Course]: A list of all course objects currently stored in the system.
        """
        return list(self.courses.values())

    def generate_report_student_courses(self, student_id: str) -> str:
        """
        Generates a report of all courses a student is registered for.

        Looks up the student by ID and compiles a list of their registered courses.
        Each course in the report includes the course ID, title, and number of credits.

        Args:
            student_id (str): The unique identifier for the student.

        Returns:
            str: A formatted string listing the student's registered courses,
                 or a message if no courses are registered.

        Raises:
            Exception: If the student ID is not found in the system.
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
    Prompts the user to enter an integer, optionally enforcing a value range.

    Continuously prompts the user until a valid integer is entered. If minimum
    and/or maximum bounds are provided, the input must fall within the specified range.

    Args:
        prompt (str): The prompt message to display to the user.
        min_val (int, optional): The minimum acceptable value (inclusive). Defaults to None.
        max_val (int, optional): The maximum acceptable value (inclusive). Defaults to None.

    Returns:
        int: The validated integer input from the user.

    Raises:
        ValueError: Not explicitly raised, but invalid input is handled and re-prompted.
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
    Prompts the user for non-empty input.

    Continuously prompts the user until a non-empty, non-whitespace-only string is entered.

    Args:
        prompt (str): The input prompt to display to the user.

    Returns:
        str: The user's non-empty input.
    """
    while True:
        s = input(prompt).strip()
        if s:
            return s
        else:
            print("Input cannot be empty.")


def admin_menu(system: RegistrationSystem, admin: Admin):
    """
    Displays the admin menu interface.

    Admin menu including function for admin able to:
        1. Add a new course.
        2. Remove an existing course.
        3. Update course details.
        4. Search for courses by ID or title.
        5. List students registered in a specific course.
        6. List all courses registered by a specific student.
        7. Logout from the system.

    The menu runs in a loop until the admin chooses to log out (Option #7).

    Args:
        system (RegistrationSystem): The system instance handling administrative operations.
        admin (Admin): The admin object representing the logged-in administrator.

    Raises:
        Exceptions from the RegistrationSystem methods are caught and displayed to the user.
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
    Displays the student menu interface.

    Student menu including function for student able to:
        1. View all available courses.
        2. Register for a course.
        3. Drop a course.
        4. View currently registered courses.
        5. Logout from the system.

    The menu loops until the student chooses to log out (Option #5).

    Args:
        system (RegistrationSystem): The system instance handling course registrations.
        student (Student): The student object representing the logged-in user.

    Raises:
        Any exceptions from the RegistrationSystem methods will be caught and displayed.
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
