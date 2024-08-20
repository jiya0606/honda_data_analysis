action_unit_plots.py will take in a folder containing CSV data from running OpenFace and create a file of bar charts that display the number of occurances of each action unit (showed as a '1' in the CSV). Example output is shown below.
![combined_action_unit_counts](https://github.com/user-attachments/assets/ae52bcd6-2f85-47ac-8d23-e5cf9b2c24d0)


head_position_plots.py will take in a folder containing CSV data from running OpenFace and create 3 files of bar charts that display the x, y, and z head positions of the participant (pose_Rx, pose_Ry, pose_Rz). Example for pose_rx is shown below.
![combined_ pose_Rx](https://github.com/user-attachments/assets/2e6befcd-82ad-446f-9355-c6f027eb2f08)

head_position_plots_combined.py will output the same results from head_position_plots.py but condensed into a singular file. Example is shown below
![combined_pose_values](https://github.com/user-attachments/assets/b56419ad-b1c2-4cf0-95dd-35e9e1490c79)

v2_head_positions.py will output the same graphs as head_position_plots_combined.py, but it will output line graphs instead of bar graphs and organize the graphs of each signal into a "Good Signal" or "Bad Signal" category. Example is shown below
![D119_S4_pose](https://github.com/user-attachments/assets/fe7d247a-2b1c-4b4a-8128-20ec20c2b3a5)

final_action_units_plots.py will output the same bar graphs as action_unit_plots.py, but it will add the percent prevalence instead of frame count for each action unit and categorize the graphs into "Good Signal" and "Bad Signal". It will also output a CSV file that contains the Pearson and Spearman correlation coefficient and average percent prevalence for each action unit under the following categories: "Before Good Signal", "After Good Signal", "Before Bad Signal", and "After Bad Signal". Example of the graphs is shown below
![D119_S4_au_graphs](https://github.com/user-attachments/assets/14510b66-8758-44c9-a4f5-b4469f45f9f8)
