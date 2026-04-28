import csv

def top_three_students(scores):
    # Sort students by score in descending order and select the top 3
    sorted_students = sorted(scores, key=lambda x: x[1], reverse=True)[:3]
    
    # Print each student's name and score
    for student, score in sorted_students:
        print(f"{student}: {score}")

# Example execution (to be called manually)
if __name__ == "__main__":
    sample_data = [
        ("Alice", 85),
        ("Bob", 92),
        ("Charlie", 78),
        ("David", 89),
        ("Eve", 90),
        ("Frank", 100)
    ]
    
    top_three_students(sample_data)

# To call the function with your own data:
# top_three_students(your_list_of_scores_here)