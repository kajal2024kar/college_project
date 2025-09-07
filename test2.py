import pandas as pd
import os
import threading

bolly = "The_project/Bollywood.xlsx"
histry = "The_project/HISTORY.xlsx"
tech = "The_project/Technology.xlsx"
science = "The_project/SCIENCE.xlsx"
sport = "The_project/SPORTS.xlsx"

def get_question(df, idx):
    return df.iloc[idx]

def print_question(row, q_num):
    print(f"\nQuestion {q_num+1}: {row['Question']}")
    print(f"A. {row['Option A']}\nB. {row['Option B']}\nC. {row['Option C']}\nD. {row['Option D']}")

def check_answer(row, user_answer):
    correct = str(row["Answer"]).strip().upper()
    user = user_answer.strip().upper()
    if user == correct:
        print("✅ Correct!")
    else:
        option_text = row.get(f"Option {correct}", "Unknown")
        print(f"❌ Wrong! The correct answer is: {correct}. {option_text}")

def load_excel(path: str):
    if not os.path.exists(path):
        print(f"Quiz file not found: {path}")
        return None
    try:
        pf = pd.read_excel(path)
        df = pf.sample(frac=1).reset_index(drop=True)
    except Exception as e:
        print("Error loading quiz file:", e)
        return None

    required_cols = {"Question", "Option A", "Option B", "Option C", "Option D", "Answer"}
    if not required_cols.issubset(df.columns):
        print("Excel file must contain columns:", required_cols)
        return None

    df = df.dropna(subset=list(required_cols))
    if df.empty:
        print("No valid questions found in the quiz file.")
        return None
    return df


def main():
    print("Choose a quiz category:")
    print("1. Bollywood")
    print("2. History")
    print("3. Technology")
    print("4. Science")
    print("5. Sports")
    choice = input("Enter 1, 2, 3, 4, or 5: ").strip()
    if choice == "1":
        df = load_excel(bolly)
    elif choice == "2":
        df = load_excel(histry)
    elif choice == "3":
        df = load_excel(tech)
    elif choice == "4":
        df = load_excel(science)
    elif choice == "5":
        df = load_excel(sport)
    else:
        print("Invalid choice.")
        return

    if df is None:
        return

    num_questions = min(10, len(df))
    for i in range(num_questions):
        row = get_question(df, i)
        print_question(row, i)
        user_answer = input("enter ")
        if user_answer is None:
            print("No answer provided in 20 seconds.")
            print("-" * 40)
            continue
        if user_answer.lower() == "q":
            print("Thank you for playing!")
            break
        check_answer(row, user_answer)
        print("-" * 40)

if __name__ == "__main__":
    main()