import tkinter as tk
import subprocess

def button_click(btn_id):
    pass
    
def exit_program():
    print("프로그램 종료")
    root.quit()

# 풀스크린 GUI 설정
root = tk.Tk()
root.title("실습용 라즈베리 파이 UI")
root.attributes("-fullscreen", True)

# 버튼들
btn1 = tk.Button(root, text="Button 1", command=lambda: button_click('btn1'), height=3, width=20)
btn2 = tk.Button(root, text="Button 2", command=lambda: button_click('btn2'), height=3, width=20)
btn3 = tk.Button(root, text="Button 3", command=lambda: button_click('btn3'), height=3, width=20)

# 종료 버튼 (처음엔 숨겨짐)
exit_btn = tk.Button(root, text="종료", command=exit_program, height=2, width=10, bg='red', fg='white')
exit_btn.pack_forget()  # 처음엔 숨기기

btn1.pack(pady=20)
btn2.pack(pady=20)
btn3.pack(pady=20)
exit_btn.pack()
root.mainloop()
