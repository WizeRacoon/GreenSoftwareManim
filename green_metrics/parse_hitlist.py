import os
import sys

def generate_hitlist(filename="time_profile.txt", top_n=15):
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()

        print(f"\n--- Top {top_n} Manim Code Bottlenecks ---")
        
        manim_lines = []
        for line in lines:
            # Look for lines that contain profiling data specifically targeting the manim directory
            if "manim" in line and ".py:" in line:
                parts = line.split()
                # Ensure it's a valid cProfile data row
                if len(parts) >= 6:
                    ncalls, tottime, percall1, cumtime, percall2 = parts[:5]
                    path_func = " ".join(parts[5:])
                    
                    # Strip the long absolute path, keeping just the filename and function
                    file_func = path_func.split("/")[-1]
                    
                    # Reformat the row to be clean and readable
                    formatted_line = f"{ncalls:>10} {tottime:>8} {percall1:>8} {cumtime:>8} {percall2:>8}  {file_func}"
                    manim_lines.append(formatted_line)

        # Print the top N bottlenecks (cProfile already sorted them by tottime)
        for line in manim_lines[:top_n]:
            print(line)
            
        # Also write the hitlist to a file so it gets saved in the experiment folder
        with open("target_hitlist.txt", "w") as out:
            out.write(f"--- Top {top_n} Manim Code Bottlenecks ---\n")
            for line in manim_lines[:top_n]:
                out.write(line + "\n")

    except FileNotFoundError:
        print(f"Error: Could not find '{filename}'. Make sure the cProfile step finished successfully.")

if __name__ == "__main__":
    generate_hitlist()