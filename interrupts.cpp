/**
 *
 * @file interrupts.cpp
 * @author Sasisekhar Govind
 *
 */

#include<interrupts.hpp>

int main(int argc, char** argv) {
    
    //vectors is a C++ std::vector of strings that contain the address of the ISR
    //delays  is a C++ std::vector of ints that contain the delays of each device
    //the index of these elemens is the device number, starting from 0
    auto [vectors, delays] = parse_args(argc, argv);
    std::ifstream input_file(argv[1]);

    std::string trace;      //!< string to store single line of trace file
    std::string execution;  //!< string to accumulate the execution output

    /******************ADD YOUR VARIABLES HERE*************************/
    const int change_context_time = 30;
    const int syscall_isr_time = 200;
    const int syscall_time = 1;
    const int iret_time = 1;
    const int switch_mode_delay = 1;
    int exec_time = 0;

    /******************************************************************/

    //parse each line of the input trace file
for (int i = 0; i < 100; i++) {

    while(std::getline(input_file, trace)) {

        auto [activity, duration_intr] = parse_trace(trace);

        /******************ADD YOUR SIMULATION CODE HERE*************************/
        if (activity == "CPU") {
            execution += std::to_string(exec_time) + ", " + std::to_string(duration_intr) + ", user program executes\n";
            exec_time += duration_intr;
        } else if (activity == "SYSCALL") {
            // User program makes a system call
            const int device_num = duration_intr; //get device #
            int IO_wait;
        
            execution += std::to_string(exec_time) + ", " + std::to_string(syscall_time) + ", user program makes a system call\n";
            exec_time++;

            // Use the function provided in interrupts.hpp for the initial interrupt overhead
            auto [intr_exec, intr_time] = intr_boilerplate(exec_time, duration_intr, change_context_time, vectors);
            execution += intr_exec;
            exec_time = intr_time;

            // Simulate the execution of the ISR
            execution += std::to_string(exec_time) + ", " + std::to_string(syscall_isr_time) + ", execute ISR for device " + std::to_string(device_num) + "\n";
            exec_time += syscall_isr_time;

            //get device IO time (ms) from device table
            std::ifstream file("device_table.txt");
            std::string line;
            int current_line = 0;

            // Read the file line by line
            while (std::getline(file, line)) {
            current_line++;
                // Check if we have reached the desired line number (device number)
                if (current_line == device_num) {
                    IO_wait = std::stoi(line);
                }
            }

            // Initiate IO and wait for it to complete
            execution += std::to_string(exec_time) + ", " + std::to_string(IO_wait) + ", IO request to device " + std::to_string(device_num) + "\n";
            exec_time += IO_wait;


            // Simulate context restoration and return
            execution += std::to_string(exec_time) + ", " + std::to_string(change_context_time) + ", context restored\n";
            exec_time += change_context_time;
            execution += std::to_string(exec_time) + ", " + std::to_string(iret_time) + ", execute IRET\n";
            exec_time += iret_time;
            
        } else if (activity == "END_IO") {
            int device_num = duration_intr;
            
            // Since we assume IO always finishes, this is where the interrupt occurs
            auto [intr_exec, intr_time] = intr_boilerplate(exec_time, device_num, change_context_time, vectors);
            execution += intr_exec;
            exec_time = intr_time;

            // Execute the ISR body using the device delay time
            int isr_exec_time = delays.at(device_num);
            execution += std::to_string(exec_time) + ", " + std::to_string(syscall_isr_time) + ", execute ISR for device " + std::to_string(device_num) + "\n";
            exec_time += syscall_isr_time;

            // Simulate context restoration and return
            execution += std::to_string(exec_time) + ", " + std::to_string(change_context_time) + ", context restored\n";
            exec_time += change_context_time;

            execution += std::to_string(exec_time) + ", " + std::to_string(iret_time) + ", execute IRET\n";
            exec_time += iret_time;

            //Return CPU to user mode: set mode bit to 1
            execution += std::to_string(exec_time) + ", " + std::to_string(switch_mode_delay) + ", switch to user mode\n";
            exec_time += switch_mode_delay;
        }
        
        /************************************************************************/

    }

    input_file.close();

    write_output(execution);

    return 0;
}

}
