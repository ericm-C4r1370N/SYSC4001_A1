import sys
import matplotlib.pyplot as plt
# NOTE: Removed 'import matplotlib.colormaps as cm' to fix ModuleNotFoundError

def generate_gantt_chart(input_stream):
    """
    Reads execution trace data from a stream and generates a Gantt-style chart.
    
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
            # Split the line by comma, assuming the format is consistent
            parts = [p.strip() for p in line.split(',', 2)]
            
            # The first two parts are expected to be integers (time and duration)
            start_time = int(parts[0])
            duration = int(parts[1])
            event_name = parts[2]
            
            data.append({
                'start': start_time,
                'duration': duration,
                'event': event_name
            })
            
        except (ValueError, IndexError) as e:
            # Inform the user if a line couldn't be parsed
            print(f"Skipping malformed line: '{line}'. Error: {e}", file=sys.stderr)

    if not data:
        print("No valid data found to plot.", file=sys.stderr)
        return

    # --- Data Preparation for Matplotlib ---
    
    # Sort data by start time to ensure bars appear in chronological order
    data.sort(key=lambda x: x['start'])
    
    events = [d['event'] for d in data]
    starts = [d['start'] for d in data]
    durations = [d['duration'] for d in data]
    
    # Reverse the lists so the first event starts at the top of the chart (index 0 on y-axis is bottom)
    events.reverse()
    starts.reverse()
    durations.reverse()

    # --- Plotting Configuration ---
    
    fig, ax = plt.subplots(figsize=(12, max(6, len(events) * 0.5))) # Dynamic height based on number of events

    # Define a color map for better visual distinction between different event types
    unique_events = list(dict.fromkeys(events))
    
    # FIX: Using the preferred, non-deprecated access path through plt.colormaps
    # This resolves both the initial deprecation warning and the ModuleNotFoundError.
    tab20_map = plt.colormaps.get_cmap('tab20')
    num_colors = tab20_map.N
    
    color_map = {event: tab20_map(i % num_colors) for i, event in enumerate(unique_events)}
    
    bar_colors = [color_map[event] for event in events]

    # Plot the horizontal bars
    # 'left' defines the starting x-position (the start time)
    # 'width' defines the length of the bar (the duration)
    ax.barh(events, durations, left=starts, height=0.6, align='center', color=bar_colors)

    # --- Customizing the Chart ---

    # Labels and Title
    ax.set_title('Program Execution Timeline (Gantt Chart)', fontsize=16, pad=20)
    ax.set_xlabel('Time (ms)', fontsize=12)
    ax.set_ylabel('Execution Event', fontsize=12)

    # Set x-axis limits (optional: extend slightly past the end of the last event)
    # Handles the case where the lists might be empty if there was no valid data (though checked above)
    if starts and durations:
        total_time = max(starts[i] + durations[i] for i in range(len(starts)))
        ax.set_xlim(0, total_time * 1.05)
    
    # Remove the spine (border) for a cleaner look
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    
    # Improve y-axis tick label visibility
    ax.tick_params(axis='y', labelsize=10)
    ax.tick_params(axis='x', labelsize=10)

    # Add duration labels to the right of each bar
    for i, (start, duration) in enumerate(zip(starts, durations)):
        # Position the text slightly to the right of the bar end for clarity
        ax.text(start + duration, events[i], 
                f'{duration}ms', 
                va='center', 
                ha='left', 
                fontsize=8, 
                color='black',
                # Use a lightweight background box for better contrast against the bar color
                bbox=dict(facecolor='white', alpha=0.5, edgecolor='none', boxstyle='round,pad=0.2'))

    plt.tight_layout(pad=3.0)
    plt.show()


if __name__ == '__main__':
    # Determine the input source
    if len(sys.argv) > 1:
        # If a command-line argument is provided, treat it as a file path
        file_path = sys.argv[1]
        try:
            with open(file_path, 'r') as f:
                generate_gantt_chart(f)
        except FileNotFoundError:
            print(f"Error: File not found at '{file_path}'", file=sys.stderr)
            sys.exit(1)
    else:
        # If no argument is provided, read from standard input (piping)
        print("Reading data from standard input (stdin)...", file=sys.stderr)
        generate_gantt_chart(sys.stdin)
