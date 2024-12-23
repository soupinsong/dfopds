##GUI FINAL TEST Almost DONE##
import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime


class User:
    def __init__(self, user_id, user_type):
        self.user_id = user_id
        self.user_type = user_type


class Issue:
    def __init__(self, issue_id, category, description, reporter_id, timestamp, severity=None, details=None):
        self.issue_id = issue_id
        self.category = category
        self.description = description
        self.reporter_id = reporter_id
        self.timestamp = timestamp
        self.severity = severity
        self.details = details
        self.status = "미해결"


class DormSystem:
    def __init__(self):
        self.users = []
        self.issues = []
        self.issue_counter = 1

    def add_user(self, user_id, user_type):
        self.users.append(User(user_id, user_type))

    def report_issue(self, user_id, category, description, severity=None, details=None):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        issue = Issue(
            issue_id=self.issue_counter,
            category=category,
            description=description,
            reporter_id=user_id,
            timestamp=timestamp,
            severity=severity,
            details=details,
        )
        self.issues.append(issue)
        self.issue_counter += 1
        return issue

    def get_user(self, user_id):
        for user in self.users:
            if user.user_id == user_id:
                return user
        return None

    def get_issues_by_user(self, user_id):
        return [issue for issue in self.issues if issue.reporter_id == user_id]

    def get_all_issues(self):
        return self.issues


