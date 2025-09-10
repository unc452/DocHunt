import tkinter as tk
from tkinter import messagebox

# 요일 매핑
WEEKDAYS = ["월", "화", "수", "목", "금", "토", "일"]

def parse_mmdd(s):
    """MMDD (예: 0818) → (month, day) 튜플"""
    s = s.strip()
    if len(s) != 4 or not s.isdigit():
        raise ValueError("MMDD 형식(예: 0818)으로 입력하세요.")
    return int(s[:2]), int(s[2:])

def generate_dates(start_mmdd, end_mmdd, start_weekday, skip_weekends):
    """시작일자, 종료일자, 시작 요일, 주말 제외 여부 기반으로 날짜 리스트 생성"""
    start_month, start_day = parse_mmdd(start_mmdd)
    end_month, end_day = parse_mmdd(end_mmdd)

    # 단순히 같은 해(2025년) 가정
    from datetime import date, timedelta
    start = date(2025, start_month, start_day)
    end = date(2025, end_month, end_day)

    # 사용자가 지정한 시작 요일을 강제 적용
    # → 실제 calendar 모듈 대신 입력된 요일을 기준으로 시뮬레이션
    current = start
    weekday_idx = WEEKDAYS.index(start_weekday)

    days = []
    while current <= end:
        weekday_name = WEEKDAYS[weekday_idx % 7]
        if not (skip_weekends and weekday_name in ["토", "일"]):
            days.append((current, weekday_name))
        current += timedelta(days=1)
        weekday_idx += 1

    return days

def check_docs():
    try:
        start_mmdd = start_entry.get()
        end_mmdd = ref_entry.get()
        start_weekday = weekday_var.get()
        skip_weekends = weekend_var.get()

        existing_input = existing_entry.get("1.0", tk.END)
        existing_dates = set(s.strip() for s in existing_input.split() if s.strip())

        # 전체 날짜 생성
        all_days = generate_dates(start_mmdd, end_mmdd, start_weekday, skip_weekends)
        all_mmdd = [d[0].strftime("%m%d") for d in all_days]

        missing = [d for d in all_mmdd if d not in existing_dates]

        result = f"총 작성해야 할 날짜: {len(all_mmdd)}일\n"
        result += f"보유한 서류: {len([d for d in all_mmdd if d in existing_dates])}일\n"
        result += f"빠진 서류: {len(missing)}일\n\n"
        result += "빠진 날짜:\n" + " ".join(missing) if missing else "빠진 날짜 없음 ✅"
        
        messagebox.showinfo("결과", result)

    except Exception as e:
        messagebox.showerror("에러", f"입력값을 확인해주세요.\n\n{e}")

# --- UI 구성 ---
root = tk.Tk()
root.title("서류미아찾기")
root.geometry("420x400")

tk.Label(root, text="시작 일자 (MMDD)").pack()
start_entry = tk.Entry(root)
start_entry.insert(0, "0818")
start_entry.pack()

tk.Label(root, text="기준 일자 (MMDD)").pack()
ref_entry = tk.Entry(root)
ref_entry.insert(0, "0909")
ref_entry.pack()

tk.Label(root, text="시작 요일 선택").pack()
weekday_var = tk.StringVar(value="월")
for w in WEEKDAYS:
    tk.Radiobutton(root, text=w, variable=weekday_var, value=w).pack(anchor="w")

weekend_var = tk.BooleanVar(value=True)
tk.Checkbutton(root, text="주말 제외", variable=weekend_var).pack()

tk.Label(root, text="보유한 서류 일자 (MMDD, 공백 구분)").pack()
existing_entry = tk.Text(root, height=5)
existing_entry.insert("1.0", "0818 0819 0822")
existing_entry.pack()

tk.Button(root, text="확인", command=check_docs).pack(pady=10)

root.mainloop()
