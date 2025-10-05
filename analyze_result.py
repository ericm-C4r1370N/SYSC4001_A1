import sys
import matplotlib.pyplot as plt

def generate_gantt_chart(input_stream):
    """    
    Data format expected: start_time (ms), duration (ms), event_name (string)
    Example: 0, 30, init() function executes
    """
    
    data = []
    
    # Read and parse the data line by line
    for line in input_stream:
        line = line.strip()
        if not line:
            continue
            
        try:
            # Split the line by comma
            parts = [p.strip() for p in line.split(',', 2)]
            
            start_time = int(parts[0])
            duration = int(parts[1])
            event_name = parts[2]
            
            data.append({
                'start': start_time,
                'duration': duration,
                'event': event_name
            })
            
        except (ValueError, IndexError) as e:
            print(f"Skipping malformed line: '{line}'. Error: {e}", file=sys.stderr)

    if not data:
        print("No valid data found to plot.", file=sys.stderr)
        return

    
    # Sort data by start time to ensure bars appear in chronological order
    data.sort(key=lambda x: x['start'])
    
    events = [d['event'] for d in data]
    starts = [d['start'] for d in data]
    durations = [d['duration'] for d in data]
    
    # Reverse the lists so the first event starts at the top of the chart (index 0 on y-axis is bottom)
    events.reverse()
    starts.reverse()
    durations.reverse()

    
    fig, ax = plt.subplots(figsize=(12, max(6, len(events) * 0.5))) # Dynamic height based on number of events

    # Define a color map for distinction between different events
    unique_events = list(dict.fromkeys(events))
    
    tab20_map = plt.colormaps.get_cmap('tab20')
    num_colors = tab20_map.N
    
    color_map = {event: tab20_map(i % num_colors) for i, event in enumerate(unique_events)}
    
    bar_colors = [color_map[event] for event in events]

    # Plot the horizontal bars
    ax.barh(events, durations, left=starts, height=0.6, align='center', color=bar_colors)


    ax.set_title('Program Execution Timeline (Gantt Chart)', fontsize=16, pad=20)
    ax.set_xlabel('Time (ms)', fontsize=12)
    ax.set_ylabel('Execution Event', fontsize=12)

    if starts and durations:
        total_time = max(starts[i] + durations[i] for i in range(len(starts)))
        ax.set_xlim(0, total_time * 1.05)
    
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    
    ax.tick_params(axis='y', labelsize=10)
    ax.tick_params(axis='x', labelsize=10)

    # Add duration labels to the right of each bar
    for i, (start, duration) in enumerate(zip(starts, durations)):
        ax.text(start + duration, events[i], 
                f'{duration}ms', 
                va='center', 
                ha='left', 
                fontsize=8, 
                color='black',
                bbox=dict(facecolor='white', alpha=0.5, edgecolor='none', boxstyle='round,pad=0.2'))

    plt.tight_layout(pad=3.0)
    plt.show()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        # If a command-line argument is provided, parse it as a file path ex) python analyze_result.py ~/Projects/SYSC4001/Assignment1/trace.txt
        file_path = sys.argv[1]
        try:
            with open(file_path, 'r') as f:
                generate_gantt_chart(f)
        except FileNotFoundError:
            print(f"Error: File not found at '{file_path}'", file=sys.stderr)
            sys.exit(1)
    else:
        # If no argument is provided, read from standard input for piping  ex) cat trace.tx | python analyze_result.py
        print("Reading data from standard input (stdin)...", file=sys.stderr)
        generate_gantt_chart(sys.stdin)