class DormApp:
    def __init__(self, root):
        self.system = DormSystem()
        self.current_user = None

        self.root = root
        self.root.title("중앙대학교 기숙사 문제 관리 시스템 🏫")
        self.root.geometry("500x400")
        self.root.configure(bg="#E0F7FA")  # 푸른 배경색

        self.login_screen()

    def login_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        tk.Label(self.root, text="CAU기숙사 문제 관리 시스템 🏫", font=("Arial", 20), bg="#E0F7FA", fg="#006064").pack(pady=20)
        tk.Label(self.root, text="사용자 ID 🆔:", bg="#E0F7FA", fg="#004D40").pack()
        self.entry_user_id = tk.Entry(self.root, font=("Arial", 14))
        self.entry_user_id.pack(pady=10)

        tk.Button(self.root, text="🔑 로그인", command=self.login, bg="#0288D1", fg="white", font=("Arial", 12)).pack(pady=10)
        tk.Button(self.root, text="📝 사용자 등록", command=self.register_screen, bg="#0288D1", fg="white", font=("Arial", 12)).pack()

    def login(self):
        user_id = self.entry_user_id.get()
        user = self.system.get_user(user_id)
        if user:
            self.current_user = user
            self.main_menu()
        else:
            messagebox.showerror("❌ 오류", "사용자를 찾을 수 없습니다.")

    def register_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="새 사용자 등록 🆕", font=("Arial", 20), bg="#E0F7FA", fg="#006064").pack(pady=20)
        tk.Label(self.root, text="사용자 ID 🆔:", bg="#E0F7FA", fg="#004D40").pack()
        self.entry_new_user_id = tk.Entry(self.root, font=("Arial", 14))
        self.entry_new_user_id.pack(pady=10)

        tk.Label(self.root, text="사용자 유형 👤:", bg="#E0F7FA", fg="#004D40").pack()
        self.user_type_var = tk.StringVar(value="학생")
        tk.OptionMenu(self.root, self.user_type_var, "학생", "층장", "사감").pack(pady=10)

        tk.Button(self.root, text="✅ 등록", command=self.register_user, bg="#0288D1", fg="white", font=("Arial", 12)).pack(pady=10)
        tk.Button(self.root, text="↩️ 뒤로", command=self.login_screen, bg="#0288D1", fg="white", font=("Arial", 12)).pack(pady=10)

    def register_user(self):
        user_id = self.entry_new_user_id.get()
        user_type = self.user_type_var.get()
        if user_id:
            self.system.add_user(user_id, user_type)
            messagebox.showinfo("🎉 등록 완료", f"사용자 {user_id}가 {user_type}로 등록되었습니다.")
            self.login_screen()
        else:
            messagebox.showerror("❌ 오류", "ID를 입력하세요.")

    def main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text=f"{self.current_user.user_type} 메뉴 🚪", font=("Arial", 20), bg="#E0F7FA", fg="#006064").pack(pady=20)

        # 학생 및 층장 공통 메뉴
        if self.current_user.user_type == "학생" or self.current_user.user_type == "층장":
            tk.Button(self.root, text="📋 문제 신고하기", command=self.report_issue_screen, bg="#0288D1", fg="white", font=("Arial", 12)).pack(pady=10)
            tk.Button(self.root, text="📜 내가 신고한 문제 보기", command=self.open_my_issues_window, bg="#0288D1", fg="white", font=("Arial", 12)).pack(pady=10)

        # 층장 및 사감 전용 메뉴
        if self.current_user.user_type == "층장" or self.current_user.user_type == "사감":
            tk.Button(self.root, text="📂 모든 문제 보기", command=self.open_all_issues_window, bg="#0288D1", fg="white", font=("Arial", 12)).pack(pady=10)
            tk.Button(self.root, text="🛠️ 문제 상태 업데이트", command=self.update_issue_screen, bg="#0288D1", fg="white", font=("Arial", 12)).pack(pady=10)

        # 공통 로그아웃 메뉴
        tk.Button(self.root, text="🔓 로그아웃", command=self.login_screen, bg="#0288D1", fg="white", font=("Arial", 12)).pack(pady=10)

    def report_issue_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="문제 신고 📋", font=("Arial", 20), bg="#E0F7FA", fg="#006064").pack(pady=20)

        tk.Label(self.root, text="문제 유형 🛠️:", bg="#E0F7FA", fg="#004D40").pack()
        self.issue_category_var = tk.StringVar(value="고장 문의")
        tk.OptionMenu(self.root, self.issue_category_var, "고장 문의", "분실 신고", "민원 신고", "기타 문의").pack(pady=10)

        tk.Label(self.root, text="문제 설명 ✏️:", bg="#E0F7FA", fg="#004D40").pack()
        self.entry_description = tk.Entry(self.root, font=("Arial", 14), width=40)
        self.entry_description.pack(pady=10)

        tk.Label(self.root, text="심각도 🚨:", bg="#E0F7FA", fg="#004D40").pack()
        self.severity_var = tk.StringVar(value="일반")
        severity_menu = tk.OptionMenu(self.root, self.severity_var, "일반", "위급")
        severity_menu.pack(pady=10)

        def update_severity_color(*args):
            color = "#FFCC80" if self.severity_var.get() == "일반" else "#FF5252"
            severity_menu.config(bg=color)

        self.severity_var.trace("w", update_severity_color)
        update_severity_color()

        tk.Button(self.root, text="📩 신고", command=self.submit_issue, bg="#0288D1", fg="white", font=("Arial", 12)).pack(pady=10)
        tk.Button(self.root, text="↩️ 뒤로", command=self.main_menu, bg="#0288D1", fg="white", font=("Arial", 12)).pack(pady=10)

    def open_my_issues_window(self):
        issues = self.system.get_issues_by_user(self.current_user.user_id)
        self.create_records_window("내 문제 기록 📜", issues)

    def open_all_issues_window(self):
        issues = self.system.get_all_issues()
        self.create_records_window("모든 문제 기록 📂", issues)

    def create_records_window(self, title, issues):
        records_window = tk.Toplevel()
        records_window.title(title)
        records_window.geometry("600x400")
        tk.Label(records_window, text=title, font=("Arial", 16), bg="#E0F7FA").pack(pady=10)
        if issues:
            record_list = tk.Text(records_window, height=20, width=70, font=("Arial", 12), bg="#F0F4C3")
            record_list.pack(pady=5)
            for idx, issue in enumerate(issues, 1):
                record_list.insert(
                    tk.END,
                    f"ID: {issue.issue_id}\n"
                    f"유형: {issue.category}\n"
                    f"내용: {issue.description}\n"
                    f"날짜: {issue.timestamp}\n"
                    f"심각도: {issue.severity}\n"
                    f"상태: {issue.status}\n\n"
                )
            record_list.config(state=tk.DISABLED)
        else:
            tk.Label(records_window, text="기록이 없습니다.", font=("Arial", 12)).pack(pady=20)

    def update_issue_screen(self):
        issue_id = simpledialog.askinteger("문제 업데이트", "문제 ID를 입력하세요:")
        issue = next((issue for issue in self.system.issues if issue.issue_id == issue_id), None)
        if issue:
            new_status = simpledialog.askstring("상태 업데이트", "새로운 상태를 입력하세요 ('미해결', '진행 중', '해결됨'):").strip()
            if new_status:
                issue.status = new_status
                messagebox.showinfo("업데이트 완료", f"문제 ID {issue_id} 상태가 {new_status}로 업데이트되었습니다.")
        else:
            messagebox.showerror("❌ 오류", "문제를 찾을 수 없습니다.")

    def submit_issue(self):
        category = self.issue_category_var.get()
        description = self.entry_description.get()
        severity = self.severity_var.get()

        if not description:
            messagebox.showerror("❌ 오류", "문제 설명을 입력하세요.")
            return

        if severity == "위급":
            confirm = messagebox.askyesno("❗ 중대/위급 신고", "❗ 중대/위급한 상황에서만 신고할 수 있습니다. 정말로 신고하시겠습니까?")
            if not confirm:
                return

        issue = self.system.report_issue(self.current_user.user_id, category, description, severity)
        messagebox.showinfo("📩 신고 완료", f"문제가 신고되었습니다. 문제 ID: {issue.issue_id}")
        self.main_menu()


if __name__ == "__main__":
    root = tk.Tk()
    app = DormApp(root)
    root.mainloop()
