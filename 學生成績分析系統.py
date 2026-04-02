# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 16:20:13 2026

@author: user
"""

import math

def compute_student_average(students):
    """
    計算每位學生的平均分數
    """
    avg_scores = {}
    
    for name, scores in students.items():
        avg = sum(scores) / len(scores)
        avg_scores[name] = round(avg, 2)
        
    return avg_scores


def top_k_students(avg_scores, k):
    """
    找出平均分數前 k 名學生
    """
    sorted_students = sorted(avg_scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_students[:k]


def class_statistics(avg_scores):
    """
    計算班級統計資訊
    """
    scores = list(avg_scores.values())
    
    class_avg = sum(scores) / len(scores)
    max_avg = max(scores)
    min_avg = min(scores)
    
    # 計算標準差
    variance = sum((x - class_avg) ** 2 for x in scores) / len(scores)
    std_dev = math.sqrt(variance)
    
    return {
        "class_avg": round(class_avg, 2),
        "max_avg": round(max_avg, 2),
        "min_avg": round(min_avg, 2),
        "std_dev": round(std_dev, 2)
    }


def find_at_risk_students(avg_scores, threshold=60):
    """
    找出平均低於 threshold 的學生
    """
    at_risk = []
    
    for name, avg in avg_scores.items():
        if avg < threshold:
            at_risk.append(name)
            
    return at_risk


def main():
    
    students = {
        "Alice": [85, 78, 92],
        "Bob": [70, 88, 90],
        "Charlie": [60, 75, 72],
        "David": [95, 90, 93],
        "Eva": [55, 65, 58]
    }

    avg_scores = compute_student_average(students)

    print("Student Average Scores")
    print("----------------------")
    
    for name, avg in avg_scores.items():
        print(f"{name} : {avg:.2f}")

    top_students = top_k_students(avg_scores, 3)

    print("\nTop 3 Students")
    print("--------------")
    
    for i, (name, score) in enumerate(top_students, start=1):
        print(f"{i}. {name} ({score:.2f})")

    stats = class_statistics(avg_scores)

    print("\nClass Statistics")
    print("----------------")
    print("Class Average :", stats["class_avg"])
    print("Max Average :", stats["max_avg"])
    print("Min Average :", stats["min_avg"])
    print("Std Dev :", stats["std_dev"])

    at_risk = find_at_risk_students(avg_scores)

    print("\nStudents Needing Help")
    print("---------------------")
    
    if len(at_risk) == 0:
        print("None")
    else:
        for student in at_risk:
            print(student)


if __name__ == "__main__":
    main()