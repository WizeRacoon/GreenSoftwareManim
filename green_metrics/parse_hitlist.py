def generate_hitlist(filepath, num_results=15):
    print(f"--- Top {num_results} Manim Code Bottlenecks ---")
    
    # Filter out Python C-bindings, built-ins, and standard NumPy modules
    ignore_list = ['{', '<', 'arrayprint.py', 'fromnumeric.py', 'numeric.py', 'copy.py']
    
    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()

        hitlist = []
        for line in lines:
            # Check if it's a file execution line and NOT in our ignore list
            if '.py:' in line and not any(ignore in line for ignore in ignore_list):
                hitlist.append(' '.join(line.split()))

        for hit in hitlist[:num_results]:
            print(hit)
            
    except FileNotFoundError:
        print(f"Error: {filepath} not found.")

if __name__ == "__main__":
    generate_hitlist('time_profile.txt', num_results=15)