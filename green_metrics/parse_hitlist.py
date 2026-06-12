import os
import sys

def generate_hitlist(filename="time_profile.txt", top_n=15):
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()

        print(f"\n--- Top {top_n} Global Code Bottlenecks (Unfiltered) ---")
        print(f"{'N-Calls':>10} {'TotTime':>8} {'PerCall':>8} {'CumTime':>8} {'PerCall':>8}  {'Source Location'}")
        print("-" * 90)
        
        manim_lines = []
        printed_count = 0
        for line in lines:
            parts = line.split()
            # Ensure it's a valid cProfile data row by checking for numeric time columns
            if len(parts) >= 6 and parts[1].replace('.', '', 1).isdigit():
                ncalls, tottime, percall1, cumtime, percall2 = parts[:5]
                path_func = " ".join(parts[5:])
                clean_path = path_func.split("/")[-1]
                
                formatted_line = f"{ncalls:>10} {tottime:>8} {percall1:>8} {cumtime:>8} {percall2:>8}  {clean_path}"
                manim_lines.append(formatted_line)
                
                if printed_count < top_n:
                    print(formatted_line)
                    printed_count += 1

        with open("target_hitlist.txt", "w") as out:
            out.write(f"--- Top {top_n} Global Code Bottlenecks (Unfiltered) ---\n")
            out.write(f"{'N-Calls':>10} {'TotTime':>8} {'PerCall':>8} {'CumTime':>8} {'PerCall':>8}  {'Source Location'}\n")
            out.write("-" * 90 + "\n")
            for line in manim_lines[:top_n]:
                out.write(line + "\n")

    except FileNotFoundError:
        print(f"Error: Could not find '{filename}'. Check your path specification.")

if __name__ == "__main__":
    target_file = sys.argv[1] if len(sys.argv) > 1 else "time_profile.txt"
    generate_hitlist(filename=target_file)